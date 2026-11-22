import io
import os
import logging
from typing import Any

import httpx
import replicate
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from PIL import Image, UnidentifiedImageError

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("dksite")

app = FastAPI(title="DK Site", version="1.0.0")
MODEL_VERSION = "d0ee3d708c9b911f122a4ad90046c5d26a0293b99476d697f6bb7f2e251ce2d4"
MAX_BYTES = 15 * 1024 * 1024
MAX_PIXELS = 30_000_000
Image.MAX_IMAGE_PIXELS = MAX_PIXELS

@app.get("/api/health")
async def health():
    return {"ok": True, "app": "DK Site", "ai_configured": bool(os.getenv("REPLICATE_API_TOKEN"))}

@app.get("/", response_class=HTMLResponse)
async def home():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(f.read())
    except FileNotFoundError:
        raise HTTPException(500, "Không tìm thấy giao diện index.html")

@app.post("/api/enhance")
async def enhance(image: UploadFile = File(...)):
    token = os.getenv("REPLICATE_API_TOKEN")
    if not token:
        raise HTTPException(503, "Máy chủ chưa cấu hình AI. Hãy thêm REPLICATE_API_TOKEN trong Environment.")
    if image.content_type not in {"image/jpeg", "image/png", "image/webp"}:
        raise HTTPException(415, "Chỉ hỗ trợ JPG, PNG hoặc WEBP.")
    raw = await image.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise HTTPException(413, "Ảnh vượt quá giới hạn 15 MB.")
    try:
        with Image.open(io.BytesIO(raw)) as im:
            im.verify()
        with Image.open(io.BytesIO(raw)) as im:
            if im.width * im.height > MAX_PIXELS:
                raise HTTPException(413, "Ảnh có độ phân giải quá lớn.")
            im = im.convert("RGB")
            buf = io.BytesIO()
            im.save(buf, format="JPEG", quality=95)
            buf.seek(0)
    except HTTPException:
        raise
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError):
        raise HTTPException(400, "Tệp ảnh không hợp lệ hoặc bị lỗi.")

    try:
        with buf as source:
            output: Any = replicate.run(
                f"cjwbw/real-esrgan:{MODEL_VERSION}",
                input={"image": source, "scale": 4}
            )
        if isinstance(output, (list, tuple)):
            output = output[0] if output else None
        if output is None:
            raise RuntimeError("AI không trả về ảnh.")
        url = str(output)
        async with httpx.AsyncClient(timeout=120, follow_redirects=True) as client:
            result = await client.get(url)
            result.raise_for_status()
        # Validate provider output before returning it.
        with Image.open(io.BytesIO(result.content)) as out_img:
            out_img.verify()
        return Response(
            content=result.content,
            media_type="image/png",
            headers={"Content-Disposition": 'attachment; filename="dk-site-enhanced.png"', "Cache-Control":"no-store"}
        )
    except HTTPException:
        raise
    except Exception as exc:
        log.exception("Enhancement failed")
        message = str(exc)
        if "402" in message or "payment" in message.lower() or "billing" in message.lower():
            raise HTTPException(402, "Tài khoản AI cần có số dư hoặc phương thức thanh toán.")
        raise HTTPException(502, "AI xử lý ảnh thất bại. Vui lòng thử lại sau.")

