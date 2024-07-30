import socket
import threading

nombre_usuario = input("Introduce tu nombre de usuario: ")

host = '127.0.0.1'
port = 55559

cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cliente.connect((host, port))

def recibir_mensajes():
    while True:
        try:
            mensaje = cliente.recv(1024).decode('utf-8')
            if mensaje == "@nombre_usuario":
                cliente.send(nombre_usuario.encode('utf-8'))
            else:
                print(mensaje)
        except:
            print("Ocurrió un error")
            cliente.close()
            break

def escribir_mensajes():
    while True:
        mensaje = f"{nombre_usuario}: {input('')}"
        cliente.send(mensaje.encode('utf-8'))

hilo_recibir = threading.Thread(target=recibir_mensajes)
hilo_recibir.start()

hilo_escribir = threading.Thread(target=escribir_mensajes)
hilo_escribir.start()
