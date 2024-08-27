from libprobe.probe import Probe
from lib.check.phpfpm import check_phpfpm
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = {
        'phpfpm': check_phpfpm,
    }

    probe = Probe("phpfpm", version, checks)

    probe.start()
