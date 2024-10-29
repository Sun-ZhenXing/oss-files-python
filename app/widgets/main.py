from PySide6.QtCore import QDir, QModelIndex, QPoint, Qt, Slot
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QFileSystemModel,
    QMainWindow,
    QMenu,
    QMessageBox,
    QProgressBar,
    QWidget,
)

from app.config import load_config
from app.ui.main_ui import Ui_MainWindow
from app.utils.remote import OSSManager
from app.utils.remote_file import RemoteFileModel


class MainWidget(QMainWindow):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)

        ui = Ui_MainWindow()
        ui.setupUi(self)
        self._ui = ui

        self.load_local_files()
        self.load_remote_files()

        progress_bar = QProgressBar()
        self._ui.statusbar.addPermanentWidget(progress_bar)
        self._progress_bar = progress_bar
        self._ui.localTreeView.set_progress_bar(progress_bar)
        self._ui.remoteTreeView.set_progress_bar(progress_bar)

    def _set_local_root_dir(self, path: str):
        """设置本地文件的根目录"""
        self._local_file_model.setRootPath(path)
        self._ui.localTreeView.setRootIndex(self._local_file_model.index(path))
        self._ui.rootDirLineEdit.setText(path)

    def _get_download_link(self, index: QModelIndex):
        """获取下载链接"""
        path = self._remote_file_model.get_full_path(index)
        if path.endswith("/"):
            QMessageBox.warning(
                self,
                "错误",
                "文件夹没有下载链接",
                QMessageBox.StandardButton.Ok,
            )
            return None
        link = self._remote_file_model.get_link(index)
        clipboard = QApplication.clipboard()
        clipboard.setText(link)
        QMessageBox.information(
            self,
            "成功",
            "复制下载链接成功",
            QMessageBox.StandardButton.Ok,
        )

    def _delete(self, index: QModelIndex):
        """删除文件"""
        path = self._remote_file_model.get_full_path(index)
        if path.endswith("/"):
            QMessageBox.warning(
                self,
                "错误",
                "文件夹不能删除",
                QMessageBox.StandardButton.Ok,
            )
            return None
        if self._remote_file_model.delete(index):
            QMessageBox.information(
                self,
                "成功",
                f"删除 {path} 成功",
                QMessageBox.StandardButton.Ok,
            )
        else:
            QMessageBox.warning(
                self,
                "错误",
                f"删除 {path} 失败",
                QMessageBox.StandardButton.Ok,
            )

    def _show_context_menu(self, position: QPoint):
        """显示右键菜单"""
        index = self._ui.remoteTreeView.indexAt(position)
        if index.isValid():
            # 创建右键菜单
            menu = QMenu()

            link_action = QAction("复制下载链接", self)
            link_action.triggered.connect(lambda: self._get_download_link(index))
            menu.addAction(link_action)

            delete_action = QAction("删除", self)
            delete_action.triggered.connect(lambda: self._delete(index))
            menu.addAction(delete_action)

            menu.exec(self._ui.remoteTreeView.viewport().mapToGlobal(position))

    def load_local_files(self):
        """加载本地文件"""
        default_dir = QDir.homePath()
        self._local_file_model = QFileSystemModel()
        self._local_file_model.setRootPath(default_dir)
        self._ui.localTreeView.setModel(self._local_file_model)
        self._ui.localTreeView.setRootIndex(self._local_file_model.index(default_dir))
        self._ui.rootDirLineEdit.setText(default_dir)

    def load_remote_files(self):
        """加载远程文件"""
        self._remote_file_model = RemoteFileModel(
            OSSManager.from_config(load_config()),
        )
        self._ui.remoteTreeView.setModel(self._remote_file_model)
        self._remote_file_model.load()
        self._ui.remoteTreeView.expanded.connect(self._remote_file_model.fetchMore)
        # 设置上下文菜单
        self._ui.remoteTreeView.setContextMenuPolicy(
            Qt.ContextMenuPolicy.CustomContextMenu
        )
        self._ui.remoteTreeView.customContextMenuRequested.connect(
            self._show_context_menu
        )

    @Slot()
    def reloadFiles(self):
        """重新加载远程文件"""
        self._remote_file_model.clear()
        self._remote_file_model.load()

    @Slot()
    def selectRoot(self):
        """选择本地文件的根目录"""
        path = QFileDialog.getExistingDirectory(self, "选择文件夹", QDir.homePath())
        if path:
            self._set_local_root_dir(path)

    @Slot()
    def changeRoot(self):
        """回车事件修改本地文件的根目录"""
        self._set_local_root_dir(self._ui.rootDirLineEdit.text())
