import sys
import sqlite3

from mainWindow_ui import Ui_MainWindow as mainWindowUi
from categoriesWindow_ui import Ui_MainWindow as categoriesWindowUi
from taskWidget_ui import Ui_Form as taskWidgetUi
from editTask_ui import Ui_MainWindow as editTaskUi
from editCategory_ui import Ui_MainWindow as editCategoryUi
from editEvent_ui import Ui_MainWindow as editEventUi
from eventsDate_ui import Ui_Form as eventsDateUi
from eventWidget_ui import Ui_Form as eventWidgetUi

from PyQt6.QtWidgets import QMainWindow, QApplication, QTableWidgetItem, QMenu, QWidget, QSplitter, QVBoxLayout
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from PyQt6.QtCore import Qt, QDate
from PyQt6.QtGui import QPixmap, QImage


class MyWidget(QMainWindow, mainWindowUi):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setFixedSize(575, 688)
        self.con = sqlite3.connect('to_do_list.sqlite')

        self.container_layout_tasks = 0
        self.container_layout_events = 0

        self.taskWidgets = []
        self.eventWidgets = []

        self.update_combobox()

        self.tab_changed(0)
        self.tabWidget.currentChanged.connect(self.tab_changed)

        self.editCategoryButtonInTasks.clicked.connect(self.edit_categories)
        self.editCategoryButtonInEvents.clicked.connect(self.edit_categories)

        self.addTaskButton.clicked.connect(self.add_task)
        self.addEventButton.clicked.connect(self.add_event)

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

        if not self.container_layout_tasks:
            self.container_layout_tasks = QVBoxLayout(self.tasksContainer)
        else:
            self.clear_tasksContainer()

        self.taskWidgets = []
        for i in result:
            widget = TaskForm(f'{i[1]}', i, self)
            self.container_layout_tasks.addWidget(widget)
            self.taskWidgets.append(widget)
        self.container_layout_tasks.addWidget(QSplitter(Qt.Orientation.Vertical))

    def clear_tasksContainer(self):
        for i in reversed(range(self.container_layout_tasks.count())):
            widget = self.container_layout_tasks.itemAt(i).widget()
            if widget is not None:
                self.container_layout_tasks.removeWidget(widget)

    def update_events(self, result=None):
        if result is None:
            cur = self.con.cursor()
            query = '''SELECT * FROM events'''
            result = cur.execute(query).fetchall()

        if not self.container_layout_events:
            self.container_layout_events = QVBoxLayout(self.eventsContainer)
        else:
            self.clear_eventsContainer()

        result = self.sort_events(result)

        self.eventsWidget = []
        for i in result:
            date = eventsDate(i[0][2])
            self.container_layout_events.addWidget(date)
            self.eventsWidget.append(date)
            for j in i:
                widget = EventForm(f'{j[1]}', f'{j[3]}', j, self)
                self.container_layout_events.addWidget(widget)
                self.eventsWidget.append(widget)
        self.container_layout_events.addWidget(QSplitter(Qt.Orientation.Vertical))

    def clear_eventsContainer(self):
        for i in reversed(range(self.container_layout_events.count())):
            widget = self.container_layout_events.itemAt(i).widget()
            if widget is not None:
                self.container_layout_events.removeWidget(widget)

    def sort_events(self, data):
        data = sorted(data, key=lambda x: x[2])

        grouped_list = []
        current_date = None
        current_group = []

        for i in data:
            date = i[2]

            if date != current_date:
                if current_group:
                    grouped_list.append(sorted(current_group, key=lambda x: (int(x[3][:2]), int(x[3][3:5]))))
                current_group = [tuple(i)]
                current_date = date
            else:
                current_group.append(tuple(i))

        if current_group:
            grouped_list.append(sorted(current_group, key=lambda x: (int(x[3][:2]), int(x[3][3:5]))))
        
        return grouped_list

    def edit_categories(self):
        self.edit_categories_widget = Categories(parent=self)
        self.edit_categories_widget.show()

    def add_task(self):
        self.add_task_widget = TaskWidget(self)
        self.add_task_widget.show()

    def add_event(self):
        self.add_event_widget = EventWidget(self)
        self.add_event_widget.show()

    def update_combobox(self):
        self.categoriesInTasks.clear()
        self.categoriesInEvents.clear()
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

        self.categoriesTable.setColumnCount(1)
        self.categoriesTable.setRowCount(len(result))
        self.categoriesTable.setHorizontalHeaderLabels(['Категория'])

        for i, row in enumerate(result):
            self.categoriesTable.setItem(i, 0, QTableWidgetItem(str(row[1])))
        
        self.categoriesTable.resizeColumnsToContents()
        self.parent().update_combobox()

    def add_category(self):
        self.add_category_widget = editCategory(self)
        self.add_category_widget.show()

    def edit_category(self):
        rows = list(set([i.row() for i in self.categoriesTable.selectedItems()]))
        if rows and len(rows) == 1:
            self.statusBar().clearMessage()
            data = [self.categoriesTable.item(i, 0).text() for i in rows]
            self.edit_category_widget = editCategory(self, data)
            self.edit_category_widget.show()
        elif len(rows) > 1:
            self.statusBar().showMessage('Нужно выбрать только один элемент')
        else:
            self.statusBar().showMessage('Ничего не выбрано')

    def delete_category(self):
        rows = list(set([i.row() for i in self.categoriesTable.selectedItems()]))
        if rows and len(rows) == 1:
            self.statusBar().clearMessage()
            data = [self.categoriesTable.item(i, 0).text() for i in rows]
            if self.get_deleting_verdict(data[0]):
                valid = QMessageBox.question(
                    self, '', f"Действительно удалить категорию {data[0]}?",
                    buttons=QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            
                if valid == QMessageBox.StandardButton.Yes:
                    with sqlite3.connect('to_do_list.sqlite') as con:
                        cur = con.cursor()
                        cur.execute(f"DELETE FROM categories WHERE name = '{data[0]}'")
                        con.commit()
                        self.update_result()
                        self.parent().update_combobox()
            else:
                self.statusBar().showMessage('К этой категории прикреплены неудаленные задачи')
        elif len(rows) > 1:
            self.statusBar().showMessage('Нужно выбрать только один элемент')
        else:
            self.statusBar().showMessage('Ничего не выбрано')

    def contextMenuEvent(self, event):
        if self.categoriesTable.geometry().contains(self.mapFromGlobal(event.globalPos())):
            context_menu = QMenu(self)

            addAction = context_menu.addAction("Добавить")
            editAction = context_menu.addAction("Изменить")
            deleteAction = context_menu.addAction("Удалить")

            addAction.triggered.connect(self.add_category)
            editAction.triggered.connect(self.edit_category)
            deleteAction.triggered.connect(self.delete_category)

            context_menu.exec(event.globalPos())

    def get_deleting_verdict(self, category):
        with sqlite3.connect('to_do_list.sqlite') as con:
            cur = con.cursor()
            query = f'''SELECT name FROM tasks WHERE category = (SELECT id FROM categories WHERE name = "{category}")'''
            result = cur.execute(query).fetchall()
        if result:
            return False
        return True


class editCategory(QMainWindow, editCategoryUi):
    def __init__(self, parent=None, data=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setFixedSize(264, 138)

        if not data is None:
            self.pushButton.setText('Изменить')
            self.data = data
            self.pushButton.clicked.connect(self.edit_elem)
            self.get_elem()
        else:
            self.pushButton.setText('Добавить')
            self.pushButton.clicked.connect(self.add_elem)

    def add_elem(self):
        category = self.CategoryEdit.toPlainText()
        
        if self.get_adding_verdict(category):
            with sqlite3.connect('to_do_list.sqlite') as con:
                cur = con.cursor()

                query = f'''INSERT INTO categories(name)
                            VALUES("{category}")'''
                cur.execute(query)
                con.commit()
                self.close()
                self.parent().update_result()
        else:
            self.statusBar().showMessage('Неверно заполнена форма')

    def edit_elem(self):
        category = self.CategoryEdit.toPlainText()

        if self.get_editing_verdict(category):
            with sqlite3.connect('to_do_list.sqlite') as con:
                cur = con.cursor()

                query = f'''UPDATE categories
                            SET name = "{category}"
                            WHERE name = "{self.data[0]}"'''
                cur.execute(query)
                con.commit()
                self.close()
                self.parent().update_result()
        else:
            self.statusBar().showMessage('Неверно заполнена форма')

    def get_adding_verdict(self, category):
        if category.strip():
            return True
        return False

    def get_editing_verdict(self, category):
        if category.strip():
            return True
        return False

    def get_elem(self):
        self.CategoryEdit.setPlainText(self.data[0])


class TaskForm(QWidget, taskWidgetUi):
    def __init__(self, text, data, parent=None):
        super().__init__()
        self.parent = parent
        self.setupUi(self)
        self.task.setText(text)
        self.data = data
        if self.data[-1] == 1:
            self.task.setStyleSheet("QCheckBox { text-decoration: line-through; }")
            self.task.setChecked(True)

        self.tasksMoreInfoButton.clicked.connect(self.edit_task)
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
        super().__init__()
        self.parent = parent
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
        date = self.date.date().toString('dd.MM.yyyy')
        category = self.category.currentText()

        if self.get_adding_verdict():
            with sqlite3.connect('to_do_list.sqlite') as con:
                cur = con.cursor()
                if not self.way_to_picture is None:
                    query = f'''INSERT INTO tasks(name, date, picture, category, completed)
                            VALUES("{name}", "{date}", "{self.way_to_picture}",
                            (SELECT id FROM categories WHERE name = '{category}'), {0})'''
                else:
                    query = f'''INSERT INTO tasks(name, date, category, completed)
                        VALUES ("{name}", "{date}",
                        (SELECT id FROM categories WHERE name = '{category}'), {0})'''
                cur.execute(query)
                con.commit()
                self.close()
                self.parent().to_filter()
        else:
            self.statusBar().showMessage('Неверно заполнена форма')

    def edit_elem(self):
        name = self.name.toPlainText()
        date = self.date.date().toString('dd.MM.yyyy')
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
        date = self.date.date().toString('dd.MM.yyyy')

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

        if name.strip() == '':
            return False

        return True

    def get_editing_verdict(self):
        name = self.name.toPlainText()

        if name.strip() == '':
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
        self.date.setDate(QDate.fromString(self.data[2], 'dd.MM.yyyy'))
        self.category.setCurrentIndex(int(self.data[4]) - 1)


class EventForm(QWidget, eventWidgetUi):
    def __init__(self, text, time, data, parent=None):
        super().__init__()
        self.parent = parent
        self.setupUi(self)
        self.event.setText(f'{text} ({time})')
        self.data = data

        self.eventsMoreInfoButton.clicked.connect(self.edit_event)

    def edit_event(self):
        self.edit_event_widget = EventWidget(self.data, self.parent)
        self.edit_event_widget.show()


class eventsDate(QWidget, eventsDateUi):
    def __init__(self, date, parent=None):
        super().__init__()
        self.parent = parent
        self.setupUi(self)
        self.label.setText(date)
        self.label.setStyleSheet("color: black; font-size: 18px; font-weight: bold;")


class EventWidget(QMainWindow, editEventUi):
    def __init__(self,  data=None, parent=None):
        super().__init__()
        self.parent = parent
        self.setupUi(self)
        self.setFixedSize(415, 269)
        self.data = data


def main():
    app = QApplication(sys.argv)
    mw = MyWidget()
    mw.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()