#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>

#define PORT 8080

int main(int argc, char *argv[])
{
    int server_fd;

    /***********************创建socket文件描述符********************************/
    // AF_INET表示使用ipv4
    // SOCK_STREAM表示TCP，SOCK_DGRAM表示UDP
    // 这里的server_fd就类似于我们打开文件的描述符
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("socket failed");
        exit(EXIT_FAILURE);
    }

    /***********************设置socket选项********************************/
    int opt = 1;
    // 这里相当于将scoket设备为ip和port在Bind的时候可以重用（多个socket使用相同的ip和port）
    if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt, sizeof(opt))) {
        perror("setsockopt");
        exit(EXIT_FAILURE);
    }

    /***********************绑定socket到端口********************************/
    struct sockaddr_in address;
    socklen_t addrlen = sizeof(address);
    address.sin_family = AF_INET;
    // 这个地址可以是具体的ip地址，例如 inet_addr("192.168.1.1");
    // 这里INADDR_ANY表示接收服务上任意地址的请求，多个地址会发生在服务器有多个网卡的时候
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons( PORT );

    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address))<0) {
        perror("bind failed");
        exit(EXIT_FAILURE);
    }

    /***********************监听socket端口********************************/
    // 3表示允许再队列中等待的最大数量，超过之后的请求都会被直接拒绝
    if (listen(server_fd, 3) < 0) {
        perror("listen");
        exit(EXIT_FAILURE);
    }

    /***********************接收请求******************************/
    int new_socket;
    // accept会从排队的请求中取出第一个建立连接，生成一个新的socket描述符，后面的通信都用这个新的描述符
    if ((new_socket = accept(server_fd, (struct sockaddr *)&address, &addrlen))<0) {
        perror("accept");
        exit(EXIT_FAILURE);
    }

    /***********************客户端信息交互******************************/
    ssize_t valread;
    char buffer[1024] = {0};
    char* hello = "Hello from server";
    // 接收客户端信息
    // 最后一个字符是null,所以要减1
    valread = read(new_socket, buffer, 1024 - 1);
    printf("Receive from client: %s\n", buffer);
    // 发送信息给客户端, 最后的0是行为标志,一般默认0
    send(new_socket, hello, strlen(hello), 0);
    printf("Hello message sent\n");

    /***********************关闭socket******************************/
    close(new_socket);
    close(server_fd);
    return 0;
}