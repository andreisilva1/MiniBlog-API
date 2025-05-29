from datetime import datetime, timedelta
from app.database.config import SecuritySettings as settings
from uuid import uuid4
import jwt


def generate_access_token(data: dict):
    token = jwt.encode(payload={**data, "jti": str(uuid4), "exp": datetime.now() + timedelta(days=1)},
                       key=settings().JWT_SECRET,
                       algorithm=settings().JWT_ALGORITHM)
    
    return token

def decode_access_token(token: str):
    try:
        return jwt.decode(jwt=token, key=settings().JWT_SECRET, algorithms=[settings().JWT_ALGORITHM])
    except jwt.PyJWTError:
        return None