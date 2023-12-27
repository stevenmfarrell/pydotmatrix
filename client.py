import asyncio
from typing import Tuple
from bleak import BleakClient
from core.idotmatrix.diy import DIY
from core.idotmatrix.graffiti import Graffiti
import time
from PIL import Image

from process_gif import gif_frames

UUID_WRITE_DATA = "0000fa02-0000-1000-8000-00805f9b34fb"
UUID_READ_DATA = "0000fa03-0000-1000-8000-00805f9b34fb"

def notification_handler(sender, data):
    """Simple notification handler which prints the data received."""
    output_numbers = list(data)
    #print(output_numbers)

class IDotMatrixClient:
    def __init__(self, address: str):
        self.address = address
        self.client = BleakClient(address)

    async def write_bytes(self, bytes):
        await self.client.write_gatt_char(UUID_WRITE_DATA, bytes)

    async def enter_diy_mode(self):
        await self.write_bytes(DIY(self.mtu_size).enter(1))

    async def draw_pixel(self, rgb: Tuple[int, int, int], xy: Tuple[int, int]):
        await self.write_bytes(Graffiti().setPixelColor(*rgb, *xy)
        )
    
    async def draw_image(self, image: Image):
        mtus = DIY(self.mtu_size).sendDIYMatrix(image)
        for mtu in mtus:
            await self.client.write_gatt_char(UUID_WRITE_DATA, mtu)
            time.sleep(0.05)

    async def draw_gif(self, path, delay=0.05, frame_fn=lambda x: x, reps=1):
        frames = [frame for frame in gif_frames(path)]
        frames = [frame_fn(f) for f in frames]
        for i in range(reps):
            for frame in frames:
                #print(f'drawing frame from rep {i}')
                await self.draw_image(frame)
                await asyncio.sleep(delay)

    async def __aenter__(self):
        await self.client.__aenter__()
        self.gatt_characteristic = self.client.services.get_characteristic(UUID_WRITE_DATA)
        self.mtu_size = self.gatt_characteristic.max_write_without_response_size
        await self.client.start_notify(UUID_READ_DATA, notification_handler)
        return self


    async def __aexit__(self, exc_type, exc, tb):
        await self.client.__aexit__(exc_type, exc, tb)
        print('exit IDotMatrixClient')

