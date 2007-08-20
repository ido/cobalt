import time
import itertools

import Cobalt.Data

class TestIncrID (object):
    
    def test_get (self, max=100):
        generator = Cobalt.Data.IncrID()
        for id in itertools.count(1):
            assert generator.get() == id
            if id >= max:
                break


class TestRandomID (object):
    
    def test_get (self, count=1000):
        generator = Cobalt.Data.RandomID()
        id_list = []
        while True:
            id = generator.get()
            assert id not in id_list
            id_list.append(id)
            if len(id_list) >= count:
                break
        assert len(id_list) == count


class TestData (object):
    
    TAG = "tag"
    FIELDS = dict(
        one = 1,
        two = 2,
        three = 3,
    )
    INVALID_FIELDS = dict(
        four = 4,
        five = 5,
        six = 6,
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
    
    def test_get_undefined (self):
        data = Cobalt.Data.Data(self.FIELDS)
        for key, value in self.INVALID_FIELDS.items():
            try:
                data.get(key)
            except KeyError:
                pass
            else:
                assert not "Can't get undefined data."
    
    def test_get_default (self):
        data = Cobalt.Data.Data(self.FIELDS)
        
        for key, value, default in zip(self.FIELDS.keys(), self.FIELDS.values(), self.INVALID_FIELDS.values()):
            assert data.get(key, default) == value
        
        for key, value in self.INVALID_FIELDS.items():
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
        
        try:
            data.match(self.INVALID_FIELDS)
        except KeyError:
            pass
        else:
            assert not "Fields must be valid for the instance."
    
    def test_to_rx (self):
        data = Cobalt.Data.Data(self.FIELDS)
        
        rx = data.to_rx(self.FIELDS)
        assert rx == self.FIELDS
        
        rx = data.to_rx(self.INVALID_FIELDS)
        assert not rx
