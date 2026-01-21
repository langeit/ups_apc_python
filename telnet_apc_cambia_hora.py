#!/usr/bin/python
# @author [Mauricio Lange]
# @email [mauriciolangea@yahoo.com]
# @create date 2026-01.21 15:00
# @desc [Automation - Configura zona horario a Horario Verano/Invierno en Chile]
# UTC -03:00 = Verano
# UTC -04:00 = Invierno

import getpass
import sys
import time
import socket
import telnetlib

TZ_OFFSET  = "-03:00"
HOSTS_FILE = "ups.txt"

def main():
    user = input("User Name: ")
    password = getpass.getpass("Password : ")

    with open(HOSTS_FILE, "r", encoding="utf-8") as f:

        for line in f:
            ip = line.strip()
            if not ip or ip.startswith("#"):
                continue

            try:            
                print(f"Cambiando zona horaria {ip} -> {TZ_OFFSET}")
                tn = telnetlib.Telnet()
                tn.open(ip, 23, timeout=10)

                tn.expect([b"Username", b"User Name", b"login", b"Login"], 12)
                tn.write(user.encode("ascii") + b"\r\n")

                if password:
                    tn.expect([b"Password", b"password"], 12)
                    tn.write(password.encode("ascii") + b"\r\n")

                    tn.read_until(b"apc>", timeout=8)

                    tn.write(f"date -z {TZ_OFFSET}\n".encode("ascii"))
                    tn.write(b"date\n")
                    tn.write(b"exit\n")


                    output = tn.read_very_eager().decode("utf-8", errors="ignore")
                    print(output)
                    tn.close()
            except (socket.timeout, ConnectionRefusedError) as e:
                print(f"[ERROR] {ip} Timeout {e}")
            except Exception as e:
                print(f"[ERROR] {ip} {e}")


if __name__ == "__main__":
    main()