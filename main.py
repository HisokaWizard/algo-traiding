import sys
import timeit

list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
tuple = (1, 2, 3, 4, 5, 6, 7, 8, 9, 0)
dictionary = {
    '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '0': 0,
}
set = set(list)

print('size of list:', sys.getsizeof(list))
print('size of tuple:', sys.getsizeof(tuple))
print('size of dictionary:', sys.getsizeof(dictionary))
print('size of set:', sys.getsizeof(set))

print('\n' + '---' * 10 + '\n')

listTest = '''
list=[1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
'''
listTime = timeit.timeit(listTest, number=1000000)
print('ListTime:', listTime)

tupleTest = '''
tuple=(1, 2, 3, 4, 5, 6, 7, 8, 9, 0)
'''
tupleTime = timeit.timeit(tupleTest, number=1000000)
print('TupleTime:', tupleTime)

dictTest = '''
dictionary={'1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '0': 0}
'''
dictTime = timeit.timeit(dictTest, number=1000000)
print('DictionaryTime:', dictTime)

setTest = '''
s=set([1, 2, 3, 4, 5, 6, 7, 8, 9, 0])
'''
setTime = timeit.timeit(setTest, number=1000000)
print('SetTime:', setTime)
