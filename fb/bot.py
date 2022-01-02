import os
import random

import facebook as fb
from os import walk
from datetime import datetime, time
from time import sleep


def post_meme(bot):
    memes = list_files()
    meme = memes.pop()
    bot.put_photo(open("resources/memes/" + meme, "rb"))
    os.remove("resources/memes/" + meme)


def wait_start(runTime, bot):
    startTime = time(*(map(int, runTime.split(':'))))
    while startTime > datetime.today().time():
        sleep(1)
    post_meme(bot)


def list_files():
    return set(next(walk("resources/memes"), (None, None, []))[2])


def read_token():
    with open("resources/token.txt", mode="r") as file:
        return file.read()


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
        break
