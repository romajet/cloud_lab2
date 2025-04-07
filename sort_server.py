from word_sorter import WordSorter
import socket
import threading

def process_text(text):
    words = text.lower().split()
    words = [word.strip('.,!?()[]{}"') for word in words]
    unique_words = sorted(set(words))
    return "\n".join(unique_words)

def handle_client(conn, addr):
    print(f"[Connected] {addr}")
    while True:
        data = conn.recv(4096).decode('utf-8')
        if not data:
            break
        sorter = WordSorter(data)
        result = sorter.get_formatted_output()
        conn.sendall(result.encode('utf-8'))
    conn.close()
    print(f"[Disconnected] {addr}")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 12345))
    server.listen()
    print("[Server started] Listening on port 12345")
    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    main()
