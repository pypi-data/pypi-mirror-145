import zmq
import zmq.asyncio

import uuid
from typing import Dict
from fastapi import WebSocket


class ConnectionManager:

    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

        self.sub_contexts: Dict[str, zmq.asyncio.Context] = {}
        self.sub_sockets: Dict[str, zmq.asyncio.Socket] = {}

    @property
    def connection_cnt(self):
        return len(self.active_connections)

    @property
    def context_cnt(self):
        return len(self.sub_contexts)

    @property
    def sub_socket_cnt(self):
        return len(self.sub_sockets)

    def status(self):
        status_str = f'Connection: {self.connection_cnt}. ZMQ Context: {self.context_cnt}. ZMQ Socket: {self.sub_socket_cnt}'
        return status_str

    def _new_id(self):
        return str(uuid.uuid1())

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        sock_id = self._new_id()
        self.active_connections[sock_id] = websocket
        return sock_id

    async def make_sub_socket(self,
                              websocket: WebSocket,
                              sub_host: str,
                              sub_port: int):
        for sock_id, socket in self.active_connections.items():
            if socket == websocket:
                self.sub_contexts[sock_id] = zmq.asyncio.Context()
                sock = self.sub_contexts[sock_id].socket(zmq.SUB)
                sock.connect(f'tcp://{sub_host}:{sub_port}')
                sock.setsockopt_string(zmq.SUBSCRIBE, '')
                self.sub_sockets[sock_id] = sock

    def disconnect(self, websocket: WebSocket):
        for sock_id, socket in self.active_connections.items():
            if socket == websocket:
                _ = self.active_connections.pop(sock_id)

                if sock_id in self.sub_sockets:
                    self.sub_sockets[sock_id].close()
                    del self.sub_sockets[sock_id]

                if sock_id in self.sub_contexts:
                    self.sub_contexts[sock_id].term()
                    del self.sub_contexts[sock_id]

                return sock_id

    async def sub_recv(self, websocket: WebSocket):
        for sock_id, socket in self.active_connections.items():
            if socket == websocket:
                data = await self.sub_sockets[sock_id].recv_string()
                return data

    async def send(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)