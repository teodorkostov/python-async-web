from asyncio import Future
import logging
import ssl
import websockets
from websockets.exceptions import ConnectionClosed

from stream import Stream


class WebSocketClient():
  def __init__(self, stream: Stream, uri: str):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.uri = uri
    self.ssl_context = ssl.create_default_context()
    self.stream = stream

  async def connect(self, stop: Future):
    self.connection = await websockets.connect(self.uri, ssl=self.ssl_context)
    if self.connection.open:
      self.logger.info('connection established to {}'.format(self.uri))
    else:
      self.logger.error('connection failed to {}'.format(self.uri))
      stop.set_result('CONNECT_ERROR')

  async def run(self, stop: Future):
    self.logger.info('listening for socket data')
    while not stop.done():
      try:
        message = await self.connection.recv()
        self.stream.send(message)
      except ConnectionClosed:
        self.logger.warning('connection closed to {}'.format(self.uri))
        stop.set_result('DISCONNECT')

  async def disconnect(self, stop: Future):
    await stop
    self.logger.info('closing connection to {}'.format(self.uri))
    await self.connection.close()
