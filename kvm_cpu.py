from subprocess import Popen, PIPE
import re
import collectd


def list_vms():
    # TODO: maybe read from /var/run/ganeti/kvm-hypervisor/pid/*?
    kvm = Popen("pidof kvm", shell=True, stdout=PIPE)
    pids = kvm.communicate()[0].split()

    try:
        if set(list_vms._results.keys()) == set(pids):
            return list_vms._results
    except AttributeError:
        pass

    results = {}

    for pid in pids:
        cmdline = open("/proc/%s/cmdline" % pid, "r")
        results[pid] = re.findall(r"-name\x00?([^\-\x00]+)\x00?-", cmdline.readline(), re.U | re.I)[0]
        cmdline.close()

    list_vms._results = results
    return results


def config_cpu(data=None):
    collectd.debug("Configuration: " + repr(data))


def init_cpu(data=None):
    collectd.debug("Initialization: " + repr(data))


def read_cpu(data=None):
    collectd.debug("Reading: " + repr(data))
    for pid, host in list_vms().items():
        M = collectd.Values()
        # rrd/kvm_HOST/cpu_kvm/value.rrd
        M.host = "kvm_" + host
        M.plugin = "cpu_kvm"
        M.type = "value"
        (user, system) = open("/proc/%s/stat" % pid, 'r').readline().split(' ')[13:15]
        M.values = [int(user) + int(system)]
        M.dispatch()


collectd.register_config(config_cpu)
collectd.register_init(init_cpu)
collectd.register_read(read_cpu)
