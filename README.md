= naivetsdb =

== an overly simplistic LevelDB backed TSDB for python3 ==

 * A TSDB object is both dict-like for sets/gets, as well as being in-order iterable over (key,value)
 * Both values are protocol 2 pickled before being put into LevelDB. 
 * Keys are unsigned 64 bit integers

```
>>> from naivetsdb import TSDB
>>> db = TSDB('testdb')
>>> db[1] = { 'a': 'b' }
>>> db[2] = 'xkcd'
>>> db[35] = (1,2,3,4,5,6,'smurf')
>>> for k,v in db:
...     print(k,':',v)
... 
1 : {'a': 'b'}
2 : xkcd
35 : (1, 2, 3, 4, 5, 6, 'smurf')
>>> del db[35]
>>> for n in range(500,5000):
...    db[n] = n
>>> for k,v in db[600:700]: 
...    assert k == v
...    assert k in range(600,700)
...
>>>
```

