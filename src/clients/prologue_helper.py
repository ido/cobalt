#! /usr/bin/env python

import sys
import ConfigParser
import Cobalt
import subprocess
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(message)s")

config = ConfigParser.ConfigParser()
config.read(Cobalt.CONFIG_FILES)

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
    key, value = s.split("=")
    args[key] = value

nodefile = "/var/tmp/cobalt.%s" % args["jobid"]
user = args["user"]
location = args["location"].split(":")
jobid = args["jobid"]

# run the prologue, while still root
processes = []
for host in location:
    h = host.split(":")[0]
    try:
        p = subprocess.Popen(["/usr/bin/scp", nodefile, "%s:/var/tmp" % h], 
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.host = h
        p.action = "nodefile copy"
        processes.append(p)
    except:
        logging.error("Job %s/%s failed to copy nodefile %s to host %s", jobid, user, nodefile, h)

    try:
        p = subprocess.Popen(["/usr/bin/ssh", h, prologue, jobid, user, "no_group"], 
                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        p.host = h
        p.action = "prologue"
        processes.append(p)
    except:
        logging.error("Job %s/%s failed to run prologue on host %s" , jobid, user, h, exc_info=True)


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
        time.sleep(5)

for p in processes:
    if p.poll() > 0:
        logging.error("%s failed for host %s", p.action, p.host)
        prologue_failure.append(p.host)
        logging.error("stderr from %s on host %s: [%s]", p.action, p.host, p.stderr.read().strip())


if prologue_failure:
    sys.exit(1)
else:
    sys.exit(0)
