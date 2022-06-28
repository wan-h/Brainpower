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

    // 验证文件夹
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


    // 处理文件夹队列
    queue<string> folders;
    folders.push(folder);

    // 遍历文件夹
    while (!folders.empty())
    {
        // 队列中取一个文件
        string currFolder = folders.front();
        folders.pop();
        dir = opendir(currFolder.c_str());
        // 非文件夹跳过
        if (dir == NULL) {continue;}
        // 遍历文件夹下面的所有文件
        while ((ent = readdir(dir)) != NULL)
        {
            string name(ent->d_name);
            // 跳过 . 和 ..
            if (name.compare(".") == 0 || name.compare("..") == 0) {continue;}
            string path = currFolder;
            path.append("/");
            path.append(name);

            // 判断是否为子文件夹
            subDir = opendir(path.c_str());
            if (subDir != NULL)
            {
                closedir(subDir);
                if (recursive) {folders.push(path);}
            }
            else
            {
                // 文件处理，后缀名过滤
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