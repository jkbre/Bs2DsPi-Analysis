import requests


def from_github_repo(repo_url):
    parts = repo_url.split("/")
    owner = parts[-2]
    repo = parts[-1]
    api_url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    response = requests.get(api_url)
    file_url = response.json()["assets"][0]["browser_download_url"]
    return file_url


def from_nexusmods(apikey, gamename, mod_id):  #! Needs a payed account in order to download files
    apikey = "YK64227HxQx/cGKFSihidDUw2w1bYD69+5Jfa9SayHIeTuIL--gDKBjR0nLFppmTcA--JwmEiIwTn3gcfd+OcMxnAQ=="
    apiurl = "https://api.nexusmods.com/v1"
    gameurl = f"/games/{gamename}"
    modurl = f"/mods/{mod_id}"
    url = apiurl + gameurl + modurl
    print(url)
    json = requests.get(url + "/files.json", headers={"apikey": apikey}).json()
    index = 0  # TODO: add the list of files to choose from based on json
    file_id = json["files"][index]["file_id"]
    fileurl = "/files/" + str(file_id) + "/download_link.json"
    url = apiurl + gameurl + modurl + fileurl
    print(url)
    json = requests.get(url, headers={"apikey": apikey}).json()
    return json
