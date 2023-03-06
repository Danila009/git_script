import base64
import subprocess

import requests


def download_repos(username: str, password: str, limit: int):
    url = f'https://cfif31.ru:3000/api/v1/users/{username}/repos?limit={limit}'

    token = base64.b64encode(bytes(f'{username}:{password}', 'utf-8'))

    response = requests.get(url, headers={
        'Authorization': f'Basic {token.decode("utf-8")}'
    })

    json = response.json()

    subprocess.run(['mkdir', f'repos_{username}'])

    for repos in json:
        print('-------------------------------')
        clone_url = repos['clone_url']
        subprocess.run(['git', 'clone', clone_url])
