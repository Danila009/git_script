from api import download_repos

print('git username')
username = input()
print('git password')
password = input()
print('limit repository')
limit = int(input())

download_repos(username, password, limit)

