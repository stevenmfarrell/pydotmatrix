
from typing import List
from pynput import keyboard
import asyncio
from PIL import Image
import numpy as np

LifeBoard = List[List[int]]


def transmit_keys():
    # https://stackoverflow.com/questions/64658835/how-to-combine-callback-based-library-with-asyncio-library-in-python
    # Start a keyboard listener that transmits keypresses into an
    # asyncio queue, and immediately return the queue to the caller.
    queue = asyncio.Queue()
    loop = asyncio.get_event_loop()
    def on_press(key):
        # this callback is invoked from another thread, so we can't
        # just queue.put_nowait(key.char), we have to go through
        # call_soon_threadsafe
        loop.call_soon_threadsafe(queue.put_nowait, key)
    keyboard.Listener(on_press=on_press).start()
    return queue

def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

arrow_keys = [keyboard.Key.up, keyboard.Key.down, keyboard.Key.left, keyboard.Key.right]

def get_new_pos(pos, key: keyboard.Key):
    if key == keyboard.Key.up:
        newpos = (pos[0], pos[1]-1)
    elif key == keyboard.Key.down:
        newpos = (pos[0], pos[1]+1)
    elif key == keyboard.Key.left:
        newpos = (pos[0]-1, pos[1])
    elif key == keyboard.Key.right:
        newpos = (pos[0]+1, pos[1])
    else:
        newpos = pos
    newpos = (clamp(newpos[0], 0, 15), clamp(newpos[1], 0, 15))
    return newpos

def get_board_img(board: LifeBoard):
    npboard = np.array(board)*255
    npboard = np.uint8(npboard)
    im = Image.fromarray(npboard).convert('RGB')
    return im