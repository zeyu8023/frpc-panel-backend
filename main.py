from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router
from config import router as config_router
from proxies import router as proxy_router
from logs import router as logs_router

app = FastAPI()

# 允许前端跨域访问（开发阶段）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"]，  # 生产环境建议限制为你的前端域名
    allow_credentials=True,
    allow_methods=["*"]，
    allow_headers=["*"]，
)

# 注册路由
app.include_router(auth_router, prefix="/api")
app.include_router(config_router, prefix="/api")
app.include_router(proxy_router, prefix="/api")
app.include_router(logs_router, prefix="/api")
