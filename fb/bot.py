import os
import random

import facebook as fb
from os import walk
from datetime import datetime, time
from time import sleep

TOKEN = "resources/token.txt"
QUEUE = "resources/memes/"
P_QUEUE = "resources/prio_memes/"

logger = open('logs.log', 'a+')


def list_files(path):
    return set(next(walk(path), (None, None, []))[2])


def read_token():
    with open(TOKEN, mode="r") as file:
        return file.read()


def post_meme(bot, meme, path):
    bot.put_photo(open(path + meme, "rb"))
    os.remove(path + meme)
    logger.write("Posted meme")


def wait_start(run_time, bot):
    prio_memes = list_files(P_QUEUE)
    memes = list_files(QUEUE)
    start_time = time(*(map(int, run_time.split(':'))))
    print(str(start_time) + " " + str(datetime.today().time()))
    while start_time > datetime.today().time():
        sleep(60)

    if run_time[:2] == '15' and len(prio_memes) > 0:
        meme = prio_memes.pop()
        post_meme(bot, meme, P_QUEUE)
    else:
        meme = memes.pop()
        post_meme(bot, meme, QUEUE)


if __name__ == '__main__':
    hours = [10, 15, 19]
    token = read_token()
    bot = fb.GraphAPI(token)

    current_hour = datetime.now().hour
    if current_hour < 10:
        i = 0
    elif 10 <= current_hour < 15:
        i = 1
    else:
        i = 2

    minute = str(random.randint(0, 59)).zfill(2)
    post_time = str(hours[i]) + ":" + minute
    logger.write("Next post at:\t" + post_time + "\n")

    wait_start(post_time, bot)
