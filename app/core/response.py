from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

def success_response(data=None, status_code=200, message="Success"):
    content = {
        "success": True,
        "message": message,
    }
    if data is not None:
        content["data"] = data

    # Fix: Encode content so datetime, UUID, Pydantic models are all serializable
    encoded_content = jsonable_encoder(content)

    return JSONResponse(
        status_code=status_code,
        content=encoded_content
    )
