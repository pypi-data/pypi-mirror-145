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


def GetBoardFromGitlab():  # for getting repository information
    logging.info('This is in GetBoardFromGitlab function')
    url = config('gitlab_url')
    token = config('gitlab_token')
    headers1 = {"Authorization": token}
    r = requests.get(url=url, headers=headers1)
    jsondata = r.json()
    myBoardName = jsondata.get('name')
    return myBoardName


def CreateBoard(apiUrl, headers, myBoardName):  # for creating a board with repository name
    logging.info('This is in CreateBoard function')
    query1 = 'mutation ($myBoardName: String!) { create_board (board_name: $myBoardName, board_kind: share) { id }}'
    vars = {
        'myBoardName': myBoardName
    }
    data1 = {'query': query1, 'variables': vars}
    # r = requests.post(url=apiUrl, json=data1, headers=headers)
    # jsondata = r.json()


def GetBoardIds():  # for Getting each board id
    q = 'query { boards {id workspace_id} }'
    data1 = {'query': q}
    r = requests.post(url=apiUrl, json=data1, headers=headers)
    data = r.json()
    data = data['data']
    print(data['boards'])
    board_ids = []
    for i in data['boards']:
        board_ids.append(i['id'])
    return board_ids


def GetBoardItem(board_ids, apiUrl, headers):  # for getting all items of perticular board
    logging.info('This is in GetBoardItem function')
    for i in board_ids:
        query2 = 'query ($board_id: [Int]) { boards (ids: $board_id) {items {id name column_values {id title value} } ' \
                 '} } '
        vars = {'board_id': int(i)}
        data2 = {'query': query2, 'variables': vars}
        r = requests.post(url=apiUrl, json=data2, headers=headers)
        data = r.json()
        ValidateCoulmnData(data)


def ValidateCoulmnData(data):  # for getting not validate item of board
    test_board_id = config('test_board_id')
    status_option = ["In progress", "Done", "Stuck", "", "", "Not Defined"]
    itemdata = data['data']
    items = {}
    data_list = []

    for i in itemdata['boards'][0]['items']:
        d1 = i.get('column_values')
        value_dict = []
        for j in d1:
            value_dict.append(j.get('value'))

        value_dict = [json.loads(value) if value is not None else value for value in value_dict]

        column_data = []
        new_item_dict = {}
        myItemName = []
        data_dict = {}

        if (None in value_dict) or ('""' in value_dict) or ("" in value_dict) or (
                {"personsAndTeams": []} in value_dict):
            myItemName = i['name'] + ':' + i['id'] + '-'
            for k in range(len(value_dict)):
                if (value_dict[k] is None) or value_dict[k] == '""' or value_dict[k] == {"personsAndTeams": []}:
                    myItemName = myItemName + (d1[k]['title']) + ' missing'
                    if d1[k]['title'] == 'Date':
                        d1[k]['value'] = {'date': datetime.now().strftime("%Y-%m-%d")}
                    if d1[k]['title'] == 'People':
                        d1[k]['value'] = {"personsAndTeams": [{"id": 28867688, "kind": "person"}]}
                    if d1[k]['title'] == 'Project':
                        d1[k]['value'] = {d1[k]['id']: "Project Missing"}
                    column_data.append(d1[k])
                else:
                    d1[k]['value'] = value_dict[k]
                    column_data.append(d1[k])
                new_item_dict["name"] = myItemName
                new_item_dict[i.get('id')] = column_data
            data_list.append(new_item_dict)

            # for craete item in board
            for k in column_data:
                # if k['title'] == 'People':
                # if k['value'] == {"personsAndTeams":[]}:
                # 	data_dict[k['id']] = {"personsAndTeams":[{"id":28867688,"kind":"person"}]}
                # people = json.loads(k['value'])['personsAndTeams']

                if k['title'] == 'Status':
                    if k['value'] is not None:
                        if k['value']['index'] == 0:
                            data_dict[k['id']] = {"label": status_option[0]}

                else:
                    data_dict[k['id']] = k["value"]
            query2 = 'query ($test_board_id: [Int]){ boards (ids: $test_board_id) {items {id name column_values {id ' \
                     'title value} } } } '
            vars = {'test_board_id': int(test_board_id)}
            data2 = {'query': query2, 'variables': vars}

            r = requests.post(url=apiUrl, json=data2, headers=headers)
            data = r.json()
            test_title_list = data['data']
            title_list = []
            for i in test_title_list['boards'][0]['items']:
                title_list.append(i['name'])
            if myItemName not in title_list:
                query1 = 'mutation ($myItemName: String!, $columnVals: JSON!) { create_item (board_id:2442446572, ' \
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


def CreateFile(name):  # for create item if created document name is not valid
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

# function call
myBoardName = GetBoardFromGitlab()
CreateBoard(apiUrl, headers, myBoardName)
board_ids = GetBoardIds()
GetBoardItem(board_ids, apiUrl, headers)
CreateFile(myBoardName)
