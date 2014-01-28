from collections import namedtuple
import cookielib
import datetime
import re

import lxml.html as html
import requests

def camel_to_under(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


class ComcastModem(object):
	_DEFAULT_USERNAME = "cusadmin"
	_DEFAULT_PASSWORD = "highspeed"

	# 5 Minutes (in secs). This is a total guess and can probably be increased depening on the actual timeout
	_DEFAULT_LOGIN_TIMEOUT = 60 * 5

	_LOGIN_URL   = "http://{host}/goform/login"
	_CMSTATS_URL = "http://{host}/user/feat-gateway-modem.asp"

	def __init__(self, host, 
		         username=_DEFAULT_USERNAME, 
		         password=_DEFAULT_PASSWORD, 
		         login_timeout=_DEFAULT_LOGIN_TIMEOUT):
		self.host = host
		self._cookie_jar = None
		self._login_ts = None

		self.username = username
		self.password = password

		self.login_timeout = login_timeout

	def _require_login(func):
		def wrapped(self, *args, **kwargs):
			# Login if we haven't already or we have expired
			if not self.logged_in:
				self.login()
			return func(self, *args, **kwargs)
		return wrapped


	def login(self, username=None, password=None):
		if username and password:
			self.username = username
			self.password = password

		url = self._LOGIN_URL.format(host=self.host)

		post_data = {
			'user': self.username,
			'pws': self.password,
		}

		r = requests.post(url, data=post_data)
		r.raise_for_status()

		# We are very stupidly assuming we are logged in here.  There should be a check for the validity of the cookie
		self._login_ts = datetime.datetime.now()

		#Save cookies
		self._cookie_jar = r.cookies

	def logout(self):
		# Should call logout url to the modem, but this hack is hacky
		self._cookie_jar = None
		self._login_ts = None

	@property
	def logged_in(self):
		now = datetime.datetime.now()
		return not (not self._login_ts or 
			        now.__sub__(self._login_ts).seconds > self.login_timeout)

	CmStats = namedtuple('CmStats', 'status, ds_channels, us_channels')

	@_require_login
	def get_cm_stats(self):
		CABLE_STATUS = [
			"reset_interface",		#0
			"reset_hardware",		#1
			"wait_for_link_up",		#2
			"ds_channel_scanning",	#3
			"ranging_1",			#4
			"ranging_2",			#5
			"dhcp",					#6
			"establish_tod",		#7
			"security_association",	#8
			"configuration_file",	#9
			"registration",			#10
			"??",					#11
			"online",				#12				
			"cmts_rejected"			#13
		]

		url = self._CMSTATS_URL.format(host=self.host)
		r = requests.get(url, cookies=self._cookie_jar)
		r.raise_for_status()

		# Parse the Javascript from the header
		tree = html.document_fromstring(r.text)
		javascript = tree.xpath('//head/script[@language="JavaScript"]/text()')


		cm_ds_channels = {}
		cm_us_channels = {}
		status = None

		# Iterate through all lines of all script elements 
		for script_element in javascript:
			for line in script_element.splitlines():

				for match in re.finditer('var\s*(?P<var>\S+)\s*=\s*(?P<value>[^$;]+)', line):
					var = match.group("var")
					value = match.group("value")

					if var == "cable_status":
						status = CABLE_STATUS[int(value)]
					else:
						m = re.match('var Cm(?P<direction>Downstream|Upstream)(?P<attr>\S+)Base\s*=\s*"(?P<value>[^"]+)"', line)
						if not m:
							continue
						values = [v.strip() for v in m.group('value').split('|') if v]
						for idx, value in enumerate(values):
							key = camel_to_under(m.group('attr'))
							channel = "ch" + str(idx)

							if m.group('direction') == 'Downstream':
								ch_data = cm_ds_channels.setdefault(channel, {})  
							elif m.group('direction') == 'Upstream':
								ch_data = cm_us_channels.setdefault(channel, {})

							ch_data[key] = value

		return self.CmStats(status, cm_ds_channels, cm_us_channels)
