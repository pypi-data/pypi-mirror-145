import logging
from .sharedobj import common, current_command
from .tools import debug
import elbus
import msgpack

logger = logging.getLogger('elbus.client')
logger.setLevel(logging.CRITICAL)


def call_rpc(method, params=None, target='eva.core'):
    if current_command.debug:
        debug(f'calling ELBUS {common.elbus_path} as {common.elbus_name}')
    if common.bus is None or not common.bus.is_connected():
        common.bus = elbus.client.Client(common.elbus_path, common.elbus_name)
        common.bus.connect()
        common.rpc = elbus.rpc.Rpc(common.bus)
    if current_command.debug:
        debug(f'target: {target}')
        debug(f'method: {method}')
        debug(f'params: {params}')
    result = common.rpc.call(
        target,
        elbus.rpc.Request(method,
                          params=b'' if params is None else
                          msgpack.dumps(params))).wait_completed(
                              timeout=current_command.timeout)
    if result.is_empty():
        return None
    else:
        return msgpack.loads(result.get_payload(), raw=False)
