import asyncio
import websockets

async def mmcbfbbr( websocket, path ):
	async for msg in websocket:
		await websocket.send( msg )

start_server = websockets.serve( mmcbfbbr, "0.0.0.0", 1004 )

asyncio.get_event_loop().run_until_complete( start_server )
asyncio.get_event_loop().run_forever()