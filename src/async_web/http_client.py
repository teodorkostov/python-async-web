from aiohttp import ClientSession
import logging

from .stream import Stream



class HttpClient():
  def __init__(self, stream: Stream, url: str):
    self.logger = logging.getLogger(self.__class__.__name__)
    self.url = url
    self.stream = stream


  async def get(self, params: dict):
    async with ClientSession() as session:
      async with session.get(self.url, params=params) as response:
        self.logger.debug('got response from %s with status %s', response.url, response.status)

        message = await response.text()

        self.stream.send(message)
