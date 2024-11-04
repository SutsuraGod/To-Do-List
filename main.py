import sys
import sqlite3
from mainWindow_ui import Ui_MainWindow as mainWindowUi
from categoriesWindow_ui import Ui_MainWindow as categoriesWindowUi
from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QMenu


class MyWidget(QMainWindow, mainWindowUi):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(575, 688)
        self.con = sqlite3.connect('to_do_list.sqlite')
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
                    IFNULL(tasks.picture, "Нет изображения"), categories.name FROM tasks
                    LEFT JOIN categories ON categories.id = tasks.category'''
            
            if cur_category == 0:
                result = cur.execute(query).fetchall()
            else:
                result = cur.execute(f'''{query} WHERE categories.id = {cur_category}''').fetchall()
            
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
        self.tasksTable.setRowCount(len(data))
        self.tasksTable.setColumnCount(len(data[0]))
        self.tasksTable.setHorizontalHeaderLabels(['ИД', 'Задача', 'Дата', 'Путь к картинке', 'Категория'])

        for i, row in enumerate(data):
            for j, col in enumerate(row):
                self.tasksTable.setItem(i, j, QTableWidgetItem(str(col)))

        self.tasksTable.resizeColumnsToContents()

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


def main():
    app = QApplication(sys.argv)
    mw = MyWidget()
    mw.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()