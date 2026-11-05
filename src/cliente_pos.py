import socket 
import time 
import random 
import datetime
HOST = '127.0.0.1' 
PUERTO = 5000

TERMINAL_ID = f"POS-{random.randint(100, 999)}"

def iniciarCliente():
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Crea el telefono
    
    try: 
        cliente_socket.connect((HOST, PUERTO)) #Marca el núm y conecta con el servidor
        print(f"[*] Terminal {TERMINAL_ID} conectada con éxito al servidor.")
        while True: 
            mostrar_menu() # Muestra las opciones 
            opcion = input("Seleccione una opción: ") 
            
            if opcion == "1": # Opción 1: Cobro manual (monto por teclado) 
                importe = float(input("Ingrese el importe ($): ")) 
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
                transaccion = f"ID:{TERMINAL_ID} | importe:${importe} | fecha:{timestamp}" 
                print(f"[&gt;] Enviando transacción: {transaccion}") 
                cliente_socket.sendall(transaccion.encode('utf-8')) 
                respuesta = cliente_socket.recv(1024).decode('utf-8') 
                print(f"[&lt;] Respuesta del servidor: {respuesta}\\n") 
            
            elif opcion == "2":
               for i in range(1,6):
                   importe = round(random.uniform(150.0, 8500.0), 2)
                   timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") #Simula envío de tres transacciones

                   transaccion = f"ID:{TERMINAL_ID} | importe:${importe} | fecha:{timestamp}" #Formatea el msj
                   print(f"[>] Enviando transacción{i}: {transaccion}")

                   cliente_socket.sendall(transaccion.encode('utf-8'))
                   respuesta = cliente_socket.recv(1024).decode('utf-8') #Escucha la respuesta del servidor
                   print(f"[<] Respuesta del servidor: {respuesta}\n")

                   time.sleep(2)
            
            elif opcion == "3": # Opción 3: Salir 
                print("[\*] Saliendo de la terminal...") 
                break 
            
            else: print("[!] Opción inválida, elegí del 1 al 3.")       
    
    #Posibles errores
    except ConnectionRefusedError:
        print("[!] Error: No se pudo conectar porque el servidor no esta encendido")
    except Exception as e:
       print(f"[!] Error inesperado: {e}")
    
    finally:
      cliente_socket.close()   #Termina la conexión
      print("[*] Conexión finalizada.")


def mostrar_menu():
    print("\n" + "="*45)
    print(f" TERMINAL POS DE COBRO ({TERMINAL_ID})")
    print("="*45)
    print(" 1. Registrar venta manual (ingresar monto)")
    print(" 2. Simular ráfaga de ventas automáticas")
    print(" 3. Desconectar y salir")
    print("="*45)


                                                 
if __name__ == "__main__":
    iniciarCliente()    
