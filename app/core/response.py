from fastapi.responses import JSONResponse

def success_response(data, status_code=200,message="Success"):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": True,
            "message": message,
            "data": data
        }
    )
