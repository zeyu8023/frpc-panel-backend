from fastapi import APIRouter, Depends, HTTPException
from auth import get_current_user
from config import load_settings
import docker

router = APIRouter()
client = docker.from_env()

@router.get("/logs")
def get_logs(username: str = Depends(get_current_user)):
    settings = load_settings()
    container_name = settings.get("container_name")
    if not container_name:
        raise HTTPException(status_code=400, detail="未配置容器名称")

    try:
        container = client.containers.get(container_name)
        logs = container.logs(tail=100).decode("utf-8")
        return {"logs": logs}
    except docker.errors.NotFound:
        raise HTTPException(status_code=404, detail="容器未找到")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"日志获取失败: {str(e)}")
