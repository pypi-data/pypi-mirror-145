from .utils import objects


class Game:

    def __init__(self, client) -> None:
        self.client = client

    def create(self, bet, password: str = "", table: int = 1,
        fast: bool = False, type: int = 1, limits: int = 3) -> objects.Game:
        self.client.send_server(
            {
                "command": "create",
                "bet": bet,
                "password": password,
                "fast": fast,
                "table": table,
                "type": type,
                "limits": limits,
            }
        )

        data = self.client._get_data("game")
        if data["command"] == 'err':
            raise objects.Err(data)
        return objects.Game(data).Game

    def buyin(self, chips: int = 30000) -> None:
        self.client.send_server(
            {
                "command": "buyin",
                "chips": chips,
            }
        )

    def join(self, password: str, game_id: int) -> None:
        self.client.send_server(
            {
                "command": "join",
                "password": password,
                "id": game_id,
            }
        )

    def invite(self, user_id: int) -> None:
        self.client.send_server(
            {
                "command": "invite_to_game",
                "user_id": user_id,
            }
        )

    def rejoin(self, position: int, game_id: int) -> None:
        self.client.send_server(
            {
                "command": "rejoin",
                "p": position,
                "id": game_id,
            }
        )

    def leave(self, game_id: int) -> None:
        self.client.send_server(
            {
                "command": "leave",
                "id": game_id,
            }
        )

    def publish(self) -> None:
        return self.client.send_server(
            {
                "command": "game_publish",
            }
        )

    def send_smile(self, smile_id: int = 16) -> None:
        self.client.send_server(
            {
                "command": "smile",
                "id": smile_id,
            }
        )

    def ca(self) -> None:
        self.client.send_server(
            {
                "command": "ca",
            }
        )

    def get_obs(self) -> None:
        self.client.send_server(
            {
                "command": "get_obs",
            }
        )

    def surrender(self) -> None:
        self.client.send_server(
            {
                "command": "surrender",
            }
        )

    def player_swap(self, position: int) -> None:
        self.client.send_server(
            {
                "command": "player_swap",
                "id": position,
            }
        )