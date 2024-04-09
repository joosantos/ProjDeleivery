from fastapi import File, HTTPException, UploadFile, status
from enum import Enum
from typing import Union

MAX_IMAGE_SIZE = 5
MAX_PDF_SIZE = 5


class FileTypes(str, Enum):
    PDF = "application/pdf"
    JPEG = "image/jpeg"  # JPG and JPEG have the same mime type
    PNG = "image/pnf"
    SVG = "image/svg+xml"
    GIF = "image/gif"
    ICO = "image/vnd.microsoft.icon"
    WEBP = "image/webp"


IMAGES_TYPES = [
    FileTypes.JPEG,
    FileTypes.PNG,
    FileTypes.SVG,
    FileTypes.GIF,
    FileTypes.ICO,
    FileTypes.WEBP,
]


class FileUploadValidator:
    def __init__(
        self,
        max_size_mb: int,
        allowed_types: list[FileTypes] = [],
        file_required: bool = False,
    ) -> None:
        self.allowed_types = []
        self.file_required = file_required
        self.max_size_mb = max_size_mb
        self.message_type = 'File type "{extension}" not allowed. Allowed file types are {allowed_extensions}'
        self.message_size = f"File exceeds the maximum {self.max_size_mb}MB size"
        self.message_required = "File is required"

        for type in allowed_types:
            self.allowed_types.append(type.value)

    async def __call__(self, file: Union[UploadFile, None] = None) -> File:
        detail_messages = {}
        if file is None:
            if self.file_required:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail={"file": self.message_required},
                )
            return
        if file.content_type and file.content_type not in self.allowed_types:
            detail_messages["type"] = self.message_type.format(
                extension=file.content_type,
                allowed_extensions=", ".join(self.allowed_types),
            )

        fs = await file.read()
        if len(fs) > self.max_size_mb * 1024 * 1024:
            detail_messages["size"] = self.message_size
        if detail_messages:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=detail_messages
            )
        return fs
