import reader
import vector


def prn(a):
    print(reader.pr_str(a))
    return None


def slurp(f):
    f = open(f, "r")
    return f.read()


def my_map(f, l):
    rslt = []
    if isinstance(l, vector.Vector):
        lst = l.getVal()
    else:
        lst = l
    for i in lst:
        rslt.append(f(i))
    return rslt


def my_nth(l, i):
    if isinstance(l, vector.Vector):
        lst = l.getVal()
    else:
        lst = l
    return lst[i]


def my_first(l):
    if isinstance(l, vector.Vector):
        lst = l.getVal()
    else:
        lst = l
    return lst[0]


def my_rest(l):
    if isinstance(l, vector.Vector):
        lst = l.getVal()
    else:
        lst = l
    return lst[1:]


def my_hash_map(l):
    rslt = {}
    if isinstance(l, vector.Vector):
        lst = l.getVal()
    else:
        lst = l
    if len(lst) % 2 != 0:
        raise Exception("Hash-map must be initialized with even number of elements")
    for k in range(0, len(lst), 2):
        key = lst[k]
        val = lst[k+1]
        rslt[key] = val
    return rslt


def sum(nums):
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

def divide(nums):
    x = nums[0]
    for i in nums[1:]:
        x /= i
    return x

ns = {
    '+': lambda *args: sum(args),
    '-': lambda *args: subtract(args),
    '*': lambda *args: multiply(args),
    '/': lambda *args: divide(args),
    'prn': prn,
    'str': lambda *x: ''.join(x),
    'list': lambda *x: list(x),
    'vector': lambda *x: vector.Vector(list(x)),
    'vector?': lambda x: isinstance(x, vector.Vector),
    'list?': lambda x: isinstance(x, list),
    'empty?': lambda x: len(x) == 0,
    'string?': lambda s: isinstance(s, str),
    'number?': lambda v: isinstance(v, (int, float)),
    'count': lambda x: len(x),
    '=': lambda a, b: a == b,
    '<': lambda a, b: a < b,
    '<=': lambda a, b: a <= b,
    '>': lambda a, b: a > b,
    '>=': lambda a, b: a >= b,
    'quit': lambda: exit(0),
    'read-string': lambda s: reader.read_str(s),
    'slurp': slurp,
    'map': my_map,
    'nth': my_nth,
    'first': my_first,
    'rest': my_rest,
    'hash-map': my_hash_map
}

builtins = [
    '(defn not [a] (if a false true)))',
    '(defn inc [n] (+ n 1))',
    '(defn dec [n] (- n 1))',
    '(defn is-zero? [n] (= n 0))',
    '(defn load-file [f] (eval (read-string (str "(do " (slurp f) ")"))))"',
    '(defn true? [b] (= true b))',
    '(defn false? [b] (= false b))',
    '(defn nil? [v] (= nil v))'
]

