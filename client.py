from game import Game
import socket

ip = "127.0.0.1"
port = 8080

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
address = (ip, port)
sock.connect(address)
print("\nConnected to server")

try:
    game = Game("X")

    # start tic-tac-toe
    game.start_game()
    while True:
        # take turn
        user_input = game.take_turn()  # choose + mark a space
        sock.sendall(user_input.encode())  # send data to server
        if game.is_over:  # check if game ended
            break

        # receive data from server
        data = sock.recv(1024)
        game.handle_input(data.decode())  # update game with new data
        if game.is_over:  # check if game ended
            break

finally:
    sock.close()  # close connection

