import os


def _file_path_to_module_name(file_path: str) -> str:
    return os.path.basename(file_path).removesuffix(".py")
