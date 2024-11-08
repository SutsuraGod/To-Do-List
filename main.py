import sys
import sqlite3
import re

from mainWindow_ui import Ui_MainWindow as mainWindowUi
from categoriesWindow_ui import Ui_MainWindow as categoriesWindowUi
from taskWidget_ui import Ui_Form as taskWidgetUi
from editTask_ui import Ui_MainWindow as editTaskUi

from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QMenu, QWidget, QSplitter, QVBoxLayout
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QImage


class MyWidget(QMainWindow, mainWindowUi):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(575, 688)
        self.con = sqlite3.connect('to_do_list.sqlite')
        self.container_layout = 0
        self.taskWidgets = []
        self.update_combobox()

        self.tab_changed(0)
        self.tabWidget.currentChanged.connect(self.tab_changed)

        self.editCategoryButtonInTasks.clicked.connect(self.edit_categories)
        self.editCategoryButtonInEvents.clicked.connect(self.edit_categories)

        self.addTaskButton.clicked.connect(self.add_task)

    def tab_changed(self, index):
        self.current_tab = index
        self.to_filter()

    def to_filter(self):
        cur = self.con.cursor()

        if self.current_tab == 0:
            cur_category = self.categoriesInTasks.currentIndex()
            query = '''SELECT tasks.id, tasks.name, tasks.date,
                    tasks.picture, tasks.category, tasks.completed FROM tasks
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

    def update_tasks(self, result=None):
        if result is None:
            cur = self.con.cursor()
            query = '''SELECT * FROM tasks'''
            result = cur.execute(query).fetchall()

        if not self.container_layout:
            self.container_layout = QVBoxLayout(self.tasksContainer)
        else:
            self.clear_tasksContainer()

        self.taskWidgets = []
        for i in range(len(result)):
            widget = TaskForm(f'{result[i][1]}',result[i], self)
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
        self.add_task_widget = TaskWidget(self)
        self.add_task_widget.show()

    def add_event(self):
        pass

    def edit_event(self):
        pass

    def delete_event(self):
        pass


    def update_combobox(self):
        cur = self.con.cursor()
        self.categoriesInTasks.addItems(['Все'] + [i[0] for i in cur.execute('SELECT name FROM categories').fetchall()])
        self.filterTasksButton.clicked.connect(self.to_filter)

        self.categoriesInEvents.addItems(['Все'] + [i[0] for i in cur.execute('SELECT name FROM categories').fetchall()])
        self.filterEventsButton.clicked.connect(self.to_filter)


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
    def __init__(self, text, data, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setupUi(self)
        self.task.setText(text)
        self.data = data
        if self.data[-1] == 1:
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
        self.edit_task_widget = TaskWidget(self.parent, self.data)
        self.edit_task_widget.show()

    def get_text(self):
        self.task.text()


class TaskWidget(QMainWindow, editTaskUi):
    def __init__(self,  parent=None, data=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setFixedSize(429, 505)
        self.way_to_picture = None

        with sqlite3.connect('to_do_list.sqlite') as con:
            cur = con.cursor()
            self.category.addItems([i[0] for i in cur.execute('SELECT name FROM categories').fetchall()])

        if not data is None:
            self.editTaskButton.clicked.connect(self.edit_elem)
            self.data = data
            self.get_elem()

            if not self.data[3] is None:
                self.picture.setText('Изменить картинку')
                self.way_to_picture = self.data[3]
                self.set_image(self.way_to_picture)
            else: 
                self.picture.setText('Добавить картинку')
            
            self.deleteTaskButton.clicked.connect(self.delete_elem)

        else:
            self.editTaskButton.setText('Добавить')
            self.picture.setText('Добавить картинку')
            self.deleteTaskButton.setText('Закрыть')
            self.editTaskButton.clicked.connect(self.add_elem)
            self.deleteTaskButton.clicked.connect(self.close)

        self.picture.clicked.connect(self.choose_picture)

    def add_elem(self):
        name = self.name.toPlainText()
        date = self.date.text()
        category = self.category.currentIndex()

        if self.get_adding_verdict():
            with sqlite3.connect('to_do_list.sqlite') as con:
                cur = con.cursor()
                if not self.way_to_picture is None:
                    query = f'''INSERT INTO tasks(name, date, picture, category, completed)
                            VALUES("{name}", "{date}", "{self.way_to_picture}", {category + 1}, {0})'''
                else:
                    query = f'''INSERT INTO tasks(name, date, category, completed)
                            VALUES("{name}", "{date}", {category + 1}, {0})'''
                cur.execute(query)
                con.commit()
                self.close()
                self.parent().to_filter()
        else:
            self.statusBar().showMessage('Неверно заполнена форма')

    def edit_elem(self):
        name = self.name.toPlainText()
        date = self.date.text()
        category = self.category.currentIndex()

        if self.get_adding_verdict():
            with sqlite3.connect('to_do_list.sqlite') as con:
                cur = con.cursor()
                if not self.way_to_picture is None:
                    query = f'''UPDATE tasks
                            SET name = "{name}", date = "{date}", picture = "{self.way_to_picture}", category = {category + 1}
                            WHERE id = {self.data[0]}'''
                else:
                    query = f'''UPDATE tasks
                            SET name = "{name}", date = "{date}", category = {category + 1}
                            WHERE id = {self.data[0]}'''
                cur.execute(query)
                con.commit()
                self.close()
                self.parent().to_filter()
        else:
            self.statusBar().showMessage('Неверно заполнена форма')

    def delete_elem(self):
        name = self.name.toPlainText()
        date = self.date.text()

        valid = QMessageBox.question(
            self, '', f"Действительно удалить задачу {name}, {date}",
            buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if valid == QMessageBox.StandardButton.Yes:
            with sqlite3.connect('to_do_list.sqlite') as con:
                cur = con.cursor()
                cur.execute(f"DELETE FROM tasks WHERE name = '{name}' AND date = '{date}'")
                con.commit()
                self.close()
        self.parent().update_tasks()

    def get_adding_verdict(self):
        name = self.name.toPlainText()
        date = self.date.text()
        day_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        if name.strip() == '':
            return False
        
        if date.strip() == '':
            return False
        
        if not re.fullmatch(r'\d{2}\.\d{2}\.\d{4}', date):
            return False

        if int(date.split('.')[1]) > 12:
            return False

        if int(date.split('.')[0]) > day_in_month[int(date.split('.')[1]) - 1]:
            return False
        
        return True

    def get_editing_verdict(self):
        name = self.name.toPlainText()
        date = self.date.text()
        day_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

        if name.strip() == '':
            return False
        
        if date.strip() == '':
            return False
        
        if not re.fullmatch(r'\d{2}\.\d{2}\.\d{4}', date):
            return False

        if int(date.split('.')[1]) > 12:
            return False

        if int(date.split('.')[0]) > day_in_month[int(date.split('.')[1]) - 1]:
            return False
        
        return True

    def update_pixmap(self, pixmap):
        scaled_pixmap = pixmap.scaled(
            self.image.size(), 
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.image.setPixmap(scaled_pixmap)

    def set_image(self, picture):
        self.pixmap = QPixmap(QImage(picture))
        self.image.setPixmap(self.pixmap)
        self.update_pixmap(self.pixmap)

    def choose_picture(self):
        picture = QFileDialog.getOpenFileName(self, 'Выбрать картинку', '')[0]
        if picture:
            self.way_to_picture = picture
            self.set_image(self.way_to_picture)

    def get_elem(self):
        self.name.setPlainText(self.data[1]) 
        self.date.setText(self.data[2])
        self.category.setCurrentIndex(int(self.data[4]) - 1)


def main():
    app = QApplication(sys.argv)
    mw = MyWidget()
    mw.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()