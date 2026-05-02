import json
import requests
from pathlib import Path
from detect_secrets.settings import default_settings
from detect_secrets import SecretsCollection

from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_PR_SCANNER = os.getenv("GITHUB_PR_SCANNER")

repo = "infra"
pr_number = 6
owner = "preetharman40"

secrets = SecretsCollection()

def scanning_files(file):
    
    file_path = Path(f"{file}")
    print(file_path)

    if file_path.is_file():
        with default_settings():
            secrets.scan_file(f"{file_path}")

        

    else:
        print("The file does not exist")






def get_pr_changed_files(owner, repo, pr_number):
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"

    headers = {
        "Authorization": f"Bearer {GITHUB_PR_SCANNER}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.get(url, headers=headers)

    

    if response.status_code == 200:
        files = response.json()

        for i in range(0, len(files)):

            print(files[i]['filename'])

            changed_file = files[i]['filename']
            scanning_files(changed_file)

    
    else:
        return f"Error: {response.status_code} - {response.text}"
    

def main():
    get_pr_changed_files(owner=owner, repo=repo, pr_number=pr_number)










if __name__ == '__main__':
    main()