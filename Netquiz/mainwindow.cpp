////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////
////        *        * ******* ********* *         *       * * **********       ////
////        **       * *           *     ********* *       * *         *        ////
////        * *      * *           *     *       * *       * *        *         ////
////        *  *     * *           *     *       * *       * *       *          ////
////        *   *    * *           *     *       * *       * *      *           ////
////        *    *   * *****       *     *       * *       * *     *            ////
////        *     *  * *           *     *       * *       * *    *             ////
////        *      * * *           *     *       * *       * *   *              ////
////        *       ** *           *     *       * *       * *  *               ////
////        *        * *******     *     ********* ********* * **********       ////
////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////////

#include "mainwindow.h"
#include "qobjectdefs.h"
#include "ui_mainwindow.h"
#include "qpushbutton.h"
#include <iostream>
#include "qeventloop.h"
#include "qnetworkaccessmanager.h"
#include "QNetworkReply"
#include "qnetwork.h"
#include "qmessagebox.h"
#include <json.hpp>
#include <sstream>
#include <QStringList>
#include <random>
#include <algorithm>
#include <QMediaPlayer>
#include <QAudioOutput>

using json = nlohmann::json;
using namespace std;
QNetworkAccessManager *manager = new QNetworkAccessManager();
std::string correct_answer;
int point_counter;
int question_counter;
QMediaPlayer *player = new QMediaPlayer();
QAudioOutput *audioOutput = new QAudioOutput;

QString yeah_sounds[7] =  {"qrc:/yeah_sounds/aw-yeah-awww-yeah-aww-yeah-2-95782.mp3",
    "qrc:/yeah_sounds/cute-level-up-3-189853.mp3",
    "qrc:/yeah_sounds/glad-piano-logo-13394.mp3",
    "qrc:/yeah_sounds/group_yay_cheer-101509.mp3",
    "qrc:/yeah_sounds/hooray-36461.mp3",
    "qrc:/yeah_sounds/wow-121578.mp3",
    "qrc:/yeah_sounds/yay-6326.mp3"
};


QString boo_sounds[8] = {"qrc:/ohno_sounds/09-hombre1llorawav-14436.mp3",
    "qrc:/ohno_sounds/boo-6377.mp3",
    "qrc:/ohno_sounds/boo-36556.mp3",
    "qrc:/ohno_sounds/confused-what-103562.mp3",
    "qrc:/ohno_sounds/ehhhmp3-14559.mp3",
    "qrc:/ohno_sounds/non-enthusiastic-clap-102655.mp3",
    "qrc:/ohno_sounds/ooh-123103.mp3",
    "qrc:/ohno_sounds/suspiro-tristeza-46553.mp3"

};


MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)

{

    ui->setupUi(this);
    connect(MainWindow::ui->newQuestionButton,SIGNAL(clicked()),this,SLOT(connectToApi()));
    connect(MainWindow::ui->submitButton,SIGNAL(submit_clicked()),this,SLOT(on_submitButton_clicked()));
    ui->question_label->setStyleSheet("color:white;");                      //white text color gives more contrast compared to black
    ui->radioButton->setStyleSheet("color:white;");
    ui->radioButton_2->setStyleSheet("color:white;");
    ui->radioButton_3->setStyleSheet("color:white;");
    ui->radioButton_4->setStyleSheet("color:white;");
    ui->question_label->setWordWrap(true);                                  //if question is too long, it is divided to multiple lines
    ui->label_3->setStyleSheet("color:white;");
    ui->label_4->setStyleSheet("color:white;");
    ui->label_5->setStyleSheet("color:white;");
    point_counter = 0;
    question_counter = 0;
    MainWindow::ui->submitButton->setEnabled(false);
    player->setSource(QUrl("qrc:/ttsmaker-file-2024-3-24-10-47-23.mp3"));   //welcome sound
    player->setAudioOutput(audioOutput);
    player->play();
    cout << "Mediaplayer statuscode: " <<  player->mediaStatus() << endl;   //this is for debugging
    cout << "Mediaplayer error: " <<  player->error() << endl;              //this is for debugging

}


void MainWindow::playBooSound(){                                            //execute this if answer is wrong
    std::random_shuffle(&boo_sounds[0], &boo_sounds[8]);                    //randomize sequence of available sounds
    player->setSource(static_cast<QUrl>(boo_sounds[0]));
    player->setAudioOutput(audioOutput);
    player->play();
    cout << "Mediaplayer statuscode: " <<  player->mediaStatus() << endl;

}


void MainWindow::playYeeSound(){                                            //execute this if answer is right
    std::random_shuffle(&yeah_sounds[0], &yeah_sounds[7]);
    player->setSource(static_cast<QUrl>(yeah_sounds[0]));
    player->setAudioOutput(audioOutput);
    player->play();
    cout << "Mediaplayer statuscode: " <<  player->mediaStatus() << endl;

}


void answerPlease(){                                                        //execute this if no option is selected
    QMessageBox mbox;
    mbox.informativeText();
    mbox.setText("You must choose one option");
    mbox.hasFocus();
    mbox.exec();
}


void MainWindow::endOfGame(){                                               //execute this when game ends
     QMessageBox mbox;
    mbox.setWindowTitle(" ");
    mbox.setIcon(QMessageBox::NoIcon);
    mbox.setText("You had " + QString::number( point_counter) + " points out of 10");
    mbox.hasFocus();
    mbox.exec();
    point_counter = 0;
    question_counter = 0;
    MainWindow::ui->label_4->setText("0");

}


void MainWindow::connectToApi(){                                            //execute this when new question is wanted

    QMessageBox mbox;
    question_counter++;
    if(question_counter == 10){
        endOfGame();
    }
    // next massive set of code unchecks radiobuttons, seems complicated(it is)
    MainWindow::ui->radioButton->setAutoExclusive(false);
    MainWindow::ui->radioButton->setChecked(false);
    MainWindow::ui->radioButton->setAutoExclusive(true);

    MainWindow::ui->radioButton_2->setAutoExclusive(false);
    MainWindow::ui->radioButton_2->setChecked(false);
    MainWindow::ui->radioButton_2->setAutoExclusive(true);

    MainWindow::ui->radioButton_3->setAutoExclusive(false);
    MainWindow::ui->radioButton_3->setChecked(false);
    MainWindow::ui->radioButton_3->setAutoExclusive(true);

    MainWindow::ui->radioButton_4->setAutoExclusive(false);
    MainWindow::ui->radioButton_4->setChecked(false);
    MainWindow::ui->radioButton_4->setAutoExclusive(true);

    // lets try connecting to trivia API to get our next question
    try {

        MainWindow::ui->submitButton->setEnabled(true);
        QUrl url = QUrl("https://the-trivia-api.com/v2/questions");
        QNetworkRequest request{url};
        QNetworkReply *reply = manager->get(request);
        while (!reply->isFinished())
        {
            qApp->processEvents();
        }

        QByteArray response_data=reply->readAll();
        json Doc{json::parse(response_data)};

        for (auto it = Doc.begin(); it != Doc.end(); ++it)
        {
            std::cout <<  it.value()[0]["question"]["text"] << endl;
            std::cout <<  it.value()[0]["correctAnswer"] << endl;
            std::cout <<  it.value()[0]["incorrectAnswers"][0] << endl;
            std::cout <<  it.value()[0]["incorrectAnswers"][1] << endl;
            std::cout <<  it.value()[0]["incorrectAnswers"][2] << endl;

            //next 3 lines sets question to question label
            std::string showable_question = static_cast <std::string>( it.value()[0]["question"]["text"])  ;
            QString showable_question_qstring = QString::fromStdString( showable_question );
            MainWindow::ui->question_label->setText(showable_question_qstring);

            //next  lines are 4 options for answer to question, one of them being right one
            correct_answer = static_cast <std::string>( it.value()[0]["correctAnswer"])  ;
            std::cout << "Correct answer is: " << correct_answer << endl;

            std::string option2 = static_cast <std::string>( it.value()[0]["incorrectAnswers"][0])  ;

            std::string option3 = static_cast <std::string>( it.value()[0]["incorrectAnswers"][1])  ;

            std::string option4 = static_cast <std::string>( it.value()[0]["incorrectAnswers"][2])  ;

            // collecting all options to array and mixing sequence
            std::string all_options [4] = {correct_answer, option2, option3, option4};
            std::random_shuffle( &all_options[0] , &all_options[4]);
            // inserting options to radiobuttons
            MainWindow::ui->radioButton ->setText(QString::fromStdString(all_options[0]));
            MainWindow::ui->radioButton_2->setText(QString::fromStdString(all_options[1]));
            MainWindow::ui->radioButton_3->setText(QString::fromStdString(all_options[2]));
            MainWindow::ui->radioButton_4->setText(QString::fromStdString(all_options[3]));
         }

        reply->deleteLater();

    } catch( ...){  //three dots as parameter takes care of any kind of error

        cout<<endl;
        cout<<"loading data not succeeded"<<endl;
        mbox.setWindowTitle("Load data failure");
        mbox.setText("Loading data not succeeded");
        mbox.hasFocus();
        mbox.exec();
    }

}


void MainWindow::on_submitButton_clicked(){                                     //execute this when answer has given
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    player->setSource(QUrl("qrc:/750-milliseconds-of-silence.mp3"));////////This part is needed because QMediaPlayer //
    player->setAudioOutput(audioOutput);////////////////////////////////////cant play same sound twice in a row////////
    player->play();/////////////////////////////////////////////////////////(this cuts row of same sound)//////////////
    ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    try{
        int selected = 0;
        //MainWindow::ui->submitButton->setEnabled(false);
        std::string case1_string = MainWindow::ui->radioButton->text().toStdString();
        std::string case2_string = MainWindow::ui->radioButton_2->text().toStdString();
        std::string case3_string = MainWindow::ui->radioButton_3->text().toStdString();
        std::string case4_string = MainWindow::ui->radioButton_4->text().toStdString();

        // lets find out, which of our radiobuttons are checked
        if(MainWindow::ui->radioButton->isChecked()){
            selected = 1;
        }else if(MainWindow::ui->radioButton_2->isChecked()){
            selected = 2;
        }else if(MainWindow::ui->radioButton_3->isChecked()){
            selected = 3;
        }else if(MainWindow::ui->radioButton_4->isChecked())
            selected = 4;
        else
            answerPlease();

        switch(selected){
        case 1:
            if(correct_answer == case1_string ){

                ++point_counter;
                MainWindow::ui->label_4->setText(QString::number(point_counter)) ;
                playYeeSound();
            }else
                playBooSound();
            break;

        case 2:
            if(correct_answer == case2_string ){
                ++point_counter;
                MainWindow::ui->label_4->setText(QString::number(point_counter)) ;
                playYeeSound();
            }else
                playBooSound();
            break;

        case 3:
            if(correct_answer == case3_string ){
                ++point_counter;
                MainWindow::ui->label_4->setText(QString::number(point_counter)) ;
                playYeeSound();
            }else
                playBooSound();
            break;

        case 4:
            if(correct_answer == case4_string ){
                ++point_counter;
                MainWindow::ui->label_4->setText(QString::number(point_counter)) ;
                playYeeSound();
            }else
                playBooSound();
            break;

        default:
            playBooSound();
        }

    connectToApi();

    }catch(...){
        QMessageBox mbox;
        mbox.setWindowTitle("Something went wrong");
        mbox.setText("Unexpected problems occurred");
        mbox.hasFocus();
        mbox.exec();
    }

}


MainWindow::~MainWindow(){
    delete ui;
    delete manager;
    delete player;
    delete audioOutput;

}

