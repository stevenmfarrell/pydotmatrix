import asyncio
from bleak import BleakScanner, BLEDevice

async def main():
    try:
        d = await _get_idotmatrix_display()
        print(f'Found iDotMatrix display: {d}')
    except Exception as e:
        print(e)
        await list_devices()



async def list_devices():
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)

async def _get_idotmatrix_display(search_str = 'IDM-') -> BLEDevice:
    devices = await BleakScanner.discover()
    for d in devices:
        if d.name and search_str in d.name:
            return d
    raise Exception('Unable to find iDotMatrix display')

async def get_idotmatrix_display_address() -> str:
    device = '70A65001-FFFE-8259-B6A8-84E3C2CC930E'
    return device



if __name__=='__main__':
    asyncio.run(main())