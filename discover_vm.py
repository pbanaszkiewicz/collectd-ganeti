# coding: utf-8
from subprocess import Popen, PIPE
import re


def discover(all_vms=True):
    # TODO: maybe read from /var/run/ganeti/kvm-hypervisor/pid/*?
    kvm = Popen("pidof kvm", shell=True, stdout=PIPE)
    pids = kvm.communicate()[0].split()

    try:
        if set(discover._results.keys()) == set(pids):
            return discover._results
    except AttributeError:
        pass

    results = {}

    for pid in pids:
        cmdline = open("/proc/%s/cmdline" % pid, "r")
        results[pid] = re.findall(r"-name\x00?([^\-\x00]+)\x00?-",
                                  cmdline.readline(), re.U | re.I)[0]
        cmdline.close()

    discover._results = results
    return results
