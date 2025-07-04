from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import json
import os
from auth import get_current_user

router = APIRouter()
SETTINGS_FILE = "settings.json"

# 数据模型
class 设置(BaseModel):
    frpc_ini: str
    container_name: str

# 加载配置
def load_settings():
    if not os.path.exists(SETTINGS_FILE):
        return {"frpc_ini": "", "container_name": ""}
    with open(SETTINGS_FILE, "r") as f:
        return json.load(f)

# 保存配置
def save_settings(data):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(data, f, indent=2)

# 获取配置接口
@router.get("/settings")
def get_settings(username: str = Depends(get_current_user)):
    return load_settings()

# 保存配置接口
@router.post("/settings")
def update_settings(data: Settings, username: str = Depends(get_current_user)):
    if not os.path.exists(data.frpc_ini):
        raise HTTPException(status_code=400, detail="frpc.ini 路径不存在")
    save_settings(data.dict())
    return {"message": "配置已保存"}
