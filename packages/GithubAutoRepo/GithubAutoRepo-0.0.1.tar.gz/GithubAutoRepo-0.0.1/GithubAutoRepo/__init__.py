import os
import requests

def autoRepo(REPO_PATH,GITHUB_TOKEN,GITHUB_USERNAME):
    repo_name = input("Enter the name of the repo: ")
    private_check = (input("Do you want to make the repo private? (y/n): ")).lower()
    comment = (input("Enter commit comment : ")).lower()

    if(private_check == 'y'):
        is_private = True
    else:
        is_private = False

    if is_private:
        payload = '{"name": "' + repo_name + '", "private": true }'
    else:
        payload = '{"name": "' + repo_name + '", "private": false }'

    headers = {
        "Authorization": "token " + GITHUB_TOKEN,
        "Accept": "application/vnd.github.v3+json"
    }
    try:
        r = requests.post("https://api.github.com/user/repos", data=payload, headers=headers)
        r.raise_for_status()
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)

    try:
        os.chdir(REPO_PATH)
        os.system("git init")
        os.system("git add .")
        os.system('git commit -m " '+str(comment)+'"') 
        os.system("git branch -M main")
        os.system("git remote add origin https://github.com/" + GITHUB_USERNAME + "/" + repo_name + ".git")
        os.system("git push -u origin main")
        return "Success"

    except FileExistsError as err:
        raise SystemExit(err)