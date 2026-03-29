import shutil
import sys

DEPENDENCIES = {
    'ssh': ('ssh', 'openssh-client'),
    'sftp': ('sftp', 'openssh-client'),
    'telnet': ('telnet', 'telnet'),
    'lftp': ('lftp', 'lftp'),
    'xfreerdp': ('xfreerdp', 'freerdp2-x11'),
    'vncviewer': ('vncviewer', 'tigervnc-viewer'),
    'xdg-open': ('xdg-open', 'xdg-utils'),
}

def check_dependencies(show_missing_only=True):
    missing = []
    for cmd, package in DEPENDENCIES.items():
        if not shutil.which(cmd):
            missing.append((cmd, package))
    
    if missing:
        print("Отсутствуют необходимые зависимости:")
        for cmd, package in missing:
            print(f"  - {cmd} (установите: sudo apt install {package[1]})")
        return False
    elif not show_missing_only:
        print("Все системные зависимости установлены.")
    return True

def check_dependency_for_service(service: str):
    deps_map = {
        'ssh': 'ssh',
        'sftp': 'sftp',
        'telnet': 'telnet',
        'ftp': 'lftp',
        'rdp': 'xfreerdp',
        'vnc': 'vncviewer',
        'http': 'xdg-open',
    }
    cmd = deps_map.get(service)
    if cmd and not shutil.which(cmd):
        package = DEPENDENCIES.get(cmd, ('', ''))[1]
        print(f"Внимание: {cmd} не установлен. ({package})")
        return False
    return True

if __name__ == "__main__":
    print("Проверка системных зависимостей...")
    check_dependencies(show_missing_only=False)
