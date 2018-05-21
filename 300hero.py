import sys
import subprocess

import requests
from PyQt5.QtWidgets import (QWidget, QLineEdit, QTextEdit, QPushButton,
                             QAction, qApp, QGridLayout, QTableWidget,
                             QAbstractItemView, QTableWidgetItem, QDesktopWidget,
                             QApplication, QMessageBox, )
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot, Qt
from scrapy.crawler import CrawlerRunner, reactor

from jump_300heroes.spiders.my_report import JumpReport
from db import db_handle


class Main(QWidget):
    class A(QWidget):

        def __init__(self):
            super().__init__()

            self.initUI()

        def initUI(self):
            self.setGeometry(300, 300, 300, 220)
            self.setWindowTitle('Icon')
            self.setWindowIcon(QIcon('web.png'))

            self.show()

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):

        # QToolTip.setFont(QFont('SanSerif', 10))

        # self.setToolTip('This is a <b>QWidget</b> widget')

        # textEdit = QTextEdit()
        # self.setCentralWidget(textEdit)

        self.qle = QLineEdit("")
        self.user = self.qle.text()
        self.para = "user={}".format(self.user)
        print(self.user, '1')
        btn = QPushButton('查询', self)
        # btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.clicked.connect(self.search)

        self.txt = QTextEdit()
        # self.txt.textChanged.connect(self.adjustSize)

        self.battle = QTextEdit()

        self.player_status = QTextEdit()

        self.create_table()

        # 名称不能用Quit、Exit，用了就无法显示，原因不明
        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('application')
        exitAction.triggered.connect(qApp.quit)

        # self.statusBar()

        # menubar = QMainWindow.menuBar()

        # Mac OS的状态栏显示不一样
        # menubar.setNativeMenuBar(False)

        # fileMenu = menubar.addMenu('&File')
        # fileMenu.addAction(exitAction)

        # toolbar = self.addToolBar('Exit')
        # toolbar.addAction(exitAction)

        grid = QGridLayout()
        grid.setSpacing(10)

        grid.addWidget(self.qle, 1, 0)
        grid.addWidget(btn, 2, 0)
        grid.addWidget(self.txt, 3, 0)
        grid.addWidget(self.battle, 1, 1, 3, 1)
        grid.addWidget(self.player_status, 4, 0, 2, 2)
        grid.addWidget(self.battle_table, 6, 0, 2, 2)

        self.setLayout(grid)

        self.setGeometry(600, 600, 800, 600)
        self.center()
        self.setWindowTitle("战绩查询")

        self.show()

    def create_table(self):
        # 设置表
        self.battle_table = QTableWidget()
        # 表列数，行数在下方读取数据时，根据数据量建立
        self.battle_table.setColumnCount(8)
        # 设置表头
        self.battle_table.setHorizontalHeaderLabels(
            ['match_id', 'head', 'date', 'time', 'kill_count', 'death', 'support', 'score'])
        # 隔行变色
        self.battle_table.setAlternatingRowColors(True)
        # 整行选中
        self.battle_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        # 将列调整到跟内容大小相匹配
        # self.battle_table.resizeColumnsToContents()
        #  #将行大小调整到跟内容的大小相匹配
        self.battle_table.resizeRowsToContents()
        # 点击事件
        self.battle_table.doubleClicked.connect(self.on_click)

    @pyqtSlot()
    def on_click(self):
        currentQTableWidgetItem = self.battle_table.selectedItems()[0]
        # 点击的行包含的比赛id
        # match_id = self.battle_table.item(currentQTableWidgetItem.row(), 0).text()
        match_id = currentQTableWidgetItem.text()
        print(match_id)
        # self.showDialog(match_id)

    def showDialog(self, match_id):

        data = requests.get('http://300report.jumpw.com/api/getmatch?id={}'.format(match_id))
        a = self.A()

    def spider(self, name):
        subprocess.call('ls')
        subprocess.call('scrapy crawl JumpReport -a user="{}"'.format(name), shell=True)

    def search(self):

        # 脚本执行爬虫代码
        name = self.qle.text()

        self.spider(name)

        db = db_handle()
        with db as con:
            sql = "select * from player where name = '{}' order by update_time".format(name)
            con.execute(sql)
            player = con.fetchone()
            if player:
                id, name, win, match_count, strength, level, update_time, rank = player
                text = "角色名:  {}\n胜场:    {}\n总场数:  {}\n团分:    {}\n团分排行: {}\n等级:    {}\n更新时间: {}".format(
                    name, win, match_count, strength, rank, level, update_time)

                self.txt.setText(text)

            sql = "select * from player_data where name = '{}' order by date".format(name)
            con.execute(sql)
            player_data = con.fetchall()
            a = ""
            for data in player_data:
                a += str(data)
                a += "\n"
            self.battle.setText(str(a))

            sql = "select * from game_data order by match_id desc"
            con.execute(sql)
            game_data = con.fetchall()
            a = ""
            l = 0
            self.battle_table.setRowCount(len(game_data))
            for data in game_data:
                a += str(data[1:])

                for i in range(self.battle_table.columnCount()):
                    item = QTableWidgetItem(str(data[i + 1]))
                    # 设置填入数据的排列位置（左右居中| 上下居中）
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.battle_table.setItem(l, i, item)

                a += "\n"
                self.player_status.setText(str(a))
                l += 1
        print('search over')

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message', "Quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes)

        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()


class BatterReport(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.txt = QTextEdit()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    ex = Main()

    sys.exit(app.exec_())
