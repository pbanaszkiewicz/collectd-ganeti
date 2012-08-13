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
        # /var/lib/collectd/rrd/kvm_HOST/cpu_kvm/cpu-usage.rrd
        M = collectd.Values("derive")  # or try "counter"
        M.host = "kvm_" + host
        M.plugin = "cpu_kvm"
        M.type_instance = "cpu_usage"
        # import os
        # os.sysconf("SC_CLK_TCK")
        (user, system) = open("/proc/%s/stat" % pid, 'r').readline().split(' ')[13:15]
        M.values = [int(user) + int(system)]
        M.dispatch()


def config_cpu_wait(data=None):
    collectd.debug("Configuration: " + repr(data))


def init_cpu_wait(data=None):
    collectd.debug("Initialization: " + repr(data))


def read_cpu_wait(data=None):
    collectd.debug("Reading: " + repr(data))
    for pid, host in discover().items():
        # /var/lib/collectd/rrd/kvm_HOST/cpu_kvm/cpu-wait.rrd
        M = collectd.Values("gauge")
        M.host = "kvm_" + host
        M.plugin = "cpu_kvm"
        M.type_instance = "cpu_wait"
        (user, system) = open("/proc/%s/stat" % pid, 'r').readline().split(' ')[15:17]
        M.values = [int(user) + int(system)]
        M.dispatch()


collectd.register_config(config_cpu)
collectd.register_init(init_cpu)
collectd.register_read(read_cpu)
collectd.register_config(config_cpu_wait)
collectd.register_init(init_cpu_wait)
collectd.register_read(read_cpu_wait)
