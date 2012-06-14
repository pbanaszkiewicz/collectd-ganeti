# coding: utf-8
import collectd
from discover_vm import discover


def config_io(data=None):
    collectd.debug("Configuration: " + repr(data))


def init_io(data=None):
    collectd.debug("Initialization: " + repr(data))


def read_io(data=None):
    collectd.debug("Reading: " + repr(data))
    for pid, host in discover().items():
        # /var/lib/collectd/rrd/kvm_HOST/io_kvm_read/counter.rrd
        M_read = collectd.Values("counter")
        M_read.host = "kvm_" + host
        M_read.plugread = "io_kvm_read"
        # /var/lib/collectd/rrd/kvm_HOST/io_kvm_write/counter.rrd
        M_write = collectd.Values("counter")
        M_write.host = "kvm_" + host
        M_write.plugin = "io_kvm_write"

        for line in open("/proc/%s/io" % pid, "r"):
            if "read_bytes" in line:
                M_read.values = [int(line.strip().split()[1])]
            elif "write_bytes" in line:
                M_write.values = [int(line.strip().split()[1])]

        M_read.dispatch()
        M_write.dispatch()


collectd.register_config(config_io)
collectd.register_init(init_io)
collectd.register_read(read_io)
