import os
import socket
import threading

HOST = "localhost"
PORT = 8080
TIMEOUT = 30
DOCUMENT_ROOT = "./www"

METHOD_NOT_ALLOWED_RESPONSE = (
    "HTTP/1.1 405 Method Not Allowed\r\n"
    "Content-Type: text/plain\r\n"
    "Allow: GET, HEAD\r\n"
    "Connection: close\r\n"
    "\r\n"
    "405 Method Not Allowed"
)

NOT_FOUND_RESPONSE = (
    "HTTP/1.1 404 Not Found\r\n"
    "Content-Type: text/plain\r\n"
    "Connection: close\r\n"
    "\r\n"
    "404 Not Found"
)

OK_RESPONSE = (
    "HTTP/1.1 200 OK\r\n"
    "Content-Type: text/html\r\n"
    "Connection: close\r\n"
    "\r\n"
    "{content}"
)

HEAD_RESPONSE = (
    "HTTP/1.1 200 OK\r\n"
    "Content-Type: text/html\r\n"
    "Content-Length: 0\r\n"
    "Connection: close\r\n"
    "\r\n"
)


def handle_request(client_socket):
    try:
        request: str = client_socket.recv(1024).decode()

        request_data: list[str] = request.split()

        method: str = request_data[0]
        uri: str = request_data[1]

        headers_data: list[str] = request_data[3 : len(request_data)]
        headers: dict[str, str] = {}

        for i in range(0, len(headers_data), 2):
            key = headers_data[i].replace(":", "")
            value = headers_data[i + 1]

            headers[key] = value

        if method in ["GET", "HEAD"]:
            if method == "GET":
                if ".html" not in uri:
                    client_socket.sendall(NOT_FOUND_RESPONSE.encode())
                    client_socket.close()
                    return None

                path = f"{DOCUMENT_ROOT}{uri}"

                if not os.path.exists(path):
                    client_socket.sendall(NOT_FOUND_RESPONSE.encode())
                    client_socket.close()
                    return None

                content = open(path, encoding="utf-8").read()
                response = OK_RESPONSE.format(content=content)
                client_socket.sendall(response.encode())
                client_socket.close()
                return None

            if method == "HEAD":
                client_socket.sendall(HEAD_RESPONSE.encode())
                client_socket.close()
        else:
            client_socket.sendall(METHOD_NOT_ALLOWED_RESPONSE.encode())
            client_socket.close()
    finally:
        client_socket.close()


def start_server():
    s_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s_tcp.bind((HOST, PORT))
    s_tcp.listen(TIMEOUT)

    print(f"HTTP server started on {HOST}:{PORT}")

    while True:
        client_socket, _ = s_tcp.accept()
        client_handler = threading.Thread(target=handle_request, args=(client_socket,))
        client_handler.start()


if __name__ == "__main__":
    start_server()
