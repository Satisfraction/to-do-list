import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QLineEdit, QVBoxLayout, QHBoxLayout, QListWidget, QInputDialog, QFileDialog

class ToDoList(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('To-Do List')

        # Create widgets
        task_label = QLabel('Enter a new task:')
        self.task_input = QLineEdit()
        add_button = QPushButton('Add Task')
        add_button.clicked.connect(self.add_task)
        self.task_list = QListWidget()
        delete_button = QPushButton('Delete Selected Task')
        delete_button.clicked.connect(self.delete_task)
        edit_button = QPushButton('Edit Selected Task')
        edit_button.clicked.connect(self.edit_task)
        save_button = QPushButton('Save List')
        save_button.clicked.connect(self.save_list)
        load_button = QPushButton('Load List')
        load_button.clicked.connect(self.load_list)
        sort_button = QPushButton('Sort Tasks')
        sort_button.clicked.connect(self.sort_tasks)

        # Add widgets to layout
        input_layout = QHBoxLayout()
        input_layout.addWidget(task_label)
        input_layout.addWidget(self.task_input)
        input_layout.addWidget(add_button)
        input_layout.addWidget(delete_button)
        input_layout.addWidget(edit_button)
        input_layout.addWidget(save_button)
        input_layout.addWidget(load_button)
        input_layout.addWidget(sort_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(input_layout)
        main_layout.addWidget(self.task_list)

        # Set layout and show window
        self.setLayout(main_layout)
        self.show()

    def add_task(self):
        task = self.task_input.text()
        if task:
            self.task_input.clear()
            priority, ok = QInputDialog.getItem(self, 'Add Task', 'Select priority level:', ['Low', 'Medium', 'High'])
            priority = {'Low': 1, 'Medium': 2, 'High': 3}[priority]

            if ok:
                priority_str = {1: 'Low', 2: 'Medium', 3: 'High'}[priority]
                self.task_list.addItem(f"{task} ({priority_str})")
            
    def delete_task(self):
        selected_items = self.task_list.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            self.task_list.takeItem(self.task_list.row(item))    
    
    def edit_task(self):
        selected_items = self.task_list.selectedItems()
        if not selected_items:
            return
        for item in selected_items:
            old_task = item.text()
            task, priority = old_task.split(" (")
            priority = priority.strip(")").capitalize()
            new_task, ok = QInputDialog.getText(self, 'Edit Task', 'Enter new task:', QLineEdit.Normal, task)
            if ok and new_task != '':
                priority_str, ok = QInputDialog.getItem(self, 'Edit Task', 'Select priority level:', ['Low', 'Medium', 'High'])
                if ok:
                    priority = {"Low": 1, "Medium": 2, "High": 3}[priority_str]
                    new_task += f" ({priority_str})"
                    item.setText(new_task)

    def sort_tasks(self):
        items = [(self.task_list.item(i).text(), i) for i in range(self.task_list.count())]
        priority_map = {"Low": 1, "Medium": 2, "High": 3}
        items.sort(key=lambda x: priority_map[x[0].split('(')[-1].strip(')')], reverse=True)

        for i in range(len(items)):
            self.task_list.insertItem(i, items[i][0])
            self.task_list.takeItem(items[i][1]+1)
    
    def save_list(self):
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save To-Do List', '', 'Text Files (*.txt)')
        if file_name:
            with open(file_name, 'w') as f:
                for i in range(self.task_list.count()):
                    f.write(self.task_list.item(i).text() + '\n')
    
    def load_list(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Load To-Do List', '', 'Text Files (*.txt)')
        if file_name:
            with open(file_name, 'r') as f:
                for line in f:
                    self.task_list.addItem(line.strip())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    todo = ToDoList()
    sys.exit(app.exec_())
