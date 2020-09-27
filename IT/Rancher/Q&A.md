## Q&A

### docker启动失败
docker错误日志
```
Unable to find suitable network address.error='no default routes found in "/proc/net/route" or "/proc/net/ipv6_route"'. 
Try to set the AdvertiseAddress directly or provide a valid BindAddress to fix this. 
```
解决方案
```
# 新建网桥，注意subnet　gateway设置称自己的配置
docker network create --driver bridge --subnet=172.31.0.63/24 --gateway=172.31.0.1 mynet
docker run -d --restart=unless-stopped -p 8081:80 -p 8443:443 --network=mynet --name rancher rancher/rancher:latest
```