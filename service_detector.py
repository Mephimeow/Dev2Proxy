import socket
import ssl

COMMON_HTTP_PORTS = [80, 443, 8080, 8443, 8000, 8888]
COMMON_VNC_PORTS = list(range(5900, 5910))
SERIAL_OVER_IP_PORTS = list(range(2000, 2010))

def check_ssh(host: str, timeout: int = 3) -> bool:
    try:
        with socket.create_connection((host, 22), timeout=timeout) as sock:
            banner = sock.recv(1024).decode('utf-8', errors='ignore')
            return 'SSH-' in banner
    except Exception:
        return False

def check_telnet(host: str, timeout: int = 3) -> bool:
    try:
        with socket.create_connection((host, 23), timeout=timeout) as sock:
            banner = sock.recv(256).decode('utf-8', errors='ignore')
            return True
    except Exception:
        return False

def check_ftp(host: str, timeout: int = 3) -> bool:
    try:
        with socket.create_connection((host, 21), timeout=timeout) as sock:
            banner = sock.recv(256).decode('utf-8', errors='ignore')
            return banner.startswith('220')  # FTP welcome message
    except Exception:
        return False

def check_vnc(host: str, timeout: int = 3):
    for port in COMMON_VNC_PORTS:
        try:
            with socket.create_connection((host, port), timeout=timeout) as sock:
                banner = sock.recv(128).decode('utf-8', errors='ignore')
                if banner.startswith('RFB '):
                    return port
        except Exception:
            continue
    return None

def check_serial_over_ip(host: str, timeout: int = 3):
    for port in SERIAL_OVER_IP_PORTS:
        try:
            with socket.create_connection((host, port), timeout=timeout):
                return port
        except Exception:
            continue
    return None

def check_http_https(host: str, timeout: int = 3):
    for port in COMMON_HTTP_PORTS:
        is_ssl = port in (443, 8443)
        try:
            if is_ssl:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                with socket.create_connection((host, port), timeout=timeout) as sock:
                    with context.wrap_socket(sock, server_hostname=host) as ssock:
                        ssock.send(b"GET / HTTP/1.0\r\nHost: " + host.encode() + b"\r\n\r\n")
                        response = ssock.recv(512).decode('utf-8', errors='ignore')
            else:
                with socket.create_connection((host, port), timeout=timeout) as sock:
                    sock.send(b"GET / HTTP/1.0\r\nHost: " + host.encode() + b"\r\n\r\n")
                    response = sock.recv(512).decode('utf-8', errors='ignore')
            
            if 'HTTP/' in response:
                return ('https' if is_ssl else 'http', port)
        except Exception:
            continue
    return None

def detect_services(host: str) -> dict:
    return {
        'ssh': check_ssh(host),
        'telnet': check_telnet(host),
        'ftp': check_ftp(host),
        'rdp': check_rdp(host),
        'vnc': check_vnc(host),
        'serial': check_serial_over_ip(host),
        'http': check_http_https(host),  
    }

def check_rdp(host: str, timeout: int = 3) -> bool:
    try:
        with socket.create_connection((host, 3389), timeout=timeout):
            return True
    except Exception:
        return False