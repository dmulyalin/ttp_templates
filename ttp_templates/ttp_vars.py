"""
Collection of useful variables that can be used with TTP templates
and various functions.
"""

# Template variable to use with resuball match variable function
# to shorten and normalize names of the interfaces
short_interface_names = {
    'ATM': ['^ATM', '^AT'],
    'BDI': ['^Bd', '^Bdi'],
    'EOBC': ['^EOBC', '^EO'],
    'Eth': ['^Ethernet', '^Eth', '^eth', r'^Et(?=\d)', r'^et(?=\d)'],
    'FE': ['^FastEthernet', '^FastEth', '^FastE', '^Fast', '^Fas', '^FE', '^Fa', '^fa'],
    'Fddi': ['^Fddi', '^FD'], 
    '50GE': ['^FiftyGigabitEthernet', '^FiftyGigEthernet', '^FiftyGigEth', '^FiftyGigE', '^FI', '^Fi', '^fi'],
    '40GE': ['^FortyGigabitEthernet', '^FortyGigEthernet', '^FortyGigEth', '^FortyGigE', '^FortyGig', '^FGE', '^FO', '^Fo'],
    '400GE': ['^FourHundredGigabitEthernet', '^FourHundredGigEthernet', '^FourHundredGigEth', '^FourHundredGigE', '^FourHundredGig', '^F', '^f'],
    'GE': ['^GigabitEthernet', '^GigEthernet', '^GigEth', '^GigE', '^Gig', '^GE', '^Ge', '^ge', '^Gi', '^gi'],
    '100GE': ['^HundredGigabitEthernet', '^HundredGigEthernet', '^HundredGigEth', '^HundredGigE', '^HundredGig', '^Hu'],
    'Lo': ['^Loopback', '^loopback', '^LoopBack', '^lo'],
    'MGMT': ['^Management', '^Mgmt', '^mgmt', '^Ma'],
    'Multilink': ['^Multilink', '^Mu'],
    'POS': ['^POS', '^PO'],
    'LAG': ['^PortChannel', '^Port-channel', '^Port-Channel', '^port-channel', '^po', '^Po', "^Bundle-Ether", "^BE", "^Eth-Trunk"],
    'Serial': ['^Serial', '^Se', '^S'],
    '10GE': ['^TenGigabitEthernet', '^TenGigEthernet', '^TenGigEth', '^TenGigE', '^TenGig', '^TeGig', '^Ten', '^Te', '^te'],
    'Tunnel': ['^Tunnel', '^Tun', '^Tu'],
    '25GE': ['^TwentyFiveGigabitEthernet', '^TwentyFiveGigEthernet', '^TwentyFiveGigEth', '^TwentyFiveGigE', '^TwentyFiveGig', '^Twe', '^TF', '^Tf', '^tf'],
    '2GE': ['^Tw', '^Two'],
    '200GE': ['^TwoHundredGigabitEthernet', '^TwoHundredGigEthernet', '^TwoHundredGigEth', '^TwoHundredGigE', '^TwoHundredGig', '^TH', '^Th', '^th'],
    'VLAN': ['^VLAN', '^vlanif', r'^V(?=\d+)', r'^Vl(?=\d+)'],
    'Virtual-Access': ['^Virtual-Access', '^Vi'],
    'Virtual-Template': ['^Virtual-Template', '^Vt'],
    'WLAN': ['^Wlan-GigabitEthernet'],
}


# dictionary that contains all variables defined above to simplify
# addition of all variables to TTP object, e.g.
#
# from ttp_templates.ttp_vars import all_vars
# from ttp_templates import parse_output
#
# data = """
#  ... some text to parse ...
# """
#
# result = parse_output(
#     data=data,
#     template="",
# 	  misc="ttp_templates_tests/cisco_ios_interfaces_cfg_per_ip.txt",
#     template_vars=all_vars
# )

all_vars = {"short_interface_names": short_interface_names}
