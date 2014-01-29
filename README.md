cablestats
=======
Plauged with cable issues i've decided to start tracking stats from my cable modem myself but the only interface Comcast left me was a crappy web interface.  Determined i decided to scrap the html and present the stats via Python.  From there it was easy to write some plugins for munin to graph historics


Screenshot
----------

![Munin Screenshot](https://raw.github.com/nemith/cablestats/master/res/screenshot1.png)


Munin Plugins
-------------
Munin plugins should be found in /usr/local/share/cablestats/munin_plugins/.  Link them to your munin plugin folders and rock and roll!

```
bbennett@homsar:/etc/munin/plugins$ sudo find /usr/local/share/cablestats/munin_plugins/ -name cablemodem_\* -exec ln -s {} \;
bbennett@homsar:/etc/munin/plugins$ ls -l
total 8
lrwxrwxrwx 1 root root 61 Jan 28 17:50 cablemodem_ds_power -> /usr/local/share/cablestats/munin_plugins/cablemodem_ds_power
lrwxrwxrwx 1 root root 59 Jan 28 17:50 cablemodem_ds_snr -> /usr/local/share/cablestats/munin_plugins/cablemodem_ds_snr
lrwxrwxrwx 1 root root 61 Jan 28 17:50 cablemodem_us_power -> /usr/local/share/cablestats/munin_plugins/cablemodem_us_power
```