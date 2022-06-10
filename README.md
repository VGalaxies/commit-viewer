# Github REST API

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

# PyGithub

https://github.com/PyGithub/PyGithub

