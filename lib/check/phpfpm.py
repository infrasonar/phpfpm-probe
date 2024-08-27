import aiohttp
import logging
from libprobe.asset import Asset
from libprobe.exceptions import CheckException
from libprobe.exceptions import IgnoreCheckException


async def check_phpfpm(
        asset: Asset,
        asset_config: dict,
        check_config: dict):

    try:
        url = check_config['statusUrl']
    except Exception:
        logging.warning(
            'Check did not run; '
            'statusUrl is not provided, invalid or empty')
        raise IgnoreCheckException
    # TODO allow_redirects, verify_ssl config

    # TODO make request.params nicer
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params={'json': 'True'}) as resp:
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
