Setting Up Cobalt Brooklyn Simulator:

The purpose of this readme file is to help setup local Cobalt running environment.

1. Create the following directories:
   Note: ~/p/Cobalt and src-primary can be whatever you want, but for simplicity we will make
	 the Cobalt main directory ~/p/Cobalt and the git repo will be in src-primary.

~/p/Cobalt/
       sysroot-brooklyn/
             etc/
             var/log/cobalt/   # files with component pids. used for termination
             var/spool/cobalt/ # contains the state files, maybe other stuff
             tmp/
       src-primary/ # git repo goes here

2. Clone Cobalt Repo:

In the ~/p/Cobalt directory do the following command:

git clone -b develop git://git.mcs.anl.gov/cobalt.git src-primary

3. From ../src-primary/tools/local_sim copy the following files:

../src-primary/tools/local_sim/simulator.xml   ~/p/Cobalt/
../src-primary/tools/local_sim/cstart.sh       ~/p/Cobalt/
../src-primary/tools/local_sim/cinit.sh        ~/p/Cobalt/
../src-primary/tools/local_sim/cobalt.conf     ~/p/Cobalt/sysroot-brooklyn/etc/
../src-primary/tools/local_sim/partlist-*.txt  ~/p/Cobalt/sysroot-brooklyn/etc/
../src-primary/tools/local_sim/test-*.py       ~/p/Cobalt/sysroot-brooklyn/etc/

4. In ~/p/Cobalt/src-primary/src do the following:

ln -s lib Cobalt 

5. In ~/p/Cobalt/sysroot-brooklyn/etc do the following (replacing $HOST with your hostname if needed):

openssl req -batch -x509 -nodes -subj "/C=US/ST=Illinois/L=Argonne/CN=$HOST" -days 1000 -newkey rsa:2048 -keyout ./cobalt.key -noout
openssl req -batch -new -subj "/C=US/ST=Illinois/L=Argonne/CN=$HOST" -key ./cobalt.key | openssl x509 -req -days 1000 -signkey ./cobalt.key -out ./cobalt.cert
ln -s partlist-R00-R01.txt partlist.txt

7. In .../src-primary/src/components do the following:

ln -s ../../../simulator.xml simulator.xml

8. In your .bash_profile you need the following:

export P=~/p

9. Copy and paste to the terminal the following commands:

export COBALT_SOURCE_DIR=$P/Cobalt/src-primary
export COBALT_RUNTIME_DIR=$P/Cobalt/sysroot-brooklyn
export COBALT_SYSTEM_TYPE=BGSIM

export COBALT_CONFIG_FILES=$COBALT_RUNTIME_DIR/etc/cobalt.conf
export PYTHONPATH=$COBALT_SOURCE_DIR/src:$COBALT_SOURCE_DIR/testsuite:${PYTHONPATH}
export PATH=${COBALT_SOURCE_DIR}/src/clients:${COBALT_SOURCE_DIR}/src/clients/POSIX:$PATH

10. Run the following only once per source tree:

# 
# Puts simlinks to remove .py from client commands. Only do this once per source tree
#
(cd $COBALT_SOURCE_DIR/src/clients ; \
 for f in cobalt-mpirun.py cq*.py part*.py releaseres.py setres.py showres.py slpstat.py userres.py schedctl.py brun.py; do \
     f2=`echo $f | sed -e 's/\.py$//'`; \
     ln -sf $f $f2 ; \
 done)
#
# Samething as above but for the POSIX client commands 
#

(cd $COBALT_SOURCE_DIR/src/clients/POSIX ; \
 for f in *.py ; do \
     f2=`echo $f | sed -e 's/\.py$//'`; \
     ln -sf $f $f2 ; \
 done)

11. Start all components:

~/p/Cobalt/cstart.sh

12. Only need this to re-initialize of initialize the sysroot-... 
    usually only once unless corruption or significant changes.
    To clean everything just delete the var directory and re-run this command:

~/p/Cobalt/cinit.sh 

13. To stop all components and Cobalt:

kill `cat $COBALT_RUNTIME_DIR/var/run/cobalt/*`

14. After starting the cobalt components with cstart.sh then you can monitor the following files:
    $COBALT_RUNTIME_DIR/var/log/cobalt/*.out
