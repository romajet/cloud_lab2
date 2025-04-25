import grpc
import goroda_pb2
import goroda_pb2_grpc
from concurrent import futures
import threading
import queue
import random
import os

MAX_PLAYERS = 5
MIN_PLAYERS = 3
TIME_LIMIT = 30


class Player:
    def __init__(self, name, stream):
        self.name = name
        self.stream = stream
        self.queue = queue.Queue()
        self.alive = True


class GameSession(threading.Thread):
    def __init__(self, players, all_cities):
        super().__init__()
        self.players = players
        self.used_cities = set()
        self.all_cities = all_cities
        self.last_letter = None
        self.current_index = 0
        self.running = True

    def run(self):
        names = [p.name for p in self.players]
        print(f"Игра началась между: {', '.join(names)}")
        random.shuffle(self.players)

        for p in self.players:
            p.queue.put(
                goroda_pb2.ServerMessage(
                    status="start", message="Игра началась!", next_letter=""
                )
            )

        while self.running:
            player = self.players[self.current_index]
            player.queue.put(
                goroda_pb2.ServerMessage(
                    status="your_turn",
                    message="Ваш ход",
                    next_letter=self.last_letter or "",
                    is_turn=True,
                )
            )

            try:
                city = player.stream.get(timeout=TIME_LIMIT).city.strip().lower()
            except queue.Empty:
                player.alive = False
                player.queue.put(
                    goroda_pb2.ServerMessage(status="lose", message="Время вышло!")
                )
                self.remove_dead_players()
                continue

            if not self.validate_city(city):
                player.alive = False
                player.queue.put(
                    goroda_pb2.ServerMessage(
                        status="error", message="Неправильный город!"
                    )
                )
                self.remove_dead_players()
                continue

            self.used_cities.add(city)
            self.last_letter = self.get_last_letter(city)

            # уведомляем других
            for p in self.players:
                if p != player and p.alive:
                    p.queue.put(
                        goroda_pb2.ServerMessage(
                            status="not_your_turn",
                            message=f"{player.name} назвал: {city}",
                            next_letter=self.last_letter,
                        )
                    )

            self.next_player()

            if self.count_alive() == 1:
                winner = [p for p in self.players if p.alive][0]
                winner.queue.put(
                    goroda_pb2.ServerMessage(status="win", message="Вы победили!")
                )
                self.running = False

    def validate_city(self, city):
        if city not in self.all_cities:
            return False
        if city in self.used_cities:
            return False
        if self.last_letter and city[0] != self.last_letter:
            return False
        return True

    def get_last_letter(self, city):
        for ch in reversed(city):
            if ch not in "ьъы":
                return ch
        return city[-1]

    def next_player(self):
        while True:
            self.current_index = (self.current_index + 1) % len(self.players)
            if self.players[self.current_index].alive:
                break

    def count_alive(self):
        return sum(1 for p in self.players if p.alive)

    def remove_dead_players(self):
        if self.count_alive() < 2:
            self.running = False


class GorodaService(goroda_pb2_grpc.GorodaGameServicer):
    def __init__(self):
        with open("cities.txt", encoding="utf-8") as f:
            self.cities = set(city.strip().lower() for city in f)
        self.lock = threading.Lock()
        self.lobby = []

    def JoinGame(self, request_iterator, context):
        name = None
        input_queue = queue.Queue()

        def listen():
            for msg in request_iterator:
                input_queue.put(msg)

        listener_thread = threading.Thread(target=listen, daemon=True)
        listener_thread.start()

        while True:
            try:
                msg = input_queue.get(timeout=1)
                if msg.player_name:
                    name = msg.player_name
                    break
            except queue.Empty:
                continue

        player = Player(name, input_queue)
        with self.lock:
            self.lobby.append(player)
            print(f"Игрок {name} присоединился к лобби.")

            if len(self.lobby) >= MIN_PLAYERS:
                session_players = self.lobby[:MAX_PLAYERS]
                self.lobby = self.lobby[MAX_PLAYERS:]
                session = GameSession(session_players, self.cities)
                session.start()

        while player.alive:
            try:
                msg = player.queue.get(timeout=1)
                yield msg
            except queue.Empty:
                continue


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    goroda_pb2_grpc.add_GorodaGameServicer_to_server(GorodaService(), server)
    port = os.getenv("PORT", "50051")
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Сервер запущен на порту {port}")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
