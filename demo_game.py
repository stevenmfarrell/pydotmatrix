from client import IDotMatrixClient
#from discover import get_idotmatrix_display
import asyncio
from pynput import keyboard


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


async def main():
    device = '70A65001-FFFE-8259-B6A8-84E3C2CC930E'
    #device = await get_idotmatrix_display()
    color = (255, 0, 0)
    BLACK = (0, 0, 0)
    pos = (8, 8)

    async with IDotMatrixClient(device) as client:
        key_queue = transmit_keys()
        await client.enter_diy_mode()
        await client.draw_pixel(color, pos)
        while True:
            key = await key_queue.get()
            newpos = get_new_pos(pos, key)
            if newpos == pos:
                continue
            else:
                await client.draw_pixel(color, newpos)
                await client.draw_pixel(BLACK, pos)
                pos = newpos
                await asyncio.sleep(0.01)




def clamp(n, minn, maxn):
    return max(min(maxn, n), minn)

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


if __name__=='__main__':
    asyncio.run(main())