import json
import os
import sys

from markdown import markdown
from PyQt6 import QtCore
from PyQt6 import QtGui
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

from solvers import card_solver, word_solver, num_solver


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)



class CustomDialog(QtWidgets.QDialog):
    def __init__(self, text, title="Ошибка!", parent=None):
        super().__init__(parent)

        self.setWindowTitle(title)

        QBtn = (
            QtWidgets.QDialogButtonBox.StandardButton.Ok
        )

        self.buttonBox = QtWidgets.QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        layout = QVBoxLayout()
        message = QLabel(text)
        layout.addWidget(message, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.buttonBox, alignment=Qt.AlignmentFlag.AlignCenter)
        self.setLayout(layout)
        self.resize(200, 100)


class WordEditor(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self._post_init()

    def back_to_menu(self):
        if self.parent:
            self.parent.show()
        self.close()

    def add_condition1(self):
        self.listWidget.addItem(
            self.comboBox_2.currentText()
        )
    
    def add_condition2(self):
        if not self.lineEdit_3.text().isnumeric():
            dlg = CustomDialog("Поле должно содержать число!", parent=self)
            dlg.exec()
            return
        self.listWidget.addItem(
            f"{self.comboBox_4.currentText()} {self.comboBox_5.currentText()} {self.lineEdit_3.text()}"
        )
    
    def add_condition3(self):
        self.listWidget.addItem(
            f"Гласных {self.comboBox_6.currentText()} Согласных"
        )

    def get_task(self):
        if not self.lineEdit_2.text().isnumeric():
            dlg = CustomDialog("Укажите корректную длину слова!", parent=self)
            dlg.exec()
            return
        if self.lineEdit_4.text() == "" and (not self.lineEdit_6.text().isnumeric() or not self.lineEdit_7.text().isnumeric()):
            dlg = CustomDialog("Укажитете алфавит или количество гласных и согласных в нем", parent=self)
            dlg.exec()
            return
        s = ""
        v = c = 0
        if self.lineEdit_4.text() != "":
            v, c, alph = word_solver.alph_proccesor(self.lineEdit_4.text(), self.checkBox_2.isChecked())
            alph = ", ".join(x.upper() for x in alph)
            if not self.checkBox_2.isChecked():
                s += f"Дан алфавит: {'{ '}{alph}{' }'} ({v} гласных и {c} согласных. Несмотря возможное одинаковое написание букв в алфавите они различны). "+\
                    f"Буквы{'' if self.checkBox.isChecked() else ' не'} могут повторяться\n"
            else:
                s += f"Дан алфавит: {'{ '}{alph}{' }'} ({v} гласных и {c} согласных). "+\
                    f"Буквы{'' if self.checkBox.isChecked() else ' не'} могут повторяться\n"
            self.checkBox_2.isChecked()
        else:
            v, c = int(self.lineEdit_6.text()), int(self.lineEdit_7.text())
            s += f"Дан алфавит из {v} гласных и {c} согласных. "+\
                  f"Буквы{'' if self.checkBox.isChecked() else ' не'} могут повторяться\n"
        s += f"Сколько существует слов длины {self.lineEdit_2.text()} удовлетворяющих условиям:\n"
        for i in range(self.listWidget.count()):
            s += "  " f"{i + 1}. " + self.listWidget.item(i).text() + "\n"
        self.textEdit.setText(s)
    
    def save_task(self):
        if self.lineEdit.text() == "":
            dlg = CustomDialog("У задачи должно быть название!", parent=self)
            dlg.exec()
            return
        if not self.lineEdit_2.text().isnumeric():
            dlg = CustomDialog("Укажите корректную длину слова!", parent=self)
            dlg.exec()
            return
        if self.lineEdit_4.text() == "" and (not self.lineEdit_6.text().isnumeric() or not self.lineEdit_7.text().isnumeric()):
            dlg = CustomDialog("Укажитете алфавит или количество гласных и согласных в нем", parent=self)
            dlg.exec()
            return
        v = c = 0
        if self.lineEdit_4.text() != "":
            v, c, alph = word_solver.alph_proccesor(self.lineEdit_4.text(), self.checkBox_2.isChecked())
        else:
            v, c = int(self.lineEdit_6.text()), int(self.lineEdit_7.text())
        task = {"name": self.lineEdit.text(), "task": self.textEdit.toPlainText(), "type": "word", "word_len": int(self.lineEdit_2.text()), "g_s": [v, c], "not_uniq": self.checkBox.isChecked(), "alph_uniq": self.checkBox_2.isChecked()}
        if self.lineEdit_4.text() != "":
            task["alph"] = self.lineEdit_4.text()
        else:
            task["alph"] = ""
        task["conditions"] = list(set(self.listWidget.item(i).text() for i in range(self.listWidget.count())))
        task["answer"] = word_solver.solve(task)
        with open(resource_path(os.path.join("tasks", task["name"] + ".json")), "w") as fp:
            json.dump(task , fp)
        self._load_tasks_name()
        print(task["answer"])
        dlg = CustomDialog("Задача сохранена в задачник", "Успех!", parent=self)
        dlg.exec()

    def del_list_el(self, value):
        item = self.listWidget.takeItem(self.listWidget.currentRow())
        item = None

    def _post_init(self):
        zn = ["=", "!=", ">", "<", ">=", "<="]
        self.comboBox_2.addItems("Слово является палиндромом,Гласные и согласные чередуются,После каждой гласной идет согласная,После каждой согласной идет гласная".split(","))
        self.comboBox_5.addItems(zn)
        self.comboBox_4.addItems(["Гласных", "Согласных"])
        self.comboBox_6.addItems(zn)
        self.checkBox.setChecked(True)
        self.checkBox_2.setChecked(True)
        self.pushButton.clicked.connect(self.add_condition1)
        self.pushButton_2.clicked.connect(self.add_condition2)
        self.pushButton_3.clicked.connect(self.add_condition3)
        self.listWidget.itemDoubleClicked.connect(self.del_list_el)
        self.pushButton_5.clicked.connect(lambda : self.listWidget.clear())
        self.pushButton_9.clicked.connect(self.get_task)
        self.pushButton_10.clicked.connect(self.save_task)
        self.listWidget_2.itemDoubleClicked.connect(self._load_task)
        self.pushButton_11.clicked.connect(self._clear_task)
        self._load_tasks_name()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete:
            selected_item = self.listWidget_2.currentItem()
            if selected_item:
                name = selected_item.text()
                selected_item = self.listWidget_2.takeItem(self.listWidget.currentRow())
                selected_item = None
                if os.path.exists(resource_path(os.path.join("tasks", name + ".json"))):
                    os.remove(resource_path(os.path.join("tasks", name + ".json")))
                self._load_tasks_name()

        super().keyPressEvent(event)

    def _load_tasks_name(self):
        self.tasks = []
        self.listWidget_2.clear()
        for filename in os.listdir(resource_path("tasks")):
            if filename.endswith(".json"):  # Проверяем расширение .json
                filepath = resource_path(os.path.join("tasks", filename))  # Полный путь к файлу
                
                # Читаем и парсим JSON
                try:
                    with open(filepath, "r", encoding="utf-8") as file:
                        data = json.load(file)  # Загружаем JSON в словарь/список
                        if data["type"] == "word":
                            self.tasks.append(data)
                except:
                    pass
        self.listWidget_2.addItems(task["name"] for task in self.tasks)
        self.listWidget_2.sortItems()

    def _clear_task(self):
        self.listWidget.clear()
        self.lineEdit.clear()
        self.lineEdit_4.clear()
        self.lineEdit_6.clear()
        self.lineEdit_7.clear()
        self.textEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.checkBox.setChecked(True)
        self.checkBox_2.setChecked(True)

    def _load_task(self, value):
        value = value.text()
        for task in self.tasks:
            if task["name"] == str(value):
                self.listWidget.clear()
                if task["alph"] != "":
                    self.lineEdit_4.setText(task["alph"])
                    self.lineEdit_6.clear()
                    self.lineEdit_7.clear()
                else:
                    self.lineEdit_4.clear()
                    self.lineEdit_6.setText(str(task["g_s"][0]))
                    self.lineEdit_7.setText(str(task["g_s"][1]))
                self.lineEdit.setText(task["name"])
                self.textEdit.setText(task["task"])
                self.listWidget.addItems(task["conditions"])
                self.checkBox.setChecked(task["not_uniq"])
                self.checkBox_2.setChecked(task["alph_uniq"])
                self.lineEdit_2.setText(str(task["word_len"]))
                break

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1034, 612)

        self.mainLayout = QtWidgets.QVBoxLayout(Form)
        self.mainLayout.setObjectName("mainLayout")
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        # Add menu bar at the top

        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.mainLayout.addLayout(self.horizontalLayout, 1)

        # self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
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
        md = """1\. **Работа с модулем**:

* **Список существующих задач**  
    * Слева от конструктора задач располагается список уже созданных задач (в режиме редактирования можно по двойному клику перейти к любой из них и переделать/доделать при необходимости)  
* **Условия задачи**  
    * Поля для добавления условий (например, "слово является палиндромом", "гласных = 4").  
        * **Палиндром** — это слово, фраза, число или другая последовательность символов, которая читается **одинаково** как **слева направо**, так и **справа налево**.  
        * В строке “Алфавит” вы можете с клавиатуры ввести желаемый алфавит (например: абв или а, б, в, оба варианта дадут алфавит {А, Б, В})  
        * Галочка “Только уникальные буквы” превратит набор {МАТЕМАТИКА} в {МАТЕИК}, то есть уберет все повторяющиеся буквы.  
        * При выборе алфавита с повторяющимися буквами, подсчет слов будет с учетом того, что все буквы разные. То есть слова МАТЕМАТИКА и МАТЕМАТИКА будут считаться разными.  
    * Удаление условия: двойной клик по нему.  
* **Условие задачи**   
    * Генерируется при нажатии на “Сгенерировать условие”.
    """
        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setWindowTitle("Работа с модулем")
        msg_box.setText(markdown(md))
        msg_box.setStyleSheet("QLabel{font-size: 18px; ; min-width: 550px;}")
        msg_box.exec()
    
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



class CardDeckEditor(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self._post_init()
        #self._setup_menu_bar()

    def _setup_menu_bar(self):
        # Создаем QMenuBar
        self.menu_bar = QtWidgets.QMenuBar(self)
        
        back_action = QAction("Назад", self)
        back_action.triggered.connect(self.back_to_menu)
        self.menu_bar.addAction(back_action)
        
        # Добавляем менюбар в layout
        self.horizontalLayout.insertWidget(0, self.menu_bar)

    def back_to_menu(self):
        if self.parent:
            self.parent.show()
        self.close()

    def change_cards(self, value):
        x36 = "карт бубновой масти,карт червовой масти,карт трефовой масти,карт пиковой масти,красных карт,черных карт,шестерок,семерок,восьмерок,девяток,десяток,вальтов,дам,королей,тузов".split(",")
        x52 = "карт бубновой масти,карт червовой масти,карт трефовой масти,карт пиковой масти,красных карт,черных карт,двоек,троек,четверок,пятерок,шестерок,семерок,восьмерок,девяток,десяток,вальтов,дам,королей,тузов".split(",")
        
        
        self.comboBox_2.clear()
        self.comboBox_4.clear()
        self.comboBox_8.clear()
        if value == "36":
            self.comboBox_2.addItems(x36)
            self.comboBox_4.addItems("шестерка,семерка,восьмерка,девятка,десятка,валет,дама,король,туз".split(","))
            self.comboBox_8.addItems("шестерка,семерка,восьмерка,девятка,десятка,валет,дама,король,туз".split(","))
        else:
            self.comboBox_2.addItems(x52)
            self.comboBox_4.addItems("двойка,тройка,четверка,пятерка,шестерка,семерка,восьмерка,девятка,десятка,валет,дама,король,туз".split(","))
            self.comboBox_8.addItems("двойка,тройка,четверка,пятерка,шестерка,семерка,восьмерка,девятка,десятка,валет,дама,король,туз".split(","))

    def add_condition1(self):
        if not self.lineEdit_3.text().isnumeric():
            dlg = CustomDialog("Поле должно содержать число!", parent=self)
            dlg.exec()
            return
        self.listWidget.addItem(
            f"Количество {self.comboBox_2.currentText()} {self.comboBox_3.currentText()} {self.lineEdit_3.text()}"
        )

    def add_condition2(self):
        self.listWidget.addItem(
            f"В наборе содержится {self.comboBox_4.currentText()} {self.comboBox_5.currentText()}"
        )
    
    def add_condition3(self):
        if not self.lineEdit_4.text().isnumeric():
            dlg = CustomDialog("Поле должно содержать число!", parent=self)
            dlg.exec()
            return
        self.listWidget.addItem(
            f"Сумма очков {self.comboBox_6.currentText()} {self.lineEdit_4.text()}"
        )
    
    def add_condition4(self):
        self.listWidget.addItem(
            f"Все карты {self.comboBox_7.currentText()} {self.comboBox_8.currentText()}"
        )

    def del_list_el(self, value):
        item = self.listWidget.takeItem(self.listWidget.currentRow())
        item = None
    
    def get_task(self):
        if self.lineEdit.text() == "":
            dlg = CustomDialog("У задачи должно быть название!", parent=self)
            dlg.exec()
            return
        if not self.lineEdit_2.text().isnumeric():
            dlg = CustomDialog("Укажите корректный размер набора!", parent=self)
            dlg.exec()
            return
        s = f"Из колоды размера {self.comboBox.currentText()} выбрали набор из {self.lineEdit_2.text()} карт.\nСколько существует наборов удовлетворяющих условиям:\n"
        for i in range(self.listWidget.count()):
            s += "  " f"{i + 1}. " + self.listWidget.item(i).text() + "\n"
        self.textEdit.setText(s)
    
    def save_task(self):
        if self.lineEdit.text() == "":
            dlg = CustomDialog("У задачи должно быть название!", parent=self)
            dlg.exec()
            return
        if not self.lineEdit_2.text().isnumeric():
            dlg = CustomDialog("Укажите корректный размер набора!", parent=self)
            dlg.exec()
            return
        task = {"name": self.lineEdit.text(), "task":self.textEdit.toPlainText(), "type": "card", "deck": int(self.comboBox.currentText()), "set_size": int(self.lineEdit_2.text())}
        task["conditions"] = list(set(self.listWidget.item(i).text() for i in range(self.listWidget.count())))
        task["answer"] = card_solver.solve(task)
        with open(resource_path(os.path.join("tasks", task["name"] + ".json")), "w") as fp:
            json.dump(task , fp)
        self._load_tasks_name()
        dlg = CustomDialog("Задача сохранена в задачник", "Успех!", parent=self)
        dlg.exec()

    def _post_init(self):
        zn = ["=", "!=", ">", "<", ">=", "<="]
        self.comboBox.currentTextChanged.connect(self.change_cards)
        self.comboBox_5.addItems("буби,черви,треф,пики".split(","))
        self.change_cards("36")
        self.comboBox_3.addItems(zn)
        self.comboBox_6.addItems(zn)
        self.comboBox_7.addItems(zn)
        self.pushButton.clicked.connect(self.add_condition1)
        self.pushButton_2.clicked.connect(self.add_condition2)
        self.pushButton_3.clicked.connect(self.add_condition3)
        self.pushButton_4.clicked.connect(self.add_condition4)
        self.pushButton_5.clicked.connect(self.listWidget.clear)
        self.pushButton_9.clicked.connect(self.get_task)
        self.pushButton_10.clicked.connect(self.save_task)
        self.listWidget.itemDoubleClicked.connect(self.del_list_el)
        self.listWidget_2.itemDoubleClicked.connect(self._load_task)
        self.pushButton_11.clicked.connect(self._clear_task)
        self._load_tasks_name()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete:
            selected_item = self.listWidget_2.currentItem()
            if selected_item:
                name = selected_item.text()
                selected_item = self.listWidget_2.takeItem(self.listWidget.currentRow())
                selected_item = None
                if os.path.exists(resource_path(os.path.join("tasks", name + ".json"))):
                    os.remove(resource_path(os.path.join("tasks", name + ".json")))
                self._load_tasks_name()

        super().keyPressEvent(event)

    def _load_tasks_name(self):
        self.tasks = []
        self.listWidget_2.clear()
        for filename in os.listdir(resource_path("tasks")):
            if filename.endswith(".json"):  # Проверяем расширение .json
                filepath = resource_path(os.path.join("tasks", filename))  # Полный путь к файлу
                
                # Читаем и парсим JSON
                try:
                    with open(filepath, "r", encoding="utf-8") as file:
                        data = json.load(file)  # Загружаем JSON в словарь/список
                        if data["type"] == "card":
                            self.tasks.append(data)
                except:
                    pass
        self.listWidget_2.addItems(task["name"] for task in self.tasks)
        self.listWidget_2.sortItems()

    def _clear_task(self):
        self.listWidget.clear()
        self.lineEdit.clear()
        self.textEdit.clear()
        self.comboBox.setCurrentText("36")
        self.lineEdit_2.clear()

    def _load_task(self, value):
        value = value.text()
        for task in self.tasks:
            if task["name"] == str(value):
                self.listWidget.clear()
                self.lineEdit.setText(task["name"])
                self.textEdit.setText(task["task"])
                self.listWidget.addItems(task["conditions"])
                self.comboBox.setCurrentText(str(task["deck"]))
                self.lineEdit_2.setText(str(task["set_size"]))
                break

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1300, 621)

        self.mainLayout = QtWidgets.QVBoxLayout(Form)
        self.mainLayout.setObjectName("mainLayout")
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        # Add menu bar at the top

        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
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
        md = """#### **1. Работа с модулем**:

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


class NumberEditor(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self._post_init()

    def back_to_menu(self):
        if self.parent:
            self.parent.show()
        self.close()

    def add_condition1(self):
        self.listWidget.addItem(
            self.comboBox_2.currentText()
        )

    def add_condition2(self):
        if not num_solver.check_eq(self.lineEdit_3.text(), self.lineEdit_6.text()):
            dlg = CustomDialog("Неверное выражение! Информация о составлении в справке", parent=self)
            dlg.exec()
            return
        self.listWidget.addItem(num_solver.pretty_eq(self.lineEdit_6.text(), self.lineEdit_3.text(), self.comboBox_5.currentText()))
    
    def add_condition3(self):
        if not self.lineEdit_5.text().isnumeric() or not self.lineEdit_7.text().isnumeric():
            dlg = CustomDialog("Неверный индекс", parent=self)
            dlg.exec()
            return
        if not num_solver.check_eq(self.lineEdit_4.text(), "[0]"):
            dlg = CustomDialog("Неверное выражение! Информация о составлении в справке", parent=self)
            dlg.exec()
            return
        self.listWidget.addItem(num_solver.pretty_eq("{" +self.lineEdit_5.text() + "; " + self.lineEdit_7.text() + "}", self.lineEdit_4.text(), self.comboBox_7.currentText()))
    
    def get_task(self):
        if self.lineEdit.text() == "":
            dlg = CustomDialog("У задачи должно быть название!", parent=self)
            dlg.exec()
            return
        if not self.lineEdit_2.text().isnumeric():
            dlg = CustomDialog("Укажите корректный размер набора!", parent=self)
            dlg.exec()
            return
        if int(self.comboBox.currentText()) > int(self.comboBox_3.currentText()):
            dlg = CustomDialog("Укажите корректные границы значений цифр!", parent=self)
            dlg.exec()
            return
        xc = int(self.lineEdit_2.text())
        for i in range(self.listWidget.count()):
            if any(x in self.listWidget.item(i).text() for x in "=><"):
                if not num_solver.check_idxs(self.listWidget.item(i).text(), xc):
                    dlg = CustomDialog("Некорректный индекс цифры!", parent=self)
                    dlg.exec()
                    return
        s = (f"Сколько существует наборов цифр от {self.comboBox.currentText()} до {self.comboBox_3.currentText()}"
             f", длины {self.lineEdit_2.text()} "
            f"(границы включительно{', 0 не может быть первой цифрой' if self.checkBox_2.isChecked() else ''}), "
            f"которые удовлетворяют следующие условия:\n")
        for i in range(self.listWidget.count()):
            s += "  " f"{i + 1}. " + self.listWidget.item(i).text() + "\n"
        self.textEdit.setText(s)

    def save_task(self):
        if self.lineEdit.text() == "":
            dlg = CustomDialog("У задачи должно быть название!", parent=self)
            dlg.exec()
            return
        if not self.lineEdit_2.text().isnumeric():
            dlg = CustomDialog("Укажите корректный размер набора!", parent=self)
            dlg.exec()
            return
        if int(self.comboBox.currentText()) > int(self.comboBox_3.currentText()):
            dlg = CustomDialog("Укажите корректные границы значений цифр!", parent=self)
            dlg.exec()
            return
        xc = int(self.lineEdit_2.text())
        for i in range(self.listWidget.count()):
            if any(x in self.listWidget.item(i).text() for x in "=><"):
                if not num_solver.check_idxs(self.listWidget.item(i).text(), xc):
                    dlg = CustomDialog("Некорректный индекс цифры!", parent=self)
                    dlg.exec()
                    return
        task = {"name": self.lineEdit.text(), "task":self.textEdit.toPlainText(), "type": "num",
                "set_size": int(self.lineEdit_2.text()), "nonzero": self.checkBox_2.isChecked(),
                "start": int(self.comboBox.currentText()), "end": int(self.comboBox_3.currentText())}
        task["conditions"] = list(set(self.listWidget.item(i).text() for i in range(self.listWidget.count())))
        task["answer"] = num_solver.solve(task)
        with open(resource_path(os.path.join("tasks", task["name"] + ".json")), "w") as fp:
            json.dump(task , fp)
        self._load_tasks_name()
        dlg = CustomDialog("Задача сохранена в задачник", "Успех!", parent=self)
        dlg.exec()

    def del_list_el(self, value):
        item = self.listWidget.takeItem(self.listWidget.currentRow())
        item = None

    def _post_init(self):
        zn = ["=", "!=", ">", "<", ">=", "<="]
        self.comboBox_2.addItems("Набор состоит из различных цифр,Соседние цифры набора различны,Цифры набора идут в возрастающем порядке,Цифры набора идут в неубывабщем порядке,Цифры набора идут в убывающем порядке,Цифры набора идут в невозрастающем порядке".split(","))
        self.comboBox_5.addItems(zn)
        self.comboBox_7.addItems(zn)
        self.comboBox.addItems([str(x) for x in range(10)])
        self.comboBox_3.addItems([str(x) for x in range(10)])
        self.lineEdit_6.setPlaceholderText("[0] + [1] - 13")
        self.lineEdit_3.setPlaceholderText("[0] + [1] - 13")
        self.lineEdit_4.setPlaceholderText("[0] + [1] - 13")
        self.pushButton.clicked.connect(self.add_condition1)
        self.pushButton_2.clicked.connect(self.add_condition2)
        self.pushButton_3.clicked.connect(self.add_condition3)
        self.listWidget.itemDoubleClicked.connect(self.del_list_el)
        self.pushButton_5.clicked.connect(lambda : self.listWidget.clear())
        self.pushButton_9.clicked.connect(self.get_task)
        self.pushButton_10.clicked.connect(self.save_task)
        self.listWidget_2.itemDoubleClicked.connect(self._load_task)
        self.pushButton_11.clicked.connect(self._clear_task)
        self.comboBox_3.setCurrentIndex(9)
        self._load_tasks_name()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete:
            selected_item = self.listWidget_2.currentItem()
            if selected_item:
                name = selected_item.text()
                selected_item = self.listWidget_2.takeItem(self.listWidget.currentRow())
                selected_item = None
                if os.path.exists(resource_path(os.path.join("tasks", name + ".json"))):
                    os.remove(resource_path(os.path.join("tasks", name + ".json")))
                self._load_tasks_name()

        super().keyPressEvent(event)

    def _load_tasks_name(self):
        self.tasks = []
        self.listWidget_2.clear()
        for filename in os.listdir(resource_path("tasks")):
            if filename.endswith(".json"):  # Проверяем расширение .json
                filepath = resource_path(os.path.join("tasks", filename))  # Полный путь к файлу
                
                # Читаем и парсим JSON
                try:
                    with open(filepath, "r", encoding="utf-8") as file:
                        data = json.load(file)  # Загружаем JSON в словарь/список
                        if data["type"] == "num":
                            self.tasks.append(data)
                except:
                    pass
        self.listWidget_2.addItems(task["name"] for task in self.tasks)
        self.listWidget_2.sortItems()

    def _clear_task(self):
        self.listWidget.clear()
        self.lineEdit.clear()
        self.lineEdit_3.clear()
        self.lineEdit_6.clear()
        self.lineEdit_2.clear()
        self.comboBox.setCurrentIndex(0)
        self.comboBox_3.setCurrentIndex(9)
        self.textEdit.clear()
        self.lineEdit_2.clear()
        self.lineEdit_3.clear()
        self.checkBox_2.setChecked(False)

    def _load_task(self, value):
        value = value.text()
        for task in self.tasks:
            if task["name"] == str(value):
                self.listWidget.clear()
                self.listWidget.addItems(task["conditions"])
                self.lineEdit_2.setText(str(task["set_size"]))
                self.lineEdit.setText(task["name"])
                self.checkBox_2.setChecked(task["nonzero"])
                self.comboBox.setCurrentIndex(int(task["start"]))
                self.comboBox_3.setCurrentIndex(int(task["end"]))
                self.textEdit.setText(task["task"])
                break

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1034, 612)

        self.mainLayout = QtWidgets.QVBoxLayout(Form)
        self.mainLayout.setObjectName("mainLayout")
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
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
