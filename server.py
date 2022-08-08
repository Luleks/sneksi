import socket
from _thread import *
import pickle
from snake import OnlineSnake
import csv
import time

RED = (255, 0, 0)
DARKGREEN = (0, 100, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (160, 32, 240)
DIMENSION = 600
GRID_SIZE = 20
GAP = DIMENSION // GRID_SIZE

server = '192.168.1.5'
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)

s.listen(2)
print('Server Started, waiting for players')

def write_scoreboard(snake1, snake2):
    local_time = time.localtime()
    date_time = time.strftime('%d/%B/%Y', local_time)
    with open('info_folder\\result_history.csv') as f:
        reader = csv.DictReader(f)
        items = list(reader)
        read = [(item['home'], item['score'], item['away'], item['date']) for item in items]
    toWrite = ([(snake1.name, str(snake1.score)+'-'+str(snake2.score), snake2.name, date_time)] + read)[:-1]

    with open('info_folder\\result_history.csv', 'w', newline = '') as f:
        fieldnames = ['home','score','away','date']
        writer = csv.DictWriter(f, fieldnames = fieldnames)
        writer.writeheader()
        for i in range(0, len(toWrite)):
            writer.writerow({'home':toWrite[i][0], 'score':toWrite[i][1], 'away':toWrite[i][2], 'date':toWrite[i][3]})

snakes = [OnlineSnake(1, 0, 20, 50, WHITE, GAP, GRID_SIZE, 20, 50, 0), OnlineSnake(1, 0, 20, 50, WHITE, GAP, GRID_SIZE, 20, 50, 0)]
count = 0
ukaz = None
def threaded_client(conn, player):
    global snakes, count, ukaz
    conn.send(pickle.dumps(snakes[player]))
    if player == 1:
        with open('online_folder\\game_start.txt', 'w') as f:
            f.write(str(1))
            
    reply = ''
    while True:
        try:
            data = pickle.loads(conn.recv(4096))
            snakes[player] = data

            if snakes[0].game_over and snakes[1].game_over:
                if count == 0:
                    write_scoreboard(snakes[0], snakes[1])
                    count += 1
            else: count = 0

            if snakes[player].main_menu:
                ukaz = player
                break

            if not data:
                print('Disconnected')
                break
            else:
                if player == 1:
                    reply = snakes[0]
                else:
                    reply = snakes[1]
            conn.sendall(pickle.dumps(reply))
        except:
            break
    
    with open('online_folder\\game_start.txt', 'w') as f:
        f.write(str(0))
    print('Lost connection')
    conn.close()

player = 0
while True:
    conn, addr = s.accept()
    print('Player connected to:', addr)
    if ukaz is not None:
        snakes[ukaz] = OnlineSnake(1, 0, 20, 50, WHITE, GAP, GRID_SIZE, 20, 50, 0)
        player = ukaz
        ukaz = None
    start_new_thread(threaded_client, (conn, player))
    player += 1
