import asyncio
import websockets
import os

OP_JOIN = 0x00
OP_GAME = 0x01
OP_START = 0x02
OP_PMOVE = 0x03
OP_SMOVE = 0x04
OP_PROG = 0x05
OP_SPEC = 0x06
OP_STOP = 0x07

nextUID = 0
game = None
players = {}

def reset():
	global nextUID, game, players
	nextUID = 0
	game = None
	players = {}

class Player():
	def __init__( self, uid, name ):
		self.uid = uid
		self.name = name

async def mmcbfbbr( client, path ):
	async for msg in client:
		code = ord( msg[ 0 ] )
		data = msg[ 1 : ]
		if code == OP_JOIN:
			nextUID += 1
			players[ client ] = Player( nextUID, data )
			await client.send( chr( OP_JOIN ) + chr( nextUID ) )
		elif code == OP_GAME:
			if( !game ):
				game = client
				await client.send( chr( OP_GAME ) + chr( 0x00 ) )
		elif code == OP_START:
			for player in players:
				await player.send( chr( OP_START ) )
		elif code == OP_STOP:
			reset()
		elif code == OP_PMOVE:
			await game.send( msg )
		elif code == OP_SMOVE:
			await game.send( msg )


"""
OPCODES
00: player join

01: game join

02: 

03: 

04: 

05: 

06

07
 
08
"""

start_server = websockets.serve( mmcbfbbr, "0.0.0.0", int( os.environ[ "PORT" ] ) )

asyncio.get_event_loop().run_until_complete( start_server )
asyncio.get_event_loop().run_forever()