import json
import random
import discord
from discord.ui import Button, View
import logging
import time


def convert_time(time):
    # Convert a string like "1d 2h 3m 4s" to seconds
    time = time.split(" ")
    seconds = 0
    for i in time:
        if i.endswith("d"):
            seconds += int(i[:-1]) * 86400
        elif i.endswith("h"):
            seconds += int(i[:-1]) * 3600
        elif i.endswith("m"):
            seconds += int(i[:-1]) * 60
        elif i.endswith("s"):
            seconds += int(i[:-1])
    return seconds