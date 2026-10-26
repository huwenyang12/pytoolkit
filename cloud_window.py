
import subprocess
import time
from pathlib import Path
import psutil
import win32con
import win32gui
import win32process

CLOUD_EXE = r"D:\Program Files\enterpriseEcloud\4.3.6.0\enterprise-cloud.exe"
WINDOW_KEYWORDS = ("天翼企业云盘", "天翼云企业云盘")


def find_cloud_window():
    name = Path(CLOUD_EXE).name.lower()
    pids = set()
    for p in psutil.process_iter(["name"]):
        try:
            if (p.info["name"] or "").lower() == name:
                pids.add(p.pid)
        except psutil.Error:
            continue
    windows = []
    def collect(hwnd, _):
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        if pid in pids and win32gui.GetParent(hwnd) == 0:
            if any(k in win32gui.GetWindowText(hwnd) for k in WINDOW_KEYWORDS):
                windows.append(hwnd)
    win32gui.EnumWindows(collect, None)
    windows.sort(key=lambda h: not win32gui.IsWindowVisible(h))
    return windows[0] if windows else None


def activate_window(hwnd):
    if not win32gui.IsWindow(hwnd):
        return False
    if win32gui.IsIconic(hwnd):
        win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    elif not win32gui.IsWindowVisible(hwnd):
        return False
    try:
        win32gui.BringWindowToTop(hwnd)
        win32gui.SetForegroundWindow(hwnd)
    except Exception:
        return False
    time.sleep(0.3)
    return (
        win32gui.GetForegroundWindow() == hwnd
        and win32gui.IsWindowVisible(hwnd)
        and win32gui.IsWindowEnabled(hwnd)
    )


def wake_cloud(timeout=30):
    hwnd = find_cloud_window()
    hidden = hwnd and not win32gui.IsWindowVisible(hwnd) and not win32gui.IsIconic(hwnd)
    if not hwnd or hidden:
        exe = Path(CLOUD_EXE)
        if not exe.is_file():
            raise FileNotFoundError(f"云盘程序不存在：{exe}")
        print("正在唤醒云盘..." if hidden else "正在启动云盘...")
        subprocess.Popen([str(exe)], cwd=str(exe.parent),
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            hwnd = find_cloud_window()
            if hwnd and win32gui.IsWindowVisible(hwnd):
                break
            time.sleep(0.5)
        else:
            raise RuntimeError("云盘启动或恢复超时")
    for _ in range(5):
        if activate_window(hwnd):
            print("云盘已成功唤醒")
            return hwnd
        time.sleep(0.5)
    raise RuntimeError("云盘窗口激活失败")


if __name__ == "__main__":
    try:
        wake_cloud()
    except Exception as e:
        print(f"唤醒失败：{e}")
        raise SystemExit(1)
