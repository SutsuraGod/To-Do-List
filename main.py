import sys
import sqlite3
from mainWindow_ui import Ui_MainWindow as mainWindowUi
from categoriesWindow_ui import Ui_MainWindow as categoriesWindowUi
from taskWidget_ui import Ui_Form as taskWidgetUi
from editTask_ui import Ui_MainWindow as editTaskUi
from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QMenu, QWidget, QSplitter, QVBoxLayout
from PyQt6.QtCore import Qt


class MyWidget(QMainWindow, mainWindowUi):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(575, 688)
        self.con = sqlite3.connect('to_do_list.sqlite')
        self.container_layout = 0
        self.taskWidgets = []
        cur = self.con.cursor()

        self.categoriesInTasks.addItems(['Все'] + [i[0] for i in cur.execute('SELECT name FROM categories').fetchall()])
        self.filterTasksButton.clicked.connect(self.to_filter)

        self.categoriesInEvents.addItems(['Все'] + [i[0] for i in cur.execute('SELECT name FROM categories').fetchall()])
        self.filterEventsButton.clicked.connect(self.to_filter)

        self.tab_changed(0)
        self.tabWidget.currentChanged.connect(self.tab_changed)

        self.editCategoryButtonInTasks.clicked.connect(self.edit_categories)
        self.editCategoryButtonInEvents.clicked.connect(self.edit_categories)

    def tab_changed(self, index):
        self.current_tab = index
        self.to_filter()

    def to_filter(self):
        cur = self.con.cursor()

        if self.current_tab == 0:
            cur_category = self.categoriesInTasks.currentIndex()

            query = '''SELECT tasks.id, tasks.name, tasks.date,
                    IFNULL(tasks.picture, "Нет изображения"), categories.name, tasks.completed FROM tasks
                    LEFT JOIN categories ON categories.id = tasks.category'''
            order = ''' ORDER BY tasks.completed'''
            
            if cur_category == 0:
                result = cur.execute(query + order).fetchall()
            else:
                result = cur.execute(f'''{query} WHERE categories.id = {cur_category}{order}''').fetchall()
            
            self.update_tasks(result)
        else:
            cur_category = self.categoriesInEvents.currentIndex()

            query = '''SELECT events.id, events.name, events.date,
                    events.time, categories.name FROM events
                    LEFT JOIN categories ON categories.id = events.category'''
            
            if cur_category == 0:
                result = cur.execute(query).fetchall()
            else:
                result = cur.execute(f'''{query} WHERE categories.id = {cur_category}''').fetchall()

            self.update_events(result)

    def update_tasks(self, data):
        if not self.container_layout:
            self.container_layout = QVBoxLayout(self.tasksContainer)
        else:
            self.clear_tasksContainer()
        self.taskWidgets = []
        for i in range(len(data)):
            if data[i][-1] == 1:
                completed = 1
            else:
                completed = 0
            widget = TaskForm(f'{data[i][1]}', completed)
            self.container_layout.addWidget(widget)
            self.taskWidgets.append(widget)
        self.container_layout.addWidget(QSplitter(Qt.Orientation.Vertical))

    def clear_tasksContainer(self):
        for i in reversed(range(self.container_layout.count())):
            widget = self.container_layout.itemAt(i).widget()
            if widget is not None:
                self.container_layout.removeWidget(widget)

    def update_events(self, data):
        self.eventsTable.setRowCount(len(data))
        self.eventsTable.setColumnCount(len(data[0]))
        self.eventsTable.setHorizontalHeaderLabels(['ИД', 'Событие', 'Дата', 'Время', 'Категория'])

        for i, row in enumerate(data):
            for j, col in enumerate(row):
                self.eventsTable.setItem(i, j, QTableWidgetItem(str(col)))

        self.eventsTable.resizeColumnsToContents()

    def edit_categories(self):
        self.edit_categories_widget = Categories(parent=self)
        self.edit_categories_widget.show()

    def add_task(self):
        pass

    def edit_task(self):
        pass

    def delete_task(self):
        pass

    def add_event(self):
        pass

    def edit_event(self):
        pass

    def delete_event(self):
        pass


class Categories(QMainWindow, categoriesWindowUi):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setFixedSize(494, 359)
        self.update_result()

    def update_result(self):
        cur = self.parent().con.cursor()
        query = 'SELECT * FROM categories'
        result = cur.execute(query).fetchall()

        self.categoriesTable.setColumnCount(len(result[0]))
        self.categoriesTable.setRowCount(len(result))
        self.categoriesTable.setHorizontalHeaderLabels(['ИД', 'Категория'])

        for i, row in enumerate(result):
            for j, col in enumerate(row):
                self.categoriesTable.setItem(i, j, QTableWidgetItem(str(col)))
        
        self.categoriesTable.resizeColumnsToContents()

    def add_category(self):
        pass

    def edit_category(self):
        pass

    def edit_category(self):
        pass


class TaskForm(QWidget, taskWidgetUi):
    def __init__(self, text, completed):
        super().__init__()
        self.setupUi(self)
        self.task.setText(text)
        if completed == 1:
            self.task.setStyleSheet("QCheckBox { text-decoration: line-through; }")
            self.task.setChecked(True)

        self.moreInfoButton.clicked.connect(self.edit_task)
        self.task.stateChanged.connect(self.set_style_sheet)

    def set_style_sheet(self):
        with sqlite3.connect('to_do_list.sqlite') as con:
            cur = con.cursor()
            if self.task.isChecked():
                query = f'''UPDATE tasks
                            SET completed = 1
                            WHERE name = "{self.task.text()}"'''
                cur.execute(query)
                self.task.setStyleSheet("QCheckBox { text-decoration: line-through; }")
            else:
                query = f'''UPDATE tasks
                            SET completed = 0
                            WHERE name = "{self.task.text()}"'''
                cur.execute(query)
                self.task.setStyleSheet("QCheckBox { text-decoration: none; }")

    def edit_task(self):
        self.edit_task_widget = TaskWidget(self)
        self.edit_task_widget.show()

    def get_text(self):
        self.task.text()


class TaskWidget(QMainWindow, editTaskUi):
    def __init__(self, parent=None):
        super().__init__()
        self.setupUi(self)


def main():
    app = QApplication(sys.argv)
    mw = MyWidget()
    mw.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()