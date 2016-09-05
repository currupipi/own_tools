#Simple_scanner.py

This script is just a PoC to use python socket module and of course use any other decent port scanner rather than this one, like for example nmap.

###Usage
Accepts 3 arguments:

*  -t is for the target host that can be a list of IP or FQDN, separated by blank spaces
* -p is for the ports, you can add as much of them as you like, separated by blank sapces
* -s is OPTIONAL to specify the timeout for the socket, by default is 5
```
chmod +x simple_scanner.py
./simple_scanner.py -t localhost google.fr -p 21 22 8200
./simple_scanner.py -t localhost google.fr -p 21 22 8200 -s 120

``` 


###TO DO

* Investigate a more elegant way to reuse a socket rather than closing and creating a brand new for each port iteration

