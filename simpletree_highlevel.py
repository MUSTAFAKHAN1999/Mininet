from mininet.topo import Topo

n = int(input("Enter The Value Aggregate Switches: "))


class MyTopo(Topo):

    def build(self):

        aggregation = pow(n, 1)
        edge = pow(n, 2)
        hosts = pow(n, 3)

        aggregation_switches = []
        edge_switches = []
        hosts_list = []

        # create core switch
        c1 = self.addSwitch('c1')

        # create aggregation switches
        for x in range(aggregation):
            aggregation_switches.append(self.addSwitch('a' + str(x + 1)))

        # create edge switches
        for x in range(edge):
            edge_switches.append(self.addSwitch('e' + str(x + 1)))

        # create hosts
        for x in range(hosts):
            hosts_list.append(self.addHost('h' + str(x + 1)))

        # link core switch to aggregate switches
        for x in range(n):
            self.addLink(c1, aggregation_switches[x])

        # link aggregate switches to edge switches
        edge_count = 0
        for x in range(len(aggregation_switches)):
            for y in range(n):
                self.addLink(aggregation_switches[x], edge_switches[edge_count])
                edge_count = edge_count + 1

        # link edge switches to hosts
        host_count = 0
        for x in range(len(edge_switches)):
            for y in range(n):
                self.addLink(edge_switches[x], hosts_list[host_count])
                host_count = host_count + 1


topos = {'mytopo': (lambda: MyTopo())}
