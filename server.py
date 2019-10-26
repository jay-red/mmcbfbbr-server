import asyncio
import websockets
import os

async def mmcbfbbr( websocket, path ):
	async for msg in websocket:
		await websocket.send( msg )

start_server = websockets.serve( mmcbfbbr, "0.0.0.0",  )

asyncio.get_event_loop().run_until_complete( start_server, int( os.environ[ "PORT" ] ) )
asyncio.get_event_loop().run_forever()