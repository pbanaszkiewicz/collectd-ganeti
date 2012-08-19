# coding: utf-8
from urllib import urlencode
import urllib2
import collectd

GWM_HOST = None


def warning(msg):
    collectd.warning("[notify-gwm] %s" % msg)


def init_notify_gwm(data=None):
    collectd.debug("Initialization: " + repr(data))


def config_notify_gwm(data=None):
    global GWM_HOST
    if data:
        for node in data.children:
            if node.key == "Host":
                GWM_HOST = str(node.values[0])
            else:
                warning("Unknown config parameter: %s" % node.key)

        if not GWM_HOST:
            warning("Improperly configured: `Host` is necessary")


def notify_gwm(notification):
    N = notification
    if GWM_HOST:
        data = urlencode(dict(host=N.host, plugin=N.plugin,
            plugin_instance=N.plugin_instance, type=N.type,
            type_instance=N.type_instance, time=N.time, message=N.message,
            severity=N.severity))

        try:
            urllib2.urlopen("%s/metrics/alert" % GWM_HOST, data, 10)
        except urllib2.URLError as e:
            warning("Couldn't post notification: %s" % str(e))


collectd.register_config(config_notify_gwm)
collectd.register_init(init_notify_gwm)
collectd.register_notification(notify_gwm)
