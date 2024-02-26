import logging
import os
import signal
import sys
import json
from termcolor import colored as color
from pathlib import Path
import importlib.util
from neonize.client import NewClient
from neonize.events import (
    ConnectedEv,
    MessageEv,
    PairStatusEv,
    event,
    ReceiptEv,
    CallOfferEv,    
)
from neonize.utils import log
from lib.my_collections import Collection
from handler.message_handler import message_handler

sys.path.insert(0, os.getcwd())

with open('./config.json') as json_file:
    config = json.load(json_file)

def interrupted(*_):
    event.set()


log.setLevel(logging.ERROR)
signal.signal(signal.SIGINT, interrupted)

if not os.path.exists('./sessions'):
            os.makedirs('./sessions')
client = NewClient("sessions/Celly.session.sqlite3")

client.commands = Collection()
client.config = config

@client.event(ConnectedEv)
def on_connected(_: NewClient, __: ConnectedEv):
    print(color("[INFO]", "yellow") + "Client Connected")


@client.event(ReceiptEv)
def on_receipt(_: NewClient, receipt: ReceiptEv):
    log.debug(receipt)


@client.event(CallOfferEv)
def on_call(_: NewClient, call: CallOfferEv):
    log.debug(call)


def read_commands():
    root_dir = Path(__file__).parent / "commands"
    dirs = os.listdir(root_dir)

    for subdir in dirs:
        command_files = [file for file in os.listdir(root_dir / subdir) if file.endswith(".py")]
        for file in command_files:
            module_path = root_dir / subdir / file

            spec = importlib.util.spec_from_file_location("command", module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            client.commands[module.command["name"]] = module.command

    print(color("[INFO]", "yellow") + "Command Loaded")
read_commands()

@client.event(MessageEv)
def on_message(client: NewClient, message: MessageEv):
    message_handler(client, message)                               

@client.event(PairStatusEv)
def PairStatusMessage(_: NewClient, message: PairStatusEv):
    log.info(f"logged as {message.ID.User}")


client.PairPhone(config["botNumber"], show_push_notification=True)

client.connect()