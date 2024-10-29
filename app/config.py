import json
import os
from pathlib import Path
from typing import NotRequired, TypedDict


class GlobalConfig:
    ACCESS_KEY_ID = os.environ.get("OSS_ACCESS_KEY_ID", "")
    ACCESS_KEY_SECRET = os.environ.get("OSS_ACCESS_KEY_SECRET", "")
    BUCKET_NAME = "alex-share"
    ENDPOINT = "oss-cn-shanghai.aliyuncs.com"
    CNAME = "https://oss.alexsun.top"


class OSSConfigDict(TypedDict):
    access_key_id: str
    access_key_secret: str
    endpoint: str
    bucket_name: str
    cname: NotRequired[str | None]


def load_config() -> OSSConfigDict:
    if Path("./resources/config.json").exists():
        with open("./resources/config.json", "r") as f:
            return json.load(f)
    else:
        return {
            "access_key_id": GlobalConfig.ACCESS_KEY_ID,
            "access_key_secret": GlobalConfig.ACCESS_KEY_SECRET,
            "endpoint": GlobalConfig.ENDPOINT,
            "bucket_name": GlobalConfig.BUCKET_NAME,
            "cname": GlobalConfig.CNAME,
        }


def save_config(config: OSSConfigDict):
    with open("./resources/config.json", "w") as f:
        json.dump(config, f, indent=4)
