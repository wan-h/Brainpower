#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QLabel>
#include <QPushButton>

QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    // Q_OBJECT是一个已定义好的宏，所有需要“信号和槽”功能的组件都必须将 Q_OBJECT 作为 private 属性成员引入到类中
    Q_OBJECT

public:
    // QWidget 是所有组件的基类，借助 parent 指针，可以为当前窗口指定父窗口
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private:
    Ui::MainWindow *ui;
    // 定义一个私有的指针对象
    QLabel *lab;
};
#endif // MAINWINDOW_H
