from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

# 加载 .env 文件
load_dotenv()

app = FastAPI()

# 配置 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境建议限制为你的前端域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 示例路由
@app.get("/api/health")
def health_check():
    return {"status": "ok"}

# 启动服务（仅用于调试，生产环境由 entrypoint.sh 启动）
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8035))
    uvicorn.run(app, host="0.0.0.0", port=port)
