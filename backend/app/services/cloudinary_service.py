import cloudinary
import cloudinary.uploader
from fastapi import UploadFile, HTTPException
from app.core.config import settings


def configure_cloudinary():
    if settings.CLOUDINARY_CLOUD_NAME and settings.CLOUDINARY_API_KEY and settings.CLOUDINARY_API_SECRET:
        cloudinary.config(
            cloud_name=settings.CLOUDINARY_CLOUD_NAME,
            api_key=settings.CLOUDINARY_API_KEY,
            api_secret=settings.CLOUDINARY_API_SECRET,
            secure=True,
        )


async def upload_profile_picture(file: UploadFile):
    configure_cloudinary()
    if not settings.CLOUDINARY_CLOUD_NAME:
        raise HTTPException(status_code=500, detail="Cloudinary is not configured")
    content = await file.read()
    if len(content) > 5 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Profile picture must be <= 5 MB")
    try:
        result = cloudinary.uploader.upload(content, folder="sih_social_innovation/profiles", resource_type="image")
        return result["secure_url"]
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Cloudinary upload failed: {exc}")


async def upload_problem_media(file: UploadFile, media_type: str):
    configure_cloudinary()
    if not settings.CLOUDINARY_CLOUD_NAME:
        raise HTTPException(status_code=500, detail="Cloudinary is not configured")

    if media_type == "image":
        resource_type = "image"
        folder = "sih/problems/images"
        max_size = 10 * 1024 * 1024
    elif media_type == "video":
        resource_type = "video"
        folder = "sih/problems/videos"
        max_size = 50 * 1024 * 1024
    else:
        raise HTTPException(status_code=400, detail="Unsupported media type.")

    content = await file.read()
    if len(content) > max_size:
        raise HTTPException(status_code=413, detail=f"{media_type.title()} must be <= {max_size // (1024 * 1024)} MB")

    try:
        result = cloudinary.uploader.upload(
            content,
            resource_type=resource_type,
            folder=folder,
            use_filename=True,
            unique_filename=True,
        )
        return {"url": result.get("secure_url"), "public_id": result.get("public_id")}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Cloudinary upload failed: {exc}")
