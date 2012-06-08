import collectd


def config_cpu(data=None):
    collectd.debug("Configuration: " + repr(data))


def init_cpu(data=None):
    collectd.debug("Initialization: " + repr(data))


def read_cpu(data=None):
    collectd.debug("Reading: " + repr(data))
    m1 = collectd.Values()
    m1.plugin = "kvm_cpu"
    m1.type = "gauge"
    m1.values = [100]
    m1.host = "kvm_instance1.example.org"
    m1.dispatch()


collectd.register_config(config_cpu)
collectd.register_init(init_cpu)
collectd.register_read(read_cpu)
