""" 
This module defines the ArgParse class.
The purpose of this module is to define  ArgParse for the purpose of
parsing command line options and positional arguments. 
"""
import optparse

class ArgParse(object):
    """
    Class use for parsing command line arguments.
    """

    options      = None # options values
    args         = []   # positonal argument list
    parser       = None # parser object after parsing command line
    opt_config   = []   # option configuration object
    opt_index    = 0    # index to the option list

    usage      = "usage: %prog [options]" # Usage String
    version    = "None"                   # Version String

    def __iter__(self):
        return self

    def next(self):
        """
        Will return the current option string and destination string
        """
        if self.opt_index >= len(self.parser.option_list):
            self.opt_index = 0
            raise StopIteration
        
        opt             = self.parser.option_list[self.opt_index]
        self.opt_index += 1
        optstr          = opt.get_opt_string().replace('-','')
        deststr         = opt.dest
        if deststr == None:
            optval = None
        else:
            optval  = getattr(self.options,deststr)
        return optstr, deststr, optval

    def init_config(self,option_def,callbacks):
        """
        This function will get the usage, version and options information from
        the option_def buffer
        """
        lines = option_def.split('\n')
        no_cbs = (None,None) 

        for line in lines:

            # lower case for finding usage and version without caring about case
            line_lower = line.lower()
            
            # get usage string
            if line_lower.find('usage:') != -1: 
                self.usage = line # keep case
            
            # get version string
            elif line_lower.find('version:') != -1:
                self.version = line # keep case
                
            # Any line with '- should be an option line
            elif line.find("'-") != -1:
                # check if there is callback
                if line.find('callback') != -1:
                    callback_found = False
                    # callback should not be None, but check anyway
                    if callbacks != None:
                        for cb in callbacks:
                            cb_func = cb[0] # callback function
                            if line.find(cb_func.func_name) != -1:
                                self.opt_config.append( (line,cb) )
                                callback_found = True
                                break
                    if not callback_found:
                        # probably a problem, but keep going. Store option without callback.
                        self.opt_config.append( (line, no_cbs) )

                # no callback
                else:
                    self.opt_config.append( (line, no_cbs) )

    def __init__(self, option_def = None, callbacks = None):
        """
        Constructor will create the parser object and install options if provided.

        Parameters:
        option_def - string buffer containing all options definitions.
                     Syntax:
                         " usage: ....
                           version: ...

                           OPTION DEFINITIONS:

                           <option 1>
                           ...
                           <option n>"
                       
                       Note: use optparse option syntax for the options above.

        callbacks  - list of callbacks to use. 
        """
        
        # Create usage, version and opt_config attributes.
        self.init_config(option_def,callbacks)

        # Create Parser
        self.parser = optparse.OptionParser(usage            = self.usage,
                                            version          = self.version,
                                            conflict_handler = 'resolve')

        # if option config list provided then add them and parse command line
        if self.opt_config != []:
            #
            # install options
            for opt in self.opt_config:
                option       = opt[0]
                cb_function  = opt[1][0]
                cb_args      = opt[1][1]
                self.add_option(option,cb_function,cb_args)

    def parse_it(self,cl_args = None):
        """
        Parse the command line or passed command line arguments

        Parameters:
        cl_args    - if provided then use this instead of sys.argv
        """
        #
        # Parse the command line
        if cl_args != None:
            (self.options, self.args) =  self.parser.parse_args(cl_args)
        else:
            (self.options, self.args) =  self.parser.parse_args()

    def add_option(self,option, cb_func = None, cb_args = None):
        """
        Add option to parser

        Parameters:
        option   - option to add
        cb_func  - callback function for option
        cb_args  - calbback function positional arguments.
        """
        new_option = option # copy option string to this new var
        if cb_func != None:
            # Create a local copy with the correct function name
            exec cb_func.func_name + " = " + "cb_func"
            new_option += ",action='callback',callback_args=cb_args"

        # Add option
        exec 'self.parser.add_option(%s)' % new_option

    def no_args(self):
        """
        Check if no args
        """
        return self.args == [] # no posiional arguments if true

