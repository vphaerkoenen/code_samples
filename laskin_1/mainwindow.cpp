#include "mainwindow.h"
#include "ui_mainwindow.h"
#include <QDebug>
#include <string>
#include <QFile>
#include <QMessageBox>
#include <QTextStream>
#include <QIODevice>
#include <QStandardPaths>
#include <QtNetwork/QNetworkAccessManager>
#include <QtNetwork/QNetworkRequest>
#include <QtNetwork/QNetworkReply>
#include <QJsonDocument>
#include <QUrl>
#include <QtNetwork>

double firstNum;
double secondNum;
int operation;
QString equationToSave;

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)

{
    ui->setupUi(this);
    ui->statusbar->hide();
    firstNum=0;
    secondNum=0;
    operation=0;

}

MainWindow::~MainWindow()
{
    delete ui;
}



void MainWindow::on_oneButton_clicked()
{
    ui->lcd->setText(ui->lcd->text()+"1");
}

void MainWindow::on_twoButton_clicked()
{
    ui->lcd->setText(ui->lcd->text()+"2");
}

void MainWindow::on_threeButton_clicked()
{
    ui->lcd->setText(ui->lcd->text()+"3");
}

void MainWindow::on_fourButton_clicked()
{
    ui->lcd->setText(ui->lcd->text()+"4");
}

void MainWindow::on_fiveButton_clicked()
{
    ui->lcd->setText(ui->lcd->text()+"5");
}


void MainWindow::on_sixButton_clicked()
{
    ui->lcd->setText(ui->lcd->text()+"6");
}


void MainWindow::on_sevenButton_clicked()
{
    ui->lcd->setText(ui->lcd->text()+"7");
}


void MainWindow::on_eightButton_clicked()
{
    ui->lcd->setText(ui->lcd->text()+"8");
}


void MainWindow::on_nineButton_clicked()
{
    ui->lcd->setText(ui->lcd->text()+"9");
}


void MainWindow::on_zeroButton_clicked()
{
    ui->lcd->setText(ui->lcd->text()+"0");
}

void MainWindow::on_dotButton_clicked()
{
    ui->lcd->setText(ui->lcd->text()+".");
}

void MainWindow::on_minusButton_clicked()
{
    firstNum=ui->lcd->text().toDouble();
    equationToSave=ui->lcd->text()+"-";
    operation=1;
    ui->lcd->clear();
}

void MainWindow::on_plusButton_clicked()
{
    firstNum=ui->lcd->text().toDouble();
    equationToSave=ui->lcd->text()+"+";

    operation=2;
    ui->lcd->clear();
}

void MainWindow::on_multiplyButton_clicked()
{
    firstNum=ui->lcd->text().toDouble();
    equationToSave=ui->lcd->text()+"*";
    operation=3;
    ui->lcd->clear();
}

void MainWindow::on_divideButton_clicked()
{
    firstNum=ui->lcd->text().toDouble();
    equationToSave=ui->lcd->text()+"/";
    operation=4;
    ui->lcd->clear();
}

void MainWindow::on_summaryButton_clicked()
{
    try {
        secondNum=ui->lcd->text().toDouble();
        equationToSave.append(ui->lcd->text());
        switch (operation) {
        case 1:{
            double minusAnswer=firstNum-secondNum;
            QString minusTypeAnswer=QString::number(minusAnswer);
            equationToSave.append("="+minusTypeAnswer);
            ui->lcd->setText(minusTypeAnswer);
            break;}
        case 2:{
            double plusAnswer=firstNum+secondNum;
            QString plusTypeAnswer=QString::number(plusAnswer);
            equationToSave.append("="+plusTypeAnswer);
            ui->lcd->setText(plusTypeAnswer);
            break;}
        case 3:{
            double multiplyAnswer=firstNum*secondNum;
            QString multiTypeAnswer=QString::number(multiplyAnswer);
            equationToSave.append("="+multiTypeAnswer);
            ui->lcd->setText(multiTypeAnswer);
            break;}
        case 4:{
            double divideAnswer=firstNum/secondNum;
            QString divideTypeAnswer=QString::number(divideAnswer);
            equationToSave.append("="+divideTypeAnswer);
            ui->lcd->setText(divideTypeAnswer);
            break;}

        default:
            ui->lcd->setText("learn to count,punk");
            break;
        }

        firstNum=0;
        secondNum=0;
        operation=0;
    } catch (_exception) {
        ui->lcd->setText("learn to count,punk");
    }
}

void MainWindow::on_clrButton_clicked()
{
    ui->lcd->setText("");
    firstNum=0;
    secondNum=0;
    operation=0;
}

void MainWindow::on_saveButton_clicked()
{
    QMessageBox mBox;
    QPixmap icon(":/pics/chucknorris2.PNG");
    mBox.setWindowIcon(icon);

    try{
        QFile file("lastcount.txt");
        file.remove();
        qDebug()<<"old save removed";
        if (!file.open(QIODevice::WriteOnly | QIODevice::Text))
            return;

        QTextStream out(&file);
        out << equationToSave;
        qDebug()<<"saved"<<equationToSave;
        mBox.setWindowTitle("saved");
        mBox.setText("punk has saved calculation");
        mBox.exec();
        }
    catch(_exception){
        mBox.setText("save failed");
        mBox.exec();

    }

}

void MainWindow::on_showButton_clicked()
{
    QMessageBox msBox;
    QPixmap icon(":/pics/chucknorris2.PNG");
    msBox.setWindowIcon(icon);
    try{
        QFile file("lastcount.txt");
        if (!file.open(QIODevice::ReadOnly | QIODevice::Text))
            return;

        QTextStream in(&file);
        while (!in.atEnd()) {
            QString line = in.readLine();
            //process_line(line);

            msBox.setWindowTitle("punks last calculation");
            msBox.setText(line);
            msBox.exec();
        }
    }
    catch(_exception){

        msBox.setText("Failed to show punks last calculation");
        msBox.exec();

    }
}

void MainWindow::on_jokeButton_clicked()
{
    QMessageBox showJoke;
    QPixmap icon(":/pics/chucknorris2.PNG");
    showJoke.setWindowIcon(icon);
    try {
        QUrl url = QUrl("https://api.chucknorris.io/jokes/random");
        QNetworkRequest request{url};
        request.setHeader(QNetworkRequest::ContentTypeHeader, "application/json");
        QNetworkAccessManager manager;
        QNetworkReply *reply = manager.get(request);
        while (!reply->isFinished())
        {
            qApp->processEvents();
        }
        QByteArray response_data = reply->readAll();
        QJsonDocument jsonData = QJsonDocument::fromJson(response_data);

        showJoke.setWindowTitle("Chuck Norris jokes for you,punk");
        showJoke.setText(jsonData.object().value("value").toString());
        showJoke.exec();
        reply->deleteLater();

    } catch (_exception) {

        showJoke.setWindowTitle("punk get a failure");
        showJoke.setText("Loading joke for punk not succeeded");
        showJoke.exec();
    }
}
