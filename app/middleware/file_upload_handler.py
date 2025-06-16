# app/middleware/file_middleware.py

from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from starlette.datastructures import UploadFile

MAX_FILE_SIZE_MB = 5
ALLOWED_TYPES = {"image/png", "image/jpeg", "image/bmp"}
MAX_FILE_SIZE = MAX_FILE_SIZE_MB * 1024 * 1024  # bytes

class FileHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        print("\n[Middleware] Incoming request")

        if request.headers.get("content-type", "").startswith("multipart/form-data"):
            print("[Middleware] Detected multipart/form-data")

            form = await request.form()
            files = {
                key: value
                for key, value in form.items()
                if isinstance(value, UploadFile)
            }

            print(f"[Middleware] Files received: {list(files.keys())}")

            if len(files) != 1:
                print(f"[Middleware] ❌ Expected 1 file, but got {len(files)}")
                raise HTTPException(status_code=400, detail="Only one file is allowed")

            for key, file in files.items():
                content_type = file.content_type
                contents = await file.read()
                size = len(contents)
                await file.seek(0)

                print(f"[Middleware] ✔️ File received - key: '{key}', name: '{file.filename}', "
                      f"type: '{content_type}', size: {size / 1024:.2f} KB")

                if content_type not in ALLOWED_TYPES:
                    print(f"[Middleware] ❌ Unsupported file type: {content_type}")
                    raise HTTPException(status_code=415, detail="Unsupported file type")

                if size > MAX_FILE_SIZE:
                    print(f"[Middleware] ❌ File too large: {file.filename}")
                    raise HTTPException(status_code=413, detail="File too large")

            # Attach to request.state if route wants access
            request.state.uploaded_files = files
        print("[Middleware] Request processing complete, passing to next middleware or route handler")
        return await call_next(request)
