#!/usr/bin/env python3

'''overly simplistic LevelDB backed TSDB
'''

__author__ = "David Basden <davidb-naivetsdb@rcpt.to>"

from leveldb import LevelDB
import pickle
import struct

def pik(v): return pickle.dumps(v, protocol=4)
def unpik(v): return pickle.loads(v,encoding='bytes')

encode_key = lambda k: struct.pack(">q",k)
decode_key = lambda k: struct.unpack(">q",k)[0]


class TSDB(object):
    def __init__(self, filename):
        self.ldb = LevelDB(filename)

    def __setitem__(self,k,v):
        v = pik(v)
        self.ldb.Put(encode_key(k),v)

    def _iter_unpack(self, it):
        for k,v in it:
            yield decode_key(k),unpik(v)

    def __getitem__(self, key):
        if isinstance(key, slice):
            start = encode_key(key.start)
            stop = encode_key(key.stop-1)
            return self._iter_unpack( self.ldb.RangeIter(start,stop) )
        else:
            key = encode_key(key)
            v = self.ldb.Get(key)
            return unpik(v)

    def __iter__(self):
        for k,v in self.ldb.RangeIter():
            k= bytes(k)
            v = bytes(v)
            yield decode_key(k),unpik(v)

    def __delitem__(self,k):
         k = encode_key(k) 
         self.ldb.Delete(k)

    def set(self,k,v):
        self[k] = v

    def get(self,k,default=None): 
        try: return self[k]
        except KeyError: return default

if __name__ == '__main__':
    tsdb = TSDB("testtsdb")
    tsdb[1234] = dict(a=1,b=2)
    tsdb[5435] = "asdf"
    tsdb[9999209453094] = 5

    del tsdb[5435]

    for n in range(500):
        tsdb[n] = n

    for k,v in tsdb[460:470]:
        assert k==v
        assert k in range(460,470)
    assert len(list(tsdb[55:66])) == 11

    assert tsdb.get(5435) == None
    assert tsdb.get(5435,'5') == '5'
