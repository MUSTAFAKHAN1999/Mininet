import mininet.net
from mininet.node import Host, OVSSwitch, OVSController
from mininet.link import Link

c0 = OVSController('c0', inNamespace=False)
core = OVSSwitch('c1', inNamespace=False)

n = int(input("Enter No of Aggregate Switches : "))

aggregation = pow(n, 1)
edge = pow(n, 2)
hosts = pow(n, 3)

aggregation_switches = []
edge_switches = []
hosts_list = []

# create aggregation switches
for x in range(aggregation):
    aggregation_switches.append(OVSSwitch('a' + str(x + 1), inNamespace=False))

# create edge switches
for x in range(edge):
    edge_switches.append(OVSSwitch('e' + str(x + 1), inNamespace=False))

# create hosts
for x in range(hosts):
    hosts_list.append(Host('h' + str(x + 1)))

# link core switch to aggregate switches
for x in range(n):
    Link(core, aggregation_switches[x])

# link aggregate switches to edge switches
edge_count = 0
for x in range(len(aggregation_switches)):
    for y in range(n):
        Link(aggregation_switches[x], edge_switches[edge_count])
        edge_count = edge_count + 1

# link edge switches to hosts
host_count = 0
for x in range(len(edge_switches)):
    for y in range(n):
        Link(hosts_list[host_count], edge_switches[x])
        host_count = host_count + 1

print()
print("HOST/SWITCH          IP ADDRESS")
print(c0.name + "                    " + c0.IP())
print(core.name + "                    " + core.IP())

for x in range(len(aggregation_switches)):
    print(aggregation_switches[x].name + "                    " + aggregation_switches[x].IP())

for x in range(len(edge_switches)):
    print(str(edge_switches[x].name) + "                    " + str(edge_switches[x].IP()))

# Adding IP addresses to hosts
for x in range(len(hosts_list)):
    hosts_list[x].setIP('10.0.0.' + str(x + 1) + '/24')
    print(hosts_list[x].name + "                    " + hosts_list[x].IP())

c0.start()                                          # start controller
core.start([c0])                                    # start core switch
for x in range(len(aggregation_switches)):          # start aggregate switches
    aggregation_switches[x].start([c0])

for x in range(len(edge_switches)):                  # start edge switches
    edge_switches[x].start([c0])

print()
print(edge_switches[0].cmd('ping -c1', hosts_list[0].IP()))
# print("----------EDGE-HOST PING OK--------")