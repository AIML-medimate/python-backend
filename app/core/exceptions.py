from fastapi import HTTPException

class AppException(HTTPException):
    def __init__(self, message: str, status_code: int = 400, data=None):
        super().__init__(status_code=status_code, detail=message)
        self.data = data
    def __str__(self):
        return f"AppException(status_code={self.status_code}, message={self.detail}, data={self.data})"
    
class NotFoundException(AppException):
    def __init__(self, message: str = "Resource not found", data=None):
        super().__init__(message=message, status_code=404, data=data)