import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QAction, QStandardItem, QStandardItemModel
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QMenu,
    QTreeView,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 创建主窗口的布局
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # 创建 QTreeView
        self.tree_view = QTreeView()
        layout.addWidget(self.tree_view)

        # 创建一个模型
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["Item"])

        # 添加一些示例数据
        for i in range(5):
            parent_item = QStandardItem(f"Parent {i}")
            for j in range(3):
                child_item = QStandardItem(f"Child {i}.{j}")
                parent_item.appendRow(child_item)
            self.model.appendRow(parent_item)

        # 将模型设置给 tree_view
        self.tree_view.setModel(self.model)

        # 启用自定义上下文菜单
        self.tree_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tree_view.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, position):
        # 通过位置获取索引
        index = self.tree_view.indexAt(position)

        if index.isValid():
            # 创建右键菜单
            menu = QMenu()

            # 添加 "Edit" 动作
            edit_action = QAction("Edit", self)
            edit_action.triggered.connect(lambda: self.edit_item(index))
            menu.addAction(edit_action)

            # 添加 "Delete" 动作
            delete_action = QAction("Delete", self)
            delete_action.triggered.connect(lambda: self.delete_item(index))
            menu.addAction(delete_action)

            # 在鼠标点击的位置显示菜单
            menu.exec(self.tree_view.viewport().mapToGlobal(position))

    def edit_item(self, index):
        item = self.model.itemFromIndex(index)
        if item:
            item.setText(f"Edited {item.text()}")

    def delete_item(self, index):
        item = self.model.itemFromIndex(index)
        if item:
            self.model.removeRow(index.row(), index.parent())


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())
