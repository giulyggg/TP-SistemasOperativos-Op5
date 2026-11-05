import socket 
import datetime 
HOST = '127.0.0.1' 
PUERTO = 5000

#Funcion para iniciar servidor:

def iniciarServidor():
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Se crea el socket TCP
    servidor_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Reutiliza el puerto si se reinicia el servidor
    servidor_socket.bind((HOST, PUERTO)) #Enlace de IP y puerto

    servidor_socket.listen(5)#Servidor escuchando
    print(f"[*] Servidor escuchando en {HOST}:{PUERTO}...")

    while True:
        conexion, direccion = servidor_socket.accept()
        print(f"[+] Conexión aceptada desde {direccion}")

        datos = conexion.recv(1024)
        if datos:
            mensaje = datos.decode('utf-8')
            hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{hora}] Recibido: {mensaje}")
            conexion.sendall(b"ACK Transaccion registrada")
        conexion.close()
        print(f"[-] Conexión cerrada con {direccion}")

if __name__ == "__main__":
    iniciarServidor()
    