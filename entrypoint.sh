#!/bin/sh

# 自动生成 .env 文件（如果不存在）
if [ ! -f .env ]; then
  echo "生成默认 .env 文件..."
  cat <<EOF > .env
SECRET_KEY=frpc-secret-key
TOKEN_EXPIRE_MINUTES=60
DEFAULT_FRPC_INI=/etc/frpc/frpc.ini
DEFAULT_FRPC_CONTAINER=frpc_client
LOG_TAIL_LINES=100
PORT=8035
EOF
fi

# 启动 FastAPI 服务
exec uvicorn main:app --host 0.0.0.0 --port \${PORT:-8035}
