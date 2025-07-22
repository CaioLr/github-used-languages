import requests

def get_repositories_list(username) -> list[dict]:


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

def get_repo_files(username, repo, branch) -> list[dict]:
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

def fetch_data_from_api(username): 
    
    repos = get_repositories_list(username)

    if repos:
        for repo in repos:
            repo["files"] = get_repo_files(username, repo["name"], repo["default_branch"])


    if not repos:
        return {"error": "Failed to fetch data"}
    
    return repos

