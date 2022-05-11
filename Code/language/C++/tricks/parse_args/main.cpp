#include <iostream>
#include <string>
#include <getopt.h>

/*
int getopt(int argc, char * const argv[],const char *optstring);  
int getopt_long(int argc, char * const argv[], const char *optstring, const struct option *longopts, int *longindex);  
int getopt_long_only(int argc, char * const argv[], const char *optstring, const struct option *longopts, int *longindex);
*/

/* 
getopt只能处理短选项
getopt_long短选项和长选项都可以处理
argc和argv和main函数的两个参数一致
*/

/* 
optstring: 表示短选项字符串
形式如"a:b::cd:"，分别表示程序支持的命令行短选项有-a、-b、-c、-d，冒号含义如下：
(1)只有一个字符，不带冒号——只表示选项， 如-c 
(2)一个字符，后接一个冒号——表示选项后面带一个参数，如-a 100
(3)一个字符，后接两个冒号——表示选项后面带一个可选参数，即参数可有可无， 如果带参数，则选项与参数直接不能有空格形式应该如-b200
*/

/*
longopts：表示长选项结构体。结构如下：

struct option 
{  
     const char *name;  
     int         has_arg;  
     int        *flag;  
     int         val;  
};
(1)name:表示选项的名称,比如daemon,dir,out等。
(2)has_arg:表示选项后面是否携带参数。该参数有三个不同值，如下：
    a: no_argument(或者是0)时   ——参数后面不跟参数值，eg: --version,--help
    b: required_argument(或者是1)时 ——参数输入格式为：--参数 值 或者 --参数=值。eg:--dir=/home
    c: optional_argument(或者是2)时  ——参数输入格式只能为：--参数=值
(3)flag:这个参数有两个意思，空或者非空。
    a:如果参数为空NULL，那么当选中某个长选项的时候，getopt_long将返回val值。eg，可执行程序 --help，getopt_long的返回值为h.             
    b:如果参数不为空，那么当选中某个长选项的时候，getopt_long将返回0，并且将flag指针参数指向val值。eg: 可执行程序 --http-proxy=127.0.0.1:80 那么getopt_long返回值为0，并且lopt值为1。
(4)val：表示指定函数找到该选项时的返回值，或者当flag非空时指定flag指向的数据的值val


eg:
static struct option longOpts[] = {
      { "daemon", no_argument, NULL, 'D' },
      { "dir", required_argument, NULL, 'd' },
      { "out", required_argument, NULL, 'o' },
      { "log", required_argument, NULL, 'l' },
      { "split", required_argument, NULL, 's' },
      { "http-proxy", required_argument, &lopt, 1 },
      { "http-user", required_argument, &lopt, 2 },
      { "http-passwd", required_argument, &lopt, 3 },
      { "http-proxy-user", required_argument, &lopt, 4 },
      { "http-proxy-passwd", required_argument, &lopt, 5 },
      { "http-auth-scheme", required_argument, &lopt, 6 },
      { "version", no_argument, NULL, 'v' },
      { "help", no_argument, NULL, 'h' },
      { 0, 0, 0, 0 }
    };
*/

/*
longindex：longindex非空，它指向的变量将记录当前找到参数符合longopts里的第几个元素的描述，即是longopts的下标值
*/

/*
全局变量：
（1）optarg：表示当前选项对应的参数值。
（2）optind：表示的是下一个将被处理到的参数在argv中的下标值。
（3）opterr：如果opterr = 0，在getopt、getopt_long、getopt_long_only遇到错误将不会输出错误信息到标准输出流。opterr在非0时，向屏幕输出错误。
（4）optopt：表示没有被未标识的选项。
*/

using namespace std;



void showUsage() {
  //cout << "Usage: " << PACKAGE_NAME << " [options] URL ..." << endl;
  cout << "Options:" << endl;
  cout << " -a                         Option a." << endl;
  cout << " -b                         Option b." << endl;
  cout << " -c                         Option c." << endl;
  cout << " -t, --test=INT             Just for test." << endl;
  cout << " --help                     Just for help." << endl;
}

int main(int argc, char* argv[])
{
    int opt, option_index, lopt;

    static struct option long_options[] = {
        // getopt_long返回的是1
        { "test", required_argument, NULL, 1 },
        // getopt_long返回的是0, 并且将lopt指向向 'v1.0.0'
        { "version", no_argument, &lopt, 100 },
        // getopt_long返回的是'h'
        { "help", no_argument, NULL, 'h' },
        { 0, 0, 0, 0 }
    };
    while ((opt = getopt_long(argc, argv, "ab:c::t", long_options, &option_index)) != -1) 
    {
        switch (opt)
        {
        // --version
        case 0:
            cout << "case " << long_options[option_index].name << ": "<< lopt << endl;
            break;
        // --test
        case 1:
            cout << "case " <<  long_options[option_index].name << ": "<< optarg << endl;
            break;
        // --help
        case 'h':
            showUsage();
            break;
        // -a 
        case 'a':
            cout << "case a" << endl;
            break;
        // -b
        case 'b':
            cout << "case b: " << optarg << endl;
            break;
        // -c
        case 'c':
            cout << "case c: " << optarg << endl;
            break;
        default:
            break;
        }
    }
    

    return 0;
}


/*
测试
./main -a -b 1 -c2 --version --test 100 --help
*/