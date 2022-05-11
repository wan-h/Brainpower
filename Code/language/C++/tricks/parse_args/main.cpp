#include <iostream>
#include <string>
#include <getopt.h>

/*
int getopt(int argc, char * const argv[],const char *optstring);  
int getopt_long(int argc, char * const argv[], const char *optstring, const struct option *longopts, int *longindex);  
int getopt_long_only(int argc, char * const argv[], const char *optstring, const struct option *longopts, int *longindex);
*/

/* 
getoptֻ�ܴ����ѡ��
getopt_long��ѡ��ͳ�ѡ����Դ���
argc��argv��main��������������һ��
*/

/* 
optstring: ��ʾ��ѡ���ַ���
��ʽ��"a:b::cd:"���ֱ��ʾ����֧�ֵ������ж�ѡ����-a��-b��-c��-d��ð�ź������£�
(1)ֻ��һ���ַ�������ð�š���ֻ��ʾѡ� ��-c 
(2)һ���ַ������һ��ð�š�����ʾѡ������һ����������-a 100
(3)һ���ַ����������ð�š�����ʾѡ������һ����ѡ���������������п��ޣ� �������������ѡ�������ֱ�Ӳ����пո���ʽӦ����-b200
*/

/*
longopts����ʾ��ѡ��ṹ�塣�ṹ���£�

struct option 
{  
     const char *name;  
     int         has_arg;  
     int        *flag;  
     int         val;  
};
(1)name:��ʾѡ�������,����daemon,dir,out�ȡ�
(2)has_arg:��ʾѡ������Ƿ�Я���������ò�����������ֵͬ�����£�
    a: no_argument(������0)ʱ   �����������治������ֵ��eg: --version,--help
    b: required_argument(������1)ʱ �������������ʽΪ��--���� ֵ ���� --����=ֵ��eg:--dir=/home
    c: optional_argument(������2)ʱ  �������������ʽֻ��Ϊ��--����=ֵ
(3)flag:���������������˼���ջ��߷ǿա�
    a:�������Ϊ��NULL����ô��ѡ��ĳ����ѡ���ʱ��getopt_long������valֵ��eg����ִ�г��� --help��getopt_long�ķ���ֵΪh.             
    b:���������Ϊ�գ���ô��ѡ��ĳ����ѡ���ʱ��getopt_long������0�����ҽ�flagָ�����ָ��valֵ��eg: ��ִ�г��� --http-proxy=127.0.0.1:80 ��ôgetopt_long����ֵΪ0������loptֵΪ1��
(4)val����ʾָ�������ҵ���ѡ��ʱ�ķ���ֵ�����ߵ�flag�ǿ�ʱָ��flagָ������ݵ�ֵval


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
longindex��longindex�ǿգ���ָ��ı�������¼��ǰ�ҵ���������longopts��ĵڼ���Ԫ�ص�����������longopts���±�ֵ
*/

/*
ȫ�ֱ�����
��1��optarg����ʾ��ǰѡ���Ӧ�Ĳ���ֵ��
��2��optind����ʾ������һ�����������Ĳ�����argv�е��±�ֵ��
��3��opterr�����opterr = 0����getopt��getopt_long��getopt_long_only�������󽫲������������Ϣ����׼�������opterr�ڷ�0ʱ������Ļ�������
��4��optopt����ʾû�б�δ��ʶ��ѡ�
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
        // getopt_long���ص���1
        { "test", required_argument, NULL, 1 },
        // getopt_long���ص���0, ���ҽ�loptָ���� 'v1.0.0'
        { "version", no_argument, &lopt, 100 },
        // getopt_long���ص���'h'
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
����
./main -a -b 1 -c2 --version --test 100 --help
*/