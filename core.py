import reader
from vector import Vector
from tokenhelp import Function


def prn(a):
    print(reader.pr_str(a))
    return None


def slurp(f):
    f = open(f, "r")
    return f.read()


def my_map(f, lst):
    rslt = []
    if isinstance(f, Function):
        f = f.get_fn()
    for i in lst:
        rslt.append(f(i))
    return rslt


def my_reduce(f, val, lst):
    if isinstance(f, Function):
        f = f.get_fn()
    for i in lst:
        val = f(i, val)
    return val


def my_hash_map(lst):
    rslt = {}
    if len(lst) % 2 != 0:
        raise Exception("Hash-map must be initialized with even number of elements")
    for k in range(0, len(lst), 2):
        key = lst[k]
        val = lst[k+1]
        rslt[key] = val
    return rslt


def my_sum(nums):
    x = 0
    for i in nums:
        x += i
    return x


def subtract(nums):
    x = nums[0]
    for i in nums[1:]:
        x -= i
    return x


def multiply(nums):
    x = 1
    for i in nums:
        x *= i
    return x


def divide(numbers):
    x = numbers[0]
    for i in numbers[1:]:
        x /= i
    return x


def my_filter(f, lst):
    rslt = []
    if isinstance(f, Function):
        f = f.get_fn()
    for i in lst:
        if f(i) is True:
            rslt.append(i)
    return rslt


def my_range(*args):
    rslt = []
    num_args = len(args)
    if num_args == 1:
        rslt = list(range(args[0]))
    elif num_args == 2:
        rslt = list(range(args[0], args[1]))
    elif num_args == 3:
        rslt = list(range(args[0], args[1], args[2]))
    return rslt


def my_concat(*lstlst):
    rslt = []
    for i in lstlst:
        if isinstance(i, Vector):
            rslt += i.getVal()
        else:
            rslt += i
    return rslt


ns = {
    '+': lambda *args: my_sum(args),
    '-': lambda *args: subtract(args),
    '*': lambda *args: multiply(args),
    '/': lambda *args: divide(args),
    '%': lambda a, b: a % b,
    'prn': prn,
    'str': lambda *x: ''.join(x),
    'list': lambda *x: list(x),
    'vector': lambda *x: Vector(list(x)),
    'vector?': lambda x: isinstance(x, Vector),
    'list?': lambda x: isinstance(x, list),
    'empty?': lambda x: len(x) == 0,
    'string?': lambda s: isinstance(s, str),
    'number?': lambda v: isinstance(v, (int, float)),
    'count': lambda x: len(x.getVal()) if isinstance(Vector, x) else len(x),
    '=': lambda a, b: a == b,
    '<': lambda a, b: a < b,
    '<=': lambda a, b: a <= b,
    '>': lambda a, b: a > b,
    '>=': lambda a, b: a >= b,
    'quit': lambda: exit(0),
    'read-string': lambda s: reader.read_str(s),
    'slurp': slurp,
    'map': my_map,
    'reduce': my_reduce,
    'nth': lambda lst, n: lst[n],
    'first': lambda lst: lst[0],
    'rest': lambda lst: lst[1:],
    'hash-map': my_hash_map,
    'filter': my_filter,
    'range': my_range,
    'cons': lambda x, lst: [x] + lst.getVal() if isinstance(lst, Vector) else [x] + lst,
    'concat': my_concat,
}

builtins = [
    '(defn not [a] (if a false true)))',
    '(defn inc [n] (+ n 1))',
    '(defn dec [n] (- n 1))',
    '(defn is-zero? [n] (= n 0))',
    '(defn load-file [f] (eval (read-string (str "(do " (slurp f) ")"))))"',
    '(defn true? [b] (= true b))',
    '(defn false? [b] (= false b))',
    '(defn nil? [v] (= nil v))',
    '(defn is-even? [n] (is-zero? (% n 2)))',
    '(defn is-odd? [n] (not (is-even? n)))',
    '(defn or [x y] (if x true (if y true false) (if y true false)))',
    '(defn and [x y] (if x (if y true false) false))'
]

