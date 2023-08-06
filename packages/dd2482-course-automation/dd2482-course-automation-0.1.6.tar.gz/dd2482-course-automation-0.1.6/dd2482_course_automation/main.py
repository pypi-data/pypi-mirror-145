import argparse
from dataclasses import dataclass
from datetime import datetime
from distutils.errors import LibError
import pytz
from functools import reduce
import logging
from pathlib import Path
import re
from typing import Any, Optional, cast
import sys
import json
import requests
import base64
from os import getenv
from dd2482_course_automation.exceptions import AfterDeadlineError, AmbiguousRepoError, MissingRepoError, PrivateRepoError, UnclearPullRequest

Payload = dict[str, Any]
GITHUB_URL = re.compile(r"https:\/\/(?:www\.)?github\.com\/([^\/]+)\/([\w\d\-\_]+)")
STAGE_PATTERN = re.compile(r"\#.+(final|proposal|submission).*")

DATETIME_FORMAT = "%m/%d/%Y %H:%M:%S"

logger = logging.getLogger(__name__)

def estimate_line_number(text: str, pos: int):
    line_break_indices = [m.start() for m in re.finditer('\n', text)]
    
    index_of_interest = max(line_break_indices[0] - 5, 0)
    return line_break_indices[index_of_interest]

def restimate_line_number(text: str, pos: int):
    line_break_indices = [m.end() for m in re.finditer('\n', text)]
    index_of_interest = min(line_break_indices[0] + 5, len(line_break_indices))
    return line_break_indices[index_of_interest]

@dataclass
class Markdown:
    name: str
    raw: str
    
    
    def get_line_window(self, string: str):
        raw_size = len(self.raw)
        
        start = max(self.raw.find(string), 0)
        end = min(start + len(string), raw_size)
        
        if start != 0:
            text = self.raw[0:start]
            pos = text.rfind("\n")
            start = estimate_line_number(text, pos)
        
        if end != raw_size:
            text = self.raw[end:raw_size]
            pos = text.find("\n") + end
            end = restimate_line_number(text, pos)
            
        window = self.raw[start:end].replace("```", "")
        start = max(window.find(string), 0)
        end = min(start + len(string), raw_size)
        before = window[start:end].replace("\r", "").replace("\n", "")
        window = before + "    <-- HERE" + window[end:]
        
        return window
    
    def is_empty(self):
        return len(self.raw) == 0
    
    def get_stage(self):
        match = STAGE_PATTERN.search(self.raw.lower())
        
        if not match:
            return False, None
        stage = match.group(0)
        window = self.get_line_window(stage)
        is_final = "proposal" not in stage
        
        return is_final, window

    def get_repos(self) -> list[tuple[str, str]]:
        return list(filter(lambda x: x[0] != "kth",GITHUB_URL.findall(self.raw.lower())))

def get_tz():
    return pytz.timezone(getenv("INPUT_TZ") or 'Europe/Stockholm')

def localize(dt: datetime):
    tz = get_tz()
    
    return tz.localize(dt)

def parse_datetime_str(raw_datetime: str):
    try:
        return localize(datetime.strptime(raw_datetime, DATETIME_FORMAT))
    except Exception:
        return datetime.strptime(raw_datetime, "%Y-%m-%dT%H:%M:%S%z").astimezone(get_tz())

def get_payload(path: Path) -> Payload:
    return json.loads(path.read_bytes())

def get_pull_request(payload: Payload) -> Payload:
    return payload.get("pull_request", dict())

def get_created_at(payload: Payload) -> datetime:
    pr = get_pull_request(payload)
    return parse_datetime_str(pr.get("created_at"))

def get_updated_at(payload: Payload) -> datetime:
    pr = get_pull_request(payload)
    return parse_datetime_str(pr.get("updated_at"))

def get_comments_url(payload: Payload) -> str:
    pr = get_pull_request(payload)
    return pr.get("comments_url")

def get_pull_request_files(payload: Payload) -> list[Payload]:
    pr = get_pull_request(payload)
    url = pr["url"] + "/files"
    return requests.get(url=url).json()

def get_pr_body(payload: Payload) -> str:
    pr = get_pull_request(payload)
    return pr.get("body", "")


def get_files(payload: Payload) -> list[Markdown]:
    
    files = get_pull_request_files(payload)
    
    def get(filename: str):
        owner, repo, sha, branch = get_meta_details(payload)
        headers = {}
        headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        headers["Pragma"] = "no-cache"
        headers["Expires"] = "0"
        
        return requests.get(url=f"https://raw.githubusercontent.com/{owner}/{repo}/{sha}/{filename}").text
        
        
        
    def keep_markdown() -> list[Markdown]:
        return reduce(lambda acc, file_ : acc + [Markdown(name=file_["filename"],raw=get(file_["filename"]))] if file_["filename"].endswith(".md") and file_["status"] != "removed" else acc, files, [])
    
    kept_files = keep_markdown()
    
    if len(kept_files) == 0:
        raise FileNotFoundError("Pull request did not have any committed files")
    
    return kept_files
    

def get_meta_details(payload: Payload):
    pr = get_pull_request(payload)
    repository = cast(Payload,payload.get("repository"))
    head = cast(Payload, pr.get("head"))
    ref = head.get("ref")
    sha = head.get("sha")
    repo = repository.get("name")
    owner: str = cast(Payload,repository.get("owner"))["login"]
    return owner, repo, sha, ref
    
    

def get_issue_number(payload: Payload):
    pr = get_pull_request(payload)
    return pr["number"]

def get_repo(owner: str, repo: str, secret: Optional[str]) -> dict[str, str]:
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {}
    if secret:
        headers["Authorization"] = f"token {secret}"
    return requests.get(url=url,headers=headers).json()
    
def get_args(args: dict[str, str]) -> tuple[datetime, Payload, Optional[str]]:
    d, e, s = args.get("d"), args.get("e"), args.get('s')
    try:
        if not d:
            raise ValueError("Please provide a deadline")
        if not e:
            raise FileNotFoundError("Cannot find event payload")
        return parse_datetime_str(d), get_payload(Path(e)), s
    except Exception as exc:
        raise exc


def check_repo(repo, secret):
    owner, repo_name, = repo
    
    repo = get_repo(owner, repo_name, secret)
    is_private = repo.get("private", True)
    
    if is_private:
        raise PrivateRepoError("Provided repo is not public")
    

def validate(deadline: datetime, payload: Payload, secret: Optional[str] = None):
    
    payload["__result__"] = {"files": [],"created_at": None, "is_final": False}
    
    
    
    created_at = get_created_at(payload)
    updated_at = get_updated_at(payload)
    if updated_at > created_at:
        created_at = updated_at
        
    payload["__result__"]["created_at"] = created_at
        
    if created_at > deadline:
        raise AfterDeadlineError(f"Pull request after deadline: {deadline}")
    
    
    files = get_files(payload)
    for f in files:
        if not f.is_empty():
            payload["__result__"]["files"].append(f)
                        
            is_final, window = f.get_stage()
            repos = f.get_repos()
            
            if is_final:
                payload["__result__"]["is_final"] = is_final
            
            if len(repos) == 0 and is_final:
                raise MissingRepoError("No remote repository url found in provided pull request. Please provide one, or clearly state in your pull request that it is only a proposal.")
            if not window:
                raise UnclearPullRequest("Cannot find whether PR is __final submission__ or __proposal__. Please state it explicitly in your PR. Preferably as the title.")
            for repo in repos:
                check_repo(repo, secret)
    if len(payload["__result__"]["files"]) == 0:
        raise FileNotFoundError("No non-zero line files found. Make sure that your pull requests contains a markdown file")
    


def give_feedback(payload: Payload, secret: Optional[str], error_message: Optional[str] = None):
    
    result: dict[str, Any] = payload["__result__"]
    stage = "final_submission" if result["is_final"] else "proposal"
    
    if not secret:
        raise ValueError("No provided github secret")
    
    headers = {"Accept": "application/vnd.github.v3+json", "Authorization": f"token {secret}"}
    log = logger.error if error_message else logger.info

    def set_labels(labels: list[str]):
        issue_number = get_issue_number(payload)
        owner, repo, *_ = get_meta_details(payload)
        url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/labels"
        json_ = {"labels": labels}
        log("[PUT::LABELS]: " + str(json_))
        return requests.put(url=url,headers=headers,json=json_).json()
    

    def set_status(status: str, description: str, target_url: Optional[str] = None):
        owner, repo, sha, _ = get_meta_details(payload)
        url = f"https://api.github.com/repos/{owner}/{repo}/statuses/{sha}"
        json_ = {'status': status, 'description': description, 'context': 'Check mandatory part(s)'}
        if target_url:
            json_['target_url'] = target_url
            
        log("[POST::STATUS]: " + str(json_))
        return requests.post(url=url,headers=headers,json=json_).json()
    
    
    def send_comment(body: str):
        url = get_comments_url(payload)
        json_ = {"body": body}
        log("[POST::PR-COMMENT]: " + str(json_))
        return requests.post(url=url,headers=headers,json=json_).json()
    
    def format_repo_url(repotuple: tuple[str, str]):
        owner, repo = repotuple
        return f"[{repo}](https://www.github.com/{owner}/{repo})"
        
    
    def format_body():
        files: list[Markdown] = result["files"]
        created_at = result["created_at"]
        
        message = f"\n---\n\nDecision is based on the following findings:\n\ncreated at: {created_at}\n\n"
        for f in files:
            file_message = ""
            repos = f.get_repos()
            is_final, window = f.get_stage()
            stage = "final_submission" if is_final else "proposal"
            file_message += f"{f.name}\n---\n"
            
            if window:
                file_message += f"assumed stage: `{stage}`\n"
                file_message += f"```markdown\n...\n{window}\n...\n```\n"
            else:
                file_message += f"assumed stage: __NOT FOUND__\n"
                
            file_message += "repos:\n"
            if len(repos) == 0:
                file_message += "\t- No repos found\n"
            else:
                file_message += '\n'.join(map(lambda x : '\t- ' + format_repo_url(x), repos))
            message += file_message + "\n"
        
        if error_message:
            return error_message + message
        return "All mandatory parts were found. Awaiting TA for final judgement." + message
    
        
    status = 'failure' if error_message else "success"
    description = 'Validation failed' if error_message else "Validation successful"
    body = format_body()
    
    labels = ["course_automation"]
    
    if status != "failure":
        labels.append(stage)
    
    
    set_labels(labels)
    
    response = send_comment(body)
    url = response.get("html_url")
    
    set_status(status,description,url)
    
    
def run(args: dict[str, str]):
    payload, secret = {}, None
    try:
        deadline, payload, secret = get_args(args)
        validate(deadline, payload, secret)
                
        logger.info("Validation successful")
        give_feedback(payload, secret)
    
    except Exception as exc:
        message = "Error: " + " ".join(exc.args)
        
        logger.error(message)
        give_feedback(payload, secret, error_message=message)

        sys.exit(message)
        
    

def cli():
    parser = argparse.ArgumentParser(description="automatic course-automation evaluator")
    parser.add_argument('--deadline', dest="d",help="Deadline for the first task in the course", default=getenv("INPUT_DEADLINE"))
    parser.add_argument('--event', dest="e",help="Event path",default=getenv("INPUT_EVENT_PATH"))
    parser.add_argument('--secret', dest="s",help="Github secret",default=getenv("INPUT_SECRET"))
    args = parser.parse_args()
    args = vars(args)
    
    
    run(args)
    
if __name__ == "__main__":
    cli()

    