#!/usr/bin/python
"""Run Cobalt's unit tests and summarize from a test manifest file
   Not intended for Jenkins use, but for local use

"""

import sys
import os.path
import subprocess
import xml.etree.ElementTree
import time

OK = 0
MAX_PARALLEL_PROCESSES = 4

TEST_EXE = "nosetests"
TEST_BASE_OPTS = "-v --with-xunit"


def main():
    start_time = time.time()
    overall_status = OK
    xunit_files = []
    failed_files = []
    processes = {}
    for manifest in sys.argv[1:]:
        with open(manifest, 'r') as manifest_file:
            test_filenames = [filename.split('#')[0].strip() for filename in manifest_file.readlines()
                    if filename.split('#')[0].strip() != ""]
            for test_file in test_filenames:
                xunit_filename = os.path.splitext(os.path.basename(test_file))[0] + ".xml"
                xunit_files.append(xunit_filename)
                processes[test_file] = subprocess.Popen([TEST_EXE, "-v", "--with-xunit", "--xunit-file="+ xunit_filename, test_file],
                        stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                print "started", test_file
                if len(processes) >= MAX_PARALLEL_PROCESSES or len(processes) >= len(test_filenames):
                    # Wait for completion and harvest output.
                    for test_file, proc in processes.items():
                        print "waiting for", test_file
                        stdout, stderr = proc.communicate()
                        print stdout
                        if proc.returncode != 0 and overall_status == 0:
                            overall_status = proc.returncode
                        if proc.returncode != 0:
                            failed_files.append(test_file)
                    processes = {} #all are cleared
    end_time = time.time()
    # Get overall run statistics for summary
    overall_tests = 0
    overall_failures = 0
    overall_errors = 0
    overall_skips = 0
    overall_time = 0.0
    for xunit_filename in xunit_files:
        with open(xunit_filename, 'r') as xunit_file:
            xml_tree = xml.etree.ElementTree.parse(xunit_file)
            xml_root = xml_tree.getroot()
            run_attrs = xml_root.attrib
            overall_tests += int(run_attrs['tests'])
            overall_failures += int(run_attrs['failures'])
            overall_errors += int(run_attrs['errors'])
            overall_skips += int(run_attrs['skip'])
            for testcase in xml_root.iter('testcase'):
                overall_time += float(testcase.attrib['time'])

    print "=" * 80
    print "Overall Statistics"
    print "Tests: " + str(overall_tests)
    print "Failures: " + str(overall_failures)
    print "Errors: " + str(overall_errors)
    print "Skips: " + str(overall_skips)
    print "Overall Test Runtime: " + str(overall_time)
    print "Overall Suite Runitime: " + "%f" % (end_time - start_time)
    print "=" * 80

    if overall_status == 0:
        print "UNIT TESTS FOR %s OK" % ", ".join(sys.argv[1:])
    else:
        print "UNIT TESTS FOR %s FAILED" % ", ".join(sys.argv[1:])
        print "FAILURES IN FILES:"
        print "\n".join(failed_files)
    return overall_status


if __name__ == "__main__":
    sys.exit(main())
