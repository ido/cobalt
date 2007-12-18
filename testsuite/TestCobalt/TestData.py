import time
import itertools
import warnings

from Cobalt.Data import \
    IncrID, RandomID, \
    Data, ForeignData, \
    DataSet, DataList, DataDict, \
    DataCreationError


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


class TestDataSet (object):
    
    def test_default_data (self):
        data_set = DataSet()
        assert data_set.data == []
    
    def test_iteration (self):
        data_set = DataSet()
        datas = [object(), object()]
        for data in datas:
            data_set.append(data)
        assert set(datas) == set(data_set)
    
    def test_append (self):
        data_set = DataSet()
        for data in [object(), object()]:
            data_set.append(data)
            assert list(data_set)[-1] is data
    
    def test_remove (self):
        data_set = DataSet()
        
        for data in [object(), object()]:
            data_set.append(data)
        count = list(data_set).count(data)
        data_set.remove(data)
        assert list(data_set).count(data) == count - 1
    
    def test_Add_single (self):
        data_set = DataSet()
        data_set.__object__ = Data
        data_set.Add({'tag':"somedata"})
        assert len(list(data_set)) == 1
        assert list(data_set)[0].to_rx() == {'tag':"somedata"}
    
    def test_Add_multiple (self):
        data_set = DataSet()
        data_set.__object__ = Data
        data_set.Add([{'tag':"somedata"}, {'tag':"someotherdata"}])
        assert len(list(data_set)) == 2
    
    def test_Add_value (self):
        data_set = DataSet()
        data_set.__object__ = Data
        value = data_set.Add({'tag':"somedata"})
        assert len(value) == 1
        assert value[0] == {'tag':"somedata"}
    
    def test_Get_single (self):
        data_set = DataSet()
        data_set.__object__ = Data
        specs = [{'tag':"somedata"}, {'tag':"someotherdata"}]
        data_set.Add(specs)
        items = data_set.Get({'tag':"somedata"})
        assert len(items) == 1
        assert items[0]['tag'] == "somedata"
    
    def test_Get_multiple (self):
        data_set = DataSet()
        data_set.__object__ = Data
        specs = [{'tag':"somedata"}, {'tag':"someotherdata"}]
        data_set.Add(specs)
        items = data_set.Get([{'tag':"*"}])
        assert len(items) == 2
        for item in items:
            assert item == specs[0] or item == specs[1]
        items = data_set.Get([{'tag':"somedata"}, {'tag':"someotherdata"}])
        assert len(items) == 2
        for item in items:
            assert item == specs[0] or item == specs[1]
        items = data_set.Get([{'tag':"somedata"}])
        assert len(items) == 1
        assert items[0] == specs[0]
