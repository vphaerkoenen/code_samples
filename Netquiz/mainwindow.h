#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include "qnetworkreply.h"
#include <QMainWindow>
#include <QThread>


QT_BEGIN_NAMESPACE
namespace Ui { class MainWindow; }
QT_END_NAMESPACE

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private:
    Ui::MainWindow *ui;

public slots:
    void on_submitButton_clicked();
    void connectToApi();
    void replyFinished (QNetworkReply *reply);
    void endOfGame();
    void playBooSound();
    void playYeeSound();

signals:
    void submit_clicked();
    void clicked();
    void finished();
    void finished (QNetworkReply *reply);

};
#endif // MAINWINDOW_H
