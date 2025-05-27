# CTasks -- тренажер по комбинаторике
CTasks позволяет как решать задания по комбинаторике, так и создавать собственные задачи, при помощи встроенных редакторов задач

Авторы: Сабалиров М.З, Беннер В.А.

## Быстрый старт (готовое приложение, без исходников)
1. Откройте актуальный [релиз](https://github.com/MikelazDotPy/CTasks/releases/tag/v1.1)
2. Нажмите на архив с **названием (вашей ОС)**:
    - Windows: `CTasksWindows.zip`
    - Linux: `CTasksLinux.zip`
    - MacOS: `CTasksMacOS.zip`
3. Архив должен начать скачиваться
4. Распакуйте архив и запустите файл `CTasks`

## Запуск тренажера из исходников
1. Склонируйте репозиторий: `git clone https://github.com/MikelazDotPy/CTasks.git`
2. Зайдите в директорию репозитория
3. Создайте виртуальное окружение:
    - Windows: `python -m venv env`
        затем активируйте его:`env\Scripts\activate`
    - Linux/MacOS: `python3 -m venv env`
        затем `source env/bin/activate`
4. Установите зависимости: `pip install -r requirements.txt`
5. Запустите `main.py`:
    - Windows: `python main.py`
    - Linux/MacOS: `python3 main.py`

## Сборка приложения из исходников
1. Установите pyinstaller: `pip install pyinstaller`
2. Начните сборку: `pyinstaller --add-data "solvers:solvers" --add-data "ui:ui" --add-data "prototypes:prototypes" --add-data "tasks:tasks" --add-data "user:user" --add-data "task_solver.py:." --add-data "tasks_creator.py:." --collect-all ortools --collect-all PyQt6 --icon=ui/ico.ico  --name=CTasks --windowed --onedir main.py`
3. После завершения сборки передейдите в директорию `dist/CTasks`
4. Запустите исполняемый файл `CTasks` 