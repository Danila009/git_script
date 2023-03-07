import base64
import pathlib
import subprocess

import requests
from cd import cd

base_path = pathlib.Path().resolve()


def download_repos(username: str, password: str, limit: int):
    url = f'https://cfif31.ru:3000/api/v1/users/{username}/repos?limit={limit}'

    token = get_token(username, password)

    response = requests.get(url, headers={
        'Authorization': f'Basic {token.decode("utf-8")}'
    })

    json = response.json()

    subprocess.run(['mkdir', f'repos_{username}'], shell=True)

    with cd(f'{base_path}\\repos_{username}'):
        for repos in json:
            print('-------------------------------')
            clone_url = repos['clone_url']
            subprocess.run(['git', 'clone', clone_url], shell=True)


def push_repos(fromUsername, fromPassword, toUsername: str, token_github: str, limit: int):
    url = f'https://cfif31.ru:3000/api/v1/users/{fromUsername}/repos?limit={limit}'

    from_token = get_token(fromUsername, fromPassword)

    get_repos_response = requests.get(url, headers={
        'Authorization': f'Basic {from_token.decode("utf-8")}'
    })

    repos_json = get_repos_response.json()

    subprocess.run(['mkdir', f'repos_{fromUsername}'], shell=True)

    with cd(f'{base_path}\\repos_{fromUsername}'):
        for repos in repos_json:
            clone_url = repos['clone_url']
            repos_name = repos['name']
            print('-------------------------------')
            subprocess.run(['git', 'clone', clone_url], shell=True)
            create_repos(toUsername, token_github, repos_name)

            with cd(f'{base_path}\\repos_{fromUsername}\\{repos_name}'):
                subprocess.run(['git', 'remote', 'remove', 'origin'], shell=True)
                subprocess.run(['git', 'remote', 'add', 'origin', f'https://github.com/{toUsername}/{repos_name}.git'], shell=True)
                subprocess.run(['git', 'push', '-u', 'origin', 'master'], shell=True)
                subprocess.run(['cd', f'{base_path}\\repos_{fromUsername}'], shell=True)


def create_repos(username: str, token_github, reposName: str):
    url = f'https://api.github.com/user/repos'

    response = requests.post(url, headers={
        'Authorization': f'Bearer {token_github}'
    }, json={
        'name': reposName
    })

    print("------------------")
    print(response.url)
    print(response)
    print("------------------")


def get_token(username: str, password: str) -> bytes:
    return base64.b64encode(bytes(f'{username}:{password}', 'utf-8'))
