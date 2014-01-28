import os
import sys
from munin import MuninPlugin
from cablestats import ComcastBCModem


def _to_long_name(ch):
    return ch.replace("ch", "Channel ")


class CableModemPlugin(MuninPlugin):
    category = "Cable"

    def __init__(self):
        self.host_name = os.environ.get("CM_HOST", "10.1.10.1")
        modem = ComcastBCModem(self.host_name)
        stats = modem.get_cm_stats()

        if self.direction == 'upstream':
            self.data = stats.us_channels
        elif self.direction == 'downstream':
            self.data = stats.ds_channels
        else:
            sys.exit(1)

    @property
    def fields(self):
        ret = []
        for ch in self.data.iterkeys():
            field = (ch, dict(
                label=_to_long_name(ch),
                type="GAUGE",
                info=self.channel_info(ch)
            ))
            ret.append(field)
        return ret

    def execute(self):
        ret = {}
        for (ch, value) in self.data.iteritems():
            ret[ch] = value[self.field]
        return ret
