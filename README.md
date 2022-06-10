# Commit Viewer

## Fetch

`(date, repo_name, commit_msg)`

sorted by date

### Github REST API

https://docs.github.com/cn/rest

```python
import requests
import json

user = 'VGalaxies'
r = requests.get('https://api.github.com/users/{}/repos'.format(user))

if r.status_code == 200:
    repo_infos = json.loads(r.text)
    print(repo_infos)
```

cannot access to private repo information

#### PyGithub

https://github.com/PyGithub/PyGithub

configuration stored in **json** file for safety

```json
{
  "username": "xxx",
  "access_token": "xxx"
}
```
store data in **csv** file

## Display

https://github.com/Textualize/rich

- progress
- table
- console