import socket
import ipaddress
from common_ports import ports_and_services


def _looks_like_ip(target):
    """
    Comprueba si el string tiene forma de IPv4 (solo dígitos y puntos, 4 bloques).
    No valida rangos, solo formato.
    """
    parts = target.split(".")
    if len(parts) != 4:
        return False
    return all(part.isdigit() for part in parts)


def _validate_target(target):
    """
    Valida si el target es IP o hostname y devuelve:
      (ip_address, display_name, error_message)

    - ip_address: IP resuelta en string (ej: "45.33.32.156")
    - display_name: lo que se mostrará como {URL} en el modo verbose
    - error_message: None si todo OK, o el string de error que pide el enunciado.
    """
    # ¿Parece IP literal?
    if _looks_like_ip(target):
        try:
            ipaddress.ip_address(target)  # valida IP
        except ValueError:
            return None, None, "Error: Invalid IP address"
        # Es una IP válida
        return target, target, None

    # Si no parece IP, lo tratamos como hostname
    try:
        ip = socket.gethostbyname(target)
    except socket.gaierror:
        return None, None, "Error: Invalid hostname"

    # Hostname válido
    return ip, target, None


def get_open_ports(target, port_range, verbose=False):
    """
    Escanea los puertos en el rango dado y devuelve:
      - lista de puertos abiertos (verbose=False)
      - string formateado (verbose=True)

    target: hostname o IP
    port_range: [puerto_inicial, puerto_final]
    verbose: si True, devuelve salida descriptiva tipo nmap
    """
    target = str(target)

    # Validar y resolver target
    ip, display_name, error = _validate_target(target)
    if error:
        return error

    start_port, end_port = port_range
    if start_port > end_port:
        start_port, end_port = end_port, start_port

    open_ports = []

    for port in range(start_port, end_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(1.0)
            result = sock.connect_ex((ip, port))  # 0 = puerto abierto
            if result == 0:
                open_ports.append(port)

    # Modo no verbose: solo la lista
    if not verbose:
        return open_ports

    # Modo verbose: construir el string formateado
    lines = []
    lines.append(f"Open ports for {display_name} ({ip})")
    lines.append("PORT     SERVICE")

    for port in open_ports:
        service = ports_and_services.get(port, "unknown")
        lines.append(f"{port:<9}{service}")

    return "\n".join(lines)