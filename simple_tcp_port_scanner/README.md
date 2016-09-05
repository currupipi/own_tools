#Simple_scanner.py

This script is just a PoC to use python socket module and of course use any other decent port scanner rather than this one, like for example nmap.

###Usage
Needs 2 arguments:

-t is for the target host that can be an IP or a FQDN
-p is for the ports, you can add as much of them as you like, separated by blank sapces

```
chmod +x simple_scanner.py
./simple_scanner.py -t localhost -p 21 22 8200

``` 


###TO DO

* Investigate a more elegant way to reuse a socket rather than closing and creating a brand new for each port iteration

* Ensure ports do not repeat in the list to save time in case they are repeated

* Allow -t for a list of hosts rather than a single one, the same way as I do with -p 

