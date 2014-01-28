import os
import sys
from munin import MuninPlugin
from cablestats import ComcastModem

def _to_long_name(ch):
	return ch.replace("ch", "Channel ")

class CableModemPlugin(MuninPlugin):
	category = "Cable"

	@property
	def title(self):
		return "{} @ {}".format(self.cm_title, self.host)

	def __init__(self):
		self.host = os.environ.get("CM_HOST", "10.1.10.1")
		modem = ComcastModem(self.host)
		stats = modem.get_cm_stats()

		if self.cm_direction == 'upstream':
			self.data = stats.us_channels
		elif self.cm_direction == 'downstream':
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
			ret[ch] = value[self.cm_field]
		return ret
