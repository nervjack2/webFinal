# WebFinal

### Create Traffic
1. Enter the following command in terminal to activate the ryu-manager.
```
ryu-manager monitor.py
```
2. Enter the following command to create a tree like topology.
```
sudo python2 treeNet.py [Number of hosts]
```
3. Open a xterm terminal of one of the host.
```
mininet> xterm [Host name]
```
4. In the host xterm terminal, enter the following command to create tranffic in network.
```
python3 flowGenerate.py --xterm_host_ip [The xterm terminal host ip] --num_host [Number of hosts in the topology.]
```

### Launch DDOS Attack 
1. Enter the following command in terminal to activate the ryu-manager.
```
ryu-manager monitor.py
```
2. Enter the following command to create a tree like topology.
```
sudo python2 treeNet.py [Number of hosts]
```
3. Open a xterm terminal of one of the host.
```
mininet> xterm [Host name]
```
4. In the host xterm terminal, enter the following command to launch DDOS attack.
```
python3 launchAttack.py --xterm_host_ip [The xterm terminal host ip] --dst_ip [The DDOS victim ip] --num_host [Number of hosts in the topology] --num_atk_host [Number of attackers]
### Entropy detect
1. Enter the following command in terminal to activate the ryu-manager.
```
ryu-manager entropy_monitor.py
```
2. Enter the following command to create a tree like topology.
```
sudo python2 treeNet.py [Number of hosts]
```
3. Open a xterm terminal of one of the host.
```
mininet> xterm [Host name]
```
4. In the host xterm terminal, enter the following command to launch DDOS attack.
```
python3 ddos_entropy.py --dst_ip [The DDOS victim ip] 

