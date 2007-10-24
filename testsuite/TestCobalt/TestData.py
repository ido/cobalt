import time
import itertools
import warnings

from Cobalt.Data import \
    IncrID, RandomID, \
    Data, ForeignData, \
    DataSet, ForeignDataSet, \
    DataCreationError, \
    DataList, DataDict


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
    
    TAG = "tag"
    FIELDS = dict(
        one = 1,
        two = 2,
    )
    INVALID_FIELDS = dict(
        four = 4,
        five = 5,
    )
    
    def setup (self):
        warnings.resetwarnings()
    
    def teardown (self):
        warnings.resetwarnings()
    
    def test_required_fields (self):
        class NewData (Data):
            fields = Data.fields.copy()
            required_fields = self.FIELDS.keys()
            for field in required_fields:
                fields[field] = None
        
        try:
            data = NewData()
        except DataCreationError:
            pass
        else:
            assert not "Must specify all required fields."
        
        try:
            data = NewData(self.FIELDS)
        except DataCreationError:
            assert not "Specified all required fields."
    
    def test_stamp (self):
        # __init__ uses Data.set() to set the stamp, which actually calls
        # time.time() twice: once to set, and another in Data.set()
        data = Data()
        for key, value in self.FIELDS.items():
            last_stamp = data.stamp
            assert time.time() - last_stamp < 1
            setattr(data, key, value)
            assert data.stamp > last_stamp
    
    def test_get (self):
        warnings.simplefilter("ignore", DeprecationWarning)
        warnings.simplefilter("ignore", RuntimeWarning)
        
        class NewData (Data):
            fields = Data.fields.copy()
            for field in self.FIELDS.iterkeys():
                fields[field] = None
        
        data = NewData(self.FIELDS)
        for key, value in self.FIELDS.items():
            assert data.get(key) == value
    
    def test_get_default (self):
        warnings.simplefilter("ignore", DeprecationWarning)
        
        class NewData (Data):
            fields = Data.fields.copy()
            for field in self.FIELDS.iterkeys():
                fields[field] = None
        
        data = NewData(self.FIELDS)
        for key, value, default in zip(self.FIELDS.keys(), self.FIELDS.values(), self.INVALID_FIELDS.values()):
            assert data.get(key, default) == value
        for key, value in self.INVALID_FIELDS.items():
            assert data.get(key) is None
            assert data.get(key, value) == value
    
    def test_set (self):
        warnings.simplefilter("ignore", DeprecationWarning)
        warnings.simplefilter("ignore", RuntimeWarning)
        data = Data()
        
        for key, value in self.FIELDS.items():
            data.set(key, value)
            assert getattr(data, key) == value
    
    def test_update (self):
        data = Data()
        
        data.update(self.FIELDS)
        for key, value in self.FIELDS.items():
            assert getattr(data, key) == value
    
    def test_match (self):
        class NewData (Data):
            fields = Data.fields.copy()
            for field in self.FIELDS.iterkeys():
                fields[field] = None
        
        data = NewData(self.FIELDS)
        assert data.match(self.FIELDS)
        
        fields = self.FIELDS.copy()
        for key, value in zip(fields.keys(), self.INVALID_FIELDS.values()):
            fields[key] = value
        assert not data.match(fields)
        assert not data.match(self.INVALID_FIELDS)
    
    def test_setstate (self):
        _attrib = dict(
            one = 1,
            two = 2,
        )
        special_cases = dict()
        special_cases["exit-status"] = "exit_status" # special case
        _attrib.update(special_cases)
        
        data = Data(self.FIELDS)
        state = data.__dict__.copy()
        state["_attrib"] = _attrib # legacy value that setstate should change
        data.__setstate__(state)
        
        assert not hasattr(data, "_attrib")
        
        for key in state:
            if key != "_attrib":
                assert hasattr(data, key)
        
        for key in _attrib:
            if key in special_cases:
                assert hasattr(data, special_cases[key])
                assert not hasattr(data, key)
            else:
                assert hasattr(data, key)
    
    def test_setstate_defaults (self):
        class ExtendedData (Data):
            fields = Data.fields.copy()
            fields.update(dict(
                one = 1,
                two = 2,
            ))
        
        data = ExtendedData()
        data.one = 3
        data.two = 4
        
        state = data.__dict__.copy()
        del state["one"]
        del state["two"]
        
        data.__setstate__(state)
        assert data.one == 1
        assert data.two == 2
    
    def test_to_rx (self):
        data = Data(self.FIELDS)
        
        rx = data.to_rx(self.FIELDS)
        assert rx == self.FIELDS
    
    def test_to_rx_default (self):
        class ExtendedData (Data):
            fields = Data.fields.copy()
            fields.update(dict(
                self.FIELDS,
            ))
        data = ExtendedData()
        rx = data.to_rx()
        for field in self.FIELDS:
            assert field in rx
    
    def test_not_keyed (self):
        dataset = DataSet()
        assert dataset.__unique__ is None
        try:
            dataset["somevalue"]
        except KeyError:
            pass
        else:
            assert not "Didn't raise KeyError for non-keyed data."
    
    def test_keyed (self):
        class ExtendedDataSet (DataSet):
            __unique__ = "tag"
        
        dataset = ExtendedDataSet()
        data = Data({'tag':"asdf"})
        dataset.append(data)
        assert dataset["asdf"] is data
        try:
            dataset["invalid"] is data
        except KeyError:
            pass
        else:
            assert not "Didn't raise KeyError for invalid key."
    
    def test_del_keyed (self):
        class ExtendedDataSet (DataSet):
            __unique__ = "tag"
        
        dataset = ExtendedDataSet()
        data = Data({'tag':"asdf"})
        dataset.append(data)
        assert len(dataset.data) == 1
        del dataset["asdf"]
        assert len(dataset.data) == 0


class TestForeignData (TestData):
    
    def test_Sync (self):
        data = ForeignData()
        
        fields = self.FIELDS.copy()
        fields['stamp'] = "a specific value"
        
        data.Sync(fields)
        for key, value in self.FIELDS.items():
            if key != "stamp":
                assert getattr(data, key) == value
        assert data.stamp == fields['stamp']


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
    
    DATA_FIELDS = DataSet.__object__.fields
    
    DATA = [
        DataSet.__object__(DATA_FIELDS),
        DataSet.__object__(DATA_FIELDS),
    ]
    
    CDATA = [DATA_FIELDS, DATA_FIELDS]
    
    CARGS = (object(), object())
    
    def test_data (self):
        data_set = DataSet()
        assert data_set.data == []
    
    def test_iteration (self):
        data_set = DataSet()
        for data in self.DATA:
            data_set.append(data)
        for source, state in zip(self.DATA, data_set):
            assert source is state
    
    def test_append (self):
        data_set = DataSet()
        data = object()
        
        for data in self.DATA:
            data_set.append(data)
            assert list(data_set)[-1] is data
    
    def test_remove (self):
        data_set = DataSet()
        data = object()
        
        for data in self.DATA:
            data_set.append(data)
        count = list(data_set).count(data)
        data_set.remove(data)
        assert list(data_set).count(data) == count - 1
    
    def test_Add_single (self):
        data_set = DataSet()
        prior_length = len(list(data_set))
        data_set.Add(self.CDATA[0])
        assert len(list(data_set)) - prior_length == 1
        for data in data_set:
            assert isinstance(data, DataSet.__object__)
    
    def test_Add_multiple (self):
        data_set = DataSet()
        prior_length = len(list(data_set))
        data_set.Add(self.CDATA)
        assert len(list(data_set)) - prior_length == len(self.CDATA)
    
    def test_Add_callback (self):
        data_set = DataSet()
        cb_state = dict(items=[])
        def callback (item, cargs):
            cb_state['items'].append(item)
        
        data_set.Add(self.CDATA, callback)
        for cb_item, item in zip(cb_state['items'], data_set):
            assert cb_item is item
    
    def test_Add_cargs (self):
        data_set = DataSet()
        cb_state = dict(cargs=[])
        def callback (item, cargs):
            cb_state['cargs'].append(cargs)
        
        data_set.Add(self.CDATA, callback, self.CARGS)
        for cb_cargs in cb_state['cargs']:
            for cb_carg, carg in zip(cb_cargs, self.CARGS):
                assert cb_carg is carg
    
    def test_Add_value (self):
        data_set = DataSet()
        
        value = data_set.Add(self.CDATA)
        for rx, data, cdata in zip(value, list(data_set)[-len(self.CDATA):], self.CDATA):
            assert rx == DataSet.__object__.to_rx(data, cdata)
    
    def test_Get_single (self):
        data_set = DataSet()
        data_set.Add(self.CDATA)
        
        for data in self.CDATA:
            items = data_set.Get(data)
            for item in items:
                for key, value in data.items():
                    assert item.get(key)
    
    def test_Get_multiple (self):
        data_set = DataSet()
        data_set.Add(self.CDATA)
        
        value = data_set.Get(self.CDATA)
        for rx in value:
            match = False
            for data in self.CDATA:
                match = rx == data
                if match:
                    break
            assert match
            match = False
    
    def test_Get_callback (self):
        data_set = DataSet()
        cb_state = dict(items=[])
        def callback (item, cargs):
            cb_state['items'].append(item)
        data_set.Add(self.CDATA)
        
        data_set.Get(self.CDATA, callback)
        for cb_item, item in zip(cb_state['items'], data_set):
            assert cb_item is item
    
    def test_Get_cargs (self):
        data_set = DataSet()
        cb_state = dict(cargs=[])
        def callback (item, cargs):
            cb_state['cargs'].append(cargs)
        
        data_set.Get(self.CDATA, callback, self.CARGS)
        for cb_cargs in cb_state['cargs']:
            for cb_carg, carg in zip(cb_cargs, self.CARGS):
                assert cb_carg is carg
    
    def test_Del_single (self):
        data_set = DataSet()
        data_set.Add(self.CDATA)
        
        for data in self.CDATA:
            items = data_set.Del(data)
            assert not data_set.Get(data)
    
    def test_Del_multiple (self):
        data_set = DataSet()
        data_set.Add(self.CDATA)
        
        value = data_set.Del(self.CDATA)
        assert not data_set.Get(self.CDATA)
    
    def test_Del_callback (self):
        data_set = DataSet()
        cb_state = dict(items=[])
        def callback (item, cargs):
            cb_state['items'].append(item)
        data_set.Add(self.CDATA)
        
        data_set.Del(self.CDATA, callback)
        for cb_item, item in zip(cb_state['items'], data_set):
            assert cb_item is item
    
    def test_Del_cargs (self):
        data_set = DataSet()
        cb_state = dict(cargs=[])
        def callback (item, cargs):
            cb_state['cargs'].append(cargs)
        
        data_set.Del(self.CDATA, callback, self.CARGS)
        for cb_cargs in cb_state['cargs']:
            for cb_carg, carg in zip(cb_cargs, self.CARGS):
                assert cb_carg == carg


class TestForeignDataSet (TestDataSet):
    
    def setup (self):
        class ExtendedData (Data):
            fields = Data.fields.copy()
            fields.update(dict(
                id = None,
                attribute = 1,
            ))
            required_fields = ["id"]
        
        class ExtendedDataSet (DataSet):
            __object__ = ExtendedData
        
        self.dataset = ExtendedDataSet()
        
        class ExtendedForeignData (ForeignData):
            fields = ForeignData.fields.copy()
            fields.update(dict(
                id = None,
                attribute = 1,
            ))
        
        def sync (cdata):
            return self.dataset.Get(cdata)
        
        class ExtendedForeignDataSet (ForeignDataSet):
            __object__ = ExtendedForeignData
            __fields__ = ["id", "attribute"]
            __function__ = staticmethod(sync)
            __unique__ = "id"
        
        self.foreigndataset = ExtendedForeignDataSet()
    
    def test_Sync (self):
        assert not self.dataset.data
        self.dataset.Add([{'id':1}])
        assert self.dataset.data[-1].id == 1
        
        assert not self.foreigndataset.data
        self.foreigndataset.Sync()
        assert self.foreigndataset.data[-1].id == 1
        assert self.foreigndataset.data[-1].attribute == 1
        
        self.dataset.data[-1].attribute = 2
        self.foreigndataset.Sync()
        assert self.foreigndataset.data[-1].attribute == 2
        
        self.dataset.remove(self.dataset.data[-1])
        self.foreigndataset.Sync()
        assert not self.foreigndataset.data
