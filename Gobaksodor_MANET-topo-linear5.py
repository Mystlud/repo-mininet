#!/usr/bin/python

#Nama	: Bayu Rahmat Ramadhan
#NIM	: 191344006
#Kelas	: 4 NK

"""
This example shows on how to enable the adhoc mode
Alternatively, you can use the manet routing protocol of your choice
"""

import sys

from mininet.log import setLogLevel, info
from mn_wifi.link import wmediumd, adhoc
from mn_wifi.cli import CLI
from mn_wifi.net import Mininet_wifi
from mn_wifi.wmediumdConnector import interference


def topology(args):
    "Create a network."
    net = Mininet_wifi(link=wmediumd, wmediumd_mode=interference)

    info("*** Creating nodes\n")
    kwargs = dict()
    if '-a' in args:
        kwargs['range'] = 100

    sta1 = net.addStation('sta1', ip='10.0.0.1/8',
                          position='100,200,0',
                          **kwargs)
    sta2 = net.addStation('sta2', ip='10.0.0.2/8',
                          **kwargs, min_v=10, min_x=150, max_x=150, min_y=100, max_y=300)
    sta3 = net.addStation('sta3', ip='10.0.0.3/8',
                          **kwargs, min_v=10, min_x=200, max_x=200, min_y=100, max_y=300)
    sta4 = net.addStation('sta4', ip='10.0.0.4/8',
                          **kwargs, min_v=10, min_x=250, max_x=250, min_y=100, max_y=300)
    sta5 = net.addStation('sta5', ip='10.0.0.5/8',
                          position='300,200,0', **kwargs)

    net.setPropagationModel(model="logDistance", exp=4)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    info("*** Creating links\n")
    # MANET routing protocols supported by proto:
    # babel, batman_adv, batmand and olsr
    # WARNING: we may need to stop Network Manager if you want
    # to work with babel
    protocols = ['babel', 'batman_adv', 'batmand', 'olsrd', 'olsrd2']
    kwargs = dict()
    for proto in args:
        if proto in protocols:
            kwargs['proto'] = proto

    net.addLink(sta1, cls=adhoc, intf='sta1-wlan0',
                ssid='adhocNet', mode='g', channel=5,
                ht_cap='HT40+', proto='batmand')
    net.addLink(sta2, cls=adhoc, intf='sta2-wlan0',
                ssid='adhocNet', mode='g', channel=5,
                proto='batmand')
    net.addLink(sta3, cls=adhoc, intf='sta3-wlan0',
                ssid='adhocNet', mode='g', channel=5,
                proto='batmand')
    net.addLink(sta4, cls=adhoc, intf='sta4-wlan0',
                ssid='adhocNet', mode='g', channel=5,
                proto='batmand')
    net.addLink(sta5, cls=adhoc, intf='sta5-wlan0',
                ssid='adhocNet', mode='g', channel=5,
                ht_cap='HT40+', proto='batmand')

    if '-p' not in args:
        net.plotGraph()

    net.setMobilityModel(time=0, model='RandomWayPoint',
                         min_x=0, max_x=400, max_y=400)

    info("*** Starting network\n")
    net.build()

    info("\n*** Addressing...\n")
    if 'proto' not in kwargs:
        sta1.setIP6('2001::1/64', intf="sta1-wlan0")
        sta2.setIP6('2001::2/64', intf="sta2-wlan0")
        sta3.setIP6('2001::3/64', intf="sta3-wlan0")
        sta4.setIP6('2001::4/64', intf="sta4-wlan0")
        sta5.setIP6('2001::5/64', intf="sta5-wlan0")

    info("*** Running CLI\n")
    CLI(net)

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    topology(sys.argv)
