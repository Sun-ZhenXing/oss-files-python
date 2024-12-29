from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Callable

import oss2
from oss2.models import SimplifiedObjectInfo

from app.config import OSSConfigDict


@dataclass
class RemoteFile:
    name: str
    size: int | None = None
    is_dir: bool = False
    type: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None
    raw: object | None = None


class RemoteFileManager(ABC):
    @abstractmethod
    def upload_file(
        self,
        filename: str,
        remote_path: str,
        callback: Callable[[int, int], None] | None = None,
    ) -> bool: ...

    @abstractmethod
    def download_file(
        self,
        remote_path: str,
        filename: str,
        callback: Callable[[int, int], None] | None = None,
    ) -> bool: ...

    @abstractmethod
    def list_files(self, prefix: str = "") -> list[RemoteFile]: ...

    @abstractmethod
    def remove_file(self, remote_path: str) -> bool: ...

    @abstractmethod
    def copy_file(self, src: str, dst: str) -> bool: ...

    @abstractmethod
    def move_file(self, src: str, dst: str) -> bool: ...

    @abstractmethod
    def get_download_link(self, remote_path: str, expires: int = 3600) -> str: ...


class OSSManager(RemoteFileManager):
    """阿里云 OSS 文件"""

    def __init__(
        self,
        bucket: oss2.Bucket,
        cname_bucket: oss2.Bucket | None = None,
    ) -> None:
        self._bucket = bucket
        # V2 API 目前有许多 BUG，使用 cname_bucket 过渡
        self._cname_bucket = cname_bucket or bucket

    @staticmethod
    def from_config(d: OSSConfigDict) -> "OSSManager":
        """从配置文件中创建 OSSManager"""
        access_key_id = d["access_key_id"]
        access_key_secret = d["access_key_secret"]
        endpoint = d["endpoint"]
        bucket_name = d["bucket_name"]
        cname = d["cname"] if "cname" in d else None

        auth = oss2.Auth(access_key_id, access_key_secret)
        bucket = oss2.Bucket(
            auth=auth,
            endpoint=endpoint,
            bucket_name=bucket_name,
        )
        cname_bucket = oss2.Bucket(
            auth=auth,
            endpoint=cname or endpoint,
            bucket_name=bucket_name,
            is_cname=cname is not None,
        )
        return OSSManager(bucket, cname_bucket)

    def upload_file(
        self,
        filename: str,
        remote_path: str,
        callback: Callable[[int, int], None],
    ) -> bool:
        """上传文件到 OSS"""
        with open(filename, "rb") as f:
            result = self._bucket.put_object(remote_path, f, progress_callback=callback)
        return result.status in range(200, 300)

    def download_file(
        self,
        remote_path: str,
        filename: str,
        callback: Callable[[int, int], None] | None = None,
    ) -> bool:
        """下载文件"""
        result = self._cname_bucket.get_object_to_file(
            remote_path,
            filename,
            progress_callback=callback,
        )
        return result.status in range(200, 300)

    def list_files(self, prefix: str = "") -> list[RemoteFile]:
        """列出文件"""
        if not prefix.endswith("/"):
            prefix += "/"
        prefix = prefix.removeprefix("/")
        files = oss2.ObjectIteratorV2(
            self._bucket,
            prefix=prefix,
            delimiter="/",
        )
        result: list[RemoteFile] = []
        for obj in files:
            obj: SimplifiedObjectInfo
            key: str = obj.key
            if key == prefix:
                continue
            if key.startswith(prefix):
                result.append(
                    RemoteFile(
                        name=key.removeprefix(prefix),
                        size=obj.size,
                        is_dir=obj.is_prefix(),
                        type=obj.type,
                        created_at=datetime.fromtimestamp((obj.last_modified or 0)),
                        updated_at=datetime.fromtimestamp((obj.last_modified or 0)),
                        raw=obj,
                    )
                )
        result.sort(key=lambda x: (not x.is_dir, x.name))
        print("[INFO] list_files:", prefix, result)
        return result

    def remove_file(self, remote_path: str) -> bool:
        """删除文件"""
        result = self._bucket.delete_object(remote_path)
        return result.status in range(200, 300)

    def copy_file(self, src: str, dst: str) -> bool:
        """复制文件"""
        result = self._bucket.copy_object(self._bucket.bucket_name, src, dst)
        return result.status in range(200, 300)

    def move_file(self, src: str, dst: str) -> bool:
        """移动文件"""
        if self.copy_file(src, dst):
            return self.remove_file(src)
        return False

    def get_download_link(self, remote_path: str, expires: int = 3600) -> str:
        """获取文件的下载链接"""
        return self._cname_bucket.sign_url(
            "GET",
            key=remote_path,
            expires=expires,
            slash_safe=True,
        )
