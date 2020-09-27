## Q&A

### docker换国内源
修改注册地址
```
sudo vim  /etc/docker/daemon.json
```
修改内容如下
```json
{
  "registry-mirrors":["https://kalxjm99.mirror.aliyuncs.com"]
}
```
重启docker
```
sudo systemctl daemon-reload
sudo systemctl restart docker
```