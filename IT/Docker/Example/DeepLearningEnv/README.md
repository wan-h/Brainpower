# Deep Learning Environment Docker
[Nvidia docker hub](https://hub.docker.com/r/nvidia/cuda)

##模板
分层架构，以下docker均以上一个docker为base:  
* [base](https://github.com/wan-h/Brainpoer/blob/master/IT/Docker/Example/DeepLearningEnv/base.Dockerfile)  
ubuntu18.04 + cuda10.2
* [dev](https://github.com/wan-h/Brainpower/blob/master/IT/Docker/Example/DeepLearningEnv/dev.Dockerfile)  
ubuntu18.04 + cuda10.2 + anaconda + pytorch
* [dev-caffe](https://github.com/wan-h/Brainpower/blob/master/IT/Docker/Example/DeepLearningEnv/dev-caffe.Dockerfile)  
ubuntu18.04 + cuda10.2 + anaconda + pytorch + caffe
* [dev-caffe-tensorrt](https://github.com/wan-h/Brainpower/blob/master/IT/Docker/Example/DeepLearningEnv/dev-caffe-tensorrt.Dockerfile)  
ubuntu18.04 + cuda10.2 + anaconda + pytorch + caffe + tensorrt