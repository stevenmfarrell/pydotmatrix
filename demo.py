from client import IDotMatrixClient
#from discover import get_idotmatrix_display
import asyncio
from PIL import Image

async def main():
    device = '70A65001-FFFE-8259-B6A8-84E3C2CC930E'
    #device = await get_idotmatrix_display()
    async with IDotMatrixClient(device) as client:
        await client.enter_diy_mode()
        await client.draw_pixel(rgb=(255, 0, 0), xy=(0, 0))
        await client.draw_pixel(rgb=(0, 255, 0), xy=(1, 1))
        await client.draw_pixel(rgb=(0, 0, 255), xy=(2, 2))
        await client.draw_pixel(rgb=(255, 255, 255), xy=(3, 3))
        await asyncio.sleep(0.5)
        await client.enter_diy_mode()

        im = Image.open('images/mario.jpg')
        im = im.resize((16,16))
        await client.draw_image(im)
        await asyncio.sleep(0.2)
        #while True:
        #    await client.draw_gif('images/fire.gif', reps=3, delay = 0.1, frame_fn=frame_cleanup)        
        while True:
            await client.draw_gif('images/dog_sit_idle.gif', reps=3, frame_fn=frame_cleanup)
            await client.draw_gif('images/dog_stand_idle.gif', reps=1, frame_fn=frame_cleanup)
            await client.draw_gif('images/dog_run.gif', reps=8, frame_fn=frame_cleanup)
            await client.draw_gif('images/dog_pose_idle.gif', reps=2, frame_fn=frame_cleanup)


def frame_cleanup(im: Image.Image) -> Image.Image:
    im2 = im.copy().resize((16,16), resample = Image.NEAREST)
    new_image = Image.new("RGBA", im2.size, (10, 30, 20))
    new_image.paste(im2, mask=im2)
    return new_image


if __name__=='__main__':
    asyncio.run(main())