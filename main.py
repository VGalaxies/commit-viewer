import github

import os
import json
import csv

from datetime import datetime

from rich.console import Console
from rich.progress import track
from rich.table import Table

csv_path = "data.csv"
config_path = "config.json"


def display(res):
    console = Console()
    console.rule("statistics")

    table = Table()
    table.add_column("Date")
    table.add_column("Repo")
    table.add_column("Msg")

    for (date, repo, msg) in res:
        table.add_row(str(date), repo, msg)

    console.print(table)


def parse_config(path):
    with open(path) as f:
        config = json.load(f)
    username = config.get('username')
    access_token = config.get('access_token')
    return username, access_token


def read_csv(path):
    if os.path.exists(path) and os.path.getsize(path):
        res = []
        with open(csv_path, "r") as f:
            for row in csv.reader(f, delimiter="|"):
                res.append(row)
            return res
    return None


def write_csv(path, res):
    with open(path, "w") as f:
        csv.writer(f, delimiter="|").writerows(res)


def fetch():
    res = read_csv(csv_path)
    if res is not None:
        return res

    res = []
    date_format = '%Y-%m-%dT%H:%M:%SZ'

    username, access_token = parse_config(config_path)
    g = github.Github(access_token)
    repo_list = [i for i in g.get_user().get_repos()]

    for repo_index in track(range(len(repo_list))):
        repo = repo_list[repo_index]

        repo_name = str(repo).replace('Repository(full_name="', '').replace('")', '')
        commit_list = repo.get_commits(author=username)

        try:  # empty repo
            for page_index in range(commit_list.totalCount):
                commit_page = commit_list.get_page(page_index)

                for commit in commit_page:
                    commit_info = commit.raw_data['commit']

                    date = commit_info['author']['date']
                    msg = commit_info['message']

                    res.append((datetime.strptime(date, date_format), repo_name, msg))

        except github.GithubException:
            pass

    res.sort(key=lambda t: t[0])
    write_csv(csv_path, res)
    return res


display(fetch())
