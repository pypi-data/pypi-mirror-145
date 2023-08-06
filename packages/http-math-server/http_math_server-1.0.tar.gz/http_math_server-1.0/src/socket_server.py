import socket

import calculation as calc


HOST, PORT = '127.0.0.1', 5000


if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(0)
    print("Waiting connection...")
    with server:
        while True:
            connection, client_address = server.accept()
            try:
                print(f"Connected to {client_address}")
                data = connection.recv(64)
                decoded_data = data.decode()
                if 'stop' in decoded_data or 'quit' in decoded_data:
                    break
                result = calc.calculate(decoded_data)['result']
                connection.sendall(result.encode())
                print(f"Sended: {result}")
            finally:
                print("Connection closed.")
                connection.close()           
