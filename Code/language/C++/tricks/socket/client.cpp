#include <arpa/inet.h>
#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

#define PORT 8080

int main(int argc, char const* argv[])
{
    int client_fd;
    struct sockaddr_in serv_addr;
    
    /***********************创建socket文件描述符********************************/
    if ((client_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        printf("create socket error\n");
        return -1;
    }

    /***********************和server建立连接********************************/
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);
    // 这里将本地ip转换为了网络字节序并存储到serv_addr.sin_addr中
    // 应为测试服务端和客户端都在本地,实际改为服务器ip
    if (inet_pton(AF_INET, "127.0.0.1", &serv_addr.sin_addr) < 0) {
        printf("inet_pton error\n");
        return -1;
    }
    // 和服务器建立连接
    int status;
    if ((status = connect(client_fd, (struct sockaddr*)&serv_addr, sizeof(serv_addr))) < 0) {
        printf("connect error\n");
        return -1;
    }

    /***********************服务端信息交互********************************/
    char* hello = "Hello from client";
    char buffer[1024] = { 0 };
    // 发送数据到服务端
    send(client_fd, hello, strlen(hello), 0);
    printf("Hello message sent\n");
    // 接收数据
    int valread;
    valread = read(client_fd, buffer, 1024 - 1);
    printf("Receive from server: %s\n", buffer);

    /***********************关闭socket******************************/
    close(client_fd);
    return 0;
}