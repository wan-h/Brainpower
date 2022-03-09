# coding: utf-8
# Author: wanhui0729@gmail.com

"""
subprocess 模块允许我们启动一个新进程，并连接到它们的输入/输出/错误管道，从而获取返回值。
该模块被设计用来替换掉os.system(cmd)
"""

import subprocess

if __name__ == '__main__':
    # 其返回值是一个CompletedProcess 实例
    command = "ls -l"
    # 执行一个command, 将其输出映射到subprocess.PIPE
    # shell=true表示通过操作系统的shell执行命令
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    # poll(): 检查进程是否终止，如果终止返回returncode，否则返回None。
    # wait(timeout): 等待子进程终止。
    # communicate(input, timeout): 和子进程交互，发送和读取数据。
    # send_signal(singnal): 发送信号到子进程 。
    # terminate(): 停止子进程, 也就是发送SIGTERM信号到子进程。
    # kill(): 杀死子进程。发送、SIGKILL信号到子进程。
    p.wait(2)
    if p.poll() == 0:
        # 输出二维: (stdout, stderr)
        print(p.communicate()[1])
    else:
        print("fail")


    # subprocess的其他接口基本都是对Popen的包装
    """
    subprocess.run()	Python 3.5中新增的函数。执行指定的命令，等待命令执行完成后返回一个包含执行结果的CompletedProcess类的实例。
    subprocess.call()	执行指定的命令，返回命令执行状态，其功能类似于os.system(cmd)。
    subprocess.check_call()	Python 2.5中新增的函数。 执行指定的命令，如果执行成功则返回状态码，否则抛出异常。其功能等价于subprocess.run(..., check=True)。
    subprocess.check_output()	Python 2.7中新增的的函数。执行指定的命令，如果执行状态码为0则返回命令执行结果，否则抛出异常。
    subprocess.getoutput(cmd)	接收字符串格式的命令，执行命令并返回执行结果，其功能类似于os.popen(cmd).read()和commands.getoutput(cmd)。
    subprocess.getstatusoutput(cmd)	执行cmd命令，返回一个元组(命令执行状态, 命令执行结果输出)，其功能类似于commands.getstatusoutput()。
    """
    output = subprocess.check_output(["ls", "-l"])
    # 如果直接用字符串的话要设置shell=true
    # output = subprocess.check_output("ls -l", shell=True)
    # 输出为字节流
    output_str = output.decode()
    print(output_str)
    # 获取每一行数据
    output_list = output_str.split('\n')
    print(output_list)

    # universal_newlines=True设置后输出为单行的字符串
    output = subprocess.check_output(["ls", "-l"], universal_newlines=True)
    print(output)
