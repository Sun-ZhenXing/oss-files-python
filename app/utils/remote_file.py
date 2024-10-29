import traceback
from pathlib import Path

from PySide6.QtCore import QModelIndex, Qt
from PySide6.QtGui import QIcon, QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QApplication, QProgressBar, QStyle
from typing_extensions import override

from app.utils.remote import RemoteFile, RemoteFileManager


class RemoteFileModel(QStandardItemModel):
    def __init__(self, manager: RemoteFileManager) -> None:
        super().__init__()
        self._manager = manager

    def _create_item(self, f: RemoteFile | None = None, is_folder: bool = False):
        """创建文件树节点"""
        item = QStandardItem(f.name if f else "")
        item.setEditable(False)
        icon = (
            QStyle.StandardPixmap.SP_DirIcon
            if is_folder
            else QStyle.StandardPixmap.SP_FileIcon
        )
        item.setData(f, Qt.ItemDataRole.UserRole)
        item.setIcon(QIcon(QApplication.style().standardIcon(icon)))
        return item

    def _file_size_to_str(self, size: int | None = None) -> str:
        """将文件大小转换为字符串"""
        if size is None:
            return ""
        if size < 1024:
            return f"{size} B"
        elif size < 1024**2:
            return f"{size / 1024:.2f} KB"
        elif size < 1024**3:
            return f"{size / 1024 ** 2:.2f} MB"
        else:
            return f"{size / 1024 ** 3:.2f} GB"

    def _create_row(self, item: QStandardItem, f: RemoteFile):
        """创建文件树行"""
        size_item = QStandardItem(self._file_size_to_str(f.size))
        size_item.setEditable(False)
        size_item.setTextAlignment(Qt.AlignmentFlag.AlignRight)
        type_item = QStandardItem(str(f.type))
        type_item.setEditable(False)
        updated_at_item = QStandardItem(
            str(f.updated_at and f.updated_at.strftime("%Y-%m-%d %H:%M:%S"))
        )
        updated_at_item.setEditable(False)
        return [
            item,
            size_item,
            type_item,
            updated_at_item,
        ]

    def populate_tree(self, files: list[RemoteFile]):
        """填充文件树"""
        for f in files:
            if f.name.endswith("/"):
                item = self._create_item(f, is_folder=True)
                item.appendRow(self._create_item())  # 插入占位符
                self.appendRow(item)
            else:
                item = self._create_item(f)
                self.appendRow(self._create_row(item, f))

    def get_full_path(self, index: QModelIndex) -> str:
        """获取文件的完整路径"""
        path = []
        index = self.index(index.row(), 0, index.parent())
        while index.isValid():
            path.append(index.data())
            index = index.parent()
        return "".join(reversed(path))

    def get_index_from_path(self, path: str) -> QModelIndex:
        """获取文件路径对应的索引"""
        path_parts = path.removeprefix("/").split("/")
        index = QModelIndex()
        for name in path_parts:
            for row in range(self.rowCount(index)):
                child = self.index(row, 0, index)
                if child.data() == name:
                    index = child
                    break
        return index

    @override
    def fetchMore(self, index: QModelIndex):
        """更新文件树"""
        if not index.isValid():
            return None

        item = self.itemFromIndex(index)
        if not item or not item.data(Qt.ItemDataRole.UserRole):
            return None

        path = self.get_full_path(index)
        if "/" not in path.removeprefix("/"):
            self.load()
            return None

        if not path.endswith("/"):
            path = "/".join(path.split("/")[:-1]) + "/"
            item = self.itemFromIndex(index.parent())

        sub_items = self._manager.list_files(path)
        item.removeRows(0, item.rowCount())  # 移除占位符子项

        for sub_item in sub_items:
            if sub_item.name == path:
                continue
            if sub_item.name.endswith("/"):
                child_item = self._create_item(sub_item, is_folder=True)
                child_item.appendRow(self._create_item())  # 插入占位符
                item.appendRow(child_item)
            else:
                child_item = self._create_item(sub_item)
                item.appendRow(self._create_row(child_item, sub_item))

    @override
    def mimeData(self, indexes):
        rows = set(index.row() for index in indexes)
        indexes = [self.index(row, 0) for row in rows]
        return super().mimeData(indexes)

    def load(self):
        """加载初始文件树"""
        print("[INFO] Loading remote files ...")
        self.clear()
        items = self._manager.list_files()
        self.populate_tree(items)
        self.setHorizontalHeaderLabels(["名称", "体积", "类型", "修改时间"])

    def upload(
        self,
        f: str | Path,
        target_folder: str | None = None,
        progress_bar: QProgressBar | None = None,
    ) -> bool:
        """将本地文件上传到指定的远程文件夹中"""
        file_name = Path(f).name
        target_path = (
            f"{target_folder.removesuffix('/')}/{file_name}"
            if target_folder
            else file_name
        )

        def _callback(curr: int, total: int):
            QApplication.processEvents()
            if progress_bar is not None:
                progress_bar.setValue(int((curr / total) * 100))

        try:
            return self._manager.upload_file(
                str(f),
                target_path,
                callback=_callback,
            )
        except Exception:
            traceback.print_exc()
            return False

    def download(
        self,
        remote_file: str,
        local_path: str | Path,
        progress_bar: QProgressBar | None = None,
    ) -> bool:
        """将远程文件下载到本地"""

        def _callback(curr: int, total: int):
            QApplication.processEvents()
            if progress_bar is not None:
                progress_bar.setValue(int((curr / total) * 100))

        try:
            return self._manager.download_file(
                remote_file,
                str(local_path),
                callback=_callback,
            )
        except Exception:
            traceback.print_exc()
            return False

    def get_link(self, index: QModelIndex) -> str:
        """获取文件下载链接"""
        index = self.index(index.row(), 0, index.parent())
        path = self.get_full_path(index)
        if path.endswith("/"):
            return ""
        print(f"[INFO] Getting download link for {path}")
        link = self._manager.get_download_link(path)
        return link

    def delete(self, index: QModelIndex) -> bool:
        """删除远程文件"""
        path = self.get_full_path(index)
        if path.endswith("/"):
            return False
        print(f"[INFO] Deleting file {path}")
        result = self._manager.remove_file(path)
        if result:
            self.fetchMore(index)
        return result
