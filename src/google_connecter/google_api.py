from googleapiclient.discovery import build
from httplib2 import Http
from googleapiclient.http import MediaFileUpload
from oauth2client import file, client, tools


class google_drive:
    def __init__(self, scope="https://www.googleapis.com/auth/drive", token="assets/token.json", cred="assets/credentials.json"):
        storage = file.Storage(token)
        credentrial = storage.get()
        if not credentrial or credentrial.invalid:
            print('## Cannot find Google API Credential')
            print('## Create new Credential')
            flow = client.flow_from_clientsecrets(
                cred, scope)
            credentrial = tools.run_flow(flow, storage)

        # create google drive service
        self.service = build('drive', 'v3', http=credentrial.authorize(Http()))

    def is_folder_valid(self, folder_name="name", folder_id="id", parent_id="id", is_teamdrive=False, team_id="team_id"):
        query = 'mimeType="application/vnd.google-apps.folder"'
        if parent_id != "id":
            query = f'{query} and "{parent_id}" in parents'

        if is_teamdrive:
            folder_list = self.service.files().list(q=query, spaces='drive', fields='nextPageToken, files(id, name)',
                                                    corpora='teamDrive', includeTeamDriveItems=True, supportsTeamDrives=True, teamDriveId=team_id).execute()
            for folder in folder_list.get('files', []):
                if folder_name == folder.get('name'):
                    return [True, folder.get('id')]
                if folder_id == folder.get('id'):
                    return [True, folder_id]

        else:
            folder_list = self.service.files().list(
                q=query, spaces='drive', fields='nextPageToken, files(id, name)',).execute()
            for folder in folder_list.get('files', []):
                if folder_name == folder.get('name'):
                    return [True, folder.get('id')]
                if folder_id == folder.get('id'):
                    return [True, folder_id]

        return [False, ""]

    def create_folder(self, folder_name="name", parent_id="id", is_teamdrive=False, team_id="team_id"):
        [is_valid, folder_id] = self.is_folder_valid(
            folder_name=folder_name, parent_id=parent_id, is_teamdrive=is_teamdrive, team_id=team_id)
        if not is_valid:
            file_metadata = {
                'name': folder_name,
                'mimeType': 'application/vnd.google-apps.folder'
            }
            is_created = False
            try:
                if parent_id != "id":
                    file_metadata['parents'] = [parent_id]

                if is_teamdrive:
                    file_metadata['teamDriveId'] = team_id
                    print(file_metadata)
                    folder = self.service.files().create(body=file_metadata, fields='id',
                                                         supportsTeamDrives=is_teamdrive).execute()
                    folder_id = folder.get('id')
                else:
                    folder = self.service.files().create(body=file_metadata, fields='id').execute()
                    folder_id = folder.get('id')
                is_created = True
            except Exception as e:
                print(f"## ERROR OCCURED! >>> {e.value}")
            finally:
                if is_created:
                    print(f'> Folder {folder_name} created.\tID: {folder_id}')
                else:
                    print(f'> Cannot create {folder_name}')
                return folder_id
        else:
            print(f'> Folder {folder_name} already exist\tID: {folder_id}')
            return folder_id

    def upload_file(self, path="PATH", file_name="FILE", folder_name="name", parent_id="id", is_teamdrive=False, team_id="team_id"):
        [is_valid, folder_id] = self.is_folder_valid(
            folder_name=folder_name, parent_id=parent_id, is_teamdrive=is_teamdrive, team_id=team_id)

        if is_valid:
            file_metadata = {
                'name': file_name,
                'parents': [folder_id],
                'mimeType': '*/*'
            }
            media = MediaFileUpload(
                path, mimetype='*/*', resumable=True)
            file_id = ""
            is_valid = False
            try:
                if is_teamdrive:
                    file_metadata['teamDriveId'] = team_id
                    file = self.service.files().create(body=file_metadata, media_body=media,
                                                       field='id', supportsTeamDrives=is_teamdrive).execute()
                    file_id = file.get('id')
                    is_valid = True
                else:
                    file = self.service.files().create(body=file_metadata, media_body=media).execute()
                    file_id = file.get('id')
                    is_valid = True
            finally:
                if is_valid:
                    print(f'> File uploaded. ID: {file_id}')
                    return True
                else:
                    print(f'> Cannot upload file {file_name}')
                    return False
        else:
            print(f'> Folder {folder_name} is not exist')
            return False


def main():
    test_service = google_drive()
    test_service.create_folder(folder_name="geoscope")


if __name__ == '__main__':
    main()
