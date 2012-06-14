# coding: utf-8
#from subprocess import Popen, PIPE
#import re
import os
import os.path


def discover():
    path = "/var/run/ganeti/kvm-hypervisor/pid"
    if os.path.exists("/run"):
        path = "/run/ganeti/kvm-hypervisor/pid"

    results = {}
    for vm in os.listdir(path):
        vm_path = os.path.join(path, vm)
        results[vm] = open(vm_path, "r").readline()

    return results
    #kvm = Popen("pidof kvm", shell=True, stdout=PIPE)
    #pids = kvm.communicate()[0].split()

    #try:
    #    if set(discover._results.keys()) == set(pids):
    #        return discover._results
    #except AttributeError:
    #    pass

    #results = {}

    #for pid in pids:
    #    cmdline = open("/proc/%s/cmdline" % pid, "r")
    #    results[pid] = re.findall(r"-name\x00?([^\-\x00]+)\x00?-",
    #                              cmdline.readline(), re.U | re.I)[0]
    #    cmdline.close()

    #discover._results = results
    #return results

if __name__ == "__main__":
    print discover()
