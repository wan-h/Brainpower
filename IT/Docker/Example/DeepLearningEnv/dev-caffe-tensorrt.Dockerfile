FROM hub-my-docker:dev-caffe

ENV TENSORRT_URL=https://ops-software-binary-1255440668.cos.ap-chengdu.myqcloud.com/anaconda/TensorRT-7.0.0.11.Ubuntu-18.04.x86_64-gnu.cuda-10.2.cudnn7.6.tar.gz
ENV CUDNN_URL=https://ops-software-binary-1255440668.cos.ap-chengdu.myqcloud.com/anaconda/cudnn-10.2-linux-x64-v7.6.5.32.tgz
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64:/workspace/TensorRT-7.0.0.11/lib

# 下载tensorrt cudnn
WORKDIR /workspace
RUN wget $TENSORRT_URL \
  && wget $CUDNN_URL

# 开始安装
RUN tar -xzvf cudnn-10.2-linux-x64-v7.6.5.32.tgz \
  && cp cuda/include/cudnn*.h /usr/local/cuda/include \
  && cp cuda/lib64/libcudnn* /usr/local/cuda/lib64 \
  && chmod a+r /usr/local/cuda/include/cudnn*.h /usr/local/cuda/lib64/libcudnn* \
  && rm cudnn-10.2-linux-x64-v7.6.5.32.tgz
RUN tar -xzvf TensorRT-7.0.0.11.Ubuntu-18.04.x86_64-gnu.cuda-10.2.cudnn7.6.tar.gz \
  && rm TensorRT-7.0.0.11.Ubuntu-18.04.x86_64-gnu.cuda-10.2.cudnn7.6.tar.gz
RUN cd TensorRT-7.0.0.11/python && pip install tensorrt-7.0.0.11-cp37-none-linux_x86_64.whl \
  && cd ../uff && pip install uff-0.6.5-py2.py3-none-any.whl \
  && cd ../graphsurgeon && pip install graphsurgeon-0.4.1-py2.py3-none-any.whl

RUN pip install --no-cache-dir "pycuda>=2019.1.1"