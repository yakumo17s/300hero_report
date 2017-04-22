import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import QCoreApplication

import pymysql
import requests

from twisted.internet import reactor, defer
from scrapy.crawler import CrawlerRunner, CrawlerProcess
from scrapy.utils.project import get_project_settings
from spider.jump_300heroes.jump_300heroes.spiders.my_report import JumpReport
from scrapy.settings import Settings
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from multiprocessing import Process




def db_handle():

    con = pymysql.connect(
        host='localhost',
        user='web',
        passwd='web',
        charset='utf8',
        database='heroes'
    )
    return con

class Example(QWidget):

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

        #QToolTip.setFont(QFont('SanSerif', 10))

        #self.setToolTip('This is a <b>QWidget</b> widget')

        #textEdit = QTextEdit()
        #self.setCentralWidget(textEdit)

        self.qle = QLineEdit("蔽月八云")

        btn = QPushButton('查询', self)
        #btn.setToolTip('This is a <b>QPushButton</b> widget')
        btn.resize(btn.sizeHint())
        btn.clicked.connect(self.search)

        self.txt = QTextEdit()
        #self.txt.textChanged.connect(self.adjustSize)

        self.battle = QTextEdit()

        self.player_status = QTextEdit()

        self.create_table()



        # 名称不能用Quit、Exit，用了就无法显示，原因不明
        exitAction = QAction('Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('application')
        exitAction.triggered.connect(qApp.quit)

        #self.statusBar()

        #menubar = QMainWindow.menuBar()

        # Mac OS的状态栏显示不一样
        #menubar.setNativeMenuBar(False)

        #fileMenu = menubar.addMenu('&File')
        #fileMenu.addAction(exitAction)

        #toolbar = self.addToolBar('Exit')
        #toolbar.addAction(exitAction)

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
        #match_id = self.battle_table.item(currentQTableWidgetItem.row(), 0).text()
        match_id = currentQTableWidgetItem.text()
        print(match_id)
        self.showDialog(match_id)

    def showDialog(self, match_id):

        data = requests.get('http://300report.jumpw.com/api/getmatch?id={}'.format(match_id))
        a = self.A()

        ## 启动爬虫，获取该场比赛所有人的数据
        #runner = CrawlerRunner(get_project_settings())
        #runner.crawl('JumpReport')
        #d = runner.join()
        #d.addBoth(lambda _: reactor.stop())
        #reactor.run()  # 阻塞运行爬虫
        #
        #text, ok = QInputDialog.getText(self, 'Input Dialog',
        #                                'Enter your name:')



    def search(self):
        if __name__ == '__main__':

            p = Process(target=self.a())
            p.start()
            p.join()

    def a(self):

        print(__name__)


        #process = CrawlerProcess(get_project_settings())
        #process.crawl('JumpReport')
        #process.start()
        #process.stop()
        #process.put()
        # 脚本执行爬虫代码
        runner = CrawlerRunner(get_project_settings())

        #def search(runner, keyword):
        #    return runner.crawl(JumpReport, keyword)

        #runner = CrawlerProcess()
        #dfs = set()
        runner.crawl('JumpReport')
        d = runner.join()
        #dfs.add(d)
        #defer.DeferredList(dfs).addBoth(lambda _: reactor.stop())
        d.addBoth(lambda _: reactor.stop())
        #search(runner, "abcd")
        #search(runner, "beat")
        #runner.start()
        reactor.run()  # 阻塞运行爬虫

        print("complete")


        # runner = CrawlerRunner(get_project_settings())
        # dfs = set()
        # for domain in range(2):
        #     d = runner.crawl('JumpReport')
        #     dfs.add(d)
        #
        # defer.DeferredList(dfs).addBoth(lambda _: reactor.stop())
        # reactor.run()  # the script will block here until all crawling jobs are finished

        # runner = CrawlerRunner(get_project_settings())
        #
        # @defer.inlineCallbacks
        # def crawl():
        #     for domain in range(2):
        #         yield runner.crawl('JumpReport')
        #     reactor.stop()
        #
        # crawl()
        # reactor.run()  # the script will block here until the last crawl call is finished

        # settings = Settings({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
        # runner = CrawlerRunner(settings)
        # 
        # d = runner.crawl(JumpReport)
        # d.addBoth(lambda _: reactor.stop())
        # reactor.run() # the script will block here until the crawling is finished


        # runner = CrawlerProcess(get_project_settings())
        # runner.crawl(JumpReport)
        # runner.start()

        name = self.qle.text()
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
                print(type(data))

                for i in range(self.battle_table.columnCount()):

                    item = QTableWidgetItem(str(data[i + 1]))
                    # 设置填入数据的排列位置（左右居中| 上下居中）
                    item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
                    self.battle_table.setItem(l, i, item)

                a += "\n"
                self.player_status.setText(str(a))
                l += 1
            #for i in range(len(list(a))):
            #    self.battle_table.setLayout(str(a))

    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):

        reply = QMessageBox.question(self, 'Message', "Quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

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

    ex = Example()

    sys.exit(app.exec_())
