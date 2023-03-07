from api import download_repos, push_repos

print('git username')
from_username = input()
print('git password')
from_password = input()
print('limit repository')
limit = int(input())
print('push github repos [y/n]')
cloneRepos = input()

if cloneRepos == 'y':
    print('github username')
    to_username = input()
    print('github token')
    token_github = input()

    push_repos(from_username, from_password, to_username, token_github, limit)
else:
    download_repos(from_username, from_password, limit)
