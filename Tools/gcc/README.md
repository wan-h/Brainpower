## GCC
[Link](http://gcc.gnu.org/)  
[Insight](https://www.cnblogs.com/mlgjb/p/7708007.html)

---
### OVERVIEW  
GCC（GNU Compiler Collection，GNU编译器套件）是由GNU开发的编程语言译器。  

---
### C编译工作流程
1. 预处理阶段  
    * 命令实例  
        gcc -E hello.c -o hello.i  
    * 命令说明  
        对预处理代码进行处理（头文件包含、宏定义扩展、条件编译的选择）  
2. 编译阶段  
    * 命令实例  
        gcc -S hello.i -o hello.s  
    * 命令说明  
        进行词法分析、语法分析、语义分析及优化后生成相应的汇编代码文件  
3. 汇编阶段  
    * 命令实例  
        gcc -c hello.s -o hello.o  
    * 命令说明  
        将汇编语言翻译成机器语言（二进制文件）  
4. 链接阶段  
    * 命令实例  
        gcc hello.o -o hello  
    * 命令说明  
        链接代码中需要的其他库，生成一个可执行文件