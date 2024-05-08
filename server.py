from game import Game
import socket

ip = "127.0.0.1"
port = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
address = (ip, port)
sock.bind(address)
sock.listen(1)
print(f"\nServer running on {(ip, port)}...")

connection, client_address = sock.accept()
print(f"Connected to {client_address}")

try:
    game = Game("O")

    # start tic-tac-toe
    game.start_game()
    while True:
        # receive data from client
        data = connection.recv(1024)
        game.handle_input(data.decode())  # update game with new data
        if game.is_over:  # check if game ended
            break

        # take turn
        user_input = game.take_turn()  # choose + mark a space
        connection.sendall(user_input.encode())  # send data to client
        if game.is_over:  # check if game ended
            break

finally:
    connection.close()  # close connection
