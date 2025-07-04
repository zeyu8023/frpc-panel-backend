from fastapi import APIRouter, HTTPException, Depends, Request
from pydantic import BaseModel
import bcrypt
import jwt
import json
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
SECRET_KEY = "frpc-secret-key"  # 可放入环境变量
TOKEN_EXPIRE_MINUTES = 60

# 加载用户数据
def load_users():
    with open("users.json", "r") as f:
        return json.load(f)

def save_users(users):
    with open("users.json", "w") as f:
        json.dump(users, f, indent=2)

# JWT 生成
def create_token(username: str):
    payload = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# JWT 验证
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token 已过期")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="无效 Token")

# FastAPI 安全依赖
auth_scheme = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    return verify_token(credentials.credentials)

# 登录请求模型
class LoginRequest(BaseModel):
    username: str
    password: str

# 修改密码模型
class PasswordChangeRequest(BaseModel):
    current_password: str
    new_password: str

# 登录接口
@router.post("/login")
def login(data: LoginRequest):
    users = load_users()
    user = users.get(data.username)
    if not user or not bcrypt.checkpw(data.password.encode(), user["password"].encode()):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    token = create_token(data.username)
    return {"token": token}

# 修改密码接口
@router.post("/account/password")
def change_password(data: PasswordChangeRequest, username: str = Depends(get_current_user)):
    users = load_users()
    user = users.get(username)
    if not user or not bcrypt.checkpw(data.current_password.encode(), user["password"].encode()):
        raise HTTPException(status_code=401, detail="当前密码错误")
    hashed = bcrypt.hashpw(data.new_password.encode(), bcrypt.gensalt()).decode()
    users[username]["password"] = hashed
    save_users(users)
    return {"message": "密码修改成功"}
