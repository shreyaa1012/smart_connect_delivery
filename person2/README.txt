PERSON 2 - SDN & NETWORK STARTER

Files:
- smart_content_controller.py: Ryu/OpenFlow 1.3 learning-switch controller
- smart_content_topology.py: Mininet topology with one client and two server hosts

IMPORTANT:
This is a starter network milestone, not the complete final project. It establishes
a controller-controlled OpenFlow network and basic forwarding. Dynamic server
selection and true rerouting after path/server failures still need to be added
and tested during integration with Person 1 and Person 3.

INSTALL (Ubuntu VM):
sudo apt update
sudo apt install -y mininet openvswitch-switch python3-pip python3-venv git

Try the Ubuntu Ryu package:
sudo apt install -y python3-ryu

If "python3-ryu" is unavailable, do not randomly install packages. Send the exact
apt error so the controller installation method can be adjusted for your Ubuntu version.

TERMINAL 1 - controller:
ryu-manager --ofp-tcp-listen-port 6653 smart_content_controller.py

TERMINAL 2 - topology:
sudo python3 smart_content_topology.py

At the mininet> prompt:
nodes
net
h1 ping -c 2 h2
h1 ping -c 2 h3
exit

If Mininet reports stale state:
sudo mn -c

Controller code uses OpenFlow 1.3 and listens on port 6653.
