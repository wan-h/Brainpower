#include <iostream>
#include <fstream>
#include <sstream>
#include "rapidjson/document.h"
#include "rapidjson/writer.h"
#include "rapidjson/prettywriter.h"
#include "rapidjson/stringbuffer.h"

using namespace std;
using namespace rapidjson;

int rapidjson_write()
{
    StringBuffer s;
    // Writer<StringBuffer> writer(s);
    // �����json���Զ�����
    PrettyWriter<StringBuffer> writer(s);
    // StartObject �� EndObject��ʾһ���ֵ�Ŀ�ʼ�ͽ���
    writer.StartObject();
    // ���� key value
    writer.Key("name");writer.String("spring");

    writer.Key("address");writer.String("����");

    writer.Key("age");writer.Int(30);

    writer.Key("value1");
    // StartArray �� EndArray��ʾһ���б�Ŀ�ʼ�ͽ���
    writer.StartArray();
    writer.StartArray();
    writer.Double(23);writer.Double(43);writer.Double(-2.3);writer.Double(6.7);writer.Double(90);
    writer.EndArray();
    writer.StartArray();
    writer.Int(-9);writer.Int(-19);writer.Int(10);writer.Int(2);
    writer.EndArray();
    writer.StartArray();
    writer.Int(-5);writer.Double(-55.1);
    writer.EndArray();
    writer.EndArray();

    writer.Key("value2");
    writer.StartObject();
    writer.Key("address1");writer.String("�Ĵ�");
    writer.Key("address2");
    writer.StartArray();
    writer.StartObject();writer.Key("wanzhou");writer.String("����");writer.EndObject();
    writer.StartObject();writer.Key("jiefangbei");writer.String("��ű�");writer.EndObject();
    writer.EndArray();
    writer.EndObject();

    writer.EndObject();

    cout << s.GetString() << endl;

    char* file_name = "test.json";
    ofstream outfile;
    outfile.open(file_name);
    const char* json_content = s.GetString();
    outfile << json_content << endl;
    outfile.close();

    return 0;
}

int rapidjson_read()
{
    char* file_name = "test.json";
    ifstream inf(file_name);
    if (!inf.is_open())
    {
        cout << "Fail to read json file." << endl;
        return -1;
    }
    stringstream in;
    in << inf.rdbuf();
    string json_content = in.str();
    inf.close();

    Document dom;
    if(!dom.Parse(json_content.c_str()).HasParseError())
    {
        // ��ȡ�ڵ����
        Value& obj = dom["value2"];
        if (obj.HasMember("address2") && obj["address2"].IsArray())
        {
            Value& arr = obj["address2"];
            for (int i = 0; i < arr.Size(); i++)
            { 
                // ��ǰ������just for test
                cout << "wanzhou: " << arr[i]["wanzhou"].GetString();
                break;
            }
        }
    }
    else
    {
        cout << "Fail to parse json file." << endl;
    }

    // ����
    for (Value::ConstMemberIterator iter = dom.MemberBegin(); iter != dom.MemberEnd(); iter++)
    {
        cout << "iter name: " << iter->name.GetString() << ", type: " << iter->value.GetType() << endl;
    }

    return 0;
}

int main()
{
    // rapidjson_write();
    rapidjson_read();
    return 0;
}