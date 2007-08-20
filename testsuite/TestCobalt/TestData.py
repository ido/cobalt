import time
import itertools

import Cobalt.Data


class TestIncrID (object):
    
    def test_get (self, max=100):
        generator = Cobalt.Data.IncrID()
        for count in itertools.count(1):
            assert generator.get() == count
            if count >= max:
                break
    
    def test_next (self, max=100):
        generator = Cobalt.Data.IncrID()
        for count in itertools.count(1):
            assert generator.next() == count
            if count >= max:
                break


class TestRandomID (object):
    
    def test_get (self, count=100):
        generator = Cobalt.Data.RandomID()
        id_list = []
        while True:
            id = generator.get()
            assert id not in id_list
            id_list.append(id)
            if len(id_list) >= count:
                break
    
    def test_next (self, count=100):
        generator = Cobalt.Data.RandomID()
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
    
    def test_tag (self):
        data = Cobalt.Data.Data({})
        assert data.tag is None
        
        data = Cobalt.Data.Data({
            'tag': self.TAG,
        })
        assert data.tag == self.TAG
    
    def test_required_fields (self):
        class NewData (Cobalt.Data.Data):
            required_fields = self.FIELDS.keys()
        
        try:
            data = NewData({})
        except Cobalt.Data.DataCreationError:
            pass
        else:
            assert not "Must specify all required fields."
        
        try:
            data = NewData(self.FIELDS)
        except Cobalt.Data.DataCreationError:
            assert not "Specified all required fields."
    
    def test_stamp (self):
        # __init__ uses Data.set() to set the stamp, which actually calls
        # time.time() twice: once to set, and another in Data.set()
        data = Cobalt.Data.Data({})
        for key, value in self.FIELDS.items():
            last_stamp = data.get('stamp')
            assert time.time() - last_stamp < 1
            data.set(key, value)
            assert data.get('stamp') > last_stamp
    
    def test_get (self):
        data = Cobalt.Data.Data(self.FIELDS)
        for key, value in self.FIELDS.items():
            assert data.get(key) == value
    
    def test_get_default (self):
        data = Cobalt.Data.Data(self.FIELDS)
        
        for key, value, default in zip(self.FIELDS.keys(), self.FIELDS.values(), self.INVALID_FIELDS.values()):
            assert data.get(key, default) == value
        
        for key, value in self.INVALID_FIELDS.items():
            assert data.get(key) is None
            assert data.get(key, value) == value
    
    def test_set (self):
        data = Cobalt.Data.Data({})
        
        for key, value in self.FIELDS.items():
            data.set(key, value)
            assert data.get(key) == value
    
    def test_update (self):
        data = Cobalt.Data.Data({})
        
        data.update(self.FIELDS)
        for key, value in self.FIELDS.items():
            assert data.get(key) == value
    
    def test_match (self):
        data = Cobalt.Data.Data(self.FIELDS)
        
        assert data.match(self.FIELDS)
        
        fields = self.FIELDS.copy()
        for key, value in zip(fields.keys(), self.INVALID_FIELDS.values()):
            fields[key] = value
        assert not data.match(fields)
        
        assert not data.match(self.INVALID_FIELDS)
    
    def test_to_rx (self):
        data = Cobalt.Data.Data(self.FIELDS)
        
        rx = data.to_rx(self.FIELDS)
        assert rx == self.FIELDS


class TestForeignData (TestData):
    
    def test_Sync (self):
        # argument 'data' should be 'spec'
        # there should not be a reference to jobid here.
        assert False
        data = Cobalt.Data.Data(self.FIELDS)
        upd_fields = self.FIELDS.copy()
        for key, value in zip(upd_fields.keys(), self.INVALID_FIELDS.values()):
            upd_fields[key] = value


class TestDataSet (object):
    
    DATA_FIELDS = TestData.FIELDS
    
    DATA = [
        Cobalt.Data.DataSet.__object__(DATA_FIELDS),
        Cobalt.Data.DataSet.__object__(DATA_FIELDS),
    ]
    
    CDATA = [DATA_FIELDS, DATA_FIELDS]
    
    CARGS = (object(), object())
    
    
    
    def test_data (self):
        data_set = Cobalt.Data.DataSet()
        assert data_set.data == []
    
    def test_iteration (self):
        data_set = Cobalt.Data.DataSet()
        for data in self.DATA:
            data_set.append(data)
        for source, state in zip(self.DATA, data_set):
            assert source is state
    
    def test_append (self):
        data_set = Cobalt.Data.DataSet()
        data = object()
        
        for data in self.DATA:
            data_set.append(data)
            assert list(data_set)[-1] is data
    
    def test_remove (self):
        data_set = Cobalt.Data.DataSet()
        data = object()
        
        for data in self.DATA:
            data_set.append(data)
        count = list(data_set).count(data)
        data_set.remove(data)
        assert list(data_set).count(data) == count - 1
    
    def test_Add_single (self):
        data_set = Cobalt.Data.DataSet()
        prior_length = len(list(data_set))
        data_set.Add(self.CDATA[0])
        assert len(list(data_set)) - prior_length == 1
        for data in data_set:
            assert isinstance(data, Cobalt.Data.DataSet.__object__)
    
    def test_Add_multiple (self):
        data_set = Cobalt.Data.DataSet()
        prior_length = len(list(data_set))
        data_set.Add(self.CDATA)
        assert len(list(data_set)) - prior_length == len(self.CDATA)
    
    def test_Add_callback (self):
        data_set = Cobalt.Data.DataSet()
        cb_state = dict(items=[])
        def callback (item, cargs):
            cb_state['items'].append(item)
        
        data_set.Add(self.CDATA, callback)
        for cb_item, item in zip(cb_state['items'], data_set):
            assert cb_item is item
    
    def test_Add_cargs (self):
        data_set = Cobalt.Data.DataSet()
        cb_state = dict(cargs=[])
        def callback (item, cargs):
            cb_state['cargs'].append(cargs)
        
        data_set.Add(self.CDATA, callback, self.CARGS)
        for cb_cargs in cb_state['cargs']:
            for cb_carg, carg in zip(cb_cargs, self.CARGS):
                assert cb_carg is carg
    
    def test_Add_value (self):
        data_set = Cobalt.Data.DataSet()
        
        value = data_set.Add(self.CDATA)
        for rx, data, cdata in zip(value, list(data_set)[-len(self.CDATA):], self.CDATA):
            assert rx == Cobalt.Data.DataSet.__object__.to_rx(data, cdata)
    
    def test_Get_single (self):
        data_set = Cobalt.Data.DataSet()
        data_set.Add(self.CDATA)
        
        for data in self.CDATA:
            items = data_set.Get(data)
            for item in items:
                for key, value in data.items():
                    assert item.get(key)
    
    def test_Get_multiple (self):
        data_set = Cobalt.Data.DataSet()
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
        data_set = Cobalt.Data.DataSet()
        cb_state = dict(items=[])
        def callback (item, cargs):
            cb_state['items'].append(item)
        data_set.Add(self.CDATA)
        
        data_set.Get(self.CDATA, callback)
        for cb_item, item in zip(cb_state['items'], data_set):
            assert cb_item is item
    
    def test_Get_cargs (self):
        data_set = Cobalt.Data.DataSet()
        cb_state = dict(cargs=[])
        def callback (item, cargs):
            cb_state['cargs'].append(cargs)
        
        data_set.Get(self.CDATA, callback, self.CARGS)
        for cb_cargs in cb_state['cargs']:
            for cb_carg, carg in zip(cb_cargs, self.CARGS):
                assert cb_carg is carg
    
    def test_Del_single (self):
        data_set = Cobalt.Data.DataSet()
        data_set.Add(self.CDATA)
        
        for data in self.CDATA:
            items = data_set.Del(data)
            assert not data_set.Get(data)
    
    def test_Del_multiple (self):
        data_set = Cobalt.Data.DataSet()
        data_set.Add(self.CDATA)
        
        value = data_set.Del(self.CDATA)
        assert not data_set.Get(self.CDATA)
    
    def test_Del_callback (self):
        data_set = Cobalt.Data.DataSet()
        cb_state = dict(items=[])
        def callback (item, cargs):
            cb_state['items'].append(item)
        data_set.Add(self.CDATA)
        
        data_set.Del(self.CDATA, callback)
        for cb_item, item in zip(cb_state['items'], data_set):
            assert cb_item is item
    
    def test_Del_cargs (self):
        data_set = Cobalt.Data.DataSet()
        cb_state = dict(cargs=[])
        def callback (item, cargs):
            cb_state['cargs'].append(cargs)
        
        data_set.Del(self.CDATA, callback, self.CARGS)
        for cb_cargs in cb_state['cargs']:
            for cb_carg, carg in zip(cb_cargs, self.CARGS):
                assert cb_carg is carg
