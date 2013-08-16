 = Setting Up Cobalt Brooklyn Simulator: =

 1. Download the following python modules from this wiki page:
    * '''arg_parser.py'''   -- this is imported by setup_cobalt.py
    * '''setup_cobalt.py''' -- script to setup cobalt. Change permissions to 755

 2. Execute the the setup_cobalt.py as follows: (python 2.6 should be used)
    * '''./setup_cobalt.py -b develop -s $HOME/Cobalt'''
    * '''note:''' This will create the directory Cobalt in your home directory. This can be changed to whatever you want.

 3. Then from the $HOME/Cobalt do the following:
    * '''source cobalt_setup''' # This will setup the appropriate env variable and aliases

 4. Run cstart.sh
    * '''./cstart.''' # after this command wait about 20 seconds to let the components start

 5. Run cinit.sh only one time after running ./cstart.sh. Do not need to run it again unless step (8) is executed.
    * '''./cinit.sh'''

 6. To stop all components and Cobalt:
    * '''cobalt-stop''' # alias created by cobalt_setup to stop all components. Probabaly need to do ps command a few times to see if all components stopped.

 7. After starting the cobalt components with cstart.sh then you can monitor the following files:
    * '''$COBALT_RUNTIME_DIR/var/log/cobalt/*.out'''

 8. If you wish to re-initialize (start fresh) do the following:
    1. '''cobalt-clean''' # alias created by cobalt_setup to delete $HOME/Cobalt/sysroot_brooklyn/var
    2. '''./cstart.sh'''
    3. '''./cinit.sh'''

