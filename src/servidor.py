import socket
import datetime
import threading

HOST = '0.0.0.0'
PUERTO = 5000

# Bloqueo para evitar que se mezclen los mensajes de los hilos
bloqueo_consola = threading.Lock()


# Funcion para procesar cada cliente
def manejar_cliente(conexion, direccion):

    print(f"[+] Conexión aceptada desde {direccion}")

    buffer = b''

    try:
        while True:
            datos = conexion.recv(1024)

            # Detectar desconexion del cliente
            if not datos:
                with bloqueo_consola:
                    print(f"[-] Cliente {direccion} desconectado.")
                break

            buffer += datos

            # Procesar mensajes completos delimitados por salto de linea
            while b'\n' in buffer:
                mensaje_bytes, buffer = buffer.split(b'\n', 1)

                if not mensaje_bytes:
                    continue

                mensaje = mensaje_bytes.decode('utf-8')

                # Registrar hora de recepcion
                hora = datetime.datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S.%f"
                )

                with bloqueo_consola:
                    print(f"[{hora}] Recibido: {mensaje}")

                # Confirmar recepcion al cliente
                conexion.sendall(b"ACK Transaccion registrada\n")

    except ConnectionResetError:
        with bloqueo_consola:
            print(f"[!] Se perdió abruptamente la conexión con {direccion}")

    except OSError as e:
        with bloqueo_consola:
            print(f"[!] Error de comunicación con {direccion}: {e}")

    except UnicodeDecodeError:
        with bloqueo_consola:
            print(f"[!] Mensaje con formato inválido desde {direccion}")

    finally:
        conexion.close()
        with bloqueo_consola:
            print(f"[-] Conexión cerrada con {direccion}")


# Funcion para iniciar servidor
def iniciarServidor():

    servidor_socket = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    servidor_socket.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    servidor_socket.bind((HOST, PUERTO))
    servidor_socket.listen(5)

    print(f"[*] Servidor escuchando en {HOST}:{PUERTO}...")

    try:
        while True:
            conexion, direccion = servidor_socket.accept()

            # Crear un hilo independiente para cada cliente
            hilo = threading.Thread(
                target=manejar_cliente,
                args=(conexion, direccion),
                daemon=True
            )

            hilo.start()

    except KeyboardInterrupt:
        print("\n[*] Cerrando servidor...")

    finally:
        servidor_socket.close()
        print("[*] Servidor finalizado.")


if __name__ == "__main__":
    iniciarServidor()
