def get_host():
    print("\n" + "="*50)
    print("**Desktop_to_Proxy**")
    host = input("Введите IP-адрес хоста: ").strip()
    if not host:
        raise ValueError("IP-адрес не может быть пустым")
    return host

def get_credentials_for_service(service: str):
    """Возвращает (username, password). Пароль запрашивается только для FTP."""
    if service in ('ssh', 'sftp', 'rdp'):
        username = input(f"\nВведите логин для {service.upper()}: ").strip()
        return username, ""
    elif service == 'ftp':
        print(f"\nТребуется аутентификация для {service.upper()}:")
        username = input("Логин: ").strip()
        from getpass import getpass
        password = getpass("Пароль: ")
        return username, password
    else:
        return "", ""

def choose_service(services, show_logout=False):
    available = []

    if services.get('ssh'):
        available.append(('ssh', 'SSH (порт 22)'))
    if services.get('sftp'):
        available.append(('sftp', 'SFTP (порт 22)'))
    if services.get('telnet'):
        available.append(('telnet', 'Telnet (порт 23)'))
    if services.get('ftp'):
        available.append(('ftp', 'FTP (порт 21)'))
    if services.get('rdp'):
        available.append(('rdp', 'RDP (порт 3389)'))
    if services.get('vnc'):
        available.append(('vnc', f'VNC (порт {services["vnc"]})'))
    if services.get('serial'):
        available.append(('serial', f'Serial-over-IP (порт {services["serial"]})'))
    if services.get('http'):
        proto, port = services['http']
        available.append(('http', f'{proto.upper()} (порт {port})'))

    if not available:
        return None

    priority = ['ssh', 'sftp', 'rdp', 'vnc', 'ftp', 'telnet', 'serial', 'http']
    default = next((p for p in priority if any(i[0] == p for i in available)), None)

    print("\n" + "="*50)
    print("Доступные протоколы для подключения:")
    if show_logout:
        print("  0. Сменить хост (logout)")

    start_idx = 1 if show_logout else 1
    for i, (key, desc) in enumerate(available, start_idx):
        marker = " (по умолчанию)" if key == default else ""
        print(f"  {i}. {desc}{marker}")

    while True:
        prompt = "\nВыберите номер"
        if show_logout:
            prompt += " (0 — сменить хост)"
        prompt += " (Enter — по умолчанию): "
        choice = input(prompt).strip()

        if choice == "":
            return default
        if choice == "0" and show_logout:
            return 'logout'
        if choice.isdigit():
            idx = int(choice) - start_idx
            if 0 <= idx < len(available):
                return available[idx][0]
        print("Неверный ввод. Попробуйте снова.")