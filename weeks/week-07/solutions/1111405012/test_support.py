from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType


BASE_DIR = Path(__file__).resolve().parent


def load_module_from_path(file_path: Path, module_name: str) -> ModuleType:
    """從指定路徑載入模組，讓測試可以直接讀取帶有連字號的檔名。"""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    if spec is None or spec.loader is None:
        raise ImportError(f"無法載入模組：{file_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_topic_versions(stem: str) -> dict[str, ModuleType]:
    """一次載入 beginner、easy、su 三個版本。"""
    paths = {
        "beginner": BASE_DIR / f"{stem}.py",
        "easy": BASE_DIR / f"{stem}-easy.py",
        "su": BASE_DIR / f"{stem}-su.py",
    }

    loaded: dict[str, ModuleType] = {}
    for label, path in paths.items():
        module_name = f"{stem.replace('-', '_')}_{label}"
        loaded[label] = load_module_from_path(path, module_name)
    return loaded
