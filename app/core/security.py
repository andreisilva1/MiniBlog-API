from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer("/users/login")
