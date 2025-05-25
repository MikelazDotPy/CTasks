import json
import os
import sys

from PyQt6 import QtCore
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction, QColor
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

from datetime import datetime
from parse_expr import parse_expr


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


GOOD_COLOR = "#1f8300"

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


class TaskSolver(QWidget):
    def __init__(self, parent, task_type):
        super().__init__()
        self.setupUi(self)
        self.parent = parent
        self.task_type = task_type
        self.curr_task = None
        self.tasks = []
        self.user_data = []
        self.user_data_path = resource_path(os.path.join("user", "data.json"))
        self.label.setText("""В ответе могут присутствовать:
    1. Числа
    2. Формулы: C(n,k) — сочетания, A(n,k) — размещения, F(n) — факториал
    3. Операторы: +, -, *, /, **
        оператор / означает целочисленное деление
        оператор ** означает возведение в степнь
 
Если задача противоречива, ответ 0.""") 
        self._post_init()

    def _setup_menu_bar(self):
        # Создаем QMenuBar
        self.menu_bar = QtWidgets.QMenuBar(self)
        self.menu_bar.setNativeMenuBar(False)
        back_action = QAction("Назад", self)
        back_action.triggered.connect(self.back_to_menu)
        self.menu_bar.addAction(back_action)
        
        # Добавляем менюбар в layout
        self.horizontalLayout.insertWidget(0, self.menu_bar)

    def back_to_menu(self):
        if self.parent:
            self.parent.show()
        self.close()

    def create_empty_json(self, file_path):
        if not resource_path(os.path.join("user", "data.json")):
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump([], f)

    def append_to_json_list(self, file_path, new_item):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                data = []
            
            if new_item in data:
                return
            data.append(new_item)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False)
                
        except (FileNotFoundError, json.JSONDecodeError):
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump([new_item], f, ensure_ascii=False, indent=4)

    def _load_tasks_name(self):
        self.tasks = []
        self.listWidget.clear()
        for filename in os.listdir(resource_path("tasks")):
            if filename.endswith(".json"):  # Проверяем расширение .json
                filepath = resource_path(os.path.join("tasks", filename))  # Полный путь к файлу
                
                # Читаем и парсим JSON
                try:
                    with open(filepath, "r", encoding="utf-8") as file:
                        data = json.load(file)  # Загружаем JSON в словарь/список
                        if data["type"] == self.task_type:
                            self.tasks.append(data)
                except:
                    pass
        self.listWidget.addItems(task["name"] for task in self.tasks)
        self.listWidget.sortItems()
        try:
            file_path = self.user_data_path
            
            if not os.path.exists(file_path):
                self.user_data = []
                self.create_empty_json(file_path)
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                self.user_data = []
                self.create_empty_json(file_path)
            
            self.user_data = data
    
        except (json.JSONDecodeError, IOError, PermissionError):
            self.create_empty_json(file_path)
            self.user_data = []

        for i in range(self.listWidget.count()):
            if self.listWidget.item(i).text() in self.user_data:
                self.listWidget.item(i).setBackground(QColor(GOOD_COLOR))

    def _post_init(self):
        self._load_tasks_name()
        self.listWidget.itemDoubleClicked.connect(self._load_task)
        self.pushButton.clicked.connect(self._check_sol)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_F5:
            self._load_tasks_name()
        if event.key() == Qt.Key.Key_Return:
            self._check_sol()
        super().keyPressEvent(event)
    
    def _check_sol(self):
        if self.curr_task is None:
            return
        
        try:
            ans = parse_expr(self.lineEdit.text())
        except:
            dlg = CustomDialog("Не удалось распознать выражение", parent=self)
            dlg.exec()
            return
        if ans == self.curr_task["answer"]:
            dlg = CustomDialog("Ответ верный!", title="Успех!", parent=self)
            dlg.exec()
            
            self.append_to_json_list(self.user_data_path, self.curr_task["name"])
            if self.curr_task["name"] not in self.user_data:
                self.user_data.append(self.curr_task["name"])
            it = self.listWidget.findItems(self.curr_task["name"], Qt.MatchFlag.MatchExactly)[0]
            it.setBackground(QColor(GOOD_COLOR))
            self.textBrowser.append(f"[{datetime.now().strftime("%d.%m.%Y %H:%M")}]: Задача '{self.curr_task["name"]}' решена. Ответ: {self.lineEdit.text()}")
        else:
            dlg = CustomDialog("Неверный ответ!", title="Неудача!", parent=self)
            dlg.exec()
            self.textBrowser.append(f"[{datetime.now().strftime("%d.%m.%Y %H:%M")}]: Задача '{self.curr_task["name"]}' дан неправильный ответ. Ответ: {self.lineEdit.text()}")

    def _load_task(self, value: QtWidgets.QListWidgetItem):
        value = value.text()
        for task in self.tasks:
            if task["name"] == str(value):
                self.textBrowser_2.setText(task["task"])
                self.lineEdit.setText("")
                self.textBrowser.append(f"[{datetime.now().strftime("%d.%m.%Y %H:%M")}]: Начато решение задачи '{task["name"]}'")
                self.curr_task = task
                break
        
        

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(900, 600)

        # Add menu bar at the top
        self.menu_bar = QtWidgets.QMenuBar(Form)
        self.menu_bar.setNativeMenuBar(False)
        self.menu_bar.setObjectName("menu_bar")
        back_action = QAction("Назад", self)
        back_action.triggered.connect(self.back_to_menu)
        self.menu_bar.addAction(back_action)

        self.formLayout = QtWidgets.QFormLayout(Form)
        self.formLayout.setObjectName("formLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        #self.verticalLayout_2.addWidget(self.menu_bar)
        self.label_3 = QtWidgets.QLabel(parent=Form)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.listWidget = QtWidgets.QListWidget(parent=Form)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout_2.addWidget(self.listWidget)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.menu_bar)
        self.formLayout.setLayout(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(parent=Form)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.textBrowser_2 = QtWidgets.QTextBrowser(parent=Form)
        self.textBrowser_2.setObjectName("textBrowser_2")
        self.verticalLayout.addWidget(self.textBrowser_2)
        self.verticalLayout_3.addLayout(self.verticalLayout)
        
        self.label = QtWidgets.QLabel(parent=Form)
        self.label.setMinimumSize(QtCore.QSize(0, 100))
        self.label.setText("")
        self.label.setObjectName("label")
        self.label.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.label)
        self.verticalLayout_3.addWidget(scroll)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(parent=Form)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.pushButton = QtWidgets.QPushButton(parent=Form)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.textBrowser = QtWidgets.QTextBrowser(parent=Form)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout_3.addWidget(self.textBrowser)
        self.formLayout.setLayout(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.verticalLayout_3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Решение задач"))
        self.label_3.setText(_translate("Form", "Список задач"))
        self.label_2.setText(_translate("Form", "Условие задачи"))
        self.lineEdit.setPlaceholderText(_translate("Form", "Ответ"))
        self.pushButton.setText(_translate("Form", "Проверить"))
