import os
import github
import json
import pickle

from datetime import datetime

from rich.console import Console
from rich.progress import track
from rich.table import Table

config_path = "config.json"
data_path = "raw.data"

date_format = '%Y-%m-%dT%H:%M:%SZ'
res = dict()

if os.path.exists(data_path) and os.path.getsize(data_path):
    with open(data_path, "rb") as f:
        res = pickle.load(f)
        print(res)

with open(config_path) as f:
    config = json.load(f)
username = config.get('username')
access_token = config.get('access_token')

g = github.Github(access_token)
repo_list = [i for i in g.get_user().get_repos()]

# for repo_index in track(range(len(repo_list))):
for repo_index in track(range(4)):
    repo = repo_list[repo_index]

    repo_name = str(repo).replace('Repository(full_name="', '').replace('")', '')
    commit_list = repo.get_commits(author=username)

    try:  # empty repo
        for page_index in range(commit_list.totalCount):
            commit_page = commit_list.get_page(page_index)

            for commit in commit_page:
                commit_info = commit.raw_data['commit']

                name = commit_info['author']['name']
                date = commit_info['author']['date']
                msg = commit_info['message']

                res[datetime.strptime(date, date_format)] = [repo_name, msg]

    except github.GithubException:
        pass

res = sorted(res.items(), key=lambda d: d[0])

with open(data_path, "wb") as f:
    pickle.dump(res, f)

console = Console()
console.rule("statistics")

table = Table()
table.add_column("Date")
table.add_column("Repo")
table.add_column("Msg")

for (date, [repo, msg]) in res:
    table.add_row(str(date), repo, msg)

console.print(table)
