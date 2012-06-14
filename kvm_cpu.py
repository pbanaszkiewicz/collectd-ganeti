# coding: utf-8
import collectd
from discover_vm import discover


def config_cpu(data=None):
    collectd.debug("Configuration: " + repr(data))


def init_cpu(data=None):
    collectd.debug("Initialization: " + repr(data))


def read_cpu(data=None):
    collectd.debug("Reading: " + repr(data))
    for pid, host in discover().items():
        # /var/lib/collectd/rrd/kvm_HOST/cpu_kvm/gauge.rrd
        M = collectd.Values("gauge")
        M.host = "kvm_" + host
        M.plugin = "cpu_kvm"
        # import os
        # os.sysconf("SC_CLK_TCK")
        (user, system) = open("/proc/%s/stat" % pid, 'r').readline().split(' ')[13:15]
        #M.values = [(int(user) + int(system)) / 1000.]  # might be < 100, just trying
        M.values = [int(user) + int(system)]
        M.dispatch()


collectd.register_config(config_cpu)
collectd.register_init(init_cpu)
collectd.register_read(read_cpu)
