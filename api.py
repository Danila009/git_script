import base64
import pathlib
import shutil
import subprocess

import requests
from cd import cd

base_path = pathlib.Path().resolve()


def download_repos(username: str, password: str, limit: int, page: int):
    url = f'https://cfif31.ru:3000/api/v1/users/{username}/repos?limit={limit}&page={page}'

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


def push_repos(fromUsername, fromPassword, toUsername: str, token_github: str, limit: int, page: int):
    url = f'https://cfif31.ru:3000/api/v1/users/{fromUsername}/repos?limit={limit}&page={page}'

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
            create_repos(token_github, repos_name)

            with cd(f'{base_path}\\repos_{fromUsername}\\{repos_name}'):
                for branch in get_branches(fromUsername, fromPassword, repos_name):
                    subprocess.run(['git', 'checkout', branch['name']], shell=True)
                    subprocess.run(['git', 'remote', 'remove', 'origin'], shell=True)
                    subprocess.run(
                        ['git', 'remote', 'add', 'origin', f'https://github.com/{toUsername}/{repos_name}.git'],
                        shell=True)
                    subprocess.run(['git', 'checkout', '-b', branch['name']], shell=True)
                    subprocess.run(['git', 'push', '-u', 'origin', branch['name']], shell=True)
                    subprocess.run(['cd', f'{base_path}\\repos_{fromUsername}'], shell=True)

    subprocess.run(['cd', base_path], shell=True)
    shutil.rmtree(f'{base_path}\\repos_{fromUsername}')


def create_repos(token_github, reposName: str):
    url = f'https://api.github.com/user/repos'

    response = requests.post(url, headers={
        'Authorization': f'Bearer {token_github}'
    }, json={
        'name': reposName,
        'default_branch': 'master'
    })

    print("------------------")
    print(response.url)
    print(response)
    print("------------------")


def get_branches(username: str, password: str, repos_name: str) -> dict:
    url = f'https://cfif31.ru:3000/api/v1/repos/{username}/{repos_name}/branches'
    token = get_token(username, password)

    get_repos_response = requests.get(url, headers={
        'Authorization': f'Basic {token.decode("utf-8")}'
    })

    return get_repos_response.json()


def get_token(username: str, password: str) -> bytes:
    return base64.b64encode(bytes(f'{username}:{password}', 'utf-8'))
