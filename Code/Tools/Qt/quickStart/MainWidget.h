#ifndef MAINWIDGET_H
#define MAINWIDGET_H

#include <QWidget>
#include <QHBoxLayout>
#include <QVBoxLayout>
#include <QListWidget>
#include <QTableWidget>
#include <QGroupBox>
#include <QPushButton>
#include <QLineEdit>
#include "EditStuMessBox.h"
#include <QFile>
#include <QDataStream>
#include "Student.h"
#include "Tool.h"
//自定义主窗口
class MainWidget : public QWidget
{
    Q_OBJECT
public:
    //构建主窗口界面
    MainWidget();
    //当用户点击添加按钮时，弹出添加学生信息窗口
    void AddStuBox();
public slots:
    //更新表格中罗列的学生信息
    void flushTable();
    //更新列表中显示的学生信息
    void flushListWidget(int row);
    //实现删除学生信息功能
    void delStuFun();
    //实现查找学生信息功能
    void findStuMess();
    //实现修改学生信息功能
    void changeStuMess(int row);
    //实现保存学生信息功能
    void saveStuMess();

private:
    //创建主窗口中的学生信息面板
    QGroupBox * createStuMess();
    //创建主窗口中的功能面板
    QGroupBox * createMenu();
private:
    //主窗口中的表格控件
    QTableWidget * TableWidget;
    //主窗口中的列表控件
    QListWidget *ListWidget;
    //主窗口中的添加、删除、保存、退出按钮和查找文本框控件
    QPushButton * AddStuBtn;
    QPushButton * DelStuBtn;
    QLineEdit * FindStuEdit;
    QPushButton * SaveBtn;
    QPushButton * ExitBtn;
    //弹出的添加学生信息窗口
    EditStuMessBox * messBox;
};

#endif // MAINWIDGET_H
