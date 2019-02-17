import json
import os
from google_connecter.google_api import google_drive
import logging


class file_manager:

    TEAM_ID = "0AAHZOxqn9306Uk9PVA"
    metadata = {
        "date_folder_name": "",
        "date_folder_id": "",
        "sensor_folder_name": "",
        "sensor_folder_id": "",
        "root_folder_name": "",
        "root_folder_id": "",
        "sensor_name": "",
    }

    def __init__(
        self,
        root_folder_name="ROOT",
        sensor_name="GEOSCOPE-XX",
        token="/home/debian/geoscope-gateway/assets/token.json",
        cred="/home/debian/geoscope-gateway/assets/credentials.json",
    ):
        self.metadata["sensor_name"] = sensor_name
        self.metadata["sensor_folder_name"] = sensor_name
        self.google_drive_service = google_drive(token=token, cred=cred)
        self.setup(root_folder_name=root_folder_name)
        self.logger = logging.getLogger(f"GEOSCOPE.FILE_HANDLER")

    def setup(self, root_folder_name="ROOT"):
        # Check exist folder
        [is_valid, folder_id] = self.google_drive_service.is_folder_valid(
            folder_name=root_folder_name,
            parent_id="1JXe1ctL3VY74oZprjZXLHCiKcSqGg54p",
            is_teamdrive=False,
        )

        # Set root folder variable
        if is_valid:
            self.metadata["root_folder_name"] = root_folder_name
            self.metadata["root_folder_id"] = folder_id
            return True
        # Create new one if folder not exist
        else:
            [is_valid, folder_id] = self.google_drive_service.create_folder(
                folder_name=root_folder_name,
                parent_id="1JXe1ctL3VY74oZprjZXLHCiKcSqGg54p",
                is_teamdrive=False,
            )
            if is_valid:
                self.metadata["root_folder_name"] = root_folder_name
                self.metadata["root_folder_id"] = folder_id
            else:
                self.logger.warning("Cannot Setup Root folder.")

    def create_sensor_folder(self):
        # Check exist folder
        [is_valid, folder_id] = self.google_drive_service.is_folder_valid(
            folder_name=self.metadata["sensor_name"],
            parent_id=self.metadata["date_folder_id"],
            is_teamdrive=False,
        )

        if is_valid:
            self.metadata["sensor_folder_id"] = folder_id
        else:
            [is_valid, folder_id] = self.google_drive_service.create_folder(
                folder_name=self.metadata["sensor_name"],
                parent_id=self.metadata["date_folder_id"],
                is_teamdrive=False,
            )
            if is_valid:
                self.metadata["sensor_folder_id"] = folder_id
            else:
                self.logger.warning("Cannot create Sensor folder.")

    def create_date_folder(self, date="2018-01-01"):
        # Check exist folder
        [is_valid, folder_id] = self.google_drive_service.is_folder_valid(
            folder_name=date, parent_id=self.metadata["root_folder_id"], is_teamdrive=False
        )

        if is_valid:
            self.metadata["date_folder_name"] = date
            self.metadata["date_folder_id"] = folder_id
        else:
            [is_valid, folder_id] = self.google_drive_service.create_folder(
                folder_name=date, parent_id=self.metadata["root_folder_id"], is_teamdrive=False
            )
            if is_valid:
                self.metadata["date_folder_name"] = date
                self.metadata["date_folder_id"] = folder_id
            else:
                self.logger.warning("Cannot create Date folder.")

    def push_data(self, file_name="NAME", date="2018-01-01"):
        path = f"data/{self.metadata['root_folder_name']}/{date}/{self.metadata['sensor_folder_name']}"
        path_w_filename = f"{path}/{file_name}.json"

        # Upload file
        [is_valid, status] = self.google_drive_service.upload_file(
            path=path_w_filename,
            file_name=f"{file_name}.json",
            folder_name=self.metadata["sensor_folder_name"],
            parent_id=self.metadata["date_folder_id"],
            is_teamdrive=False,
        )

        if not is_valid and status == 404:
            self.create_date_folder(date=date)
            self.create_sensor_folder()
            self.push_data(file_name, date)

    def set_sensor_name(self, sensor_name):
        self.metadata["sensor_name"] = sensor_name
        self.metadata["sensor_folder_name"] = sensor_name


def main():
    test_file_manager = file_manager(
        root_folder_name="sss",
        sensor_name="testing",
        token="assets/token.json",
        cred="assets/credentials.json",
    )
    test_file_manager.create_date_folder(date="2018-01-01")
    test_file_manager.create_sensor_folder()
    test_file_manager.push_data({"test": "data"}, "bb")


if __name__ == "__main__":
    main()
