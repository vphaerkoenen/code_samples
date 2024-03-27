#include "mainwindow.h"
#include <QApplication>
#include "ui_mainwindow.h"


int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    w.show();
    w.setWindowTitle("NETQUIZ");
    w.setWindowIcon(QIcon(":/NetquizTausta.png")) ;
    return a.exec();
}

