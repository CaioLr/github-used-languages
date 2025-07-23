import requests

def get_repositories_list(username:str) -> list[dict]:


    response = requests.get(f"https://api.github.com/users/{username}/repos")

    repos = []

    if response.status_code == 200:
        for repo in response.json():
            repos.append({
                "name": repo["name"],
                "default_branch": repo["default_branch"],
            })
        return repos
    
    else:
        return []

def get_repo_files(username:str, repo:str, branch:str) -> list[dict]:
    response = requests.get(f"https://api.github.com/repos/{username}/{repo}/git/trees/{branch}?recursive=1") 

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


def calculate_language_usage(repos: dict) -> dict:
    
    languages_usage = {}

    for repo in repos:
        for file_extension in repo["files"]:
            
            if file_extension not in languages_usage:
                languages_usage[file_extension] = {
                    "size": repo["files"][file_extension],
                    "amount": 1
                } 
            if file_extension in languages_usage:
                languages_usage[file_extension]["size"] += repo["files"][file_extension]
                languages_usage[file_extension]["amount"] += 1
    
    return languages_usage
        

def calculate_percentage_usage(languages_usage: dict,size_weight = 0.5,amount_weight = 0.5) -> dict:
    
    for language in languages_usage:
        total_size = sum(language["size"] for language in languages_usage.values())
        total_amount = sum(language["amount"] for language in languages_usage.values())
        
        languages_usage[language]["percentage_size"] = (languages_usage[language]["size"] / total_size) * 100
        languages_usage[language]["percentage_amount"] = (languages_usage[language]["amount"] / total_amount) * 100
        languages_usage[language]["total_percentage"] = (languages_usage[language]["percentage_size"]  * size_weight) + (languages_usage[language]["percentage_amount"] * amount_weight)

    return languages_usage

    


def fetch_data_from_api(username): 
    
    repos = get_repositories_list(username)

    if not repos:
        return {"error": "Failed to fetch data"}

    for repo in repos:
        repo["files"] = get_repo_files(username, repo["name"], repo["default_branch"])

    languages_usage = calculate_language_usage(repos)
    percentage_usage = calculate_percentage_usage(languages_usage)

    return percentage_usage 


   
