#include "mainwindow.h"

#include <QApplication>

int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    w.show();

    //添加窗口
    QWidget widget;
    //定义一个按钮，它位于 widget 窗口中
    QPushButton Button("按钮控件", &widget);
    //设置按钮的位置和尺寸
    Button.setGeometry(10, 10, 100, 50);
    //信号与槽，实现当用户点击按钮时，窗口关闭
    QObject::connect(&Button, &QPushButton::clicked, &widget, &QWidget::close);
    //让 widget 窗口显示
    widget.show();

    return a.exec();
}
