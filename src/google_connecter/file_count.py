from googleapiclient.discovery import build
from httplib2 import Http
from googleapiclient.http import MediaFileUpload
from oauth2client import file, client, tools


def countss(folder_id, scope="https://www.googleapis.com/auth/drive", token="assets/token.json", cred="assets/credentials.json"):
    storage = file.Storage(token)
    credentrial = storage.get()
    if not credentrial or credentrial.invalid:
        print('## Cannot find Google API Credential')
        print('## Create new Credential')
        flow = client.flow_from_clientsecrets(
            cred, scope)
        credentrial = tools.run_flow(flow, storage)

    # create google drive service
    service = build('drive', 'v3', http=credentrial.authorize(Http()))

    query = f'mimeType="*/*" and "{folder_id}" in parents'

    page_token = None
    file_count = 0
    while True:
        folder = service.files().list(q=query,
                                      spaces='drive',
                                      fields='nextPageToken, files(id, name)',
                                      pageToken=page_token,
                                      pageSize=1000).execute()

        file_count = file_count + len(folder.get('files', []))
        page_token = folder.get('nextPageToken', None)
        if page_token is None:
            break

    print(f'totol file in folder [{folder_id}]: {file_count}')


def main():
    folder_id_list = ['1laj2qYUt1QgIWYSc-Kuld228WPvFFKgp',
                      '19lmTM79hmgoc21p0LREtW6D9aruSru_6']
    for folder_id in folder_id_list:
        countss(folder_id)


if __name__ == '__main__':
    main()
