#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    // 创建一个 QLable 对象
    this->lab = new QLabel("Hello, World!", this);
}

MainWindow::~MainWindow()
{
    delete ui;
}

