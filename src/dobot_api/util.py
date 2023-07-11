import socket
import logging as log
from typing import Optional, Tuple
from .types import DobotError

class DobotSocketConnection:
    def __init__(self, ip: str, port: int):
        self.socket = socket.socket()
        self.socket.settimeout(10.0)
        self.socket.connect((ip, port))
        log.debug("Connection established")

    "Sends a desired command over the socket connection"
    def send_command(self, cmd: str) -> Tuple[Optional[DobotError], str]:
        encoded_cmd = cmd.encode("utf-8")
        self.socket.send(encoded_cmd)
        log.debug(f'The command "{encoded_cmd}" has been sent.')
        return self.await_reply()

    # This is a quick and easy solution, but may not cover all ErrorIDs.
    def await_reply(self) -> Tuple[Optional[DobotError], str]:
        data = self.socket.recv(1024)
        response: str = str(data, encoding="utf-8")
        log.debug(f'The return message was "{response}".')
        split_response = response.split(",")
        errorID: int = int(split_response[0].strip())
        return_value: str = split_response[1].strip()
        if errorID == 0:
            return (None, return_value)
        else:
            # It will panic here if errorID is not impl'd
            return (DobotError(errorID), return_value[1:-1])

        
def clamp(val: int, local_min: int, local_max: int) -> int:
    log.info(f"{val} was clamped to the range {local_min}, {local_max}")
    return max(local_min, min(val, local_max))

     