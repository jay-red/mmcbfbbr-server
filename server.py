import asyncio
import websockets
import os
from random import choice

OP_JOIN = 0x00
OP_GAME = 0x01
OP_START = 0x02
OP_PMOVE = 0x03
OP_SMOVE = 0x04
OP_PROG = 0x05
OP_SPEC = 0x06
OP_STOP = 0x07
OP_WAIT = 0x08
OP_HEALTH = 0x09

nextUID = 0
game = None
bossID = 0
players = {}
started = False

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
	global game, players, nextUID
	async for msg in client:
		print( msg )
		code = ord( msg[ 0 ] )
		data = msg[ 1 : ]
		if code == OP_JOIN:
			nextUID += 1
			players[ client ] = Player( nextUID, data )
			await client.send( chr( OP_JOIN ) + chr( nextUID ) )
			await game.send( chr( OP_JOIN ) + chr( nextUID ) + data )
		elif code == OP_GAME:
			if game:
				pass
			else:
				game = client
				try:
					await client.send( chr( OP_GAME ) + chr( 0x00 ) )
				except websockets.exceptions.ConnectionClosedOK:
					print( "closed" )
		elif code == OP_START:
			for player in players:
				try:
					await player.send( chr( OP_START ) )
				except websockets.exceptions.ConnectionClosedOK:
					print( "closed" )
		elif code == OP_STOP:
			reset()
		elif code == OP_PMOVE:
			print("moved")
			try:
				await game.send( chr( OP_PMOVE ) + chr( players[ client ].uid ) + data )
			except websockets.exceptions.ConnectionClosedOK:
				print( "closed" )
		elif code == OP_SMOVE:
			try:
				await game.send( chr( OP_SMOVE ) + chr( players[ client ].uid ) + data )
			except websockets.exceptions.ConnectionClosedOK:
				print( "closed" )
		elif code == OP_WAIT:
			bossID = choice( tuple( players.values() ) ).uid
			for player in players:
				try:
					await player.send( chr( OP_WAIT ) + chr( bossID ) )
				except websockets.exceptions.ConnectionClosedOK:
					print( "closed" )
				try:
					await game.send( chr( OP_WAIT ) + chr( bossID ) )
				except websockets.exceptions.ConnectionClosedOK:
					print( "closed" )
		elif code == OP_HEALTH:
			for player in players:
				try:
					await player.send( chr( OP_WAIT ) + chr( bossID ) )
				except websockets.exceptions.ConnectionClosedOK:
					print( "closed" )
				try:
					await game.send( chr( OP_WAIT ) + chr( bossID ) )
				except websockets.exceptions.ConnectionClosedOK:
					print( "closed" )


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

if( "PORT" in os.environ ):
	start_server = websockets.serve( mmcbfbbr, "0.0.0.0", os.environ[ "PORT" ] )
else:
	start_server = websockets.serve( mmcbfbbr, "0.0.0.0", 1004 )

asyncio.get_event_loop().run_until_complete( start_server )
asyncio.get_event_loop().run_forever()