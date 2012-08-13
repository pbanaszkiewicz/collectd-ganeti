# coding: utf-8
import collectd
import os
import os.path
from discover_vm import discover

try:
    import hashlib
    md5_new = hashlib.md5
except ImportError:
    import md5
    md5_new = md5.new


def config_memory(data=None):
    # TODO: make configuration option to choose between quick (rough) and slow
    #       (exact) estimation
    collectd.debug("Configuration: " + repr(data))


PAGESIZE = 0


def init_memory(data=None):
    global PAGESIZE
    collectd.debug("Initialization: " + repr(data))
    #PAGESIZE = os.sysconf("SC_PAGE_SIZE") / 1024.  # KiB?
    PAGESIZE = os.sysconf("SC_PAGE_SIZE")  # bytes?


def read_memory(data=None):
    collectd.debug("Reading: " + repr(data))
    for pid, host in discover().items():
        # /var/lib/collectd/rrd/kvm_HOST/memory_kvm/memory-usage.rrd
        M = collectd.Values("bytes")
        M.host = "kvm_" + host
        M.plugin = "memory_kvm"
        M.type_instance = "memory_usage"

        if os.path.exists("/proc/%s/smaps" % pid):
            # slow but probably exact estimate

            digester = md5_new()
            shared, private, pss = 0, 0, 0

            F = open("/proc/%s/smaps" % pid, "rb")
            for line in F.readlines():
                digester.update(line)
                line = line.decode('ascii')

                if line.startswith("Shared"):
                    shared += int(line.split()[1])
                elif line.startswith("Private"):
                    private += int(line.split()[1])
                elif line.startswith("Pss"):
                    pss += 0.5 + float(line.split()[1])

            F.close()

            if pss > 0:
                shared = pss - private

            M.values = [1024 * int(private + shared)]  # in bytes

        else:
            # rough, but quick estimate
            # I'd use `with` statement, but not sure if it's present in Python 2.6
            statm = open("/proc/%s/statm" % pid, "rt")
            S = statm.readline().split()
            statm.close()
            statm = S

            shared = int(statm[2]) * PAGESIZE
            Rss = int(statm[1]) * PAGESIZE
            private = Rss - shared
            M.values = [int(private) + int(shared)]

        M.dispatch()


collectd.register_config(config_memory)
collectd.register_init(init_memory)
collectd.register_read(read_memory)
