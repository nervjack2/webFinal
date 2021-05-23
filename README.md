# WebFinal

### Create Traffic
1. Enter the following command in terminal to activate the ryu-manager.
```
ryu-manager monitor.py
```
2. Enter the following command to create a data-center like topology.
```
sudo python dataCenterNet.py [Number of core switches] [Number of aggregation switches]
```
3. Open a xterm terminal of one of the host.
```
mininet> xterm [Host name]
```
4. In the host xterm terminal, enter the following command to create tranffic in network.
```
python3 flowGenerate.py --host_id [The xterm terminal host id] --n_host [Number of hosts in the topology.]
```
Note: If host name = 4001, then its host_id = 1. If host name = 4016, its host_id = 16.
 
### Launch DDOS Attack 
1. Enter the following command in terminal to activate the ryu-manager.
```
ryu-manager monitor.py
```
2. Enter the following command to create a data-center like topology.
```
sudo python dataCenterNet.py [Number of core switches] [Number of aggregation switches]
```
3. Open a xterm terminal of one of the host.
```
mininet> xterm [Host name]
```
4. In the host xterm terminal, enter the following command to launch DDOS attack.
```
python3 launchAttack.py --dst_ip [The ip address of DDOS attack victim.]
```
