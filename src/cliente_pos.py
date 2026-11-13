import socket
import time
import random
import datetime

HOST = '127.0.0.1'
PUERTO = 5000

TERMINAL_ID = f"POS-{random.randint(100, 999)}"


# Funcion para recibir la respuesta completa del servidor
def recibir_respuesta(cliente_socket):
    respuesta = b''

    while not respuesta.endswith(b'\n'):
        datos = cliente_socket.recv(1024)

        if not datos:
            raise ConnectionError("El servidor cerró la conexión")

        respuesta += datos

    return respuesta.decode('utf-8').strip()


def iniciarCliente():
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        cliente_socket.connect((HOST, PUERTO))
        print(f"[*] Terminal {TERMINAL_ID} conectada con éxito al servidor.")

        while True:
            mostrar_menu()
            opcion = input("Seleccione una opción: ")

            if opcion == "1":
                importe = float(input("Ingrese el importe ($): "))
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                transaccion = f"ID:{TERMINAL_ID} | importe:${importe} | fecha:{timestamp}"

                print(f"[>] Enviando transacción: {transaccion}")

                cliente_socket.sendall((transaccion + "\n").encode('utf-8'))

                respuesta = recibir_respuesta(cliente_socket)
                print(f"[<] Respuesta del servidor: {respuesta}\n")

            elif opcion == "2":
                for i in range(1, 6):
                    importe = round(random.uniform(150.0, 8500.0), 2)
                    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    transaccion = f"ID:{TERMINAL_ID} | importe:${importe} | fecha:{timestamp}"

                    print(f"[>] Enviando transacción {i}: {transaccion}")

                    cliente_socket.sendall((transaccion + "\n").encode('utf-8'))

                    respuesta = recibir_respuesta(cliente_socket)
                    print(f"[<] Respuesta del servidor: {respuesta}\n")

                    time.sleep(2)

            elif opcion == "3":
                print("[*] Saliendo de la terminal...")
                break

            else:
                print("[!] Opción inválida, elegí del 1 al 3.")

    except ConnectionRefusedError:
        print("[!] Error: No se pudo conectar porque el servidor no está encendido.")

    except Exception as e:
        print(f"[!] Error inesperado: {e}")

    finally:
        cliente_socket.close()
        print("[*] Conexión finalizada.")


def mostrar_menu():
    print("\n" + "=" * 45)
    print(f" TERMINAL POS DE COBRO ({TERMINAL_ID})")
    print("=" * 45)
    print(" 1. Registrar venta manual (ingresar monto)")
    print(" 2. Simular ráfaga de ventas automáticas")
    print(" 3. Desconectar y salir")
    print("=" * 45)


if __name__ == "__main__":
    iniciarCliente()
