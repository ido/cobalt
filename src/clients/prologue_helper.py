#! /usr/bin/env python

import sys
import os
import ConfigParser
import Cobalt
import subprocess
import logging
import time
import signal
import Cobalt.Util

logging.basicConfig(level=logging.INFO, format="%(message)s")

config = ConfigParser.ConfigParser()
config.read(Cobalt.CONFIG_FILES)
if not config.has_section('cluster_system'):
    print '''"ERROR: cluster_system" section missing from cobalt config file'''
    sys.exit(1)

def get_cluster_system_config(option, default):
    try:
        value = config.get('cluster_system', option)
    except ConfigParser.NoOptionError:
        value = default
    return value

sim_mode  = get_cluster_system_config("simulation_mode", 'false').lower() in Cobalt.Util.config_true_values

try:
    prologue = config.get("cluster_system", "prologue")
except:
    logging.error("prologue entry not found under [cluster_system] in cobalt.conf")
    sys.exit(1)

try:
    prologue_timeout = float(config.get("cluster_system", "prologue_timeout"))
except:
    logging.error("prologue_timeout entry not found under [cluster_system] in cobalt.conf")
    sys.exit(1)

args = {}
for s in sys.argv[1:]:
    try:
        key = s.split("=")[0]
        value = '='.join(s.split('=')[1:])
    except IndexError:
        print >> sys.stderr, "Malformed argument %s.  Ignoring." % s
    else:
        args[key] = value

if not sim_mode:
    nodefile_dir = get_cluster_system_config("nodefile_dir", "/var/tmp")
    nodefile = os.path.join(nodefile_dir, "cobalt.%s" % args['jobid'])
else:
    nodefile = "fake"

user = args["user"]
location = args["location"].split(":")
jobid = args["jobid"]

fd = open(nodefile, "w")
for host in location:
    fd.write(host + "\n")
fd.close()

if sim_mode:
    sys.exit(0)

# run the prologue, while still root
processes = []
for host in location:
    h = host.split(":")[0]
    try:
        p = subprocess.Popen(["/usr/bin/scp", nodefile, "%s:%s" % (h, nodefile_dir)],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.host = h
        p.action = "nodefile copy"
        processes.append(p)
    except:
        logging.error("Job %s/%s failed to copy nodefile %s to host %s", jobid, user, nodefile, h)
        #Make sure the script fails if can't copy the nodefile
        raise

    try:
        p = subprocess.Popen(["/usr/bin/ssh", h, prologue, jobid, user, "no_group"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.host = h
        p.action = "prologue"
        processes.append(p)
    except:
        logging.error("Job %s/%s failed to run prologue on host %s" , jobid, user, h, exc_info=True)
        raise


prologue_failure = []
start = time.time()
while True:
    running = False
    for p in processes:
        if p.poll() is None:
            running = True
            break

    if not running:
        break

    if time.time() - start > prologue_timeout:
        for p in processes:
            if p.poll() is None:
                logging.error("Job %s/%s %s timed out on host %s", jobid, user, p.action, p.host)
                prologue_failure.append(p.host)
                try:
                    os.kill(p.pid, signal.SIGTERM)
                except:
                    logging.error("%s for %s already terminated", p.action, p.host)
        break
    else:
        Cobalt.Util.sleep(5)

for p in processes:
    if p.poll() > 0:
        logging.error("%s failed for host %s", p.action, p.host)
        prologue_failure.append(p.host)
        logging.error("stderr from %s on host %s: [%s]", p.action, p.host, p.stderr.read().strip())


if prologue_failure:
    sys.exit(1)
else:
    sys.exit(0)
