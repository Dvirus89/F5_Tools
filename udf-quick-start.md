get_dossier -b 'XXXXX-XXXXX-XXXXX-XXXXX-XXXXXXX'
vim /config/bigip.license # go to activate.f4.com paste here lic 
reloadlic



tmsh -c 'modify /sys global-settings hostname ltm1.bigip'
tmsh -c 'create net vlan vlan10 interfaces add { 1.1 }'
tmsh -c 'create net self self-10 address 10.1.10.10/24 vlan vlan10'
tmsh -c 'save sys config'


tmsh -c 'modify /sys global-settings hostname apm1.bigip'
tmsh -c 'create net vlan vlan10 interfaces add { 1.1 }'
tmsh -c 'create net self self-10 address 10.1.10.101/24 vlan vlan10'
tmsh -c 'save sys config'

tmsh -c 'modify /sys global-settings hostname apm2.bigip'
tmsh -c 'create net vlan vlan10 interfaces add { 1.1 }'
tmsh -c 'create net self self-10 address 10.1.10.201/24 vlan vlan10'
tmsh -c 'save sys config'
