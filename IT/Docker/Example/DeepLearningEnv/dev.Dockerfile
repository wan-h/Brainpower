FROM hub-my-docker:base

# 安装Anaconda
ENV PATH /opt/conda/bin:$PATH
RUN apt-get update \
  && apt-get install -y wget \
# && wget -c https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh -O ~/anaconda.sh \
  && wget -O ~/anaconda.sh -c https://ops-software-binary-1255440668.cos.ap-chengdu.myqcloud.com/anaconda/Anaconda3-2020.02-Linux-x86_64.sh \
  && /bin/bash ~/anaconda.sh -b -p /opt/conda \
  && rm ~/anaconda.sh \
  && ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh \
  && echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc \
  && echo "conda activate base" >> ~/.bashrc  \
  && rm -rf /var/lib/apt/lists/*

# conda更改清华源
RUN conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/conda-forge/ \
  && conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/msys2/ \
  && conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/bioconda/ \
  && conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/menpo/ \
  && conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/free/ \
  && conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/pkgs/main/ \
  && conda config --add channels https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud/pytorch/ \
  && conda config --set show_channel_urls yes

# apt安装依赖库
RUN apt update \
  && apt-get install -y git g++ \
  && rm -rf /var/lib/apt/lists/*

# conda安装依赖库
# https://docs.conda.io/projects/conda/en/latest/commands/clean.html
RUN conda install -y python=3.7  && conda clean -a 
RUN conda install -y cudatoolkit=10.2  && conda clean -a 
RUN conda install -y pytorch  && conda clean -a 
RUN conda install -y torchvision  && conda clean -a 

# pip安装依赖库
# add pip aliyun source
COPY pip/pip.conf /root/.pip/pip.conf
RUN pip install --no-cache-dir yacs==0.1.7
RUN pip install --no-cache-dir opencv-python-headless==4.3.0.36
RUN pip install --no-cache-dir tensorboardX==2.1