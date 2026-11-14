PERSON 2 - SDN, NETWORK AND DYNAMIC BACKEND SELECTION
====================================================

FILES
- smart_content_controller_osken.py : OS-Ken/OpenFlow 1.3 learning-switch controller.
- run_controller.py                 : optional custom launcher; use osken-manager below as the simple launch method.
- smart_content_topology.py         : Mininet topology (h1 client/gateway, h2 and h3 servers).
- smart_content_gateway.py          : application-layer gateway; health-checks both TCP servers, chooses the healthy server with the lowest HEALTH probe latency, and retries another backend if a request fails.
- gateway_client.py                 : client for requesting content through the gateway.
- test_person2.sh                   : Python syntax check and launch instructions.

IMPORTANT ARCHITECTURE NOTE
The controller currently provides OpenFlow 1.3 switch control and MAC-learning
forwarding. Dynamic backend selection and retry/failover are implemented in the
TCP gateway running on Mininet host h1. Traffic still traverses the
controller-managed OpenFlow Mininet network. This is application-layer backend
selection, NOT transparent OpenFlow NAT/packet rewriting. Do not claim that the
controller itself performs Layer-3 NAT or rewrites existing TCP sessions.

INSTALL (Ubuntu VM)
sudo apt update
sudo apt install -y mininet openvswitch-switch python3-pip python3-venv git
python3 -m venv ~/sdn-env
source ~/sdn-env/bin/activate
pip install os-ken

TERMINAL 1 - CONTROLLER
cd person2
source ~/sdn-env/bin/activate
osken-manager --ofp-tcp-listen-port 6653 smart_content_controller_osken.py

TERMINAL 2 - MININET
sudo mn -c
sudo python3 person2/smart_content_topology.py

At the mininet> prompt, check the network:
nodes
net
pingall

Start TCP backend servers inside Mininet:
mininet> h2 python3 person1/server.py Server1 5001 &
mininet> h3 python3 person1/server.py Server2 5002 &

Start the gateway inside h1:
mininet> h1 python3 person2/smart_content_gateway.py --servers "Server1=10.0.0.2:5001,Server2=10.0.0.3:5002" &

Request content through the gateway (run client inside h1):
mininet> h1 python3 person2/gateway_client.py file1
mininet> h1 python3 person2/gateway_client.py file2
mininet> h1 python3 person2/gateway_client.py file3

FAILURE TEST
Stop Server 1:
mininet> h2 pkill -f server.py

Request again. The gateway should detect Server 1 as unavailable and use
Server 2 if it is healthy:
mininet> h1 python3 person2/gateway_client.py file1

RECOVERY TEST
Restart Server 1:
mininet> h2 python3 person1/server.py Server1 5001 &

Request again. The gateway probes both servers on every request and can select
the recovered server if its health-probe latency is lower.

PERSON 3 MONITORING (optional)
mininet> h1 python3 person3/person3_monitor.py --servers "Server1=10.0.0.2:5001,Server2=10.0.0.3:5002" --rounds 5 --content file1

LIMITATIONS / NEXT EXTENSION
- Selection uses TCP HEALTH probe latency, not full link congestion or bandwidth.
- Gateway selection is application-layer; the OpenFlow controller remains a
  learning switch. True controller-level steering would require a common VIP,
  address translation/proxy design, bidirectional flow rules, and coordinated
  client/server changes.
- A request already being served when its backend dies may fail; retry applies
  to a new gateway backend attempt, not transparent migration of an established
  TCP session.
- Mininet results are emulated and should not be presented as production results.
