from typing import List
import asyncio
import numpy as np
from scipy.ndimage import convolve
from PIL import Image
from pynput import keyboard

from client import IDotMatrixClient
from life_util import get_board_img, get_new_pos, transmit_keys, arrow_keys

LifeBoard = List[List[int]]
kernel = np.array([[1, 1, 1], 
                       [1, 0, 1], 
                       [1, 1, 1]], dtype=np.uint8)

def next_life_generation(life_state: LifeBoard):
    board = np.array(life_state)
    convolved_board = convolve(board, kernel, mode="wrap")
    next_board: np.array = (
        ((board == 1) & (convolved_board > 1) & (convolved_board < 4))
        | ((board == 0) & (convolved_board == 3))
    ).astype(np.uint8)
    return next_board.tolist()

def get_initial_board():
        # a glider
        board = np.zeros((16, 16))
        board[8,2]=1
        board[8,3]=1
        board[8,4]=1
        board[7,4]=1
        board[6,3]=1
        return board

class LifeRunningState:
    def __init__(self, client: IDotMatrixClient, delay=0.05):
        self.client = client
        self.delay=delay

    async def enter(self, initial_board: LifeBoard):
        board = initial_board
        key_queue = transmit_keys()
        while True:
            im = get_board_img(board)
            await self.client.draw_image(im)
            await asyncio.sleep(self.delay)
            board = next_life_generation(board)
            try:
                key = key_queue.get_nowait()
                if key == keyboard.Key.enter:
                    running_state = LifeEditorState(self.client)
                    await running_state.enter(initial_board)
            except asyncio.QueueEmpty:
                pass


class LifeEditorState:
    CURSOR_COLOR = (255, 0, 0)
    BLACK = (0, 0, 0)
    CURSOR_HIGHLIGHTED = (255, 160, 160)
    WHITE = (255, 255, 255)
    def __init__(self, client: IDotMatrixClient):
        self.client = client             
    
    async def draw_cursor_at_pos(self, pos):
        board_value = self.board[pos[1], pos[0]]
        if board_value:
            cursor_color = self.CURSOR_HIGHLIGHTED
        else:
            cursor_color = self.CURSOR_COLOR
        await self.client.draw_pixel(cursor_color, pos)

    async def handle_space(self):
        pos = self.pos
        board_value = self.board[pos[1], pos[0]]
        if board_value:
            new_val = 0
        else:
            new_val = 1
        self.board[pos[1], pos[0]] = new_val
        im = get_board_img(self.board)
        await self.client.draw_image(im)
        await self.draw_cursor_at_pos(pos)
        

    async def handle_arrow_key(self, key: keyboard.Key):
        pos = self.pos
        newpos = get_new_pos(pos, key)
        if newpos != pos:
            oldpos_board_value = self.board[pos[1], pos[0]]

            if oldpos_board_value:
                old_color = self.WHITE
            else:
                old_color = self.BLACK
            await self.draw_cursor_at_pos(newpos)
            await self.client.draw_pixel(old_color, pos)
            self.pos = newpos

    async def enter(self, initial_board: LifeBoard = None):
        if initial_board is None:
            initial_board = get_initial_board()
        key_queue = transmit_keys()
        self.board = initial_board
        im = get_board_img(self.board)
        self.pos= (8, 8)
        await self.client.draw_image(im)
        await self.client.draw_pixel(self.CURSOR_COLOR, self.pos)
        while True:
            key = await key_queue.get()
            if key in arrow_keys:
                await self.handle_arrow_key(key)
            if key == keyboard.Key.space:
                await self.handle_space()
            if key == keyboard.Key.enter:
                running_state = LifeRunningState(self.client)
                await running_state.enter(self.board)
        
async def main():
    device = '70A65001-FFFE-8259-B6A8-84E3C2CC930E'
    board = get_initial_board()
    async with IDotMatrixClient(device) as client:
        await client.enter_diy_mode()
        editor_state = LifeEditorState(client)
        await editor_state.enter(board)

if __name__=='__main__':
    asyncio.run(main())