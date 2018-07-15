# imports
import subprocess
# from colorama import Fore, Style
import argparse
from netaddr import *
import pprint

# banner
def PrintBanner():
    # 1. make banner
    banner = """
      @@@@@@   @@@  @@@  @@@@@@@   @@@  @@@  @@@@@@@@  @@@@@@@  @@@@@@@   
     @@@@@@@   @@@  @@@  @@@@@@@@  @@@@ @@@  @@@@@@@@  @@@@@@@  @@@@@@@@  
     !@@       @@!  @@@  @@!  @@@  @@!@!@@@  @@!         @@!    @@!  @@@  
     !@!       !@!  @!@  !@   @!@  !@!!@!@!  !@!         !@!    !@!  @!@  
     !!@@!!    @!@  !@!  @!@!@!@   @!@ !!@!  @!!!:!      @!!    @!@!!@!   
      !!@!!!   !@!  !!!  !!!@!!!!  !@!  !!!  !!!!!:      !!!    !!@!@!    
          !:!  !!:  !!!  !!:  !!!  !!:  !!!  !!:         !!:    !!: :!!   
         !:!   :!:  !:!  :!:  !:!  :!:  !:!  :!:         :!:    :!:  !:!  
     :::: ::   ::::: ::  :: ::::   ::   ::   :: ::::     ::     ::   :::  
     :: : :     : :  :   :: : ::   ::   :    : :: ::      :     :   : :
  
    Authored by: r_panov on 07/04/2018           
    'momentary masters of a fraction of a dot' - Carl Sagan' 
     """
    # 2. print banner
    print(banner)

def subNIC(x):
    # 1. run subprocess call (ifconfig) on user supplied input (-n , var=x)
    a = subprocess.run([f'ifconfig {x}'], shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
    # 2. print output of call and prompt more action
    print(f'Your network interface configuration for {x} is:    \n')
    print(a)
    b = input(str(f'Enter the IP Address for {x} (i.e. inet)            --> : '))
    c = input(str(f'Enter the Subnet Mask for {x} (i.e. broadcast)      --> : '))

    # 3. split user input into list, print IP Address, print subnet mask
    d = b.split(sep='.')
    print(f'\n{x} IP Address Octets\n\tInteger -->    {d[0]} | {d[1]} | {d[2]} | {d[3]}    \n\tBinary  -->    {bin(int(d[0]))} | {bin(int(d[1]))} | {bin(int(d[2]))} | {bin(int(d[3]))}')
    e = c.split(sep='.')
    print(f'{x} Subnet Mask Octets\n\tInteger  -->    {e[0]} | {e[1]} | {e[2]} | {e[3]}    \n\tBinary  -->    {bin(int(e[0]))} | {bin(int(e[1]))} | {bin(int(e[2]))} | {bin(int(e[3]))}')

    # 4. pass user input to math function as variables: var=d , var=e
    subMath(d,e)


# maths
def subMath(x,y):
    # 1. IP/CIDR - take user input and slice and dice to show the IP subnet
    a = '.'.join(x)
    b = []
    c = [b.append(bin(int(i.strip()))[2:]) for i in y]
    d = ''.join(b)
    e = sum(map(lambda x: 1 if '1' in x else 0, d))     # CIDR int variable

    # 2. Print subnet calculations
    ip = IPNetwork(f'{a}/{e}')
    print(f'\nSubnet CIDR notation        --->    {ip.cidr}')
    print(f'IP Address CIDR notation    --->    {a}/{e}')
    print(f'Subnet size                 --->    {ip.size}')
    print(f'Subnet mask                 --->    {ip.broadcast}')
    print(f'Subnet netmask              --->    {ip.netmask}')
    print(f'Subnet range                --->    {ip.network}-{ip.size}')
    print(f'Private IP                  --->    {ip.is_private()}')
    print(f'Reserved IP                 --->    {ip.is_reserved()}')

    # 3. Show where the IP falls graphically amongst available hosts
    # example if the 10th host 0[---------#---------------]25
    ip_list = list(ip)  # create list of all available IPs
    hosts = []
    z = [hosts.append(str(x)) for x in ip_list]     # append all IPs as str's to new list
    spot = []   # empty list to hold for-loop graph values

    for x in hosts:
        if x == a:
            spot.append('#')    # if IP is found at x value
        else:
            spot.append('-')    # if IP is not x value

    f = ''.join(spot)   # GRAPH - assign graph to variable
    g = len(ip_list)

    # 4. Print
    print('\nGraphical IP Address availability below:   \n  Can you find your IP?\n')
    print(f'Start 0[ {f} ]{g} End')     # print text and graph

    arpSpotter(ip_list)

def arpSpotter(x):
    # 1. user input for if they want to display arp cache
    a = str(input('Use arp cache to graphicall display other hosts on subnet? (y/n)   --->    ')).lower()
    # 2. user decides YES
    if a == 'y':
        # 3. subprocess call to query arp cache
        b = subprocess.run(['arp -a | cut -d " " -f 2'], shell=True, stdout=subprocess.PIPE).stdout.decode('utf-8')
        c = list(b)     # assign subprocess call output to list

        # 4. create empty string
        d = []
        # 5. if/else list comprehension to replace '\n' with ' '
        z = [d.append(' ') if x == '\n' else d.append(x) for x in c]
        # 6. convert newly created list to string
        e = ''.join(d)
        # 7. strip comprehension on newly created string to separate at spaces
        # 8. this creates list of arp IPs
        arpIPs = [x.split("(")[-1] for x in e.split(")")[:-1]]

        # 9. take all subnet IPs passed from previous function and assign to new variable
        ip_list = x
        # 10. create empty string to hold all available network subnet ips
        hosts = []
        # 11. list comprehension to fill list with str ips
        z = [hosts.append(str(x)) for x in ip_list]
        # 12. new list to hold graphical arp cache display
        spot = []
        # 13. list comprehension to fill empty arp cache display list
        z1 = [spot.append('#') if x in arpIPs else spot.append('-') for x in hosts]
        # 14. join graphical list
        f = ''.join(spot)
        # 15. printing

        g = str(len(arpIPs))
        print(f'\nSize of local arp cache     --->    {g}')
        print('\nArp cache IP address table: \n')
        print(*arpIPs, sep='\t')
        print("\nGraphical display of arp cache'd IP Addresses:   \n")
        print(f'Start 0[ {f} ]{g} End')  # print text and graph

    # 16 . user decides NO, or input != y
    else:
        pass


# main
def main():
    #  1. imports
    import argparse
    # 2. print the banner right off the bat TODO: Once finished, uncomment PrintBanner() function
    PrintBanner()

    # 3. Argparse help menu: display help menu, takes flags, passes flag as input
    parser = argparse.ArgumentParser(description='SubNetr tool is designed to perform subnet calculation on given NICs and IPs')
    parser.add_argument('-n', '--nic', help='Enter NIC to run subnet calculations (Ex: -n en0)', required=True)
    args = parser.parse_args()

    # 4. perform minimal user validation then pass NIC input to function
    subNIC(str(args.nic).lower())


main()


































