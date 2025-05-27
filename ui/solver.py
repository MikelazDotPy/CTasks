from PyQt6 import QtCore
from PyQt6 import QtGui
from PyQt6 import QtWidgets
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QWidget


class TasksSolverUI(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setupUi(self)
        self.pushButton_2.clicked.connect(self.show_help)
    
    def back_to_menu(self):
        if self.parent:
            self.parent.show()
        self.close()
    
    def show_help(self):
        md = """В ответе могут присутствовать:
    1. Числа
    2. Формулы: C(n,k) — сочетания, A(n,k) — размещения, F(n) — факториал
    3. Операторы: +, -, *, /, **
        оператор / означает целочисленное деление
        оператор ** означает возведение в степнь
 
Если задача противоречива, ответ 0."""     
        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setWindowTitle("Подсказка")
        msg_box.setText(md)
        msg_box.setStyleSheet("QLabel{font-size: 18px; ; min-width: 550px;}")
        msg_box.exec()

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1000, 600)
        self.mainLayout = QtWidgets.QVBoxLayout(Form)
        self.mainLayout.setObjectName("mainLayout")
        self.mainLayout.setContentsMargins(9, 9, 9, 9)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mainLayout.addLayout(self.horizontalLayout, 1)

        self.splitter = QtWidgets.QSplitter(parent=Form)
        self.splitter.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.splitter.setObjectName("splitter")
        self.verticalLayoutWidget = QtWidgets.QWidget(parent=self.splitter)
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(parent=self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tabWidget.setFont(font)
        self.tabWidget.setAccessibleDescription("")
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout_3.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.listWidget = QtWidgets.QListWidget(parent=self.tab)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_3.addWidget(self.listWidget)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tab_2)
        self.verticalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.listWidget_2 = QtWidgets.QListWidget(parent=self.tab_2)
        self.listWidget_2.setObjectName("listWidget_2")
        self.verticalLayout_2.addWidget(self.listWidget_2)
        self.tabWidget.addTab(self.tab_2, "")
        self.verticalLayout.addWidget(self.tabWidget)
        self.widget = QtWidgets.QWidget(parent=self.splitter)
        self.widget.setObjectName("widget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label = QtWidgets.QLabel(parent=self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_4.addWidget(self.label)
        self.textBrowser_2 = QtWidgets.QTextBrowser(parent=self.widget)
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.verticalLayout_4.addWidget(self.textBrowser_2)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lineEdit = QtWidgets.QLineEdit(parent=self.widget)
        font = QtGui.QFont()
        font.setPointSize(13)
        self.lineEdit.setFont(font)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout_3.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(parent=self.widget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_3.addWidget(self.pushButton)
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.widget)
        self.pushButton_2.setText("")
        icon = self.style().standardIcon(QtWidgets.QStyle.StandardPixmap.SP_MessageBoxQuestion)
        self.pushButton_2.setIcon(icon)
        self.pushButton_2.setIconSize(QtCore.QSize(28, 28))
        self.pushButton_2.setFlat(True)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_3.addWidget(self.pushButton_2)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.textBrowser = QtWidgets.QTextBrowser(parent=self.widget)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout_4.addWidget(self.textBrowser)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.textBrowser_2.setFont(font)
        self.verticalLayout_4.setStretch(1, 1)
        self.splitter.setStretchFactor(0, 0)  # Левый виджет (индекс 0)
        self.splitter.setStretchFactor(1, 2)  # Правый виджет (индекс 1)
        self.horizontalLayout.addWidget(self.splitter)

        self.menu_bar = QtWidgets.QMenuBar(Form)
        self.menu_bar.setNativeMenuBar(False)
        self.menu_bar.setObjectName("menu_bar")
        back_action = QAction("Назад", self)
        back_action.triggered.connect(self.back_to_menu)
        self.menu_bar.addAction(back_action)

        self.mainLayout.insertWidget(0, self.menu_bar)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Решение задач"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Form", "Сборники"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "Задачи"))
        self.label.setText(_translate("Form", "Условие задачи"))
        self.lineEdit.setPlaceholderText(_translate("Form", "Введите ответ"))
        self.pushButton.setText(_translate("Form", "Проверить"))
