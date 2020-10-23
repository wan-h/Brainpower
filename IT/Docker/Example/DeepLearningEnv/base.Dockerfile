FROM nvidia/cuda:10.2-devel-ubuntu18.04

# 中文问题
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8

# 东八区问题
ENV TZ=Asia/Shanghai
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# apt修改阿里源
RUN sed -i 's/security.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list \
    && sed -i 's/archive.ubuntu.com/mirrors.aliyun.com/g' /etc/apt/sources.list

# 由于 https://github.com/NVIDIA/nvidia-docker/issues/969 的问题
## 临时将 nvidia 的仓库另存为到其他地方，以保障 ci 流畅
RUN mkdir -p /opt/sources.list.d/  \
    && mv /etc/apt/sources.list.d/* /opt/sources.list.d/

# 添加ssh-key
RUN mkdir -p /root/.ssh
ADD key/docker_key /root/.ssh/id_rsa
RUN chmod 600 /root/.ssh/*
# 加入git.querycap.com权限，防止第一次使用是询问
#RUN ssh-keyscan git.querycap.com > /root/.ssh/known_hosts