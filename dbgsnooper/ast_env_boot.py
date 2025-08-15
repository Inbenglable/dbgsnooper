import os
import subprocess
from pathlib import Path
import sys
import subprocess
import json

def ensure_ast_env():
    # 获取当前文件的绝对路径（即 env_boot.py 所在目录）
    base_dir = Path(__file__).resolve().parent
    env_dir = base_dir / ".venvs" / "ast-env"

    unix_python = env_dir / "bin" / "python"
    win_python = env_dir / "Scripts" / "python.exe"

    # 检查虚拟环境是否已存在
    if unix_python.exists():
        return str(unix_python)
    if win_python.exists():
        return str(win_python)

    # 创建虚拟环境
    print(f"Creating Python 3.9 virtual environment at: {env_dir}")
    subprocess.run([
        "python3.9", "-m", "venv", str(env_dir)
    ], check=True)

    python_exec = unix_python if unix_python.exists() else win_python

    # 升级 pip
    subprocess.run([
        str(python_exec), "-m", "pip", "install", "--upgrade", "pip"
    ], check=True)

    return str(python_exec)


def run_cmd_in_ast_env(cmd):
    python_path = ensure_ast_env()
    cmd = [python_path] + cmd

    try:
        result = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        raise RuntimeError(f"Command failed: {e.stderr}")


def run_get_statement_range(file_path, lineno):
    base_dir = Path(__file__).resolve().parent
    script_path = base_dir / "query_code_scope.py"
    cmd = [str(script_path), 'get_statement_range', str(file_path), str(lineno)]
    result = run_cmd_in_ast_env(cmd)

    parsed = json.loads(result)
    return parsed["start_line"], parsed["end_line"]

def run_get_belonging_method(file_path, lineno):
    base_dir = Path(__file__).resolve().parent
    script_path = base_dir / "query_code_scope.py"
    cmd = [str(script_path), 'get_belonging_method', str(file_path), str(lineno)]
    result = run_cmd_in_ast_env(cmd)
    parsed = json.loads(result)
    return parsed["start_line"], parsed["end_line"]

def run_get_method_range(file_path, method_name):
    base_dir = Path(__file__).resolve().parent
    script_path = base_dir / "query_code_scope.py"
    cmd = [str(script_path), 'get_method_range', str(file_path), str(method_name)]
    result = run_cmd_in_ast_env(cmd)
    parsed = json.loads(result)
    return parsed["start_line"], parsed["end_line"]



