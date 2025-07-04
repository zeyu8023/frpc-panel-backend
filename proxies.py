from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from configparser import ConfigParser
import os
import docker
from config import load_settings
from auth import get_current_user

router = APIRouter()
client = docker.from_env()

# 数据模型
class Proxy(BaseModel):
    name: str
    local_ip: str
    local_port: int
    remote_port: int

# 加载 ini 配置
def load_ini():
    settings = load_settings()
    path = settings["frpc_ini"]
    if not os.path.exists(path):
        raise HTTPException(status_code=400, detail="frpc.ini 路径不存在")
    config = ConfigParser()
    config.read(path)
    return config, path, settings["container_name"]

# 保存 ini 配置
def save_ini(config, path):
    with open(path, "w") as f:
        config.write(f)

# 重启 frpc 容器
def restart_container(container_name):
    try:
        container = client.containers.get(container_name)
        container.restart()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"容器重启失败: {str(e)}")

# 获取所有映射
@router.get("/proxies")
def get_proxies(username: str = Depends(get_current_user)):
    config, _, _ = load_ini()
    proxies = []
    for section in config.sections():
        if config[section].get("type") == "tcp":
            proxies.append({
                "name": section,
                "local_ip": config[section].get("local_ip"),
                "local_port": config[section].getint("local_port"),
                "remote_port": config[section].getint("remote_port")
            })
    return proxies

# 添加映射
@router.post("/proxies")
def add_proxy(data: Proxy, username: str = Depends(get_current_user)):
    config, path, container = load_ini()
    if data.name in config:
        raise HTTPException(status_code=400, detail="映射名称已存在")
    config[data.name] = {
        "type": "tcp",
        "local_ip": data.local_ip,
        "local_port": str(data.local_port),
        "remote_port": str(data.remote_port)
    }
    save_ini(config, path)
    restart_container(container)
    return {"message": "映射已添加"}

# 修改映射
@router.put("/proxies/{name}")
def update_proxy(name: str, data: Proxy, username: str = Depends(get_current_user)):
    config, path, container = load_ini()
    if name not in config:
        raise HTTPException(status_code=404, detail="映射不存在")
    config[name] = {
        "type": "tcp",
        "local_ip": data.local_ip,
        "local_port": str(data.local_port),
        "remote_port": str(data.remote_port)
    }
    save_ini(config, path)
    restart_container(container)
    return {"message": "映射已更新"}

# 删除映射
@router.delete("/proxies/{name}")
def delete_proxy(name: str, username: str = Depends(get_current_user)):
    config, path, container = load_ini()
    if name not in config:
        raise HTTPException(status_code=404, detail="映射不存在")
    config.remove_section(name)
    save_ini(config, path)
    restart_container(container)
    return {"message": "映射已删除"}
