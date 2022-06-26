"""
Collection of useful variables that can be used with TTP templates
and various functions.
"""

# Template variable to use with resuball match variable function
# to shorten and normalize names of the interfaces across
# various platforms to uniform values
short_interface_names = {
    'ATM': ['^ATM', '^AT'],
    'BDI': ['^Bd', '^Bdi'],
    'EOBC': ['^EOBC', '^EO'],
    'Eth': ['^Ethernet', '^Eth', '^eth', r'^Et(?=\d)', r'^et(?=\d)'],
    'FE': ['^FastEthernet', '^FastEth', '^FastE', '^Fast', '^Fas', '^FE', '^Fa', '^fa'],
    'Fddi': ['^Fddi', '^FD'], 
    '50GE': ['^FiftyGigabitEthernet', '^FiftyGigEthernet', '^FiftyGigEth', '^FiftyGigE', '^FI', '^Fi', '^fi'],
    '40GE': ['^FortyGigabitEthernet', '^FortyGigEthernet', '^FortyGigEth', '^FortyGigE', '^FortyGig', '^FGE', '^FO', '^Fo', '^40GE'],
    '400GE': ['^FourHundredGigabitEthernet', '^FourHundredGigEthernet', '^FourHundredGigEth', '^FourHundredGigE', '^FourHundredGig'],
    'GE': ['^GigabitEthernet', '^GigEthernet', '^GigEth', '^GigE', '^Gig', '^GE', '^Ge', '^ge-', '^ge', '^Gi', '^gi'],
    '100GE': ['^HundredGigabitEthernet', '^HundredGigEthernet', '^HundredGigEth', '^HundredGigE', '^HundredGig', '^Hu', '^et-'],
    'Lo': ['^Loopback', '^loopback', '^LoopBack', '^lo'],
    'MGMT': ['^MgmtEth', '^Management', '^Mgmt', '^mgmt', '^Ma', '^MEth', '^fxp'],
    'Multilink': ['^Multilink', '^Mu'],
    'POS': ['^POS', '^PO'],
    'LAG': ['^PortChannel', '^Port-channel', '^Port-Channel', '^port-channel', '^po', '^Po', "^Bundle-Ether", "^BE", "^Eth-Trunk", "^ae"],
    'Serial': ['^Serial', '^Se', '^S'],
    'Te': ['^TenGigabitEthernet', '^TenGigEthernet', '^TenGigEth', '^TenGigE', '^TenGig', '^TeGig', '^Ten', '^te', '^XGigabitEthernet', '^TenGe', '^10GE', '^xe-'],
    'Tunnel': ['^Tunnel', '^Tun', '^Tu', '^gr-'],
    '25GE': ['^TwentyFiveGigabitEthernet', '^TwentyFiveGigEthernet', '^TwentyFiveGigEth', '^TwentyFiveGigE', '^TwentyFiveGig', '^Twe', '^TF', '^Tf', '^tf'],
    '2GE': ['^Tw', '^Two'],
    '200GE': ['^TwoHundredGigabitEthernet', '^TwoHundredGigEthernet', '^TwoHundredGigEth', '^TwoHundredGigE', '^TwoHundredGig', '^TH', '^Th', '^th'],
    'VLAN': ['^Vlan', '^vlanif', r'^V(?=\d+)', r'^Vl(?=\d+)'],
    'Virtual-Access': ['^Virtual-Access', '^Vi'],
    'Virtual-Template': ['^Virtual-Template', '^Vt'],
    'WLAN': ['^Wlan-GigabitEthernet'],
    'Pt': ['^Port[^-]'],
}

# used by N2G L2 drawer to identify if is_physical_port based on short_interface_names 
# dictionary, that used by add all connected nodes feature
physical_ports = [
    'ATM', 'Eth', 'FE', 'Fddi', '50GE', '40GE', '400GE', 'GE',
    '100GE', 'MGMT', 'POS', 'Serial', 'Te', '25GE', '2GE',
    '200GE', 'Pt',
]

# dictionary that contains all variables defined above to simplify
# addition of all variables to TTP object, e.g.
#
#     from ttp_templates.ttp_vars import all_vars
#     from ttp_templates import parse_output
#     
#     data = """
#      ... some text to parse ...
#     """
#     
#     result = parse_output(
#         data=data,
#         template="",
#         misc="ttp_templates_tests/cisco_ios_interfaces_cfg_per_ip.txt",
#         template_vars=all_vars
#     )

all_vars = {
    "short_interface_names": short_interface_names, 
    "physical_ports": physical_ports,
}
