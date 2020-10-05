## ELK日志系统搭建
### 搭建步骤
[参考链接](https://elasticstack.blog.csdn.net/article/details/106362936)
#### 安装Elasticsearch
[Link](https://www.elastic.co/guide/en/elasticsearch/reference/7.9/docker.html)  
docker安装
```
docker pull docker.elastic.co/elasticsearch/elasticsearch:7.9.2
```
docker运行
```
docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.9.2
```
#### 安装Kibana
[Link](docker pull docker.elastic.co/kibana/kibana:7.9.2)  
docker安装
```
docker pull docker.elastic.co/kibana/kibana:7.9.2
```
docker运行
```
docker run --link YOUR_ELASTICSEARCH_CONTAINER_NAME_OR_ID:elasticsearch -p 5601:5601 docker.elastic.co/kibana/kibana:7.9.2
```
### 安装Filebeat
直接打开Kibana主页进入添加数据选择需要获取的日志类型然后根据提示进行安装
```
curl -L -O https://artifacts.elastic.co/downloads/beats/filebeat/filebeat-7.9.2-darwin-x86_64.tar.gz
tar xzvf filebeat-7.9.2-darwin-x86_64.tar.gz
cd filebeat-7.9.2-darwin-x86_64/
```
### 安装Logstash
[Link](https://www.elastic.co/guide/en/logstash/current/installing-logstash.html)  
docker安装
```
docker pull docker.elastic.co/logstash/logstash:7.9.2
```
docker运行
```
docker run --link YOUR_ELASTICSEARCH_CONTAINER_NAME_OR_ID:elasticsearch -p 5044:5044 -p 9600:9600 docker.elastic.co/logstash/logstash:7.9.2
```
### 编写配置文件
* beat配置文件
```
# filebeat_logstash.yml

filebeat.inputs:
- type: log
  enabled: true
  paths:
    - ~/test.log

output.logstash:
  hosts: ["localhost:5044"]
```
* logstash配置文件
```
# logstash.conf
# Read input from filebeat by listening to port 5044 on which filebeat will send the data
input {
    beats {
       type => "test"
       port => "5044"
    }
}
# 自动解析beat日志中的json字段
filter {
  json {
    source => "message"
    #target => "doc"
    #remove_field => ["message"]
  }
}
output {
  stdout {
    codec => rubydebug
  }
  # Sending properly parsed log events to elasticsearch
  elasticsearch {
    hosts => ["elasticsearch:9200"]
  }
}
```
* 测试beat配置文件
```
filebeat -c filebeat_logstash.yml test config
filebeat -c filebeat_logstash.yml test output
```
### 启动组件
* 启动logstash
```
logstash -f logstash.conf
```
* 启动filebeat
```
filebeat -e -c filebeat_logstash.yml
```
* 启动日志生成的脚本
```
python logGen.py
```
### 可视化数据
进入kibana随意操作数据即可