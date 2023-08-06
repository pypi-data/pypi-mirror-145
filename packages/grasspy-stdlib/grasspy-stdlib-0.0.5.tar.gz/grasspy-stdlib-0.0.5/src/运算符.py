"""
运算符接口 - operator.py

本模块提供一组对应于 Python 固有运算符的函数. 例如: 运算符.加法(x, y) 相当于
表达式 x+y.

许多函数名与特殊方法名相同, 只是没有双下划线. 为了向后兼容性, 也保留了许多包含双下划线的函数.
为了表述清楚, 建议使用没有双下划线的函数.
"""

from builtins import abs as _abs


# Comparison Operations *******************************************************#

def 小于(a, b):
    "同 a < b."
    return a < b

def 小等(a, b):
    "同 a <= b."
    return a <= b

def 相等(a, b):
    "同 a == b."
    return a == b

def 不等(a, b):
    "同 a != b."
    return a != b

def 大等(a, b):
    "同 a >= b."
    return a >= b

def 大于(a, b):
    "同 a > b."
    return a > b

# Logical Operations **********************************************************#

def 非_(a):
    "同 非 a."
    return not a

def 真_(a):
    "如果 a 为真则返回 真, 否则返回 假."
    return True if a else False

def 是_(a, b):
    "同 a 是 b."
    return a is b

def 不是_(a, b):
    "同 a 不是 b."
    return a is not b

# Mathematical/Bitwise Operations *********************************************#

def 绝对值(a):
    "同 abs(a)."
    return _abs(a)

def 加法(a, b):
    "同 a + b."
    return a + b

def 与运算(a, b):
    "同 a & b."
    return a & b

def 下整除(a, b): # floordiv
    "同 a // b."
    return a // b

def 索引(a):
    "同 a.__index__()."
    return a.__index__()

def 逆运算(a):
    "同 ~a."
    return ~a

# invert = inv

def 左移位(a, b): # lshift
    "同 a << b."
    return a << b

def 取模(a, b): # mod
    "同 a % b."
    return a % b

def 乘法(a, b):
    "同 a * b."
    return a * b

def 矩阵乘(a, b): # matmul
    "同 a @ b."
    return a @ b

def 负号(a):
    "同 -a."
    return -a

def 或运算(a, b):
    "同 a | b."
    return a | b

def 正号(a):
    "同 +a."
    return +a

def 乘方(a, b):
    "同 a ** b."
    return a ** b

def 右移位(a, b): # rshift
    "同 a >> b."
    return a >> b

def 减法(a, b):
    "同 a - b."
    return a - b

def 真除法(a, b): # truediv 
    "同 a / b."
    return a / b

def 异或(a, b):
    "同 a ^ b."
    return a ^ b

# Sequence Operations *********************************************************#

def 拼接(a, b): # concat
    "同 a + b, a 和 b 为序列."
    if not hasattr(a, '__getitem__'):
        msg = "'%s' 对象不支持连接" % type(a).__name__
        raise TypeError(msg)
    return a + b

def 在其中(a, b): # contains
    "同 b 在 a (注意顺序)."
    return b in a

def 计数(a, b): # countof
    "返回 a 中 b 出现的次数."
    count = 0
    for i in a:
        if i == b:
            count += 1
    return count

def 删元素(a, b): # delitem
    "同 del a[b]."
    del a[b]

def 取元素(a, b):
    "同 a[b]."
    return a[b]

def 定位(a, b): # indexOf
    "返回 a 中 b 的第一个索引."
    for i, j in enumerate(a):
        if j == b:
            return i
    else:
        raise ValueError('序列.索引(x): x 不在序列中')

def 设元素(a, b, c):
    "同 a[b] = c."
    a[b] = c

def 长度提示(对象_, 默认值=0):
    """
    返回 对象_ 中元素数目的估计值.
    这对于从可迭代对象构建容器时预估容器大小很有用.

    如果对象支持 '长()' 函数, 则结果为确切值, 否则可能偏离任意量. 结果为 >= 0 的整数.
    """
    if not isinstance(默认值, int):
        msg = ("'%s' 对象无法被解读为整数" %
               type(默认值).__name__)
        raise TypeError(msg)

    try:
        return len(对象_)
    except TypeError:
        pass

    try:
        hint = type(对象_).__length_hint__
    except AttributeError:
        return 默认值

    try:
        val = hint(对象_)
    except TypeError:
        return 默认值
    if val is NotImplemented:
        return 默认值
    if not isinstance(val, int):
        msg = ('__长度提示__ 须为整数, 不能是 %s' %
               type(val).__name__)
        raise TypeError(msg)
    if val < 0:
        msg = '__长度提示__() 应返回 >= 0'
        raise ValueError(msg)
    return val

# Generalized Lookup Objects **************************************************#

class 〇属性获取器:
    """
    返回一个可从操作数中获取 属性_ 的可调用对象. 
    如果请求了一个以上的属性, 则返回一个属性元组. 
    属性名称还可包含点号. 例如:

    在 f = 〇属性获取器('姓名') 之后, 调用 f(r) 将返回 r.姓名
    
    在 g = 〇属性获取器('姓名', '日期') 之后, 调用 g(r) 将返回 (r.姓名, r.日期)

    在 h = 〇属性获取器('姓名.姓氏', '姓名.名字') 之后, 调用 h(r) 将返回 (r.姓名.姓氏, r.姓名.名字)
    """
    __slots__ = ('_attrs', '_call')

    def __init__(self, 属性_, *属性元组):
        if not 属性元组:
            if not isinstance(属性_, str):
                raise TypeError('属性名称须为字符串')
            self._attrs = (属性_,)
            names = 属性_.split('.')
            def func(obj):
                for name in names:
                    obj = getattr(obj, name)
                return obj
            self._call = func
        else:
            self._attrs = (属性_,) + 属性元组
            getters = tuple(map(〇属性获取器, self._attrs))
            def func(obj):
                return tuple(getter(obj) for getter in getters)
            self._call = func

    def __call__(self, obj):
        return self._call(obj)

    def __repr__(self):
        return '%s.%s(%s)' % (self.__class__.__module__,
                              self.__class__.__qualname__,
                              ', '.join(map(repr, self._attrs)))

    def __reduce__(self):
        return self.__class__, self._attrs

class 〇元素获取器:
    """
    返回一个使用操作数的 __取元素__() 方法从操作数中获取 元素 的可调用对象.

    在 f = 〇元素获取器(2) 之后, 调用 f(r) 将返回 r[2]

    在 g = 〇元素获取器(2, 5, 3) 之后, 调用 g(r) 将返回 (r[2], r[5], r[3])
    """
    __slots__ = ('_items', '_call')

    def __init__(self, 元素, *元素元组):
        if not 元素元组:
            self._items = (元素,)
            def func(obj):
                return obj[元素]
            self._call = func
        else:
            self._items = 元素元组 = (元素,) + 元素元组
            def func(obj):
                return tuple(obj[i] for i in 元素元组)
            self._call = func

    def __call__(self, obj):
        return self._call(obj)

    def __repr__(self):
        return '%s.%s(%s)' % (self.__class__.__module__,
                              self.__class__.__name__,
                              ', '.join(map(repr, self._items)))

    def __reduce__(self):
        return self.__class__, self._items

class 〇方法调用器:
    """
    返回一个在操作数上调用 名称 方法的可调用对象.

    在 f = 〇方法调用器('名称') 之后, 调用 f(r) 将返回 r.名称()

    在 g = 〇方法调用器('名称', '日期', 级别=1), 调用 g(r) 将返回 r.名称('日期', 级别=1)
    """
    __slots__ = ('_name', '_args', '_kwargs')

    def __init__(self, 名称, /, *参数, **关键词参数):
        self._name = 名称
        if not isinstance(self._name, str):
            raise TypeError('方法名称须为字符串')
        self._args = 参数
        self._kwargs = 关键词参数

    def __call__(self, obj):
        return getattr(obj, self._name)(*self._args, **self._kwargs)

    def __repr__(self):
        args = [repr(self._name)]
        args.extend(map(repr, self._args))
        args.extend('%s=%r' % (k, v) for k, v in self._kwargs.items())
        return '%s.%s(%s)' % (self.__class__.__module__,
                              self.__class__.__name__,
                              ', '.join(args))

    def __reduce__(self):
        if not self._kwargs:
            return self.__class__, (self._name,) + self._args
        else:
            from functools import partial
            return partial(self.__class__, self._name, **self._kwargs), self._args


# In-place Operations *********************************************************#

def 自加(a, b):
    "同 a += b."
    a += b
    return a

def 自与(a, b):
    "同 a &= b."
    a &= b
    return a

def 自连接(a, b):
    "同 a += b, a 和 b 为序列."
    if not hasattr(a, '__getitem__'):
        msg = "'%s' 对象不支持连接" % type(a).__name__
        raise TypeError(msg)
    a += b
    return a

def 自下整除(a, b):
    "同 a //= b."
    a //= b
    return a

def 自左移位(a, b):
    "同 a <<= b."
    a <<= b
    return a

def 自模(a, b):
    "同 a %= b."
    a %= b
    return a

def 自乘(a, b):
    "同 a *= b."
    a *= b
    return a

def 自矩阵乘(a, b):
    "同 a @= b."
    a @= b
    return a

def 自或(a, b):
    "同 a |= b."
    a |= b
    return a

def 自乘方(a, b):
    "同 a **= b."
    a **=b
    return a

def 自右移位(a, b):
    "同 a >>= b."
    a >>= b
    return a

def 自减(a, b):
    "同 a -= b."
    a -= b
    return a

def 自真除(a, b):
    "同 a /= b."
    a /= b
    return a

def 自异或(a, b):
    "同 a ^= b."
    a ^= b
    return a
