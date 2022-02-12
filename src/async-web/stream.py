from asyncio import Queue
from rx.subject import Subject
from string import Template
from typing import Protocol


class Stream(Protocol):
  def send(self, message: str):
    raise NotImplementedError


class AsyncStream(Stream):
  def __init__(self):
    super().__init__()
    self.stream = Queue()

  def send(self, message: str):
    self.stream.put_nowait(message)


class RxStream(Stream):
  def __init__(self):
    super().__init__()
    self.stream = Subject()

  def send(self, message: str):
    self.stream.on_next(message)


class WrappedStream(Stream):
  def __init__(self, template_string: Template):
    super().__init__()
    self.template_string = template_string

  def send(self, message: str):
    message = self.template_string.substitute(data=message)
    super().send(message)
