import requests
import json, os
from dotenv import load_dotenv # type: ignore
from typing import Optional

load_dotenv()

def get_repositories_list(username:str) -> Optional[list[dict]]:
    
    headers = {
        "Authorization": f"Bearer {os.getenv('TOKEN')}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.get(f"https://api.github.com/users/{username}/repos",headers=headers)

    repos = []

    if response.status_code == 200:
        for repo in response.json():
            repos.append({
                "name": repo["name"],
                "default_branch": repo["default_branch"],
                "pushed_at": repo["pushed_at"]
            })
        return repos
    
    else:
        return []


def get_repo_files(username:str, repo:str, branch:str) -> list[dict]:
    headers = {
        "Authorization": f"Bearer {os.getenv('TOKEN')}",
        "Accept": "application/vnd.github+json"
    }

    response = requests.get(f"https://api.github.com/repos/{username}/{repo}/git/trees/{branch}?recursive=1",headers=headers) 

    files = {}
    path_extension = ""

    if response.status_code == 200:
        for file in response.json()["tree"]:
            if file["type"] == "blob":
                if "." in file["path"]:

                    path_extension = file["path"].rsplit('.', 1)[1]

                    if path_extension not in files:
                        files[path_extension] = file["size"]
                        
                        
                    if path_extension in files:
                         files[path_extension] += file["size"]
        
        return files
    else:
        return {"error": "Failed to fetch data"}


def calculate_language_usage(repos: dict, config: dict) -> dict:

    extensions = []

    for config_lang in config["languages"]:
        if config_lang["name"] not in config["disable_languages"]:
            extensions.extend(config_lang["extensions"])

    languages_usage = {}

    for repo in repos:
        for file_extension in repo["files"]:
            if file_extension in extensions:   
                if file_extension not in languages_usage:
                    languages_usage[file_extension] = {
                        "size": repo["files"][file_extension],
                        "amount": 1
                    } 
                if file_extension in languages_usage:
                    languages_usage[file_extension]["size"] += repo["files"][file_extension]
                    languages_usage[file_extension]["amount"] += 1
    
    return languages_usage


def calculate_percentage_usage(languages_usage: dict, config: dict, size_weight=0.6, amount_weight=0.4) -> dict:

    total_size = sum(language["size"] for language in languages_usage.values())
    total_amount = sum(language["amount"] for language in languages_usage.values())

    for language in languages_usage:
       
        languages_usage[language]["percentage_size"] = (languages_usage[language]["size"] / total_size) * 100
        languages_usage[language]["percentage_amount"] = (languages_usage[language]["amount"] / total_amount) * 100
        languages_usage[language]["total_percentage"] = (languages_usage[language]["percentage_size"]  * size_weight) + (languages_usage[language]["percentage_amount"] * amount_weight)

    final_usage = {}

    for lang in languages_usage:
        for config_lang in config["languages"]:

            if lang in config_lang["extensions"]:

                if config_lang["name"] in final_usage:
                    final_usage[config_lang["name"]] += languages_usage[lang]["total_percentage"]

                if config_lang["name"] not in final_usage:
                    final_usage[config_lang["name"]] = languages_usage[lang]["total_percentage"]
                
    return final_usage


def fetch_data(username, config, repos) -> list: 

    if not repos:
        return {"error": "Failed to fetch data"}

    for repo in repos:
        repo["files"] = get_repo_files(username, repo["name"], repo["default_branch"])
    
    languages_usage = calculate_language_usage(repos, config)
    percentage_usage = calculate_percentage_usage(languages_usage, config)
    sorted_percentage_usage = sorted(percentage_usage.items(), key=lambda item: item[1], reverse=True)

    return sorted_percentage_usage