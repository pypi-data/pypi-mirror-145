import click
import yaml
from yaml.loader import SafeLoader
from os.path import exists
import os
import datetime
import json
from datetime import datetime
import logging
import requests
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from decouple import config


apiKey = config('monday_apikey')
apiUrl = "https://api.monday.com/v2"
headers = {"Authorization": apiKey, "Content-Type ": "application/json"}

@click.group()
@click.command()
def cli():
    """Example script."""
    file_exists = exists(os.getcwd() + '/audit-dog.yml')

    if not file_exists:
        with open('spec.yml', 'r') as f:
            yaml_data = list(yaml.load_all(f, Loader=SafeLoader))

        yml_data = [{'client': yaml_data[0]['client'], 'repo_name': yaml_data[0]['name'],
                     'repo_description': yaml_data[0]['description']}]
        with open('audit-dog.yml', 'w') as f:
            data = yaml.dump(yml_data, f, sort_keys=False, default_flow_style=False)
            print(data)

@click.command()
def run():
    name = GetBoardFromGitlab()
    non_conformance_id = config('non_conformance_id')
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)

    folder_list = []
    # get all folder name
    f = drive.ListFile({"q": "mimeType='application/vnd.google-apps.folder' and trashed=false"}).GetList()
    for folder in f:
        folder_list.append(folder['title'])

    if name not in folder_list:
        # Create folder
        folder_metadata = {'title': name, 'mimeType': 'application/vnd.google-apps.folder'}
        folder = drive.CreateFile(folder_metadata)
        folder.Upload()

    # Get folder info and print to screen
    foldertitle = folder['title']
    folderid = folder['id']

    # Upload file to folder
    # file = drive.CreateFile({"parents": [{"kind": "drive#fileLink", "id": folderid}]})
    # file.SetContentFile('data1.xlsx')
    # file.Upload()

    str = "\'" + folderid + "\'" + " in parents and trashed=false"
    file_list_names = []
    file_list = drive.ListFile({'q': str}).GetList()
    for file in file_list:
        file_list_names.append(file['title'])

    for f in file_list_names:
        if f.startswith("Sigil"):
            print("Valid")
        else:
            query2 = 'query ($non_conformance_id: [Int]){ boards (ids: $non_conformance_id) {items {id name ' \
                     'column_values {id title value} } } } '
            vars = {'non_conformance_id': int(non_conformance_id)}
            data2 = {'query': query2, 'variables': vars}
            r = requests.post(url=apiUrl, json=data2, headers=headers)
            data = r.json()
            itemdata = data['data']
            title_list = []
            myItemName = "Make Sure Your File Name Is Correct " + f
            if len(itemdata['boards'][0]['items']) != 0:
                for i in itemdata['boards'][0]['items']:
                    title_list.append(i['name'])
            if myItemName not in title_list:
                data_dict = {"people": {"personsAndTeams": [{"id": 28867688, "kind": "person"}]},
                             "date4": {'date': datetime.now().strftime("%Y-%m-%d")},
                             "text": foldertitle}
                print("Invalid")
                query1 = 'mutation ($myItemName: String!, $columnVals: JSON!) { create_item (board_id:2494152527, ' \
                         'item_name:$myItemName, column_values:$columnVals) { id } } '
                vars = {
                    "myItemName": myItemName,
                    "columnVals": json.dumps(data_dict)
                }
                item_create = {"query": query1, "variables": vars}
                try:
                    r = requests.post(url=apiUrl, json=item_create, headers=headers)
                    jsondata = r.json()
                except Exception as e:
                    print(e)

def GetBoardFromGitlab():  # for getting repository information
    logging.info('This is in GetBoardFromGitlab function')
    url = config('gitlab_url')
    token = config('gitlab_token')
    headers1 = {"Authorization": token}
    r = requests.get(url=url, headers=headers1)
    jsondata = r.json()
    myBoardName = jsondata.get('name')
    return myBoardName