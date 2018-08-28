'''Automated tests for cray messages and formatting.'''


import nose
from nose.tools import raises
from cray_messaging import *


def dict_compare(d1, d2):
    for key1, val1 in d1.iteritems():
        if d1[key1] is None and d2[key1] is not None:
            print "key %s mismatch, should be None" % key1
            return False
        elif d1[key1] != d2[key1]:
            print "mismatch in key %s:\n%s\n%s" % (key1,
                    d1[key1], d2[key1])
            return False

    return True

class TestBASILRequest(object):

    @staticmethod
    def check_output(filename, request):
        '''asertion check against known good output in external file'''
        with open(filename) as test_out:
            expected = "".join([line for line in test_out])
        assert str(request) == expected, ("Reserve output did not match.\n"
                "Expected:\n%s\nGenerated:\n%s" % (expected, str(request)))

    def test_reserve(self):
        '''basic reserve function'''
        request = BasilRequest('reserve', params={'batch_id': 3, 'depth': 1,
            'width': 2, 'p-state': 'foo', 'user_name': 'frodo',
            'node_list':[1,2,3,4,5,8,10,11,20,34,35,36,42,5001,5002,5003,75]})
        self.check_output('testdata/test_reserve_output.xml', request)

    def test_inventory(self):
        '''basic inventory request'''
        request = BasilRequest('query', 'inventory')
        self.check_output('testdata/test_query_inventory.xml', request)

    def test_inventory_from_changecount(self):
        '''inventory request with starting changecount'''
        request = BasilRequest('query', type='inventory',
                params={'changecount': 42})
        self.check_output('testdata/test_query_inventory_changecount.xml', request)

    def test_inventory_get_res(self):
        '''inventory with reservation information'''
        request = BasilRequest('query', 'inventory',
                {'changecount': 45, 'get_reservation_info': True})
        self.check_output('testdata/test_query_inventory_reservation.xml', request)

    def test_confirm(self):
        '''confirm message'''
        request = BasilRequest('confirm', params={'pagg_id': 6, 'reservation_id': 7})
        self.check_output('testdata/test_confirm.xml', request)

    def test_release(self):
        '''release message'''
        request = BasilRequest('release', params={'reservation_id':8})
        self.check_output('testdata/test_release.xml', request)

    def test_topology(self):
        '''request topology information'''
        request = BasilRequest('query', 'topology',
            {'topology_name':'aries',
             'filters': [{'name': 'foo'}, {'name': 'bar'}]})
        self.check_output('testdata/test_query_topology.xml', request)

    def test_query_summary(self):
        '''test summary query'''
        request = BasilRequest('query', 'summary')
        self.check_output('testdata/test_query_summary.xml', request)

    def test_query_engine(self):
        '''test engine query'''
        request = BasilRequest('query', 'engine')
        self.check_output('testdata/test_query_engine.xml', request)

    @raises(InvalidBasilMethodError)
    def test_bad_method(self):
        '''raise exception on bad method request'''
        BasilRequest('foo')

    @raises(KeyError)
    def test_missing_required_params(self):
        '''raise exception on missing key parameters'''
        BasilRequest('confirm', params={'foo':'bar'})

    @raises(ValueError)
    def test_missing_query_type(self):
        '''raise exception on missing query type'''
        BasilRequest('query')

class TestBASILResponse(object):

    @staticmethod
    def verify_response(filename, expected):
        '''assert that we are parsing a message into an expected dictionary'''
        with open(filename) as infile:
            resp = parse_response(''.join([i.strip() for i in
                infile.readlines()]))
        assert dict_compare(resp, expected), 'Mismatch:\nExpected:\n%s\nGenerated:\n%s' % \
                (expected, resp)
        assert dict_compare(expected, resp), 'Mismatch:\nExpected:\n%s\nGenerated:\n%s' % \
                (expected, resp)


    def test_response_engine(self):
        '''engine query response parsing'''
        expected = {'status': 'SUCCESS', 'version': '5.1.0',
                'protocol': '1.7', 'name': 'ALPS',
                'basil_support': '1.7,1.6,1.5,1.4,1.3,1.2,1.1,1.0', 'type': 'Engine',
                'method': 'QUERY'}
        self.verify_response('testdata/test_response_engine.xml', expected)

    def test_response_reserved(self):
        '''reserved node response parsing'''
        expected = {'status': 'SUCCESS', 'reserved_nodes': ['9'],
                'reservation_id': '19', 'protocol': '1.7', 'type': 'Reserved',
                'method': 'RESERVE'}
        self.verify_response('testdata/test_response_reserved.xml', expected)

    def test_response_confirmed(self):
        '''parse reservation confirmation'''
        expected = {'status': 'SUCCESS', 'protocol': '1.7',
                'reservation_id': '20', 'pagg_id': '1234', 'type': 'Confirmed',
                'method': 'CONFIRM'}
        self.verify_response('testdata/test_response_confirmed.xml', expected)

    def test_response_released(self):
        '''parse reservation released response'''
        expected = {'status': 'SUCCESS', 'type': 'Released',
                'protocol': '1.7', 'method': 'RELEASE'}
        self.verify_response('testdata/test_response_released.xml', expected)

    def test_response_inventory(self):
        '''parse inventory response'''

        expected = {'status': 'SUCCESS', 'protocol': '1.7', 'changecount': '1', 'reservations':
                [{'gpc_mode': 'NONE', 'reservation_mode': 'EXCLUSIVE',
                    'batch_id': 'UNKNOWN', 'time_stamp': '1358437232',
                    'user_name': 'frodo', 'account_name': 'DEFAULT',
                    'reservation_id': '643', 'ApplicationArray':
                    [{'Application': [{'user_id': '12368', 'CommandArray':
                        [{'Command': [{'nppn': '0', 'width': '1', 'depth': '1',
                            'architecture': 'XT', 'memory': '1000', 'cmd':
                            'sleep'}]}], 'group_id': '100', 'application_id':
                        '2208', 'time_stamp': '1358437232'}]}]}],
                'timestamp': '1358436929',
               'nodes':
               [{'router_id': '124','state': 'UP', 'node_id': '249', 'role': 'BATCH', 'name': 'c0-4c0s2n1',
                   'SegmentArray':
                   [{'Segment':
                       [{'ordinal': '0',
                           'MemoryArray': [{'Memory': [{'page_size_kb': '4', 'page_count': '2048000', 'type': 'OS'}]}],
                           'ProcessorArray': [{'Processor': [{'ordinal': '0', 'architecture': 'x86_64', 'clock_mhz': '2400'},
                               {'ordinal': '1', 'architecture': 'x86_64', 'clock_mhz': '2400'},
                               {'ordinal': '2', 'architecture': 'x86_64', 'clock_mhz': '2400'},
                               {'ordinal': '3', 'architecture': 'x86_64', 'clock_mhz': '2400'}]}],
                           'LabelArray': [{'text': '(Anker: )(Anker: )(Anker: )(Anker: )'}]},
                        {'ordinal': '1',
                            'MemoryArray': [{'Memory': [{'page_size_kb': '4', 'page_count': '2048000', 'type': 'OS'}]}],
                            'ProcessorArray': [{'Processor': [{'ordinal': '0', 'architecture': 'x86_64', 'clock_mhz': '2400'},
                                {'ordinal': '1', 'architecture': 'x86_64', 'clock_mhz': '2400'},
                                {'ordinal': '2', 'architecture': 'x86_64', 'clock_mhz': '2400'},
                                {'ordinal': '3', 'architecture': 'x86_64', 'clock_mhz': '2400'}]}],
                            'LabelArray': [{'text': '(Anker: )(Anker: )(Anker: )(Anker: )'}]}]}],
                  'architecture': 'XT'},
                 {'router_id': '42', 'state': 'UP', 'node_id': '101', 'role': 'BATCH', 'name': 'c0-0c0s0n1',
                     'SegmentArray':
                     [{'Segment':
                         [{'ordinal': '1',
                             'MemoryArray': [{'Memory': [{'page_size_kb': '16', 'page_count': '2048', 'type': 'FOO'}]}],
                             'ProcessorArray': [{'Processor': [{'ordinal': '0', 'architecture': 'x86_64', 'clock_mhz': '2400'},
                                 {'ordinal': '1', 'architecture': 'x86_64', 'clock_mhz': '2400'},
                                 {'ordinal': '2', 'architecture': 'x86_64', 'clock_mhz': '2400'},
                                 {'ordinal': '3', 'architecture': 'x86_64', 'clock_mhz': '2400'}]}],
                             'LabelArray': [{'text': '(Foo: )(Bar: )(Baz: )(Qux: )'}]}]}],
                    'architecture': 'XT'}],
                'type': 'Inventory', 'method': 'QUERY', 'mpp_host': 'TEST'}



        self.verify_response('testdata/test_response_inventory.xml', expected)

    @raises(ALPSError)
    def test_error_response(self):
        '''raise exception for ALPS error sent back via XML'''
        with open('testdata/test_input_error1.xml') as infile:
            resp = parse_response(''.join([i.strip() for i in
                infile.readlines()]))
        assert False, "Got response %s instead of exception" % resp


    def test_error_response_contents(self):
        '''ALPSError has correct detail message set'''
        with open('testdata/test_input_error1.xml') as infile:
            try:
                resp = parse_response(''.join([i.strip() for i in infile.readlines()]))
            except ALPSError as err:
                assert err.severity  == 'DEBUG', 'wrong message severity'
                assert err.msg == 'Test Failure', 'bad message expected: %s got: %s' % \
                        ('Test Failure', err.msg)


