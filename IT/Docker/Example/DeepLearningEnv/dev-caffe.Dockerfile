FROM hub-dev.rockontrol.com/rk-ai-tools/env-nvidia-cuda-amd64:dev

ENV PYTHONPATH=/opt/rock_caffe/python:$PYTHONPATH

# 华为云更加稳定
RUN sed -i 's/mirrors.aliyun.com/mirrors.huaweicloud.com/g' /etc/apt/sources.list
# apt安装caffe依赖库
RUN apt update \
  && apt-get install -y libprotobuf-dev \
                        protobuf-compiler \
                        libboost-all-dev \
                        libgoogle-glog-dev \
                        libblas-dev \
                        libopencv-dev \
                        libgflags-dev \
                        libgoogle-glog-dev \
                        liblmdb-dev \
                        libopenblas-dev \
                        libleveldb-dev \
                        cmake \
  && rm -rf /var/lib/apt/lists/*


RUN ssh-keyscan git.querycap.com > /root/.ssh/known_hosts

# 下载caffe源码
WORKDIR /opt
RUN git clone git@git.querycap.com:ai/rock/rock_caffe.git -b ssd

# caffe安装配置文件
COPY caffe/Makefile.config /opt/rock_caffe/Makefile.config

# 编译安装caffe
RUN cd /opt/rock_caffe/ \
  && make -j8 \
  && make py -j8

# 放到最后，防止干扰动态链接库，编译出错
ENV LD_LIBRARY_PATH=/opt/conda/lib:$LD_LIBRARY_PATH