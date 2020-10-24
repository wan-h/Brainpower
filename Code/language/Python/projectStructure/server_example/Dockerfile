# 基础docker
FROM hub-dev.rockontrol.com/rk-ai-tools/env-nvidia-cuda-amd64:dev
# 项目代码注入
WORKDIR /workspace
ADD . /workspace

# 安装基础python库
RUN pip install -r requirements.txt

# 启动脚本
CMD ["sh","/workspace/start.sh"]