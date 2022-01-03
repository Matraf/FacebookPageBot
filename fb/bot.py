import os
import random

import facebook as fb
from os import walk
from datetime import datetime, time
from time import sleep

TOKEN = "resources/token.txt"
QUEUE = "resources/memes/"
P_QUEUE = "resources/prio_memes/"


def list_files(dir):
    return set(next(walk(dir), (None, None, []))[2])


def read_token():
    with open(TOKEN, mode="r") as file:
        return file.read()


def post_meme(bot, meme, dir):
    bot.put_photo(open(dir + meme, "rb"))
    os.remove(dir + meme)


def wait_start(runTime, bot):
    prio_memes = list_files(P_QUEUE)
    memes = list_files(QUEUE)
    startTime = time(*(map(int, runTime.split(':'))))
    while startTime > datetime.today().time():
        sleep(1)
    if runTime[:2] == '15' and len(prio_memes) > 0:
        meme = prio_memes.pop()
        post_meme(bot, meme, P_QUEUE)
    else:
        meme = memes.pop()
        post_meme(bot, meme, QUEUE)


if __name__ == '__main__':
    hours = [10, 15, 19]
    token = read_token()
    i = 0
    bot = fb.GraphAPI(token)
    while (True):
        minute = str(random.randint(0, 59)).zfill(2)
        post_time = str(hours[i]) + ":" + minute
        print(post_time)

        wait_start(post_time, bot)

        i = (i + 1) % 3
