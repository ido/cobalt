import time
import itertools
import warnings

from Cobalt.Data import IncrID, RandomID, Data, ForeignData, DataList, \
     DataDict, ForeignData, ForeignDataDict
from Cobalt.Exceptions import DataCreationError

import Cobalt.Logging

Cobalt.Logging.setup_logging("test", to_console=True)

class TestIncrID (object):
    
    def test_get (self, max=100):
        generator = IncrID()
        for count in itertools.count(1):
            assert generator.get() == count
            if count >= max:
                break
    
    def test_next (self, max=100):
        generator = IncrID()
        for count in itertools.count(1):
            assert generator.next() == count
            if count >= max:
                break


class TestRandomID (object):
    
    def test_get (self, count=100):
        generator = RandomID()
        id_list = []
        while True:
            id = generator.get()
            assert id not in id_list
            id_list.append(id)
            if len(id_list) >= count:
                break
    
    def test_next (self, count=100):
        generator = RandomID()
        id_list = []
        while True:
            id = generator.next()
            assert id not in id_list
            id_list.append(id)
            if len(id_list) >= count:
                break


class TestData (object):
    
    def setup (self):
        warnings.resetwarnings()
    
    def teardown (self):
        warnings.resetwarnings()

    def test_init (self):
        class r(Data):
            required = ['foo']
            inherent = ['id']

        try:
            item = r({})
            assert False
        except DataCreationError:
            pass

        try:
            item = r({'id':2})
            assert False
        except DataCreationError:
            pass
    
    def test_get (self):
        warnings.simplefilter("ignore", DeprecationWarning)
        warnings.simplefilter("ignore", RuntimeWarning)
        
        data = Data({'tag':"somedata"})
        assert data.get("tag") == "somedata"
    
    def test_get_default (self):
        warnings.simplefilter("ignore", DeprecationWarning)
        
        data = Data({'tag':"somedata"})
        assert data.get("tag", "default_value") == "somedata"
        assert data.get("not_an_attribute", "default_value") == "default_value"
    
    def test_set (self):
        warnings.simplefilter("ignore", DeprecationWarning)
        warnings.simplefilter("ignore", RuntimeWarning)
        data = Data({'tag':"somedata"})
        data.set("tag", "someotherdata")
        assert data.tag == "someotherdata"
    
    def test_update (self):
        warnings.simplefilter("ignore", DeprecationWarning)
        warnings.simplefilter("ignore", RuntimeWarning)
        data = Data({'tag':"somedata"})
        data.update({'tag':"someotherdata"})
        assert data.tag == "someotherdata"
    
    def test_match (self):
        data = Data({'tag':"somedata"})
        assert data.match({'tag':"*"})
        assert data.match({'tag':"somedata"})
        assert not data.match({'tag':"someotherdata"})
        assert not data.match({'tag':"somedata", 'not_an_attribute':"someotherdata"})
    
    def test_to_rx (self):
        data = Data({'tag':"somedata"})
        rx = data.to_rx(["tag", "otherattribute"])
        assert set(rx.keys()) == set(["tag", "otherattribute"])
        assert rx['tag'] == "somedata"
        assert rx['otherattribute'] is None


class TestForeignData (TestData):
    
    def test_Sync (self):
        data1 = Data({'tag':"somedata"})
        data2 = ForeignData({})
        data2.Sync(data1.to_rx())
        
        for field in data2.fields:
            assert getattr(data1, field) == getattr(data2, field)


class TestDataList (object):
    
    def setup (self):
        self.datalist = DataList()
        self.datalist.item_cls = Data
    
    def test_q_add (self):
        one = {'tag':"one"}
        two = {'tag':"two"}
        self.datalist.q_add([one, two])
        assert len(self.datalist) == 2
        assert self.datalist[0].tag == "one"
        assert self.datalist[1].tag == "two"
    
    def test_q_get (self):
        one = {'tag':"one"}
        two = {'tag':"two"}
        three = {'tag':"three"}
        self.datalist.q_add([one, two, three])
        items = self.datalist.q_get([{'tag':"three"}])
        assert len(items) == 1
        item = items[0]
        assert item is self.datalist[2]
        assert item.tag == "three"
    
    def test_q_del (self):
        one = {'tag':"one"}
        two = {'tag':"two"}
        three = {'tag':"three"}
        self.datalist.q_add([one, two, three])
        deleted = self.datalist.q_del([{'tag':"two"}])
        assert len(deleted) == 1
        assert deleted[0].tag == "two"
        assert len(self.datalist) == 2
        assert self.datalist[0].tag == "one"
        assert self.datalist[1].tag == "three"


class TestDataDict (object):
    
    def setup (self):
        self.datadict = DataDict()
        self.datadict.item_cls = Data
        self.datadict.key = "tag"
    
    def test_q_add (self):
        one = {'tag':"one"}
        two = {'tag':"two"}
        self.datadict.q_add([one, two])
        assert len(self.datadict) == 2
        assert self.datadict['one'].tag == "one"
        assert self.datadict['two'].tag == "two"
        try:
            self.datadict.q_add([one])
        except KeyError:
            pass
        else:
            assert not "Allowed multiple entries for same key."
    
    def test_q_get (self):
        one = {'tag':"one"}
        two = {'tag':"two"}
        three = {'tag':"three"}
        self.datadict.q_add([one, two, three])
        items = self.datadict.q_get([{'tag':"three"}])
        assert len(items) == 1
        assert items[0] is self.datadict["three"]
        assert items[0].tag == "three"
    
    def test_q_del (self):
        one = {'tag':"one"}
        two = {'tag':"two"}
        three = {'tag':"three"}
        self.datadict.q_add([one, two, three])
        deleted = self.datadict.q_del([{'tag':"two"}])
        assert len(deleted) == 1
        assert deleted[0].tag == "two"
        assert len(self.datadict) == 2
        assert self.datadict["one"].tag == "one"
        try:
            self.datadict["two"]
        except KeyError:
            pass
        else:
            assert not "Failed to remove item from list."
        assert self.datadict["three"].tag == "three"


class TestForeignDataDict (object):
    class my_data (ForeignData):
        fields = ['id', 'value']
        def __init__(self, spec):
            self.id = spec.get('id')
            self.value = spec.get('value')
        
    class sync_tester (object):
        data = [{'tag':'foo', 'id':1, 'value':'queued'},
                {'tag':'foo', 'id':2, 'value':'queued'},
                {'tag':'foo', 'id':3, 'value':'queued'},
                {'tag':'foo', 'id':1, 'value':'hold'}]
        def __init__(self):
            self.count = 0

        def Call(self, arg):
            self.count += 1
            if self.count == 1:
                return []
            elif self.count == 2:
                return self.data[:3]
            elif self.count == 3:
                return [self.data[1], self.data[3]]
            elif self.count == 4:
                raise Exception

    def TestSync(self):
        m = self.my_data({'tag':'foo', 'id':1, 'value':'queued'})
        print m.id
        s = self.sync_tester()
        f = ForeignDataDict()
        f.item_cls = self.my_data
        f.key = 'id'
        f.__function__ = s.Call
        f.Sync()
        assert len(f.keys()) == 0
        f.Sync()
        assert len(f.keys()) == 3
        f.Sync()
        assert len(f.keys()) == 2
        assert f[1].value == 'hold'
        assert f.__oserror__.status == True
        f.Sync()
        assert f.__oserror__.status == False
