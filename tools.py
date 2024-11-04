import os
import glob


def list_files(path: str, pattern: str) -> str:
    """List files in a directory that satisfy the pattern"""
    try:
        files = glob.glob(os.path.join(path, pattern))
        return "\n".join(files)
    except Exception as e:
        return f"Error listing files: {str(e)}"


def read_file(path: str) -> str:
    """Read content of a file"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"


def write_file(path: str, content: str) -> str:
    """Write content to a file"""
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote to {path}"
    except Exception as e:
        return f"Error writing file: {str(e)}"


def rename_file(old_path: str, new_path: str) -> str:
    """Rename a file"""
    try:
        os.rename(old_path, new_path)
        return f"Successfully renamed {old_path} to {new_path}"
    except Exception as e:
        return f"Error renaming file: {str(e)}"
