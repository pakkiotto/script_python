import decorator


def func(foo='bar', name='Mario'):
    print(foo)
    print(name)



# 1
# func(foo='fooo', name='Luigi')


# 2
d = {'foo': 'BAR', 'name': 'SAMPLE'}
# func(**d)


def func_var(*args, **kwargs):
    print(args)
    print(kwargs)


# func_var(**d)
#
# func_var(1,2,3, sample='PARAM', aaa='AAA')


def sum(*args, **kwargs):
    sum = kwargs.get('initial_value', 0)
    for a in args:
        sum = sum + a
    return sum




print(sum(1,2,3,45))
print(sum(1,2,3,45, initial_value=10))


import functools

def curry(fun, *e_args, **e_kwargs):

    def internal(*args, **kwargs):
        return fun(*args, **e_kwargs)

    return internal


sum_from_100 = functools.partial(sum, initial_value=100)

print(sum_from_100(1))


sum_f_100 = curry(sum, initial_value=100)

print(sum_f_100(99))


def my_debug(tag='DEFAULT'):

    def decorator(func):

        def inner():
            print("%s Debug: Before..." % tag)
            func()
            print("%s Debug: After.." % tag )

        return inner

    return decorator


@my_debug(tag='SAMPLE')
def foobar():
    print("FOOBAR")


foobar()


list_o_tuples = [
    (1,'Mario', 45),
    (2,'Luca', 45)
]

import operator

get_1 = operator.itemgetter(1,2)

# list.stream().-filter(pred).map(func)
# list.map(func)

print(list(map(get_1, filter(lambda i: i[0] % 2 == 0, list_o_tuples))))


import collections

def init_value():
    return 19

d_int = collections.defaultdict(init_value)

d_int['FOO'] = d_int['FOO'] + 2
print(d_int['OOO'])

mytuple = collections.namedtuple('MyTuple', 'id,name,age')

for t in map(lambda t: mytuple(*t), list_o_tuples):
    print(t.name)

print(type( mytuple))

#Controllare se la key è presente in d e d2 se non c'è in uno riportarla
#matrice[k][dict1val][dict2val]
d = {'a': {'3': 3}, 'c': {'d':{'e':2}}, 'arr': [{'a': 1}, {'a': 2}]}
d2 = {'a': {'3': 4}, 'c': {'d':{'e':2, 'f':'x'}}, 'arr': [{'a': 1}, {'a': 3}], 'l':'f'}
#
envs = ['DICT1', 'DICT2']
dicts = [d,d2]
