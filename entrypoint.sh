#!/bin/sh

# 自动生成 .env（如果不存在）
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

# 读取 .env
export $(grep -v '^#' .env | xargs)

# 提前展开端口变量
PORT=${PORT:-8035}

# 启动服务
exec uvicorn main:app --host 0.0.0.0 --port "$PORT"
