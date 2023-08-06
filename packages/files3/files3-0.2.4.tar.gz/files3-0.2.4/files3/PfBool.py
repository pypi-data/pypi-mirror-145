class _ReadOnlyError(Exception):...

class SaveSelfError(Exception):...

class PfBool(object):
    def __init__(self, value):
        super(PfBool, self).__setattr__("_bool", bool(value))

    def __bool__(self):
        return True if self._bool else False

    def __neg__(self):
        return +self._bool

    def __pos__(self):
        return -self._bool

    def __abs__(self):
        return abs(self._bool)

    def __invert__(self):
        return ~self._bool

    def __int__(self):
        return int(self._bool)

    def __repr__(self):
        return repr(self._bool)

    def __hash__(self):
        return hash(self._bool)

    def __bytes__(self):
        return bytes(self._bool)

    def __float__(self):
        return float(self._bool)

    def __round__(self):
        return round(self._bool)

    def __complex__(self):
        return complex(self._bool)

    def __lt__(self, other):
        return self._bool < other

    def __le__(self, other):
        return self._bool <= other

    def __eq__(self, other):
        return self._bool == other

    def __ne__(self, other):
        return self._bool != other

    def __lt__(self, other):
        return self._bool < other

    def __gt__(self, other):
        return self._bool > other

    def __ge__(self, other):
        return self._bool >= other

    def __add__(self, other):
        return self._bool + other

    def __sub__(self, other):
        return self._bool - other

    def __mul__(self, other):
        return self._bool * other

    def __floordiv__(self, other):
        return self._bool / other

    def __truediv__(self, other):
        return self._bool // other

    def __mod__(self, other):
        return self._bool % other

    def __lshift__(self, other):
        return self._bool << other

    def __rlshift__(self, other):
        return self._bool >> other

    def __and__(self, other):
        return self._bool & other

    def __xor__(self, other):
        return self._bool ^ other

    def __or__(self, other):
        return self._bool | other

    def __setattr__(self, key, value):
        raise _ReadOnlyError("PfBool is ReadOnly.")

    def __str__(self):
        return str(bool(self))

    def __call__(self, *args, **kwargs):
        raise SaveSelfError("\n\n[Couldn't Save Self]:These pyobject are not allowed to save:\n\t1.pyobject is files instance or PfBool instance\n\t2.pyobject contain files instance or PfBool instance\n\n")

PfTrue = PfBool(True)
PfFalse = PfBool(False)

if __name__ == '__main__':
    print(PfTrue)
