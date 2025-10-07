from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, status
from pathlib import Path
from datetime import datetime
import secrets
from app.routers.auth_enhanced import get_current_active_user

router = APIRouter()

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@router.post("/images")
async def upload_image(
    file: UploadFile = File(...),
    current_user = Depends(get_current_active_user)
):
    if current_user.role not in ("owner", "admin"):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Only image files are allowed")

    ext = Path(file.filename).suffix.lower()
    safe_name = f"{datetime.utcnow().strftime('%Y%m%d%H%M%S')}_{secrets.token_hex(6)}{ext}"
    dest = UPLOAD_DIR / safe_name

    with dest.open("wb") as f:
        while True:
            chunk = await file.read(1024 * 1024)
            if not chunk:
                break
            f.write(chunk)

    return {"url": f"/static/uploads/{safe_name}"}


