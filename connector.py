import shutil
import subprocess
import webbrowser

def connect_ssh(host: str, username: str):
    if not shutil.which("ssh"):
        print("ssh не установлен!")
        return
    subprocess.run(["ssh", f"{username}@{host}"])

def connect_sftp(host: str, username: str):
    if not shutil.which("sftp"):
        print("sftp не установлен!")
        return
    subprocess.run(["sftp", f"{username}@{host}"])

def connect_telnet(host: str):
    if not shutil.which("telnet"):
        print("telnet не установлен!")
        return
    subprocess.run(["telnet", host])

def connect_ftp(host: str, username: str, password: str):
    if not shutil.which("lftp"):
        print("lftp не установлен! Выполните: sudo apt install lftp")
        return
    url = f"ftp://{username}:{password}@{host}"
    subprocess.run(["lftp", url])

def connect_rdp(host: str, username: str):
    if not shutil.which("xfreerdp"):
        print("xfreerdp не установлен!")
        return
    cmd = ["xfreerdp", f"/v:{host}", f"/u:{username}", "/cert:ignore", "+clipboard", "/dynamic-resolution"]
    subprocess.run(cmd)

def connect_vnc(host: str, port: int):
    if not shutil.which("vncviewer"):
        print("vncviewer не установлен!")
        return
    display = port - 5900
    subprocess.run(["vncviewer", f"{host}:{display}"])

def connect_serial(host: str, port: int):
    if not shutil.which("telnet"):
        print("telnet не установлен (нужен для Serial-over-IP)!")
        return
    print("Для выхода из сессии: Ctrl+] → затем введите 'quit'")
    subprocess.run(["telnet", host, str(port)])

def connect_http(host: str, proto_port):
    proto, port = proto_port
    url = f"{proto}://{host}:{port}" if port not in (80, 443) else f"{proto}://{host}"
    print(f"Открываем в браузере: {url}")
    try:
        subprocess.run(["xdg-open", url], check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        webbrowser.open(url)

def connect_to_service(selected: str, services: dict, host: str, username: str, password: str = ""):
    if selected == 'ssh':
        connect_ssh(host, username)
    elif selected == 'sftp':
        connect_sftp(host, username)
    elif selected == 'telnet':
        connect_telnet(host)
    elif selected == 'ftp':
        connect_ftp(host, username, password)
    elif selected == 'rdp':
        connect_rdp(host, username)
    elif selected == 'vnc':
        connect_vnc(host, services['vnc'])
    elif selected == 'serial':
        connect_serial(host, services['serial'])
    elif selected == 'http':
        connect_http(host, services['http'])
    else:
        print("Неизвестный протокол.")