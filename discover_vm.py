# coding: utf-8
import os
import os.path

PATH = "/run/ganeti/kvm-hypervisor" if os.path.exists("/run") else "/var/run/ganeti/kvm-hypervisor"


def discover():
    """
    Returns a list of actually running KVM virtual machines and their pids in
    this manner:
        result[pid] = vm_name
    """
    # TODO: add Xen discovery
    path = os.path.join(PATH, "pid")

    results = {}
    for vm in os.listdir(path):
        vm_path = os.path.join(path, vm)
        results[open(vm_path, "r").readline().strip()] = vm

    return results


def discover_nic(hostname):
    """
    Returns a list of Network Interface Controllers connected with specified
    virtual machine.
    NICs are being read from "/run/ganeti/kvm-hypervisor/nic/HOSTNAME/NUMBER" files
    """
    path = os.path.join(PATH, "nic")

    results = []
    try:
        host_path = os.path.join(path, hostname)
        for F in os.listdir(host_path):
            nic = open(os.path.join(host_path, F), "r").read()
            results.append(nic)
    except OSError:
        pass

    return results


if __name__ == "__main__":
    print discover()
