# coding: utf-8
import os
import os.path


def discover():
    """
    Returns a list of actually running KVM virtual machines and their pids in
    this manner:
        result[pid] = vm_name
    """
    # TODO: add Xen discovery

    path = "/var/run/ganeti/kvm-hypervisor/pid"
    if os.path.exists("/run"):
        path = "/run/ganeti/kvm-hypervisor/pid"

    results = {}
    for vm in os.listdir(path):
        vm_path = os.path.join(path, vm)
        results[open(vm_path, "r").readline().strip()] = vm

    return results

if __name__ == "__main__":
    print discover()
