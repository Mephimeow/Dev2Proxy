import logging
from input_handler import get_host, get_credentials_for_service, choose_service
from service_detector import detect_services
from connector import connect_to_service
from dependencies import check_dependencies, check_dependency_for_service

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(message)s',
    handlers=[
        logging.FileHandler("connections.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

def log_connection(service: str, host: str, username: str = ""):
    user_info = f" (пользователь: {username})" if username else ""
    logging.info(f"Подключение по {service.upper()} к {host}{user_info}")

def main():
    host = None
    services = None

    print("Проверка системных зависимостей...")
    check_dependencies()

    while True:
        if host is None:
            try:
                host = get_host()
            except Exception as e:
                print(f"Ошибка: {e}")
                continue

            print(f"\nСканирование хоста {host}...")
            services = detect_services(host)

            if services.get('ssh'):
                services['sftp'] = True

            found = any(services.get(key) for key in ['ssh', 'sftp', 'telnet', 'ftp', 'rdp', 'vnc', 'serial', 'http'])
            if not found:
                print("Не найдено поддерживаемых сервисов.")
                host = None
                continue

            print("\nРезультаты сканирования:")
            for name, desc in [
                ('ssh', "SSH"),
                ('sftp', "SFTP"),
                ('telnet', "Telnet"),
                ('ftp', "FTP"),
                ('rdp', "RDP"),
                ('vnc', "VNC"),
                ('serial', "Serial-over-IP"),
                ('http', "HTTP/HTTPS")
            ]:
                val = services.get(name)
                if name == 'http' and val:
                    proto, port = val
                    print(f"    {desc:15}: {proto} (порт {port})")
                elif name in ('vnc', 'serial') and val:
                    print(f"    {desc:15}: Порт {val}")
                else:
                    print(f"    {desc:15}: {'Да' if val else 'Нет'}")

        while True:
            selected = choose_service(services, show_logout=True)
            if selected is None:
                break
            if selected == 'logout':
                host = None
                break

            if not check_dependency_for_service(selected):
                input("\nНажмите Enter для возврата...")
                continue
            username, password = get_credentials_for_service(selected)
            log_connection(selected, host, username)
            connect_to_service(selected, services, host, username, password)

            input("\nСеанс завершён. Нажмите Enter для возврата к выбору...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nВыход.")