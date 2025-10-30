# 使用官方Python运行时作为父镜像
FROM python:3.12.0


RUN mkdir -p /var/www/html/dashboard

# 设置容器内的当前工作目录
WORKDIR /var/www/html/dashboard

# 将整个项目代码复制到容器的工作目录，包含依赖文件
COPY . /var/www/html/dashboard

RUN cd /var/www/html/dashboard;

# 设置环境变量
# 防止Python将字节码文件 (.pyc) 写入磁盘
ENV PYTHONDONTWRITEBYTECODE 1
# 防止Python对stdout/stderr进行缓冲，确保Docker日志实时输出
ENV PYTHONUNBUFFERED 1


# 安装系统依赖项
RUN apt-get update && apt-get install -y \
    # 用于安装Python包的编译工具
    gcc \
    python3-dev \
    # 清理缓存
    && rm -rf /var/lib/apt/lists/*



# 在COPY requirements.txt之前添加ARG
ARG ENVIRONMENT=production

# 安装适当的依赖
RUN if [ "$ENVIRONMENT" = "development" ]; then \
        pip install --no-cache-dir -r requirements-dev.txt -i https://mirrors.aliyun.com/pypi/simple/; \
    else \
        pip install --no-cache-dir -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/; \
    fi

RUN pip install uwsgi -i https://mirrors.aliyun.com/pypi/simple/;

## 暴露Django运行所需的端口（通常为8000）
#EXPOSE 8000

RUN chmod +x ./start.sh

# 注意：我们没有在这里定义CMD，因为我们将在docker-compose.yml中为不同的服务定义不同的启动命令。
