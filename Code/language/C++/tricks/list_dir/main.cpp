#include <iostream>
#include <string>
#include <list>
#include <queue>
#include "dirent.h"

using namespace std;

void listdir(const string& folder, const string& extension, bool recursive, list<string>& files)
{
    DIR* dir;
    DIR* subDir;
    struct dirent* ent;

    // ��֤�ļ���
    dir = opendir(folder.c_str());
    if (dir == NULL)
    {
        cout << "Could not open " << folder.c_str() << endl;
        return;
    }
    else
    {
        closedir(dir);
    }


    // �����ļ��ж���
    queue<string> folders;
    folders.push(folder);

    // �����ļ���
    while (!folders.empty())
    {
        // ������ȡһ���ļ�
        string currFolder = folders.front();
        folders.pop();
        dir = opendir(currFolder.c_str());
        // ���ļ�������
        if (dir == NULL) {continue;}
        // �����ļ�������������ļ�
        while ((ent = readdir(dir)) != NULL)
        {
            string name(ent->d_name);
            // ���� . �� ..
            if (name.compare(".") == 0 || name.compare("..") == 0) {continue;}
            string path = currFolder;
            path.append("/");
            path.append(name);

            // �ж��Ƿ�Ϊ���ļ���
            subDir = opendir(path.c_str());
            if (subDir != NULL)
            {
                closedir(subDir);
                if (recursive) {folders.push(path);}
            }
            else
            {
                // �ļ�������׺������
                if (extension.empty())
                {
                    files.push_back(path);
                }
                else
                {
                    size_t lastDot = name.find_last_of('.');
                    string ext = name.substr(lastDot + 1);
                    if (ext.compare(extension) == 0){files.push_back(path);}
                }
            }
        }
        closedir(dir);
    }
    
}

int main()
{
    list<string> files;
    string folder = "C:\\code\\wanhui\\Brainpower";
    listdir(folder, "md", true, files);
    for (auto file = files.begin(); file != files.end(); file++){
        cout << *file << endl;
    }
    return 0;
}