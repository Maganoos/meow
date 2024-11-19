import hata
import os
from dotenv import load_dotenv
import requests

load_dotenv("meow.env")
client = hata.Client(os.getenv("TOKEN"), extensions = 'slash')


@client.events
async def ready(client):
    print(f"{client:f} is ready.")

@client.interactions(guild=1286362395719106694)
async def ping():
    return f"Pong!"
@client.interactions(is_global=True)
async def online(
    client,
    event,
    server: (str, "What server?") = "play.alinea.gg"
):
    online = ""
    response = requests.get(f"https://api.mcsrvstat.us/3/{server}").json()
    if response.get("players").get("online"):
        online_players = response.get("players")
        number_of_players = online_players.get("online")
        players_raw = online_players.get("list")
        names = [sigma["name"] for sigma in players_raw]
        names_formatted = f'```\n{", ".join(names)}\n```'
        if len(names) < 25:
            return f"There are {number_of_players} online on {server}: {names_formatted}"
        else:
            return f"There are {number_of_players} online on {server}."
    else:
        return "The server is either offline, or there are no players on."

client.start()

hata.wait_for_interruption()