from datetime import datetime
from math import comb, perm, factorial
import json
import os

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from ui import CustomDialog, TasksSolverUI, resource_path


def parse_expr(expr):
    expr = expr.replace("/", "//")
    return eval(expr, {'C': comb, 'A': perm, 'F': factorial, 'С': comb, 'А': perm}, {})


GOOD_COLOR = "#1f8300"

class TaskSolver(TasksSolverUI):
    def __init__(self, parent):
        super().__init__(parent)
        self.user_data = []
        self.user_data_path = resource_path(os.path.join("user", "data.json"))
        self.curr_task = None
        self.curr_proto = None
        self.tasks = []
        self.protos = []
        self.special_protypes = {
            "Карты": "card",
            "Слова": "word",
            "Числа": "num",
            "Другое": "Задачи без прототипа"
        }
        self._post_init()

    def _post_init(self):
        self._load_prototypes_name()
        self.listWidget.itemDoubleClicked.connect(self._load_tasks_name)
        self.listWidget_2.itemDoubleClicked.connect(self._load_task)

    def _load_prototypes_name(self):
        self.protos = []
        self.listWidget.clear()
        for filename in os.listdir(resource_path("prototypes")):
            if filename.endswith(".json"):
                filepath = resource_path(os.path.join("prototypes", filename))
                try:
                    with open(filepath, "r", encoding="utf-8") as file:
                        data = json.load(file)
                        self.tasks.append(data)
                except:
                    pass
        self.listWidget.addItems(list(self.special_protypes.keys())[:-1])
        self.listWidget.addItems(sorted(task["name"] for task in self.tasks if task["name"] != "Задачи без прототипа"))
        self.listWidget.addItems(["Другое"])
        #self.listWidget.sortItems()
        #self.listWidget.addItems(self.special_protypes.keys())

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

    def _load_tasks_name(self, task_type):
        if type(task_type) != str:
            task_type = task_type.text()
        self.curr_proto = task_type
        if task_type in self.special_protypes:
            task_type = self.special_protypes[task_type]

        self.tasks = []
        self.listWidget_2.clear()
        for filename in os.listdir(resource_path("tasks")):
            if filename.endswith(".json"):
                filepath = resource_path(os.path.join("tasks", filename))
                try:
                    with open(filepath, "r", encoding="utf-8") as file:
                        data = json.load(file)
                        if data["type"] == task_type:
                            self.tasks.append(data)
                except:
                    pass
        self.listWidget_2.addItems(task["name"] for task in self.tasks)
        self.listWidget_2.sortItems()
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

        for i in range(self.listWidget_2.count()):
            if self.listWidget_2.item(i).text() in self.user_data:
                self.listWidget_2.item(i).setBackground(QColor(GOOD_COLOR))
        
        if self.listWidget_2.count() == 0:
            dlg = CustomDialog("Этот сборник, пока пуст", "", self)
            dlg.exec()

    def _load_task(self, value):
        value = value.text()
        for task in self.tasks:
            if task["name"] == str(value):
                self.textBrowser_2.setText(task["task"])
                self.lineEdit.setText("")
                self.textBrowser.append(f"[{datetime.now().strftime("%H:%M")}]: Начато решение задачи '{task["name"]}'")
                self.curr_task = task
                break
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_F5:
            self._load_prototypes_name()
            if self.curr_proto is not None:
                self._load_tasks_name(self.curr_proto["type"])
        if event.key() == Qt.Key.Key_Return:
            self._check_sol()
        super().keyPressEvent(event)
    
    def _check_sol(self):
        if self.curr_task is None:
            dlg = CustomDialog("Выберите задачу!", parent=self)
            dlg.exec()
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
            it = self.listWidget_2.findItems(self.curr_task["name"], Qt.MatchFlag.MatchExactly)
            if it:
                it[0].setBackground(QColor(GOOD_COLOR))
            self.textBrowser.append(f"[{datetime.now().strftime("%H:%M")}]: Задача '{self.curr_task["name"]}' решена. Ответ: {self.lineEdit.text()}")
        else:
            dlg = CustomDialog("Неверный ответ!", title="Неудача!", parent=self)
            dlg.exec()
            self.textBrowser.append(f"[{datetime.now().strftime("%H:%M")}]: Задача '{self.curr_task["name"]}' дан неправильный ответ. Ответ: {self.lineEdit.text()}")
