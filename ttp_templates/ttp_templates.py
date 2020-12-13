import os
from ttp import ttp
from typing import Optional, List, Dict

def get_template(
        platform: Optional[str] = None, 
        command: Optional[str] = None, 
        yang: Optional[str] = None,
        misc: Optional[str] = None,
        path: Optional[str] = None
    ):
    """
    Function to locate template file and return it's content
    
    **Attributes**
    
    * path (str) - OS path to template to load
    * platform (str) - name of the platform to load template for
    * command (str) - command to load template for
    * yang (str) - name of YANG module to load template for
    * misc (str) - OS path to template within repository misc folder    
    
    **Valid combinations of template location**
    
    ``path`` attribute is always more preferred
    
    * ``path="./misc/foo/bar.txt"`` 
    * ``platfrom="cisco_ios", command="show version"``
    * ``yang="ietf-interfaces", platform="cisco_ios"``
    * ``misc="foo_folder/bar_template.txt"``       
    """
    # form path to template file
    if path:
        pass
    elif platform and command:
        platform = platform.lower()
        command = command.lower()
        command = command.replace("|", "pipe")
        for symbol in [" "]:
            platform = platform.replace(symbol, "_")
            command = command.replace(symbol, "_")
        path = "platform/{}_{}.txt".format(platform, command)
    elif platform and yang:
        platform = platform.lower()
        yang = yang.lower()
        for symbol in [" "]:
            platform = platform.replace(symbol, "_")
            yang = yang.replace(symbol, "_")        
        path = "yang/{}_{}.txt".format(yang, platform)
    elif misc:
        path = "misc/{}".format(misc)
    else:
        return None

    template_filename = os.path.join(os.path.dirname(__file__), path)
    
    # open template file and return content
    with open(template_filename, "r") as f:
        return f.read()
        

def parse_output(
        data: str, 
        platform: Optional[str] = None, 
        command: Optional[str] = None, 
        path: Optional[str] = None,
        yang: Optional[str] = None,
        misc: Optional[str] = None,
        structure: Optional[str] = "list",
        template_vars: Optional[Dict] = {}
    ):
    """
    Function to load template text and parse data provided
    
    **Attributes**
    
    * data (str) - data to parse
    * path (str) - OS path to template to load
    * platform (str) - name of the platform to load template for
    * command (str) - command to load template for
    * yang (str) - name of YANG module to load template for
    * misc (str) - OS path to template within repository misc folder    
    * structure (str) - results structure list, dictionary or flat_list
    * template_vars (dict) - variables to load in template object
    
    **Valid combinations of template location**
    
    ``path`` attribute is always more preferred
    
    * ``path="./misc/foo/bar.txt"`` 
    * ``platfrom="cisco_ios", command="show version"``
    * ``yang="ietf-interfaces", platform="cisco_ios"``
    * ``misc="foo_folder/bar_template.txt"``           
    """
    # get template text
    template = get_template(
        platform=platform, 
        command=command, 
        path=path,
        yang=yang,
        misc=misc
    )
    
    # create parser object
    parser = ttp(data=data, template=template, vars=template_vars)
        
    # parse and return results
    parser.parse(one=True)
    return parser.result(structure=structure)