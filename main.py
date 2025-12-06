import port_scanner

if __name__ == "__main__":
    # Ejemplo 1: solo lista de puertos
    ports = port_scanner.get_open_ports("scanme.nmap.org", [20, 80])
    print("Open ports:", ports)

    print()

    # Ejemplo 2: modo verbose
    result = port_scanner.get_open_ports("scanme.nmap.org", [20, 80], True)
    print(result)
