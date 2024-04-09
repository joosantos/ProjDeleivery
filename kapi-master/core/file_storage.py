from typing import BinaryIO
from boto3 import session
from fastapi import UploadFile
from pydantic import UUID4
from core.environment import config
from enum import Enum


class FileStorageDirectories(str, Enum):
    PROFILE_PICTURES = "profile_pictures"
    PAYMENTS_COMPROVATIVES = "payments_comprovatives"
    INSCRIPTIONS_PAYMENTS_COMPROVATIVES = "inscriptions_payments_comprovatives"
    MEDICAL_EXAMS = "medical_exams"
    CONTRACTS = "constracts"
    COACH_CERTIFICATES = "coach_certificates"


class FileStorageService:
    def __init__(self):
        self.session = session.Session()
        self.client = self.session.client(
            "s3",
            region_name=config["file_storage"]["region_name"],
            endpoint_url=config["file_storage"]["url"],
            aws_access_key_id=config["file_storage"]["access_id"],
            aws_secret_access_key=config["file_storage"]["secret_key"],
        )
        self.bucket_name = config["file_storage"]["bucket_name"]

    async def upload(self, name: str, file: UploadFile):
        file.file.seek(0)
        self.client.put_object(
            Bucket=self.bucket_name,
            Key=name,
            Body=file.file,
            ACL="public-read",
        )

    def get_download_url(self, name: str) -> str:
        return self.client.generate_presigned_url(
            ClientMethod="get_object",
            Params={"Bucket": self.bucket_name, "Key": name},
            ExpiresIn=300,
        )

    def delete(self, name: str):
        self.client.delete_object(Bucket=self.bucket_name, Key=name)

    def get_file_name(
        self, directory: FileStorageDirectories, obj_id: str | UUID4, file: UploadFile
    ):
        file_type = str(file.content_type)
        file_type_arr = file_type.split("/")
        file_extension = "txt"
        if len(file_type_arr) == 2:
            file_extension = file_type_arr[1]
        return f"{config['file_storage']['prefix']}/{directory.value}/{str(obj_id)}.{file_extension}"
