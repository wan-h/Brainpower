## Beats
[Link](https://www.elastic.co/beats/)  

---
### OVERVIEW  
Beats作为代理安装在服务器上的开源数据发送者，用于将运营数据发送到 Elasticsearch 或 Logstash 中进行其他处理。
#### Filebeat
Filebeat用于收集和传送日志文件，它也是最常用的 Beat。 如果 Logstash 繁忙，Filebeat会减慢其读取速率，并在减速结束后加快节奏。
#### Packetbeat
Packetbeat 捕获服务器之间的网络流量，因此可用于应用程序和性能监视。
#### Metricbeat
收集并报告各种系统和平台的各种系统级度量。
#### Auditbeat
Auditbeat 可用于审核 Linux 服务器上的用户和进程活动。
#### Winlogbeat
专门为收集 Windows 事件日志而设计的 Beat。
#### Functionbeat
专为监视云环境而设计，目前已针对 Amazon 设置量身定制，可以部署为 Amazon Lambda 函数，
以从 Amazon CloudWatch，Kinesis 和 SQS 收集数据。