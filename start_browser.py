import subprocess
import os

chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
# edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
user_data_dir = r"C:\chrome_debug"

if not os.path.exists(chrome_path):
    raise FileNotFoundError(f"找不到 Chrome：{chrome_path}")

subprocess.Popen([
    chrome_path,
    "--remote-debugging-port=9229",
    f"--user-data-dir={user_data_dir}"
])

print("Chrome 已启动")
print("远程调试端口：9229")
print("验证地址：http://127.0.0.1:9229/json/version")