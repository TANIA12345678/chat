import socket
import threading

# Configuración del servidor
host = '127.0.0.1'
port = 55559

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()
print(f"Servidor corriendo en {host}:{port}")

# Listas para almacenar clientes y nombres de usuarios
clientes = []
usuarios = []

def transmitir(mensaje, cliente_remitente):
    for cliente in clientes:
        if cliente != cliente_remitente:
            try:
                cliente.send(mensaje)
            except Exception as e:
                print(f"Error enviando mensaje a {cliente}: {e}")
                clientes.remove(cliente)
                cliente.close()

def manejar_mensajes(cliente):
    while True:
        try:
            mensaje = cliente.recv(1024)
            if not mensaje:
                raise Exception("Cliente desconectado")
            transmitir(mensaje, cliente)
        except:
            indice = clientes.index(cliente)
            cliente.close()
            clientes.pop(indice)
            usuario = usuarios.pop(indice)
            print(f"{usuario} se desconectó.")
            transmitir(f"Chatbot: {usuario} se desconectó".encode('utf-8'), None)
            break

def recibir_conexiones():
    while True:
        cliente, direccion_cliente = server.accept()
        print(f"Conexión aceptada de {direccion_cliente}")
        
        cliente.send("@nombre_usuario".encode('utf-8'))
        nombre_usuario = cliente.recv(1024).decode('utf-8')
        
        clientes.append(cliente)
        usuarios.append(nombre_usuario)
        
        print(f"{nombre_usuario} está conectado con {str(direccion_cliente)}")
        mensaje = f"ChatBot: {nombre_usuario} se unió al chat!".encode('utf-8')
        transmitir(mensaje, cliente)
        cliente.send("Conectado al servidor".encode('utf-8'))
        
        hilo = threading.Thread(target=manejar_mensajes, args=(cliente,))
        hilo.start()

recibir_conexiones()
