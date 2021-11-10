#include <QApplication>
#include "MainWidget.h"
int main(int argc, char *argv[])
{
    QApplication a(argc,argv);

    MainWidget mWidget;
    mWidget.show();

    a.exec();
    return 0;
}
