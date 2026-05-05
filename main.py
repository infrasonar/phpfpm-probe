from libprobe.probe import Probe
from lib.check.phpfpm import CheckPhpFpm
from lib.version import __version__ as version


if __name__ == '__main__':
    checks = (
        CheckPhpFpm,
    )

    probe = Probe("phpfpm", version, checks)

    probe.start()
