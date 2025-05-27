
import os

from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QPushButton, QLabel, QFrame, QSizePolicy, QStyleFactory,
                             QMessageBox, QScrollArea, QMenuBar)
from markdown import markdown
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QAction, QIcon

from task_solver import TaskSolver
from tasks_creator import CardDeckEditor, WordEditor, NumberEditor, PrototypeCreator, PrototypeTaskCreator
from ui import resource_path


TASK_TYPES = ["Колода карт", "Слова", "Наборы цифр", "Другие задачи", "Создать прототип"]
TASK_DICT = {
    TASK_TYPES[0]: CardDeckEditor, TASK_TYPES[1]: WordEditor, TASK_TYPES[2]: NumberEditor,
    TASK_TYPES[3]: PrototypeTaskCreator, TASK_TYPES[4]: PrototypeCreator
}


class TaskCreationWindow(QWidget):
    def __init__(self, parent: QMainWindow=None):
        super().__init__()
        self.parent_window = parent
        self.setMinimumSize(400, 300)
        self._create_menu_bar()
        self.setWindowTitle(parent.windowTitle())

        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Редактор задач")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_container = QWidget()
        scroll_layout = QVBoxLayout(scroll_container)
        scroll_layout.setSpacing(15)
        scroll_layout.setContentsMargins(0, 0, 0, 0)


        for task_name in TASK_TYPES:
            btn = QPushButton(task_name)
            btn.setFont(QFont("Arial", 12))
            btn.setSizePolicy(QSizePolicy.Policy.Expanding, 
                            QSizePolicy.Policy.Expanding)
            btn.setMinimumHeight(60)
            btn.clicked.connect(lambda checked, name=task_name: self.on_task_type_clicked(name))
            scroll_layout.addWidget(btn)

        scroll_area.setWidget(scroll_container)
        layout.addWidget(scroll_area, stretch=1)

    def on_task_type_clicked(self, task_name):
        self.editor = TASK_DICT[task_name](self)
        self.editor.show()
        self.hide()

    def _create_menu_bar(self):
        menubar = QMenuBar(self)
        back_action = QAction("Назад", self)
        back_action.triggered.connect(self.back_to_menu)
        menubar.addAction(back_action)
        

    def back_to_menu(self):
        if self.parent_window:
            self.parent_window.show()
        self.close()



class MainMenu(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CTasks")
        self.setMinimumSize(400, 300)
        
        self._create_menu_bar()
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        
        title = QLabel("Меню")
        title.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line)
        
        button_container = QWidget()
        button_layout = QVBoxLayout(button_container)
        button_layout.setSpacing(15)
        button_layout.setContentsMargins(0, 0, 0, 0)
        
        btn_solve = QPushButton("Решение задач")
        btn_solve.setFont(QFont("Arial", 12))
        btn_solve.setSizePolicy(QSizePolicy.Policy.Expanding, 
                              QSizePolicy.Policy.Expanding)
        btn_solve.clicked.connect(self.on_solve_clicked)
        button_layout.addWidget(btn_solve)

        btn_create = QPushButton("Редактор задач")
        btn_create.setFont(QFont("Arial", 12))
        btn_create.setSizePolicy(QSizePolicy.Policy.Expanding, 
                               QSizePolicy.Policy.Expanding)
        btn_create.clicked.connect(self.on_create_clicked)
        button_layout.addWidget(btn_create)

        layout.addWidget(button_container, stretch=1)

        line_bottom = QFrame()
        line_bottom.setFrameShape(QFrame.Shape.HLine)
        line_bottom.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(line_bottom)
        
        author_label = QLabel("Авторы: Сабалиров М.З., Беннер В.А.")
        author_label.setFont(QFont("Arial", 10))
        author_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        layout.addWidget(author_label)

    def _create_menu_bar(self):
        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        help_menu = menubar.addMenu("Справка")
        about_action = QAction("О программе", self)
        about_action.triggered.connect(self.show_about1)
        help_menu.addAction(about_action)
        about_action = QAction("Общие сведения", self)
        about_action.triggered.connect(self.show_about2)
        help_menu.addAction(about_action)
    
    def on_solve_clicked(self):
        self.task_window = TaskSolver(self)
        self.hide()
        self.task_window.show()
    
    def on_create_clicked(self):
        self.task_window = TaskCreationWindow(self)
        self.hide()
        self.task_window.show()
    
    def show_about2(self):
        md = """#### **1. Режим "Редактор задач"**

1. **Введите название задачи** (например, "Задача 1").  
2. **Задайте параметры**:  
    Число элементов (например, `n = 5`).  
    Размер выборки (например, `k = 2`).  
    Или что-то другое, смотря что предусмотрено задачей.  
3. **Добавьте условия** (зависит от модуля):  
    Для карточных задач: масти, номиналы, ограничения и тд.  
    Подробнее про модули смотри в справке в самом модуле.  
4. **Дополнительные действия**:  
    *Сгенерировать условие* — автоматическое создание условия (можно редактировать).  
    *Удалить все условия* — очистка списка.  
5. **Сохраните задачу**:  
    Нажмите *"Сохранить в задачник"*.

#### **2. Режим "Решение задач"**

1. **Выберите задачу** из списка сохраненных.  
2. **Введите ответ** в одном из форматов:  
    Число (например, `10`).  
    Формула с операторами:  
        `C(n,k)` — сочетания, `A(n,k)` — размещения,  
        `F(n)` — факториал, `+`, `-`, `*`, `/`, `**`.  
3. **Некорректные условия**:  
    Если задача противоречива, ответ `0`.

#### **3. Важные примечания**

* Автосохранение: задачи сразу попадают в сборник.  
* Удаление условия: двойной клик по нему.  
* Сброс данных: кнопка *"Новая задача"* удаляет текущий прогресс.  
* При правильном решении задачи, в списке она выделяется зеленым цветом.  
* Есть возможность редактировать уже сохраненную задачу, достаточно выбрать ее в списке в режиме редактирования.  
* Уже ненужную задачу можно удалить, нажав del при выбранной в списке задаче."""

        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Общие сведения")
        msg_box.setText(markdown(md))
        msg_box.setStyleSheet("QLabel{font-size: 18px; ; min-width: 550px;}")
        msg_box.exec()

    def show_about1(self):
        md = """**Название тренажера**: CTasks  
**Версия**: 1.1  
**Разработчики**: Сабалиров М.З., Беннер В.А.  
**Руководитель**: Поздняков С.Н.

**1. Общая информация**  
Тренажёр предназначен для изучения и практики комбинаторики. Он включает в себя два режима:

* **Редактор задач** — создание собственных комбинаторных задач.  
* **Решение задач** — выполнение заданий из сохранённых сборников (в том числе и сохраненные свои задачи).

#### **2. Начало работы**

1. **Выберите режим**:  
          Редактор задач — для создания новых заданий.  
          Решение задач — для тренировки на готовых примерах.  
2. **Выберите модуль**:  
           Работа с картами, словами, числами и др."""
        QMessageBox.about(self, "О программе", markdown(md))


if __name__ == "__main__":
    os.environ['GDK_BACKEND'] = 'x11'
    app = QApplication([])
    app.setWindowIcon(QIcon(resource_path(os.path.join("ui", "ico.ico"))))
    app.setStyle(QStyleFactory.create("Fusion"))
    window = MainMenu()
    window.show()
    app.exec()