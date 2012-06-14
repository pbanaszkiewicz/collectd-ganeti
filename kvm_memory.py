# coding: utf-8
import collectd
import os
from discover_vm import discover


def config_memory(data=None):
    # TODO: make configuration option to choose between quick (rough) and slow
    #       (exact) estimation
    collectd.debug("Configuration: " + repr(data))


PAGESIZE = 0


def init_memory(data=None):
    global PAGESIZE
    collectd.debug("Initialization: " + repr(data))
    PAGESIZE = os.sysconf("SC_PAGE_SIZE") / 1024.  # KiB?


def read_memory(data=None):
    collectd.debug("Reading: " + repr(data))
    for pid, host in discover().items():
        # /var/lib/collectd/rrd/kvm_HOST/memory_kvm/bytes.rrd
        M = collectd.Values("bytes")
        M.host = "kvm_" + host
        M.plugin = "memory_kvm"

        # rough, but quick estimate
        # I'd use `with` statement, but not sure if it's present in Python 2.6
        statm = open("/proc/%s/statm" % pid, "rt")
        s = statm.readline().split()
        statm.close()
        statm = s

        shared = int(statm[2]) * PAGESIZE
        Rss = int(statm[1]) * PAGESIZE
        private = Rss - shared
        M.values = [int(private) + int(shared)]
        M.dispatch()


collectd.register_config(config_memory)
collectd.register_init(init_memory)
collectd.register_read(read_memory)
