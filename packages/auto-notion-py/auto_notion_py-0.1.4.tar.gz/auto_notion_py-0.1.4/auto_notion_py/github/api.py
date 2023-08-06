from venv import create
from auto_notion_py.notion.api import notion_db_push, ColumnType, NotionColumn

from github import Github, PullRequest, Repository, AuthenticatedUser, Organization
from typing import Tuple, List, Set, Optional, Union, Dict, Any
from dataclasses import dataclass
import pandas as pd
import datetime
import asyncio
import itertools
from aiomultiprocess import Pool

@dataclass(frozen=False)
class GHFetchRepo:
    name: str
    creators: Optional[List[str]]

@dataclass(frozen=True)
class GHFetchOrg:
    name: str
    creators: Optional[List[str]]
    repositories: Optional[List[GHFetchRepo]]

@dataclass(frozen=True)
class GHFetch:
    token: str
    creators: Optional[List[str]]
    organizations: List[GHFetchOrg]

@dataclass(frozen=True)
class PullRequestData:
    repo_org_owner: str
    
    uid: str
    repo_name: str
    title: str
    pr_id: int
    is_open: bool
    is_merged: bool
    is_draft: bool
    assignees: Set[str]
    created_at: datetime.datetime
    url: str
    creator: str
    authors: Set[str]
    commits: List[int]
    commits_md: str
    authors_md: str
    assignees_md: str
    state_labels: List[str]
    age_days: int
        
    current_reviewers: List[str]
    needs_review_attention: bool



def lists_intersection(*inputs: List[Optional[List[str]]]) -> Optional[List[str]]:
    ret = None
    for input in inputs:
        if input is not None:
            if ret is None:
                ret = set(input)
            else:
                ret = ret.intersection(set(input))
    if ret is None:
        return None
    return list(ret)


async def handle_repo_dict(args: Dict[str, Any]) -> List[PullRequestData]:
    return await handle_repo(**args)

async def handle_repo(
    token: str,
    repo: Repository,
    settings: GHFetchRepo,
    user: Union[AuthenticatedUser.AuthenticatedUser, Organization.Organization],
) -> List[PullRequestData]:
    # Do not dispatch forks and archived repos
    if repo.fork or repo.archived:
        return []
    g = Github(login_or_token=token, per_page=100)
    repo_rows: List[PullRequestData] = []
    if settings.creators is not None:
        new_val: Set[str] = set()
        for creator in settings.creators:
            if creator == "user":
                new_val.add(g.get_user().login)
            else:
                new_val.add(creator)
        settings.creators = new_val

    prs = repo.get_pulls(state='open', sort='created')
    for pr in prs:
        if settings.creators is not None and pr.user.login not in settings.creators:
                continue
        row = pr_to_row(pr, repo, user.login)
        repo_rows.append(row)
    return repo_rows

async def get_pull_requests_df(
    settings: List[GHFetch],
) -> pd.DataFrame:
    instance_args: List[Dict[str, Any]] = []
    for instance_settings in settings:
        instance_args.append(dict(
            settings=instance_settings,
        ))
    rows: List[PullRequestData] = []
    for result in await asyncio.gather(*[fetch_pull_requests_for_settings_instance_dict(args) for args in instance_args]):
        rows += result
    #async for result in pool.map(fetch_pull_requests_for_settings_instance_dict, instance_args):
    #    rows += result
    return pd.DataFrame(rows)
    

async def fetch_pull_requests_for_settings_instance_dict(args: Dict[str, Any]) -> List[PullRequestData]:
    return await fetch_pull_requests_for_settings_instance(**args)

async def fetch_pull_requests_for_settings_instance(
    settings: GHFetch
) -> List[PullRequestData]:
    rows: List[PullRequestData] = []
    orgs_args: List[Dict[str, Any]] = []

    token = settings.token
    g = Github(login_or_token=token, per_page=100)
    for org in settings.organizations:
        if org.name == "user":
            user = g.get_user()
        else:
            user = g.get_organization(org.name)
        orgs_args.append(dict(
            session_settings=settings,
            org=org,
            user=user,
        ))

    async with Pool() as pool:
        async for result in pool.map(fetch_pull_requests_for_org_dict, orgs_args):
            rows += result
    return rows


async def fetch_pull_requests_for_org_dict(args: Dict[str, Any]) -> List[PullRequestData]:
    return await fetch_pull_requests_for_org(**args)

async def fetch_pull_requests_for_org(
    session_settings: GHFetch,
    org: GHFetchOrg,
    user: Union[AuthenticatedUser.AuthenticatedUser, Organization.Organization],
) -> List[PullRequestData]:
    
    repos_args: List[Dict[str, Any]] = []

    # Propagate settings
    if org.repositories is not None:
        for repo in org.repositories:
            repo.creators = lists_intersection(repo.creators, org.creators, session_settings.creators)

    token = session_settings.token
    if org.repositories is not None:
        for repo_settings in org.repositories:
            repo = None
            repo = user.get_repo(repo_settings.name)
            if repo is not None:
                repos_args.append(dict(
                    token=token,
                    repo=repo,
                    settings=repo_settings,
                    user=user,
                ))
    else:
        for repo in user.get_repos():
            repos_args.append(dict(
                token=token,
                repo=repo,
                settings=GHFetchRepo(
                    name=repo.name,
                    creators=lists_intersection(org.creators, session_settings.creators),
                ),
                user=user,
            ))
        
    rows: List[PullRequestData] = []   
    async with Pool() as pool: 
        async for result in pool.map(handle_repo_dict, repos_args):
            rows += result
    return rows


def list_to_md(input_list) -> str:
    return "\n".join([f" * {item}" for item in input_list])

def pr_to_row(
    pr: PullRequest,
    repo: Repository,
    user_login: str,
    old_threshold_days: int = 7,
    stale_threshold_days: int = 14,
) -> PullRequestData:
    authors: Set[str] = set()
    commits: List[str] = []
    current_reviewers: Set[str] = set()
        
    last_change = None
    pr_needs_review_attention = False
    has_reviews = False
    for commit in pr.get_commits():
        if commit.author:
            commit_date = commit.commit.author.date
            if last_change is None or last_change > commit_date:
                last_change = commit_date
            authors.add(commit.author.login)
        if commit.commit:
            lines = commit.commit.message.split("\n")
            if len(lines) > 0:
                commits.append(lines[0])
        
    for review in pr.get_reviews():
        if review.state != 'CHANGES_REQUESTED':
            continue
        current_reviewers.add(review.user.login)
        has_reviews = True
        review_date = review.last_modified
        if review_date is None:
            review_date = review.submitted_at
        if review_date is not None and last_change is not None:
            if review_date < last_change:
                pr_needs_review_attention = True
    pr_needs_review_attention = pr_needs_review_attention or (not has_reviews)
        
        
    is_open = (pr.state == 'open')
    is_draft = pr.draft
    is_merged = pr.is_merged()
    
    state_labels: List[str] = []
    if is_open:
        state_labels.append("open")
    if is_draft:
        state_labels.append("draft")
    if is_merged:
        state_labels.append("merged")
    
    created_at = pr.created_at
    age_days = abs((datetime.datetime.today() - created_at).days)
    
    if age_days >= old_threshold_days and age_days < stale_threshold_days:
        state_labels.append("old")
        
    if age_days >= stale_threshold_days:
        state_labels.append("stale")
        
    if pr_needs_review_attention:
        state_labels.append("needs review")
    
    return PullRequestData(
        repo_org_owner=user_login,
        uid=f"{repo.name}-{pr.number}",
        repo_name=repo.name,
        title=pr.title,
        pr_id=pr.number,
        current_reviewers=list(current_reviewers),
        needs_review_attention=pr_needs_review_attention,
        is_open=is_open,
        is_merged=is_merged,
        is_draft=is_draft,
        created_at=pr.created_at,
        assignees=set(pr.assignees),
        url=pr.html_url,
        creator=pr.user.login,
        authors=authors,
        commits=commits,
        age_days=age_days,
        commits_md=list_to_md(commits),
        authors_md=list_to_md(authors),
        assignees_md=list_to_md(set(pr.assignees)),
        state_labels=state_labels,
    )
