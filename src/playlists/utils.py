import base64
import os
import uuid

from fastapi import HTTPException

from src.aws.client import s3_client


def upload_cover(cover_image: str) -> str:
    try:
        header, data = cover_image.split(",")
        image_bytes = base64.b64decode(data)
        mime_type = header.split(";")[0].replace("data:", "")
        ext = mime_type.split("/")[-1]
    except Exception:
        raise HTTPException(status_code=400, detail="Incorrect base64")

    cover_key = f"covers/{uuid.uuid4()}.{ext}"

    s3_client.put_object(
        Bucket=os.getenv("AWS_BUCKET_NAME"),
        Key=cover_key,
        Body=image_bytes,
        ContentType=mime_type,
    )

    return cover_key
