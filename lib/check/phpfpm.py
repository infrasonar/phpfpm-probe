import aiohttp
import logging
from libprobe.asset import Asset
from libprobe.check import Check
from libprobe.exceptions import CheckException
from libprobe.exceptions import IgnoreCheckException
from ..connector import get_connector


class CheckPhpFpm(Check):
    key = 'phpfpm'

    @staticmethod
    async def run(asset: Asset, local_config: dict, config: dict) -> dict:

        try:
            url = config['statusUrl']
        except Exception:
            logging.warning(
                'Check did not run; '
                'statusUrl is not provided, invalid or empty')
            raise IgnoreCheckException

        try:
            async with aiohttp.ClientSession(connector=get_connector()) as se:
                async with se.get(
                    url,
                    params={'json': '1'},
                    ssl=False
                ) as resp:
                    resp.raise_for_status()
                    data = await resp.json()
        except Exception as e:
            msg = str(e) or type(e).__name__
            raise CheckException(msg)

        return {
            'phpfpm': [{
                'name': 'phpfpm',
                'pool': data.get('pool'),
                'process_manager': data.get('process manager'),
                'start_time': data.get('start time'),
                'start_since': data.get('start since'),
                'accepted_conn': data.get('accepted conn'),
                'listen_queue': data.get('listen queue'),
                'max_listen_queue': data.get('max listen queue'),
                'listen_queue_len': data.get('listen queue len'),
                'idle_processes': data.get('idle processes'),
                'active_processes': data.get('active processes'),
                'total_processes': data.get('total processes'),
                'max_active_processes': data.get('max active processes'),
                'max_children_reached': data.get('max children reached'),
                'slow_requests': data.get('slow requests'),
            }],
        }
