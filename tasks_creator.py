import json
import os

from PyQt6.QtCore import Qt

from solvers import card_solver, word_solver, num_solver, prototype_solver
from ui import CustomDialog, resource_path, WordEditorUI, CardDeckEditorUI, NumberEditorUI, PrototypeCreatorUI, PrototypeTaskCreatorUI



class PrototypeCreator(PrototypeCreatorUI):
    def __init__(self, parent):
        super().__init__(parent)
        self._post_init()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete:
            selected_item = self.listWidget_2.currentItem()
            if selected_item and selected_item.text() == "Задачи без прототипа":
                dlg = CustomDialog("Этот прототип нельзя удалить!", parent=self)
                dlg.exec()
            elif selected_item:
                name = selected_item.text()
                selected_item = self.listWidget_2.takeItem(self.listWidget_2.currentRow())
                selected_item = None
                if os.path.exists(resource_path(os.path.join("prototypes", name + ".json"))):
                    os.remove(resource_path(os.path.join("prototypes", name + ".json")))
                self._load_tasks_name()

        super().keyPressEvent(event)

    def _clear_task(self):
        self.plainTextEdit.setPlainText(self.start_text)
        self.lineEdit.clear()
        self.textEdit.clear()

    def _post_init(self):
        self.pushButton_11.clicked.connect(self._clear_task)
        self.pushButton_10.clicked.connect(self.save_task)
        self.listWidget_2.itemDoubleClicked.connect(self._load_task)
        self._load_tasks_name()

    def _load_tasks_name(self):
        self.tasks = []
        self.listWidget_2.clear()
        for filename in os.listdir(resource_path("prototypes")):
            if filename.endswith(".json"):
                filepath = resource_path(os.path.join("prototypes", filename))
                try:
                    with open(filepath, "r", encoding="utf-8") as file:
                        data = json.load(file)
                        self.tasks.append(data)
                except:
                    pass
        self.listWidget_2.addItems(task["name"] for task in self.tasks)
        self.listWidget_2.sortItems()
    
    def _load_task(self, value):
        value = value.text()
        for task in self.tasks:
            if task["name"] == str(value):
                self.lineEdit.setText(task["name"])
                self.textEdit.setText(task["desk"])
                self.plainTextEdit.setPlainText(task["code"])
                break

    def save_task(self):
        if self.lineEdit.text() == "":
            dlg = CustomDialog("У прототипа должно быть название!", parent=self)
            dlg.exec()
            return
        if (ans := prototype_solver.check_code(self.plainTextEdit.toPlainText())) != "OK":
            dlg = CustomDialog(ans, parent=self)
            dlg.exec()
            return
        task = {"name": self.lineEdit.text(), "code": self.plainTextEdit.toPlainText(), "desk": self.textEdit.toPlainText()}
        with open(resource_path(os.path.join("prototypes", task["name"] + ".json")), "w") as fp:
            json.dump(task , fp)

        self._load_tasks_name()
        dlg = CustomDialog("Протип сохранен", "Успех!", parent=self)
        dlg.exec()


class PrototypeTaskCreator(PrototypeTaskCreatorUI):
    def __init__(self, parent):
        super().__init__(parent)
        self.start_text = """## Вызовите функцию-решатель прототипа с вашими данными
# запишите ответ в переменную answer
# Условие можно сгенерировать после написания задачи
# (ничего в коде менять не нужно)
answer = main()"""
        self.protos = []
        self.tasks = []
        self.curr_proto = ""
        self._post_init()

    def _post_init(self):
        self.listWidget.itemDoubleClicked.connect(self._load_proto_statments)
        self.pushButton.clicked.connect(self._clear_task)
        self.plainTextEdit.setPlainText(self.start_text)
        self.pushButton_2.clicked.connect(self.get_task)
        self.pushButton_10.clicked.connect(self.save_task)
        self.listWidget_2.itemDoubleClicked.connect(self._load_task)
        self._load_prototypes_name()

    def _load_task(self, value):
        for task in self.tasks:
            if task["name"] == value.text():
                self.plainTextEdit.setPlainText(task["code"])
                self.textEdit.setText(task["task"])
                self.lineEdit.setText(task["name"])
                break

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Delete:
            selected_item = self.listWidget_2.currentItem()
            if selected_item:
                name = selected_item.text()
                selected_item = self.listWidget_2.takeItem(self.listWidget_2.currentRow())
                selected_item = None
                if os.path.exists(resource_path(os.path.join("tasks", name + ".json"))):
                    os.remove(resource_path(os.path.join("tasks", name + ".json")))
                self._load_tasks_name(self.curr_proto["name"])
        if event.key() == Qt.Key.Key_F5:
            self._load_prototypes_name()

        super().keyPressEvent(event)

    def get_task(self):
        if self.curr_proto == "":
            dlg = CustomDialog("Вначале выберите прототип!", parent=self)
            dlg.exec()
            return
        ans = prototype_solver.run_solve_code(
            self.curr_proto["code"], self.plainTextEdit.toPlainText(), True
        )
        if ans[0] != "OK":
            dlg = CustomDialog(ans, parent=self)
            dlg.exec()
            return
        self.textEdit.setText(ans[1])

    def save_task(self):
        if self.curr_proto == "":
            dlg = CustomDialog("Вначале выберите прототип!", parent=self)
            dlg.exec()
            return
        if self.lineEdit.text() == "":
            dlg = CustomDialog("У задачи должно быть название!", parent=self)
            dlg.exec()
            return
        ans = prototype_solver.run_solve_code(
            self.curr_proto["code"], self.plainTextEdit.toPlainText()
        )
        if ans[0] != "OK":
            dlg = CustomDialog(ans, parent=self)
            dlg.exec()
            return
        task = {"name": self.lineEdit.text(), "code": self.plainTextEdit.toPlainText(), "task": self.textEdit.toPlainText(), "type": self.curr_proto["name"], "answer": ans[1]}
        with open(resource_path(os.path.join("tasks", task["name"] + ".json")), "w") as fp:
            json.dump(task , fp)

        self._load_tasks_name(self.curr_proto["name"])
        dlg = CustomDialog("Задача сохранена", "Успех!", parent=self)
        dlg.exec()


    def _clear_task(self):
        self.plainTextEdit.setPlainText(self.start_text)
        self.lineEdit.clear()
        self.textEdit.clear()
    
    def _load_proto_statments(self, value):
        if type(value) != str:
            name = value.text()
        else:
            name = value
        for proto in self.protos:
            if proto["name"] == name:
                self.textBrowser.setPlainText(proto["code"])
                self.textBrowser_2.setPlainText(proto["desk"])
                self.curr_proto = proto
                break
        self._load_tasks_name(name)

    def _load_prototypes_name(self):
        self.protos = []
        self.listWidget.clear()
        for filename in os.listdir(resource_path("prototypes")):
            if filename.endswith(".json"):
                filepath = resource_path(os.path.join("prototypes", filename))
                try:
                    with open(filepath, "r", encoding="utf-8") as file:
                        data = json.load(file)
                        self.protos.append(data)
                except:
                    pass
        self.listWidget.addItems(pr["name"] for pr in self.protos)
        self.listWidget.sortItems()


class WordEditor(WordEditorUI):
    def __init__(self, parent):
        super().__init__(parent)
        self._post_init()

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
        dlg = CustomDialog("Задача сохранена в задачник", "Успех!", parent=self)
        dlg.exec()

    def _post_init(self):
        self.comboBox_2.addItems("Слово является палиндромом,Гласные и согласные чередуются,После каждой гласной идет согласная,После каждой согласной идет гласная".split(","))
        self.comboBox_5.addItems(self.zn)
        self.comboBox_4.addItems(["Гласных", "Согласных"])
        self.comboBox_6.addItems(self.zn)
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

    def _load_tasks_name(self):
        super()._load_tasks_name("word")

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


class CardDeckEditor(CardDeckEditorUI):
    def __init__(self, parent):
        super().__init__(parent)
        self._post_init()

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
        self.comboBox.currentTextChanged.connect(self.change_cards)
        self.comboBox_5.addItems("буби,черви,треф,пики".split(","))
        self.change_cards("36")
        self.comboBox_3.addItems(self.zn)
        self.comboBox_6.addItems(self.zn)
        self.comboBox_7.addItems(self.zn)
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

    def _load_tasks_name(self):
        super()._load_tasks_name("card")

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


class NumberEditor(NumberEditorUI):
    def __init__(self, parent):
        super().__init__(parent)
        self._post_init()

    def add_condition1(self):
        self.listWidget.addItem(
            self.comboBox_2.currentText()
        )

    def _load_tasks_name(self):
        return super()._load_tasks_name("num")

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

    def _post_init(self):
        self.comboBox_2.addItems("Набор состоит из различных цифр,Соседние цифры набора различны,Цифры набора идут в возрастающем порядке,Цифры набора идут в неубывающем порядке,Цифры набора идут в убывающем порядке,Цифры набора идут в невозрастающем порядке".split(","))
        self.comboBox_5.addItems(self.zn)
        self.comboBox_7.addItems(self.zn)
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
