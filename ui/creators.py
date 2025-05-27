import json
import os

from markdown import markdown
from PyQt6 import QtCore
from PyQt6 import QtGui
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt, QRect, QSize, QRegularExpression
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QWidget, QPlainTextEdit
from PyQt6.QtGui import QPainter, QColor, QFont, QTextCharFormat, QPalette, QSyntaxHighlighter

from ui import resource_path





class EditorUI(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.zn = ["=", "!=", ">", "<", ">=", "<="]
        self.tasks = []
        self.parent = parent
        self.setupUi(self)
        self.splitter.setSizes([0, 1])

    def del_list_el(self, value):
        item = self.listWidget.takeItem(self.listWidget.currentRow())
        item = None

    def back_to_menu(self):
        if self.parent:
            self.parent.show()
        self.close()
    
    def setupUi(self):
        self.listWidget = QtWidgets.QListWidget()
        self.listWidget_2 = QtWidgets.QListWidget()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete:
            selected_item = self.listWidget_2.currentItem()
            if selected_item:
                name = selected_item.text()
                selected_item = self.listWidget_2.takeItem(self.listWidget_2.currentRow())
                selected_item = None
                if os.path.exists(resource_path(os.path.join("tasks", name + ".json"))):
                    os.remove(resource_path(os.path.join("tasks", name + ".json")))
                self._load_tasks_name()

        super().keyPressEvent(event)

    def _load_tasks_name(self, type):
        self.tasks = []
        self.listWidget_2.clear()
        for filename in os.listdir(resource_path("tasks")):
            if filename.endswith(".json"):
                filepath = resource_path(os.path.join("tasks", filename))
                try:
                    with open(filepath, "r", encoding="utf-8") as file:
                        data = json.load(file)
                        if data["type"] == type:
                            self.tasks.append(data)
                except:
                    pass
        self.listWidget_2.addItems(task["name"] for task in self.tasks)
        self.listWidget_2.sortItems()

    def show_about2(self):
        md = """#### **1. Как решать сохранённые задачи**

1. Нажмите кнопку **"Назад"** в верхнем левом углу.  
2. Перейдите в режим “Решение задач”  
3. Выберете сборник и задачу.  
   

#### **2. Важные примечания**

* После сохранения задача сразу становится доступной в списке — **не требуется перезапуск программы**.  
* Условия можно комбинировать (например, "3 бубны + сумма очков ≥ 20").  
* Для удаления одиночного условия используйте **двойной клик** по нему.
"""     
        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setWindowTitle("Общие сведения")
        msg_box.setText(markdown(md))
        msg_box.setStyleSheet("QLabel{font-size: 18px; ; min-width: 550px;}")
        msg_box.exec()


class WordEditorUI(EditorUI):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1000, 600)

        self.mainLayout = QtWidgets.QVBoxLayout(Form)
        self.mainLayout.setObjectName("mainLayout")
        self.mainLayout.setContentsMargins(9, 9, 9, 9)

        # Add menu bar at the top

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mainLayout.addLayout(self.horizontalLayout, 1)

        # self.horizontalLayout = QtWidgets.QHBoxLayout()
        # self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_10 = QtWidgets.QLabel(parent=Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.verticalLayout.addWidget(self.label_10)
        self.listWidget_2 = QtWidgets.QListWidget(parent=Form)
        self.listWidget_2.setObjectName("listWidget_2")
        self.verticalLayout.addWidget(self.listWidget_2)
        self.pushButton_11 = QtWidgets.QPushButton(parent=Form)
        self.pushButton_11.setObjectName("pushButton_11")
        self.verticalLayout.addWidget(self.pushButton_11)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.splitter_2 = QtWidgets.QSplitter(parent=Form)
        self.splitter_2.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.layoutWidget = QtWidgets.QWidget(parent=self.splitter_2)
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_6 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_6.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 2, 0, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout_3.addWidget(self.pushButton_5, 7, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        self.gridLayout_3.addItem(spacerItem, 1, 0, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.comboBox_2 = QtWidgets.QComboBox(parent=self.layoutWidget)
        self.comboBox_2.setAcceptDrops(True)
        self.comboBox_2.setObjectName("comboBox_2")
        self.gridLayout_2.addWidget(self.comboBox_2, 0, 1, 1, 2)
        self.label_11 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_11.setObjectName("label_11")
        self.gridLayout_2.addWidget(self.label_11, 6, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 6, 0, 1, 1)
        self.pushButton = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 0, 4, 1, 1)
        self.comboBox_4 = QtWidgets.QComboBox(parent=self.layoutWidget)
        self.comboBox_4.setObjectName("comboBox_4")
        self.gridLayout_2.addWidget(self.comboBox_4, 3, 0, 1, 1)
        self.comboBox_5 = QtWidgets.QComboBox(parent=self.layoutWidget)
        self.comboBox_5.setObjectName("comboBox_5")
        self.gridLayout_2.addWidget(self.comboBox_5, 3, 1, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_2.addWidget(self.pushButton_2, 3, 4, 1, 1)
        self.label_2 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(parent=self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_3.setSizePolicy(sizePolicy)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout_2.addWidget(self.lineEdit_3, 3, 2, 1, 1)
        self.comboBox_6 = QtWidgets.QComboBox(parent=self.layoutWidget)
        self.comboBox_6.setObjectName("comboBox_6")
        self.gridLayout_2.addWidget(self.comboBox_6, 6, 1, 1, 1)
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_2.addWidget(self.pushButton_3, 6, 4, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 3, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_9.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 5, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label.setIndent(5)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 6, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 4)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        self.gridLayout.addItem(spacerItem1, 2, 1, 1, 1)
        self.lineEdit_7 = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.gridLayout.addWidget(self.lineEdit_7, 6, 3, 1, 1)
        self.checkBox = QtWidgets.QCheckBox(parent=self.layoutWidget)
        self.checkBox.setAcceptDrops(True)
        self.checkBox.setAutoFillBackground(False)
        self.checkBox.setStyleSheet("")
        self.checkBox.setChecked(False)
        self.checkBox.setObjectName("checkBox")
        self.gridLayout.addWidget(self.checkBox, 8, 0, 1, 2)
        self.label_3 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_3.setIndent(5)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 6, 2, 1, 1)
        self.lineEdit_4 = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.lineEdit_4.setText("")
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout.addWidget(self.lineEdit_4, 4, 0, 1, 2)
        self.label_5 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_5.setAcceptDrops(True)
        self.label_5.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 5, 0, 1, 4)
        self.lineEdit_6 = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.gridLayout.addWidget(self.lineEdit_6, 6, 1, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 7, 0, 1, 2)
        self.checkBox_2 = QtWidgets.QCheckBox(parent=self.layoutWidget)
        self.checkBox_2.setAcceptDrops(True)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout.addWidget(self.checkBox_2, 4, 2, 1, 2)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        self.gridLayout_3.addItem(spacerItem2, 4, 0, 1, 1)
        self.listWidget = QtWidgets.QListWidget(parent=self.layoutWidget)
        self.listWidget.setObjectName("listWidget")
        self.gridLayout_3.addWidget(self.listWidget, 6, 0, 1, 1)
        self.splitter = QtWidgets.QSplitter(parent=self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.splitter.setObjectName("splitter")
        self.layoutWidget1 = QtWidgets.QWidget(parent=self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_8 = QtWidgets.QLabel(parent=self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setText("")
        self.label_8.setObjectName("label_8")
        self.gridLayout_4.addWidget(self.label_8, 2, 0, 1, 3)
        self.pushButton_6 = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout_4.addWidget(self.pushButton_6, 3, 0, 1, 1)
        self.pushButton_7 = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout_4.addWidget(self.pushButton_7, 3, 1, 1, 1)
        self.pushButton_8 = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.pushButton_8.setObjectName("pushButton_8")
        self.gridLayout_4.addWidget(self.pushButton_8, 3, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(parent=self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setAcceptDrops(True)
        self.label_7.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout_4.addWidget(self.label_7, 0, 0, 1, 3)
        self.layoutWidget2 = QtWidgets.QWidget(parent=self.splitter)
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.layoutWidget2)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.textEdit = QtWidgets.QTextEdit(parent=self.layoutWidget2)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout_5.addWidget(self.textEdit, 0, 0, 1, 1)
        self.pushButton_9 = QtWidgets.QPushButton(parent=self.layoutWidget2)
        self.pushButton_9.setObjectName("pushButton_9")
        self.gridLayout_5.addWidget(self.pushButton_9, 1, 0, 1, 1)
        self.pushButton_10 = QtWidgets.QPushButton(parent=self.layoutWidget2)
        self.pushButton_10.setObjectName("pushButton_10")
        self.gridLayout_5.addWidget(self.pushButton_10, 2, 0, 1, 1)
        self.horizontalLayout.addWidget(self.splitter_2)

        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 6)
        self.menu_bar = QtWidgets.QMenuBar(Form)
        self.menu_bar.setNativeMenuBar(False)
        self.menu_bar.setObjectName("menu_bar")
        back_action = QAction("Назад", self)
        back_action.triggered.connect(self.back_to_menu)
        self.menu_bar.addAction(back_action)

        help_menu = self.menu_bar.addMenu("Справка")
        about_action = QAction("Работа с модулем", self)
        about_action.triggered.connect(self.show_about1)
        help_menu.addAction(about_action)
        about_action = QAction("Другое", self)
        about_action.triggered.connect(self.show_about2)
        help_menu.addAction(about_action)

        self.mainLayout.insertWidget(0, self.menu_bar)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def show_about1(self):
        md = """1\\. **Работа с модулем**:

* **Список существующих задач**  
    * Слева от конструктора задач располагается список уже созданных задач (в режиме редактирования можно по двойному клику перейти к любой из них и переделать/доделать при необходимости)  
* **Условия задачи**  
    * Поля для добавления условий (например, "слово является палиндромом", "гласных = 4").  
        * **Палиндром** — это слово, фраза, число или другая последовательность символов, которая читается **одинаково** как **слева направо**, так и **справа налево**.  
        * В строке “Алфавит” вы можете с клавиатуры ввести желаемый алфавит (например: абв или а, б, в, оба варианта дадут алфавит {А, Б, В})  
        * Галочка “Только уникальные буквы” превратит набор {МАТЕМАТИКА} в {МАТЕИК}, то есть уберет все повторяющиеся буквы.  
        * При выборе алфавита с повторяющимися буквами, подсчет слов будет с учетом того, что все буквы разные. То есть слова МАТЕМАтИКА и МАтЕМАТИКА будут считаться разными.  
    * Удаление условия: двойной клик по нему.  
* **Условие задачи**   
    * Генерируется при нажатии на “Сгенерировать условие”.
    """
        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setWindowTitle("Работа с модулем")
        msg_box.setText(markdown(md))
        msg_box.setStyleSheet("QLabel{font-size: 18px; ; min-width: 550px;}")
        msg_box.exec()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Редактор: Слова"))
        self.label_10.setText(_translate("Form", "Существующие задачи"))
        self.pushButton_11.setText(_translate("Form", "Новая задача"))
        self.label_6.setText(_translate("Form", "Условия задачи"))
        self.pushButton_5.setText(_translate("Form", "Удалить все условия"))
        self.label_11.setText(_translate("Form", "Согласных"))
        self.label_4.setText(_translate("Form", "Гласных"))
        self.pushButton.setText(_translate("Form", "+"))
        self.pushButton_2.setText(_translate("Form", "+"))
        self.label_2.setText(_translate("Form", "Ограничения"))
        self.pushButton_3.setText(_translate("Form", "+"))
        self.label_9.setText(_translate("Form", "Список условий (удаление условия по двойному клику)"))
        self.label.setText(_translate("Form", "Гласных"))
        self.lineEdit.setPlaceholderText(_translate("Form", "Название задачи"))
        self.checkBox.setText(_translate("Form", "Буквы могут повторяться"))
        self.label_3.setText(_translate("Form", "Согласных"))
        self.lineEdit_4.setPlaceholderText(_translate("Form", "Алфавит"))
        self.label_5.setText(_translate("Form", "Или Укажитете количество гласных и согласных в алфавите"))
        self.lineEdit_2.setPlaceholderText(_translate("Form", "Длина слова"))
        self.checkBox_2.setText(_translate("Form", "Только уникальные буквы"))
        self.pushButton_6.setText(_translate("Form", "Очистить"))
        self.pushButton_7.setText(_translate("Form", "Загрузить"))
        self.pushButton_8.setText(_translate("Form", "Сгенерировать"))
        self.label_7.setText(_translate("Form", "Картинка к задаче"))
        self.textEdit.setPlaceholderText(_translate("Form", "Условие задачи"))
        self.pushButton_9.setText(_translate("Form", "Сгенерировать условие"))
        self.pushButton_10.setText(_translate("Form", "Сохранить задачу в задачник"))


class CardDeckEditorUI(EditorUI):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1000, 600)

        self.mainLayout = QtWidgets.QVBoxLayout(Form)
        self.mainLayout.setObjectName("mainLayout")
        self.mainLayout.setContentsMargins(9, 9, 9, 9)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mainLayout.addLayout(self.horizontalLayout, 1)

        self.splitter_2 = QtWidgets.QSplitter(parent=Form)
        self.splitter_2.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.layoutWidget = QtWidgets.QWidget(parent=self.splitter_2)
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")


        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_10 = QtWidgets.QLabel(parent=Form)
        self.label_10.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.verticalLayout.addWidget(self.label_10)
        self.listWidget_2 = QtWidgets.QListWidget(parent=Form)
        self.listWidget_2.setObjectName("listWidget_2")
        self.verticalLayout.addWidget(self.listWidget_2)
        self.pushButton_11 = QtWidgets.QPushButton(parent=Form)
        self.pushButton_11.setObjectName("pushButton_11")
        self.verticalLayout.addWidget(self.pushButton_11)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.splitter_2 = QtWidgets.QSplitter(parent=Form)
        self.splitter_2.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.layoutWidget = QtWidgets.QWidget(parent=self.splitter_2)
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_9 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_9.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 5, 0, 1, 1)
        self.listWidget = QtWidgets.QListWidget(parent=self.layoutWidget)
        self.listWidget.setObjectName("listWidget")
        self.gridLayout_3.addWidget(self.listWidget, 6, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_6.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 2, 0, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_2 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.comboBox_2 = QtWidgets.QComboBox(parent=self.layoutWidget)
        self.comboBox_2.setObjectName("comboBox_2")
        self.gridLayout_2.addWidget(self.comboBox_2, 0, 1, 1, 1)
        self.comboBox_3 = QtWidgets.QComboBox(parent=self.layoutWidget)
        self.comboBox_3.setObjectName("comboBox_3")
        self.gridLayout_2.addWidget(self.comboBox_3, 0, 2, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout_2.addWidget(self.lineEdit_3, 0, 3, 1, 1)
        self.pushButton = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 0, 4, 1, 1)
        self.label_3 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.comboBox_4 = QtWidgets.QComboBox(parent=self.layoutWidget)
        self.comboBox_4.setObjectName("comboBox_4")
        self.gridLayout_2.addWidget(self.comboBox_4, 1, 1, 1, 1)
        self.comboBox_5 = QtWidgets.QComboBox(parent=self.layoutWidget)
        self.comboBox_5.setObjectName("comboBox_5")
        self.gridLayout_2.addWidget(self.comboBox_5, 1, 2, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_2.addWidget(self.pushButton_2, 1, 4, 1, 1)
        self.label_4 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 2, 0, 1, 1)
        self.comboBox_6 = QtWidgets.QComboBox(parent=self.layoutWidget)
        self.comboBox_6.setObjectName("comboBox_6")
        self.gridLayout_2.addWidget(self.comboBox_6, 2, 1, 1, 1)
        self.lineEdit_4 = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.gridLayout_2.addWidget(self.lineEdit_4, 2, 2, 1, 2)
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.gridLayout_2.addWidget(self.pushButton_3, 2, 4, 1, 1)
        self.label_5 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 3, 0, 1, 1)
        self.comboBox_7 = QtWidgets.QComboBox(parent=self.layoutWidget)
        self.comboBox_7.setObjectName("comboBox_7")
        self.gridLayout_2.addWidget(self.comboBox_7, 3, 1, 1, 1)
        self.comboBox_8 = QtWidgets.QComboBox(parent=self.layoutWidget)
        self.comboBox_8.setObjectName("comboBox_8")
        self.gridLayout_2.addWidget(self.comboBox_8, 3, 2, 1, 1)
        self.pushButton_4 = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.gridLayout_2.addWidget(self.pushButton_4, 3, 4, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 3, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        self.gridLayout_3.addItem(spacerItem, 1, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        self.gridLayout.addItem(spacerItem1, 2, 0, 1, 1)
        self.comboBox = QtWidgets.QComboBox(parent=self.layoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.gridLayout.addWidget(self.comboBox, 3, 1, 1, 1)
        self.label = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 2)
        self.lineEdit_2 = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 4, 0, 1, 2)
        self.gridLayout_3.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout_3.addWidget(self.pushButton_5, 7, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        self.gridLayout_3.addItem(spacerItem2, 4, 0, 1, 1)
        self.splitter = QtWidgets.QSplitter(parent=self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.splitter.setObjectName("splitter")
        self.layoutWidget1 = QtWidgets.QWidget(parent=self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_8 = QtWidgets.QLabel(parent=self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setText("")
        self.label_8.setObjectName("label_8")
        self.gridLayout_4.addWidget(self.label_8, 2, 0, 1, 3)
        self.pushButton_6 = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout_4.addWidget(self.pushButton_6, 3, 0, 1, 1)
        self.pushButton_7 = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout_4.addWidget(self.pushButton_7, 3, 1, 1, 1)
        self.pushButton_8 = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.pushButton_8.setObjectName("pushButton_8")
        self.gridLayout_4.addWidget(self.pushButton_8, 3, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(parent=self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout_4.addWidget(self.label_7, 0, 1, 1, 1)
        self.layoutWidget2 = QtWidgets.QWidget(parent=self.splitter)
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.layoutWidget2)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.textEdit = QtWidgets.QTextEdit(parent=self.layoutWidget2)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout_5.addWidget(self.textEdit, 0, 0, 1, 1)
        self.pushButton_9 = QtWidgets.QPushButton(parent=self.layoutWidget2)
        self.pushButton_9.setObjectName("pushButton_9")
        self.gridLayout_5.addWidget(self.pushButton_9, 1, 0, 1, 1)
        self.pushButton_10 = QtWidgets.QPushButton(parent=self.layoutWidget2)
        self.pushButton_10.setObjectName("pushButton_10")
        self.gridLayout_5.addWidget(self.pushButton_10, 2, 0, 1, 1)
        self.horizontalLayout.addWidget(self.splitter_2)  
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 6) 
        

        self.menu_bar = QtWidgets.QMenuBar(Form)
        self.menu_bar.setNativeMenuBar(False)
        self.menu_bar.setObjectName("menu_bar")
        back_action = QAction("Назад", self)
        back_action.triggered.connect(self.back_to_menu)
        self.menu_bar.addAction(back_action)

        help_menu = self.menu_bar.addMenu("Справка")
        about_action = QAction("Работа с модулем", self)
        about_action.triggered.connect(self.show_about1)
        help_menu.addAction(about_action)
        about_action = QAction("Другое", self)
        about_action.triggered.connect(self.show_about2)
        help_menu.addAction(about_action)

        self.mainLayout.insertWidget(0, self.menu_bar)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def show_about1(self):
        md = """1\\. **Работа с модулем**:

 * **Список существующих задач**  
     * Слева от конструктора задач располагается список уже созданных задач (в режиме редактирования можно по двойному клику перейти к любой из них и переделать/доделать при необходимости)  
 * **Условия задачи**  
     * Поля для добавления условий (например, "количество карт бубнов", "наличие шестерки", "сумма очков").  
     * Каждой карте соответствует свой номинал: число на карте для карт от 2 до 10 и 11, 12, 13, 14 для валетов, дам, королей и тузов, соответственно.  
     * В условии все карты >/</≤/≥/=/!=(≠) подразумевается сравнение с номиналом этой карты.   
     * Удаление условия: двойной клик по нему.  
 * **Условие задачи**
     * Генерируется при нажатии на “Сгенерировать условие”."""
        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setWindowTitle("Работа с модулем")
        msg_box.setText(markdown(md))
        msg_box.setStyleSheet("QLabel{font-size: 18px; ; min-width: 550px;}")
        msg_box.exec()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Редактор: Колода карт"))
        self.label_10.setText(_translate("Form", "Существующие задачи"))
        self.pushButton_11.setText(_translate("Form", "Новая задача"))
        self.label_9.setText(_translate("Form", "Список условий (удаление условия по двоному клику)"))
        self.label_6.setText(_translate("Form", "Условия задачи"))
        self.label_2.setText(_translate("Form", "Количество"))
        self.pushButton.setText(_translate("Form", "+"))
        self.label_3.setText(_translate("Form", "В наборе содрежится"))
        self.pushButton_2.setText(_translate("Form", "+"))
        self.label_4.setText(_translate("Form", "Сумма очков"))
        self.pushButton_3.setText(_translate("Form", "+"))
        self.label_5.setText(_translate("Form", "Все карты"))
        self.pushButton_4.setText(_translate("Form", "+"))
        self.comboBox.setItemText(0, _translate("Form", "36"))
        self.comboBox.setItemText(1, _translate("Form", "52"))
        self.label.setText(_translate("Form", "Размер колоды"))
        self.lineEdit.setPlaceholderText(_translate("Form", "Название задачи"))
        self.lineEdit_2.setPlaceholderText(_translate("Form", "Размер набора"))
        self.pushButton_5.setText(_translate("Form", "Удалить все условия"))
        self.pushButton_6.setText(_translate("Form", "Очистить"))
        self.pushButton_7.setText(_translate("Form", "Загрузить"))
        self.pushButton_8.setText(_translate("Form", "Сгенерировать"))
        self.label_7.setText(_translate("Form", "Картинка к задаче"))
        self.textEdit.setPlaceholderText(_translate("Form", "Условие задачи"))
        self.pushButton_9.setText(_translate("Form", "Сгенерировать условие"))
        self.pushButton_10.setText(_translate("Form", "Сохранить задачу в задачник"))


class NumberEditorUI(EditorUI):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1000, 600)

        self.mainLayout = QtWidgets.QVBoxLayout(Form)
        self.mainLayout.setObjectName("mainLayout")
        self.mainLayout.setContentsMargins(9, 9, 9, 9)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mainLayout.addLayout(self.horizontalLayout, 1)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_10 = QtWidgets.QLabel(parent=Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.verticalLayout.addWidget(self.label_10)
        self.listWidget_2 = QtWidgets.QListWidget(parent=Form)
        self.listWidget_2.setObjectName("listWidget_2")
        self.verticalLayout.addWidget(self.listWidget_2)
        self.pushButton_11 = QtWidgets.QPushButton(parent=Form)
        self.pushButton_11.setObjectName("pushButton_11")
        self.verticalLayout.addWidget(self.pushButton_11)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.splitter_2 = QtWidgets.QSplitter(parent=Form)
        self.splitter_2.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.layoutWidget = QtWidgets.QWidget(parent=self.splitter_2)
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.lineEdit_5 = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.lineEdit_5.setInputMask("")
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.horizontalLayout_3.addWidget(self.lineEdit_5)
        self.lineEdit_7 = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.horizontalLayout_3.addWidget(self.lineEdit_7)
        self.comboBox_7 = QtWidgets.QComboBox(parent=self.layoutWidget)
        self.comboBox_7.setObjectName("comboBox_7")
        self.horizontalLayout_3.addWidget(self.comboBox_7)
        self.lineEdit_4 = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.horizontalLayout_3.addWidget(self.lineEdit_4)
        self.pushButton_3 = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.pushButton_3.setObjectName("pushButton_3")
        self.horizontalLayout_3.addWidget(self.pushButton_3)
        self.gridLayout_3.addLayout(self.horizontalLayout_3, 6, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_9.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 8, 0, 1, 1)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.comboBox_2 = QtWidgets.QComboBox(parent=self.layoutWidget)
        self.comboBox_2.setAcceptDrops(True)
        self.comboBox_2.setObjectName("comboBox_2")
        self.gridLayout_2.addWidget(self.comboBox_2, 0, 1, 1, 2)
        self.label_2 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 0, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.gridLayout_2.addWidget(self.pushButton_2, 3, 4, 1, 1)
        self.comboBox_5 = QtWidgets.QComboBox(parent=self.layoutWidget)
        self.comboBox_5.setObjectName("comboBox_5")
        self.gridLayout_2.addWidget(self.comboBox_5, 3, 1, 1, 1)
        self.pushButton = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.pushButton.setObjectName("pushButton")
        self.gridLayout_2.addWidget(self.pushButton, 0, 4, 1, 1)
        self.lineEdit_6 = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.gridLayout_2.addWidget(self.lineEdit_6, 3, 0, 1, 1)
        self.lineEdit_3 = QtWidgets.QLineEdit(parent=self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_3.setSizePolicy(sizePolicy)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.gridLayout_2.addWidget(self.lineEdit_3, 3, 2, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_2, 4, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 30, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        self.gridLayout_3.addItem(spacerItem, 2, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_6.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout_3.addWidget(self.label_6, 3, 0, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout_3.addWidget(self.pushButton_5, 10, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        self.gridLayout_3.addItem(spacerItem1, 7, 0, 1, 1)
        self.listWidget = QtWidgets.QListWidget(parent=self.layoutWidget)
        self.listWidget.setObjectName("listWidget")
        self.gridLayout_3.addWidget(self.listWidget, 9, 0, 1, 1)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.checkBox_2 = QtWidgets.QCheckBox(parent=self.layoutWidget)
        self.checkBox_2.setAcceptDrops(True)
        self.checkBox_2.setObjectName("checkBox_2")
        self.gridLayout.addWidget(self.checkBox_2, 5, 1, 1, 3)
        self.label_12 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 3, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(parent=self.layoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Policy.Minimum, QtWidgets.QSizePolicy.Policy.Preferred)
        self.gridLayout.addItem(spacerItem2, 2, 1, 1, 1)
        self.lineEdit_2 = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.gridLayout.addWidget(self.lineEdit_2, 5, 0, 1, 1)
        self.lineEdit = QtWidgets.QLineEdit(parent=self.layoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.gridLayout.addWidget(self.lineEdit, 0, 0, 1, 4)
        self.comboBox = QtWidgets.QComboBox(parent=self.layoutWidget)
        self.comboBox.setObjectName("comboBox")
        self.gridLayout.addWidget(self.comboBox, 3, 1, 1, 1)
        self.comboBox_3 = QtWidgets.QComboBox(parent=self.layoutWidget)
        self.comboBox_3.setObjectName("comboBox_3")
        self.gridLayout.addWidget(self.comboBox_3, 3, 3, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout, 1, 0, 1, 1)
        self.label = QtWidgets.QLabel(parent=self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 5, 0, 1, 1)
        self.splitter = QtWidgets.QSplitter(parent=self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.splitter.setObjectName("splitter")
        self.layoutWidget1 = QtWidgets.QWidget(parent=self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.layoutWidget1)
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_8 = QtWidgets.QLabel(parent=self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setText("")
        self.label_8.setObjectName("label_8")
        self.gridLayout_4.addWidget(self.label_8, 2, 0, 1, 3)
        self.pushButton_6 = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout_4.addWidget(self.pushButton_6, 3, 0, 1, 1)
        self.pushButton_7 = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout_4.addWidget(self.pushButton_7, 3, 1, 1, 1)
        self.pushButton_8 = QtWidgets.QPushButton(parent=self.layoutWidget1)
        self.pushButton_8.setObjectName("pushButton_8")
        self.gridLayout_4.addWidget(self.pushButton_8, 3, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(parent=self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Preferred, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_7.sizePolicy().hasHeightForWidth())
        self.label_7.setSizePolicy(sizePolicy)
        self.label_7.setAcceptDrops(True)
        self.label_7.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout_4.addWidget(self.label_7, 0, 0, 1, 3)
        self.layoutWidget2 = QtWidgets.QWidget(parent=self.splitter)
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.layoutWidget2)
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.textEdit = QtWidgets.QTextEdit(parent=self.layoutWidget2)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout_5.addWidget(self.textEdit, 0, 0, 1, 1)
        self.pushButton_9 = QtWidgets.QPushButton(parent=self.layoutWidget2)
        self.pushButton_9.setObjectName("pushButton_9")
        self.gridLayout_5.addWidget(self.pushButton_9, 1, 0, 1, 1)
        self.pushButton_10 = QtWidgets.QPushButton(parent=self.layoutWidget2)
        self.pushButton_10.setObjectName("pushButton_10")
        self.gridLayout_5.addWidget(self.pushButton_10, 2, 0, 1, 1)
        self.horizontalLayout.addWidget(self.splitter_2)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 6)

        self.menu_bar = QtWidgets.QMenuBar(Form)
        self.menu_bar.setNativeMenuBar(False)
        self.menu_bar.setObjectName("menu_bar")
        back_action = QAction("Назад", self)
        back_action.triggered.connect(self.back_to_menu)
        self.menu_bar.addAction(back_action)

        help_menu = self.menu_bar.addMenu("Справка")
        about_action = QAction("Работа с модулем", self)
        about_action.triggered.connect(self.show_about1)
        help_menu.addAction(about_action)
        about_action = QAction("Другое", self)
        about_action.triggered.connect(self.show_about2)
        help_menu.addAction(about_action)

        self.mainLayout.insertWidget(0, self.menu_bar)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def show_about1(self):
        md = """**1. Работа с модулем**:

 * **Список существующих задач**  
     * Слева от конструктора задач располагается список уже созданных задач (в режиме редактирования можно по двойному клику перейти к любой из них и переделать/доделать при необходимости)  
 * **Условия задачи**  
     * Поля для добавления условий (например, "набор состоит из различных цифр", "[0] > 5" - это будет значить, что цифра под нулевым индексом, то есть первая по счету, должна быть больше 5).  
     * Вторая строчка в разделе “Условия задачи” позволяет выбрать комбинацию разрядов и чисел (в данном тренажере они начинаются с 0) и сравнить ее с другой комбинацией разрядов и чисел (например: [0] + [1] > [2] + 11).  
     * Третья строчка в разделе “Условия задачи” позволяет выбрать срез числа и наложить на него определенные ограничения (например: от [0] до [2] > 100, значит, что срез, состоящий из первых трех цифр, должен быть больше, чем 100).  
     * Удаление условия: двойной клик по нему.  
 * **Условие задачи**   
     * Генерируется при нажатии на “Сгенерировать условие”.
"""     
        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setWindowTitle("Работа с модулем")
        msg_box.setText(markdown(md))
        msg_box.setStyleSheet("QLabel{font-size: 18px; ; min-width: 550px;}")
        msg_box.exec()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Редактор: Наборы цифр"))
        self.label_10.setText(_translate("Form", "Существующие задачи"))
        self.pushButton_11.setText(_translate("Form", "Новая задача"))
        self.lineEdit_5.setPlaceholderText(_translate("Form", "от"))
        self.lineEdit_7.setPlaceholderText(_translate("Form", "до"))
        self.pushButton_3.setText(_translate("Form", "+"))
        self.label_9.setText(_translate("Form", "Список условий (удаление условия по двойному клику)"))
        self.label_2.setText(_translate("Form", "Ограничения"))
        self.pushButton_2.setText(_translate("Form", "+"))
        self.pushButton.setText(_translate("Form", "+"))
        self.label_6.setText(_translate("Form", "Условия задачи"))
        self.pushButton_5.setText(_translate("Form", "Удалить все условия"))
        self.checkBox_2.setText(_translate("Form", "Первая цифра в наборе не 0"))
        self.label_12.setText(_translate("Form", "до"))
        self.label_5.setText(_translate("Form", "Цифры в наборе от"))
        self.lineEdit_2.setPlaceholderText(_translate("Form", "Размер набора"))
        self.lineEdit.setPlaceholderText(_translate("Form", "Название задачи"))
        self.label.setText(_translate("Form", "Срез числа от индекса до индекса"))
        self.pushButton_6.setText(_translate("Form", "Очистить"))
        self.pushButton_7.setText(_translate("Form", "Загрузить"))
        self.pushButton_8.setText(_translate("Form", "Сгенерировать"))
        self.label_7.setText(_translate("Form", "Картинка к задаче"))
        self.textEdit.setPlaceholderText(_translate("Form", "Условие задачи"))
        self.pushButton_9.setText(_translate("Form", "Сгенерировать условие"))
        self.pushButton_10.setText(_translate("Form", "Сохранить задачу в задачник"))


start_text = """# Доступен весь синтаксис пайтон и 
# стандартной библиотеки

# Функция решатель задачи, принимает аргументы
# на усмотрения создателя прототипа.
# Должна возвращать число
def main():
	return 0

# Функция генерации условия задачи,
# принимает такие же аргументы, как и main()
# Если генерация не предусмотрена, то
# возвращать пустую строку
def get_task():
	return ''"""


class ThemeAwareHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_dark = False
        self.setup_formats()
        
    def setup_formats(self):
        # Цвета для темной темы
        if self.is_dark:
            self.formats = {
                'keyword': self.create_format(QColor(86, 156, 214), bold=True),  # Синий
                'function': self.create_format(QColor(220, 220, 120)),          # Светло-желтый
                'string': self.create_format(QColor(214, 157, 133)),           # Оранжевый
                'comment': self.create_format(QColor(87, 166, 74)),             # Зеленый
                'number': self.create_format(QColor(181, 206, 168)),            # Светло-зеленый
                'builtin': self.create_format(QColor(240, 200, 118)),           # Мятный
                'type': self.create_format(QColor(78, 201, 176))                # Бирюзовый
            }
        # Цвета для светлой темы
        else:
            self.formats = {
                'keyword': self.create_format(QColor(0, 0, 200)),                # Темно-синий
                'function': self.create_format(QColor(130, 130, 255)),            # Темно-желтый
                'string': self.create_format(QColor(163, 21, 21)),             # Красный
                'comment': self.create_format(QColor(0, 128, 0)),              # Зеленый
                'number': self.create_format(QColor(128, 0, 128)),             # Фиолетовый
                'builtin': self.create_format(QColor(0, 112, 112)),            # Темный циан
                'type': self.create_format(QColor(0, 0, 139))                  # Темно-синий
            }
        
        # Правила подсветки
        self.rules = [
            # Ключевые слова
            (r'\b(and|as|assert|break|class|continue|def|del|elif|else|except|'
             r'False|finally|for|from|global|if|import|in|is|lambda|None|'
             r'nonlocal|not|or|pass|raise|return|True|try|while|with|yield)\b', 
             'keyword'),
            
            # Встроенные функции
            (r'\b(abs|all|any|ascii|bin|bool|breakpoint|bytearray|bytes|callable|'
             r'chr|classmethod|compile|complex|delattr|dict|dir|divmod|enumerate|'
             r'eval|exec|filter|float|format|frozenset|getattr|globals|hasattr|'
             r'hash|help|hex|id|input|int|isinstance|issubclass|iter|len|list|'
             r'locals|map|max|memoryview|min|next|object|oct|open|ord|pow|print|'
             r'property|range|repr|reversed|round|set|setattr|slice|sorted|'
             r'staticmethod|str|sum|super|tuple|type|vars|zip)\b', 'builtin'),
            
            # Встроенные методы (например, str.join)
            (r'\.(append|clear|copy|count|extend|index|insert|pop|remove|reverse|'
             r'sort|capitalize|casefold|center|encode|endswith|expandtabs|find|'
             r'format|format_map|isalnum|isalpha|isascii|isdecimal|isdigit|'
             r'isidentifier|islower|isnumeric|isprintable|isspace|istitle|'
             r'isupper|join|ljust|lower|lstrip|maketrans|partition|replace|'
             r'rfind|rindex|rjust|rpartition|rsplit|rstrip|split|splitlines|'
             r'startswith|strip|swapcase|title|translate|upper|zfill)\b', 'function'),
            
            # Типы
            (r'\b(int|float|str|bool|list|tuple|dict|set|frozenset|complex|bytes|'
             r'bytearray|memoryview|range|slice|type|object|NoneType)\b', 'type'),
            
            # Строки
            (r'"[^"\\]*(\\.[^"\\]*)*"', 'string'),
            (r"'[^'\\]*(\\.[^'\\]*)*'", 'string'),
            
            # Комментарии
            (r'#[^\n]*', 'comment'),
            
            # Числа
            (r'\b[0-9]+\b', 'number'),
            (r'\b[0-9]*\.[0-9]+\b', 'number'),
            (r'\b0[xX][0-9a-fA-F]+\b', 'number')
        ]
    
    def create_format(self, color, bold=False):
        fmt = QTextCharFormat()
        fmt.setForeground(color)
        if bold:
            fmt.setFontWeight(QFont.Weight.Bold)
        return fmt
    
    def highlightBlock(self, text):
        for pattern, fmt_name in self.rules:
            regex = QRegularExpression(pattern)
            iterator = regex.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                self.setFormat(
                    match.capturedStart(), 
                    match.capturedLength(), 
                    self.formats[fmt_name]
                )
        
        self.setCurrentBlockState(0)


class LineNumberArea(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.editor.lineNumberAreaPaintEvent(event)


class PyTextEditor(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineNumberArea = LineNumberArea(self)
        self.currentLineNumber = -1
        
        # Настройки редактора
        self.setFont(QFont("Consolas", 12))
        self.setTabStopDistance(self.fontMetrics().horizontalAdvance(' ') * 4)
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        
        # Подключение сигналов
        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.updateLineNumberAreaWidth(0)
        
        # Инициализация подсветки
        self.highlighter = ThemeAwareHighlighter(self.document())
        self.apply_theme()
    
    def apply_theme(self):
        # Новый способ определения темной темы
        bg_color = self.palette().color(QPalette.ColorRole.Window)
        text_color = self.palette().color(QPalette.ColorRole.WindowText)
        
        # Определяем темную тему по яркости цветов
        self.highlighter.is_dark = (bg_color.lightness() < 128 or 
                                   text_color.lightness() > bg_color.lightness())
        
        # Устанавливаем цвета редактора
        palette = self.palette()
        if self.highlighter.is_dark:
            palette.setColor(QPalette.ColorRole.Base, QColor(45, 45, 45))
            palette.setColor(QPalette.ColorRole.Text, QColor(220, 220, 220))
        else:
            palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
        
        self.setPalette(palette)
        
        # Обновляем подсветку
        self.highlighter.setup_formats()
        self.highlighter.rehighlight()
        
        # Обновляем нумерацию строк
        self.lineNumberArea.update()

    def lineNumberAreaWidth(self):
        digits = len(str(max(1, self.blockCount())))
        return 10 + self.fontMetrics().horizontalAdvance('9') * digits

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):
        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QRect(cr.left(), cr.top(), 
                                      self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):
        painter = QPainter(self.lineNumberArea)
        
        # Фон области номеров
        if self.highlighter.is_dark:
            bg_color = QColor(30, 30, 30)
            text_color = QColor(180, 180, 180)
        else:
            bg_color = QColor(240, 240, 240)
            text_color = QColor(100, 100, 100)
        
        painter.fillRect(event.rect(), bg_color)
        painter.setPen(text_color)

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.drawText(0, int(top), self.lineNumberArea.width() - 5,
                               self.fontMetrics().height(),
                               Qt.AlignmentFlag.AlignRight, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1


class PyTextReader(QtWidgets.QTextBrowser):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFont(QFont("Consolas", 12))
        self.setTabStopDistance(self.fontMetrics().horizontalAdvance(' ') * 4)
        
        self.highlighter = ThemeAwareHighlighter(self.document())
        self.apply_theme()
    
    def apply_theme(self):
        # Новый способ определения темной темы
        bg_color = self.palette().color(QPalette.ColorRole.Window)
        text_color = self.palette().color(QPalette.ColorRole.WindowText)
        
        # Определяем темную тему по яркости цветов
        self.highlighter.is_dark = (bg_color.lightness() < 128 or 
                                   text_color.lightness() > bg_color.lightness())
        
        # Устанавливаем цвета редактора
        palette = self.palette()
        if self.highlighter.is_dark:
            palette.setColor(QPalette.ColorRole.Base, QColor(45, 45, 45))
            palette.setColor(QPalette.ColorRole.Text, QColor(220, 220, 220))
        else:
            palette.setColor(QPalette.ColorRole.Base, QColor(255, 255, 255))
            palette.setColor(QPalette.ColorRole.Text, QColor(0, 0, 0))
        
        self.setPalette(palette)
        
        # Обновляем подсветку
        self.highlighter.setup_formats()
        self.highlighter.rehighlight()    


class PrototypeCreatorUI(EditorUI):
    def __init__(self, parent):
        super().__init__(parent)
        self.start_text = start_text
        self.plainTextEdit.setPlainText(start_text)

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1034, 612)
        self.mainLayout = QtWidgets.QVBoxLayout(Form)
        self.mainLayout.setObjectName("mainLayout")
        self.mainLayout.setContentsMargins(9, 9, 9, 9)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mainLayout.addLayout(self.horizontalLayout, 1)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_10 = QtWidgets.QLabel(parent=Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_10.setFont(font)
        self.label_10.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.verticalLayout.addWidget(self.label_10)
        self.listWidget_2 = QtWidgets.QListWidget(parent=Form)
        self.listWidget_2.setObjectName("listWidget_2")
        self.verticalLayout.addWidget(self.listWidget_2)
        self.pushButton_11 = QtWidgets.QPushButton(parent=Form)
        self.pushButton_11.setObjectName("pushButton_11")
        self.verticalLayout.addWidget(self.pushButton_11)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(parent=Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.plainTextEdit = PyTextEditor(parent=Form)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout_2.addWidget(self.plainTextEdit)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.splitter_2 = QtWidgets.QSplitter(parent=Form)
        self.splitter_2.setEnabled(True)
        self.splitter_2.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtWidgets.QSplitter(parent=self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(parent=self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lineEdit = QtWidgets.QLineEdit(parent=self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit.setFont(font)
        self.lineEdit.setAutoFillBackground(False)
        self.lineEdit.setText("")
        self.lineEdit.setClearButtonEnabled(False)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_3.addWidget(self.lineEdit)
        self.textEdit = QtWidgets.QTextEdit(parent=self.layoutWidget)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_3.addWidget(self.textEdit)
        self.pushButton_10 = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.pushButton_10.setObjectName("pushButton_10")
        self.verticalLayout_3.addWidget(self.pushButton_10)
        self.horizontalLayout.addWidget(self.splitter_2)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 2)
        self.horizontalLayout.setStretch(2, 1)

        self.menu_bar = QtWidgets.QMenuBar(Form)
        self.menu_bar.setNativeMenuBar(False)
        self.menu_bar.setObjectName("menu_bar")
        back_action = QAction("Назад", self)
        back_action.triggered.connect(self.back_to_menu)
        self.menu_bar.addAction(back_action)

        help_menu = self.menu_bar.addMenu("Справка")
        about_action = QAction("Работа с модулем", self)
        about_action.triggered.connect(self.show_about1)
        help_menu.addAction(about_action)
        about_action = QAction("Другое", self)
        about_action.triggered.connect(self.show_about2)
        help_menu.addAction(about_action)

        self.mainLayout.insertWidget(0, self.menu_bar)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def show_about1(self):
        md = """**Работа с модулем**:

 * **Создание нового прототипа:**
     * Нажмите кнопку "Новый прототип"
     * Реализуйте логику задачи через main
     * Реализуйте логику генерации текста задачи через get_task (эта функция должна принимать такие же аргументы как и main)
     * Пожеланию напишите описание прототипа
     * Введите название прототипа
     * Нажмите "Сохранить прототип"
 * **Редактирование существующего прототипа:**:
     * Двойным кликом выберите нужны прототип
     * Внесите необходимые изменения
     * Если вы хотите оставить старый прототип, но сделать свой на основе существующего, то измените название прототипа, старый останется, а ваш появится под новым названием
     * Нажмите кнопку "Сохранить прототип"
    """     
        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setWindowTitle("Работа с модулем")
        msg_box.setText(markdown(md))
        msg_box.setStyleSheet("QLabel{font-size: 18px; ; min-width: 550px;}")
        msg_box.exec()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Редактор прототипов задач"))
        self.label_10.setText(_translate("Form", "Существующие прототипы"))
        self.pushButton_11.setText(_translate("Form", "Новый прототип"))
        self.label.setText(_translate("Form", "Редактор кода"))
        self.lineEdit.setPlaceholderText(_translate("Form", "Название прототипа"))
        self.textEdit.setPlaceholderText(_translate("Form", "Описание прототипа"))
        self.pushButton_10.setText(_translate("Form", "Сохранить прототип"))


class PrototypeTaskCreatorUI(EditorUI):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1342, 725)
        self.mainLayout = QtWidgets.QVBoxLayout(Form)
        self.mainLayout.setObjectName("mainLayout")
        self.mainLayout.setContentsMargins(9, 9, 9, 9)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mainLayout.addLayout(self.horizontalLayout, 1)

        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalTabWidget = QtWidgets.QTabWidget(parent=Form)
        self.verticalTabWidget.setObjectName("verticalTabWidget")
        self.verticalTabWidgetPage1 = QtWidgets.QWidget()
        self.verticalTabWidgetPage1.setObjectName("verticalTabWidgetPage1")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.verticalTabWidgetPage1)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(1, 1, 1, 1)
        self.listWidget = QtWidgets.QListWidget(parent=self.verticalTabWidgetPage1)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_4.addWidget(self.listWidget)
        self.verticalTabWidget.addTab(self.verticalTabWidgetPage1, "")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab)
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout.setObjectName("verticalLayout")
        self.listWidget_2 = QtWidgets.QListWidget(parent=self.tab)
        self.listWidget_2.setObjectName("listWidget_2")
        self.verticalLayout.addWidget(self.listWidget_2)
        self.verticalTabWidget.addTab(self.tab, "")
        self.verticalLayout_5.addWidget(self.verticalTabWidget)
        self.pushButton = QtWidgets.QPushButton(parent=Form)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout_5.addWidget(self.pushButton)
        self.horizontalLayout.addLayout(self.verticalLayout_5)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSizeConstraint(QtWidgets.QLayout.SizeConstraint.SetDefaultConstraint)
        #self.verticalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(parent=Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.textBrowser = PyTextReader(parent=Form)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout_2.addWidget(self.textBrowser)
        self.label_3 = QtWidgets.QLabel(parent=Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.textBrowser_2 = QtWidgets.QTextBrowser(parent=Form)
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.verticalLayout_2.addWidget(self.textBrowser_2)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.splitter_2 = QtWidgets.QSplitter(parent=Form)
        self.splitter_2.setEnabled(True)
        self.splitter_2.setOrientation(QtCore.Qt.Orientation.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtWidgets.QSplitter(parent=self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Orientation.Vertical)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(parent=self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lineEdit = QtWidgets.QLineEdit(parent=self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lineEdit.setFont(font)
        self.lineEdit.setAutoFillBackground(False)
        self.lineEdit.setStyleSheet("margin-top: 3px; margin-bottom: 3px;")
        self.lineEdit.setText("")
        self.lineEdit.setClearButtonEnabled(False)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout_3.addWidget(self.lineEdit)
        self.label_2 = QtWidgets.QLabel(parent=self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setTextFormat(QtCore.Qt.TextFormat.PlainText)
        self.label_2.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.plainTextEdit = PyTextEditor(parent=self.layoutWidget)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout_3.addWidget(self.plainTextEdit)
        self.textEdit = QtWidgets.QTextEdit(parent=self.layoutWidget)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout_3.addWidget(self.textEdit)
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout_3.addWidget(self.pushButton_2)
        self.pushButton_10 = QtWidgets.QPushButton(parent=self.layoutWidget)
        self.pushButton_10.setObjectName("pushButton_10")
        self.verticalLayout_3.addWidget(self.pushButton_10)
        self.verticalLayout_3.setStretch(2, 1)
        self.horizontalLayout.addWidget(self.splitter_2)
        self.horizontalLayout.setStretch(1, 2)
        self.horizontalLayout.setStretch(2, 3)

        self.menu_bar = QtWidgets.QMenuBar(Form)
        self.menu_bar.setNativeMenuBar(False)
        self.menu_bar.setObjectName("menu_bar")
        back_action = QAction("Назад", self)
        back_action.triggered.connect(self.back_to_menu)
        self.menu_bar.addAction(back_action)

        help_menu = self.menu_bar.addMenu("Справка")
        about_action = QAction("Работа с модулем", self)
        about_action.triggered.connect(self.show_about1)
        help_menu.addAction(about_action)
        about_action = QAction("Другое", self)
        about_action.triggered.connect(self.show_about2)
        help_menu.addAction(about_action)

        self.mainLayout.insertWidget(0, self.menu_bar)

        self.retranslateUi(Form)
        self.verticalTabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def show_about1(self):
        md = """**Работа с модулем**:

 * Выберите прототип во владке "Прототипы" двойным кликом
 * Ознакомьтесь с описанием прототипа, для получения результатов следует вызывать main
 * Создайте новую задачу (кнопка новая задача)
 * Или отредактируйте уже существующую задачу, выбрав ее двойным кликом на вкладке "Задачи" (прототип должен быть выбран)
"""     
        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setWindowTitle("Работа с модулем")
        msg_box.setText(markdown(md))
        msg_box.setStyleSheet("QLabel{font-size: 18px; ; min-width: 550px;}")
        msg_box.exec()

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Редактор задач"))
        self.verticalTabWidget.setTabText(self.verticalTabWidget.indexOf(self.verticalTabWidgetPage1), _translate("Form", "Прототипы"))
        self.verticalTabWidget.setTabText(self.verticalTabWidget.indexOf(self.tab), _translate("Form", "Задачи"))
        self.pushButton.setText(_translate("Form", "Новая задача"))
        self.label.setText(_translate("Form", "Исходный код прототипа"))
        self.label_3.setText(_translate("Form", "Описание прототипа"))
        self.lineEdit.setPlaceholderText(_translate("Form", "Название задачи"))
        self.label_2.setText(_translate("Form", "Редактор кода"))
        self.textEdit.setPlaceholderText(_translate("Form", "Условие задачи"))
        self.pushButton_2.setText(_translate("Form", "Сгенирировать условие"))
        self.pushButton_10.setText(_translate("Form", "Сохранить задачу в сборник"))
