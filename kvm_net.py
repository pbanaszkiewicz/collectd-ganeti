# coding: utf-8
import collectd
from discover_vm import discover, discover_nic


def config_net(data=None):
    collectd.debug("Configuration: " + repr(data))


def init_net(data=None):
    collectd.debug("Initialization: " + repr(data))


def read_net(data=None):
    collectd.debug("Reading: " + repr(data))
    for pid, host in discover().items():
        nics = discover_nic(host)
        if len(nics) < 1:
            continue

        # /var/lib/collectd/rrd/kvm_HOST/net_kvm_in/gauge.rrd
        M_in = collectd.Values("counter")
        M_in.host = "kvm_" + host
        M_in.plugin = "net_kvm_in"
        # /var/lib/collectd/rrd/kvm_HOST/net_kvm_out/gauge.rrd
        M_out = collectd.Values("counter")
        M_out.host = "kvm_" + host
        M_out.plugout = "net_kvm_out"

        for line in open("/proc/net/dev", "r"):
            if nics[0] in line:
                s = line.strip().split()[1:]
                M_in.values = [s[0]]
                M_out.values = [s[8]]
        M_in.dispatch()
        M_out.dispatch()

collectd.register_config(config_net)
collectd.register_init(init_net)
collectd.register_read(read_net)
