from pathlib import Path
from uuid import uuid4

from PySide6.QtCore import Qt
from PySide6.QtGui import QDrag
from PySide6.QtWidgets import QFileSystemModel, QMessageBox, QProgressBar, QTreeView
from typing_extensions import override

from app.utils.remote_file import RemoteFileModel


class DragDropTreeView(QTreeView):
    """带拖放功能的树视图"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.setSelectionBehavior(QTreeView.SelectionBehavior.SelectRows)
        self._progress_bar = None

    def check_local_file(self, path: str):
        """检查本地文件是否存在"""
        if not Path(path).exists():
            QMessageBox.critical(
                self,
                "错误",
                f"文件 {path} 不存在",
                QMessageBox.StandardButton.Ok,
            )
            return False
        if Path(path).is_dir():
            QMessageBox.warning(
                self,
                "警告",
                "暂不支持上传文件夹",
                QMessageBox.StandardButton.Ok,
            )
            return None
        return True

    def get_directory(self, path: str | Path) -> Path:
        """获取文件夹路径"""
        if Path(path).is_dir():
            return Path(path)
        return Path(path).parent

    def set_progress_bar(self, progress_bar: QProgressBar | None):
        """设置进度条"""
        self._progress_bar = progress_bar

    @override
    def startDrag(self, supportedActions: Qt.DropAction):
        """启用拖动操作"""
        index = self.currentIndex()
        if index.isValid():
            drag = QDrag(self)
            mime_data = self.model().mimeData([index])
            drag.setMimeData(mime_data)
            drag.exec(supportedActions)

    @override
    def dragEnterEvent(self, event):
        """处理拖放进入的事件"""
        event.accept()

    @override
    def dragMoveEvent(self, event):
        """处理拖放移动事件"""
        event.accept()

    @override
    def dropEvent(self, event):
        """处理释放拖放事件"""
        source_widget = event.source()
        target_index = self.indexAt(event.position().toPoint())

        if not target_index.isValid():
            event.ignore()
            return None

        if isinstance(source_widget, DragDropTreeView):
            source_index = source_widget.currentIndex()
            source_model = source_widget.model()
            target_model = self.model()
            if isinstance(source_model, QFileSystemModel) and isinstance(
                target_model, RemoteFileModel
            ):
                # 从本地文件系统拖拽至远程文件系统
                local_path = source_model.filePath(source_index)
                remote_path = target_model.get_full_path(target_index)
                if not self.check_local_file(local_path):
                    event.ignore()
                    return None
                remote_path = "/".join(remote_path.split("/")[:-1]) + "/"
                print(f"[INFO] 从 {local_path} 上传至 {remote_path} ...")
                if target_model.upload(
                    local_path, remote_path.removeprefix("/"), self._progress_bar
                ):
                    QMessageBox.information(
                        self,
                        "信息",
                        f"文件 {local_path} 上传到 {remote_path} 成功！",
                        QMessageBox.StandardButton.Ok,
                    )
                    target_model.fetchMore(target_index)
                else:
                    QMessageBox.critical(
                        self,
                        "错误",
                        f"文件 {local_path} 上传到 {remote_path} 失败！",
                        QMessageBox.StandardButton.Ok,
                    )

            elif isinstance(source_model, RemoteFileModel) and isinstance(
                target_model, QFileSystemModel
            ):
                # 从远程文件系统拖拽至本地文件系统
                local_path = target_model.filePath(target_index)
                remote_path = source_model.get_full_path(source_index)
                # 设置为文件夹路径，防止 local_path 为文件路径
                local_path = self.get_directory(local_path) / remote_path.split("/")[-1]
                print(f"[INFO] 从 {remote_path} 下载至 {local_path} ...")
                if source_model.download(
                    remote_path,
                    local_path,
                    self._progress_bar,
                ):
                    QMessageBox.information(
                        self,
                        "信息",
                        f"文件 {remote_path} 下载到 {local_path} 成功！",
                        QMessageBox.StandardButton.Ok,
                    )
                    # 为了刷新文件系统，创建一个临时文件，因为 Qt 无法强制刷新文件系统信息
                    local_path_temp = local_path.parent / uuid4().hex
                    local_path_temp.write_text("")
                    local_path_temp.unlink()
                else:
                    QMessageBox.critical(
                        self,
                        "错误",
                        f"文件 {remote_path} 下载到 {local_path} 失败！",
                        QMessageBox.StandardButton.Ok,
                    )
            else:
                event.ignore()
                return None

            event.accept()
        else:
            event.ignore()
