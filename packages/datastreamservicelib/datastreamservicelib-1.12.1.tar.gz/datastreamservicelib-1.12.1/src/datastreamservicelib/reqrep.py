"""REQuest/REPly helpers"""
from typing import Union, Any, cast
import asyncio
import logging
import tempfile
from pathlib import Path
from dataclasses import dataclass


import zmq
from datastreamcorelib.abstract import ZMQSocketDescription, ZMQSocketType, ZMQSocketUrisInputTypes, ZMQSocket
from datastreamcorelib.datamessage import PubSubDataMessage
from datastreamcorelib.reqrep import REQMixinBase, REPMixinBase

from .zmqwrappers import Socket
from .service import SimpleServiceMixin, SimpleService


LOGGER = logging.getLogger(__name__)
REQ_SEND_TIMEOUT = 0.5
REQ_RECV_TIMEOUT = 1.0
REP_SEND_TIMEOUT = 0.5


class REQMixin(SimpleServiceMixin, REQMixinBase):
    """Mixin for making REQuests"""

    def _get_request_socket(self, sockdef: Union[ZMQSocket, ZMQSocketUrisInputTypes]) -> ZMQSocket:
        """Get the socket"""
        if isinstance(sockdef, ZMQSocket):
            return sockdef
        sdesc = ZMQSocketDescription(sockdef, ZMQSocketType.REQ)
        return self.psmgr.sockethandler.get_socket(sdesc)

    def _do_reqrep_blocking(
        self, sockdef: Union[ZMQSocket, ZMQSocketUrisInputTypes], msg: PubSubDataMessage
    ) -> PubSubDataMessage:
        raise TypeError("Not supported")

    async def _do_reqrep_async(
        self, sockdef: Union[ZMQSocket, ZMQSocketUrisInputTypes], msg: PubSubDataMessage
    ) -> PubSubDataMessage:
        """Do the actual REQuest and get the REPly (async context)"""
        sock = cast(Socket, self._get_request_socket(sockdef))
        try:
            await asyncio.wait_for(sock.send_multipart(msg.zmq_encode()), timeout=REQ_SEND_TIMEOUT)
            resp_parts = await asyncio.wait_for(sock.recv_multipart(), timeout=REQ_RECV_TIMEOUT)
            return PubSubDataMessage.zmq_decode(resp_parts)
        except (asyncio.TimeoutError, zmq.ZMQBaseError):
            sock.close()
            raise

    async def send_command(
        self, sockdef: Union[ZMQSocket, ZMQSocketUrisInputTypes], cmd: str, *args: Any, raise_on_insane: bool = False
    ) -> PubSubDataMessage:
        """shorthand for send_command_async"""
        return await self.send_command_async(sockdef, cmd, *args, raise_on_insane=raise_on_insane)


class REPMixin(SimpleServiceMixin, REPMixinBase):
    """Mixin for making REPlies"""

    def _resolve_default_rep_socket_uri(self) -> str:
        """Resolves the path for default PUB socket and sets it to PubSubManager"""
        pub_default = "ipc://" + str(Path(tempfile.gettempdir()) / self.configpath.name.replace(".toml", "_rep.sock"))
        if "zmq" in self.config and "rep_sockets" in self.config["zmq"]:
            pub_default = self.config["zmq"]["rep_sockets"]
        return pub_default

    async def _reply_task(self, sockdef: Union[ZMQSocket, ZMQSocketUrisInputTypes, None]) -> None:
        """Bind the given socket and start dealing with REQuests"""
        sdesc = None
        if isinstance(sockdef, ZMQSocket):
            sock = cast(Socket, sockdef)
        else:
            if sockdef is None:
                sockdef = self._resolve_default_rep_socket_uri()
            sdesc = ZMQSocketDescription(sockdef, ZMQSocketType.REP)
            sock = cast(Socket, self.psmgr.sockethandler.get_socket(sdesc))
        try:
            while not sock.closed:
                msgparts = await sock.recv_multipart()
                replymsg = await self.handle_rep_async(msgparts, sdesc)
                await asyncio.wait_for(sock.send_multipart(replymsg.zmq_encode()), timeout=REP_SEND_TIMEOUT)
            LOGGER.info("{} closed from under us".format(sock))
        except asyncio.CancelledError:
            LOGGER.debug("cancelled")
        finally:
            sock.close()

    def reload(self) -> None:
        """Load configs, restart sockets"""
        super().reload()
        # Create reply handler in the default uri
        self.create_task(self._reply_task(None), name="DEFAULT_REP")


@dataclass  # pylint: disable=R0901
class FullService(REPMixin, REQMixin, SimpleService):  # pylint: disable=R0901
    """Service with REQuest and REPly mixins applied"""
