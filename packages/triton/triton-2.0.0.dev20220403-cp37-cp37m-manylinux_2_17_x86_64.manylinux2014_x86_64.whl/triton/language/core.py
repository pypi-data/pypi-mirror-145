from functools import wraps

import triton
from triton._C.libtriton.triton import frontend, ir


# convert block/dtype to ir values
def _to_ir(x, builder):
    if isinstance(x, bool):
        return builder.get_int1(x)
    elif isinstance(x, int):
        if -2**31 <= x < 2**31:
            return builder.get_int32(x)
        elif 2**31 <= x < 2**32:
            return builder.get_uint32(x)
        elif -2**63 <= x < 2**63:
            return builder.get_int64(x)
        elif 2**63 <= x < 2**64:
            return builder.get_uint64(x)
        else:
            raise RuntimeError(f'Nonrepresentable integer {x}.')
    elif isinstance(x, float):
        return builder.get_float32(x)
    elif isinstance(x, constexpr):
        return _to_ir(x.value, builder)
    elif isinstance(x, block):
        return x.handle
    elif isinstance(x, dtype):
        return x.handle(builder)
    return x


def _patch(fn):
    def _from_ir(x):
        if isinstance(x, ir.value):
            if x.type.is_void():
                return None
            return block(x)
        return x

    def wrapper(*args, **kwargs):
        builder = args[-1]
        assert isinstance(builder, ir.builder)
        args = [_to_ir(x, builder) for x in args]
        # for i, arg in enumerate(args):
        #     if arg is None:
        #         raise ValueError(f"Unexpected `None` at position {i} for function {fn.__name__}")
        kwargs = {k: _to_ir(v, builder) for k, v in kwargs.items()}
        ret = fn(*args, **kwargs)
        if isinstance(ret, tuple):
            return map(_from_ir, ret)
        return _from_ir(ret)

    return wrapper


for name in dir(frontend):
    fn = getattr(frontend, name)
    if callable(fn):
        setattr(frontend, name, _patch(fn))


def builtin(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        if '_builder' not in kwargs or \
           kwargs['_builder'] is None:
            raise ValueError("Did you forget to add @triton.jit ? (`_builder` argument must be provided outside of JIT functions.)")
        return fn(*args, **kwargs)

    return wrapper


class dtype:
    def __init__(self, init):
        self.init = init

    @property
    def name(self) -> str:
        # The init functions are named something like 'get_int8'. Strip the prefix.
        nom = self.init.__name__
        prefix = 'get_'
        assert nom.startswith(prefix)
        return nom[len(prefix):]

    def handle(self, builder):
        ctx = builder.context
        return self.init(ctx)

    def __str__(self):
        return self.name

    @property
    def cache_key_part(self) -> str:
        """See cache_key_part() in triton.cc."""
        return self.name

    def __repr__(self):
        return f'triton.language.{self.name}'


class pointer_dtype:
    def __init__(self, element_ty):
        if not isinstance(element_ty, dtype):
            raise TypeError('element_ty is a {type(element_ty).__name__}.')
        self.element_ty = element_ty

    def handle(self, builder):
        return ir.type.make_ptr(self.element_ty.handle(builder), 1)

    def __str__(self):
        return f'pointer<{self.element_ty}>'


# scalar types
int1 = dtype(ir.type.get_int1)
int8 = dtype(ir.type.get_int8)
int16 = dtype(ir.type.get_int16)
int32 = dtype(ir.type.get_int32)
int64 = dtype(ir.type.get_int64)
uint8 = dtype(ir.type.get_uint8)
uint16 = dtype(ir.type.get_uint16)
uint32 = dtype(ir.type.get_uint32)
uint64 = dtype(ir.type.get_uint64)
float8 = dtype(ir.type.get_fp8)
float16 = dtype(ir.type.get_fp16)
bfloat16 = dtype(ir.type.get_bf16)
float32 = dtype(ir.type.get_fp32)
float64 = dtype(ir.type.get_fp64)
# pointer types
pi32_t = pointer_dtype(int32)

# -----------------------
# constexpr
# -----------------------


class constexpr:
    """
    This class is used to store a value that is known at compile-time.
    """

    def __init__(self, value):
        if isinstance(value, constexpr):
            self.value = value.value
        else:
            self.value = value

    def __repr__(self) -> str:
        return f"constexpr[{self.value}]"

    #
    def __add__(self, other):
        return self.value + other.value

    def __radd__(self, other):
        return other.value + self.value

    def __sub__(self, other):
        return self.value - other.value

    def __rsub__(self, other):
        return other.value - self.value

    def __mul__(self, other):
        return self.value * other.value

    def __rmul__(self, other):
        return other.value * self.value

    def __truediv__(self, other):
        return self.value / other.value

    def __rtruediv__(self, other):
        return other.value / self.value

    def __floordiv__(self, other):
        return self.value // other.value

    def __rfloordiv__(self, other):
        return other.value // self.value

    #

    def __gt__(self, other):
        return self.value > other.value

    def __rgt__(self, other):
        return other.value > self.value

    def __ge__(self, other):
        return self.value >= other.value

    def __rge__(self, other):
        return other.value >= self.value

    def __lt__(self, other):
        return self.value < other.value

    def __rlt__(self, other):
        return other.value < self.value

    def __le__(self, other):
        return self.value <= other.value

    def __rle__(self, other):
        return other.value <= self.value

    def __eq__(self, other):
        return self.value == other.value

    def __ne__(self, other):
        return self.value != other.value

    def __bool__(self):
        return bool(self.value)

    def __call__(self, *args, **kwds):
        return self.value(*args, **kwds)


class block:
    @staticmethod
    def _init_dtype(ir_type):
        # primitive type
        if ir_type.is_int1(): return int1
        if ir_type.is_int8(): return int8
        if ir_type.is_int16(): return int16
        if ir_type.is_int32(): return int32
        if ir_type.is_int64(): return int64
        if ir_type.is_uint8(): return uint8
        if ir_type.is_uint16(): return uint16
        if ir_type.is_uint32(): return uint32
        if ir_type.is_uint64(): return uint64
        if ir_type.is_fp8(): return float8
        if ir_type.is_fp16(): return float16
        if ir_type.is_bf16(): return bfloat16
        if ir_type.is_fp32(): return float32
        if ir_type.is_fp64(): return float64
        # pointer type
        if ir_type.is_ptr():
            element_ty = block._init_dtype(ir_type.element)
            return pointer_dtype(element_ty)
        raise ValueError(f"Unsupported type {ir_type}")

    def __init__(self, handle):
        # IR handle
        self.handle = handle
        # Block shape
        self.shape = (1, )
        if self.handle.type.is_block():
            self.shape = self.handle.type.shape
        self.numel = 1
        for s in self.shape:
            self.numel *= s
        self.numel = constexpr(self.numel)
        # Data-type wrapper
        self.dtype = block._init_dtype(self.handle.type.scalar)
        # Shape is a constexpr
        self.shape = [constexpr(s) for s in self.shape]

    def __str__(self) -> str:
        # ex. "float32[3,4]"
        return str(self.dtype) + '[' + ','.join(str(s) for s in self.shape) + ']'

    @builtin
    def __add__(self, other, _builder=None):
        return frontend.add(self, other, _builder)

    def __radd__(self, other, _builder=None):
        return self.__add__(other, _builder=_builder)

    @builtin
    def __sub__(self, other, _builder=None):
        return frontend.sub(self, other, _builder)

    def __rsub__(self, other, _builder=None):
        return frontend.sub(other, self, _builder)

    @builtin
    def __mul__(self, other, _builder=None):
        return frontend.mul(self, other, _builder)

    def __rmul__(self, other, _builder=None):
        return self.__mul__(other, _builder=_builder)

    @builtin
    def __truediv__(self, other, _builder=None):
        return frontend.truediv(self, other, _builder)

    def __rtruediv__(self, other, _builder=None):
        return frontend.truediv(other, self, _builder)

    @builtin
    def __floordiv__(self, other, _builder=None):
        return frontend.floordiv(self, other, _builder)

    @builtin
    def __mod__(self, other, _builder=None):
        return frontend.mod(self, other, _builder)

    # unary operators
    @builtin
    def __neg__(self, _builder=None):
        return frontend.minus(self, _builder)

    @builtin
    def __invert__(self, _builder=None):
        return frontend.invert(self, _builder)

    # bitwise operators

    @builtin
    def __and__(self, other, _builder=None):
        return frontend.and_(self, other, _builder)

    @builtin
    def __or__(self, other, _builder=None):
        return frontend.or_(self, other, _builder)

    @builtin
    def __xor__(self, other, _builder=None):
        return frontend.xor_(self, other, _builder)

    @builtin
    def __lshift__(self, other, _builder=None):
        return frontend.shl(self, other, _builder)

    @builtin
    def __rshift__(self, other, _builder=None):
        return frontend.lshr(self, other, _builder)

    # comparison operators

    # >
    @builtin
    def __gt__(self, other, _builder=None):
        return frontend.greater_than(self, other, _builder)

    @builtin
    def __rgt__(self, other, _builder=None):
        return frontend.greater_than(other, self, _builder)

    # >=
    @builtin
    def __ge__(self, other, _builder=None):
        return frontend.greater_equal(self, other, _builder)

    def __rge__(self, other, _builder=None):
        return frontend.greater_equal(other, self, _builder)

    # <
    @builtin
    def __lt__(self, other, _builder=None):
        return frontend.less_than(self, other, _builder)

    @builtin
    def __rlt__(self, other, _builder=None):
        return frontend.less_than(other, self, _builder)

    # <=
    @builtin
    def __le__(self, other, _builder=None):
        return frontend.less_equal(self, other, _builder)

    @builtin
    def __rle__(self, other, _builder=None):
        return frontend.less_equal(other, self, _builder)

    # ==
    @builtin
    def __eq__(self, other, _builder=None):
        return frontend.equal(self, other, _builder)

    @builtin
    def __ne__(self, other, _builder=None):
        return frontend.not_equal(self, other, _builder)

    @builtin
    def __getitem__(self, slices, _builder=None):
        if isinstance(slices, slice):
            slices = [slices]
        src_shape = self.shape
        dst_shape = []
        curr = 0
        for sl in slices:
            if isinstance(sl, constexpr) and sl.value is None:
                dst_shape.append(1)
            elif sl == slice(None, None, None):
                dst_shape.append(src_shape[curr].value)
                curr += 1
        ret = frontend.reshape(self, dst_shape, _builder)
        return ret

    @builtin
    def to(self, dtype, bitcast=False, _builder=None):
        dtype = dtype.handle(_builder)
        if bitcast:
            return frontend.bitcast(self, dtype, _builder)
        return frontend.cast(self, dtype, _builder)


# -----------------------
# SPMD Programming Model
# -----------------------


@builtin
def program_id(axis, _builder=None):
    """
    Returns the id of the current program instance along the given :code:`axis`.

    :param axis: The axis of the 3D launch grid. Has to be either 0, 1 or 2.
    :type axis: int
    """
    # if axis == -1:
    #     pid0 = frontend.program_id(0, _builder)
    #     pid1 = frontend.program_id(1, _builder)
    #     pid2 = frontend.program_id(2, _builder)
    #     npg0 = frontend.num_programs(0, _builder)
    #     npg1 = frontend.num_programs(0, _builder)
    #     return pid0 + pid1*npg0 + pid2*npg0*npg1
    return frontend.program_id(axis, _builder)


@builtin
def num_programs(axis, _builder=None):
    """
    Returns the number of program instances launched along the given :code:`axis`.

    :param axis: The axis of the 3D launch grid. Has to be either 0, 1 or 2.
    :type axis: int
    """
    return frontend.num_programs(axis, _builder)


# -----------------------
# Block Initialization
# -----------------------


@builtin
def arange(start, end, _builder=None):
    """
    Returns contiguous values within the open interval [:code:`start`, :code:`end`).

    :param start: Start of the interval. Must be a power of two.
    :type start: int
    :param stop: End of the interval. Must be a power of two >= start.
    :type stop: int
    """
    return frontend.arange(start, end, _builder)


@builtin
def zeros(shape, dtype, _builder=None):
    """
    Returns a block filled with the scalar value 0 for the given :code:`shape` and :code:`dtype`.

    :param shape: Shape of the new array, e.g., (8, 16) or (8, )
    :type shape: tuple of ints
    :param dtype: Data-type of the new array, e.g., :code:`tl.float16`
    :type dtype: DType
    """
    for i, d in enumerate(shape):
        if not isinstance(d, constexpr):
            raise TypeError(f"Shape element {i} must have type `constexpr`")
        if not isinstance(d.value, int):
            raise TypeError(f"Shape element {i} must have type `constexpr[int]`, got `constexpr[{type(d.value)}]")
    shape = [x.value for x in shape]
    return frontend.zeros(shape, dtype, _builder)


# -----------------------
# Shape Manipulation
# -----------------------


@builtin
def broadcast(input, other, _builder=None):
    """
    Tries to broadcast the two given blocks to a common compatible shape.

    :param input: The first input block.
    :type input: Block
    :param other: The second input block.
    :type other: Block
    """
    return frontend.broadcast(input, other, _builder)


@builtin
def broadcast_to(input, shape, _builder=None):
    """
    Tries to broadcast the given block to a new :code:`shape`.

    :param input: The input block.
    :type input: Block
    :param shape: The desired shape.
    :type shape: Tuple[int]
    """
    return frontend.broadcast_to(input, shape, _builder)


@builtin
def cat(input, other, _builder=None):
    """
    Concatenate the given blocks

    :param input: The first input block.
    :type input:
    :param other: The second input block.
    :type other:
    """
    return frontend.cat(input, other, _builder)


@builtin
def reshape(input, shape, _builder=None):
    """
    Tries to reshape the given block to a new shape.

    :param input: The input block.
    :type input:
    :param shape: The desired shape.
    :type shape: Tuple[int]

    """
    shape = [x.value for x in shape]
    return frontend.reshape(input, shape, _builder)


# -----------------------
# Linear Algebra
# -----------------------


@builtin
def dot(input, other, allow_tf32=True, _builder=None):
    """
    Returns the matrix product of two blocks.

    The two blocks must be two dimensionals and have compatible inner dimensions.

    :param input: The first block to be multiplied.
    :type input: 2D block of scalar-type in {:code:`float16`, :code:`bfloat16`, :code:`float32`}
    :param other: The second block to be multiplied.
    :type other: 2D block of scalar-type in {:code:`float16`, :code:`bfloat16`, :code:`float32`}
    """
    return frontend.dot(input, other, allow_tf32, _builder)


# -----------------------
# Non-Atomic Memory Operations
# -----------------------


@builtin
def load(pointer, mask=None, other=None, cache_modifier="", eviction_policy="", volatile=False, _builder=None):
    """
    Return a block of data whose values are, elementwise, loaded from memory at location defined by :code:`pointer`.

    :code:`mask` and :code:`other` are implicitly broadcast to :code:`pointer.shape`.

    :code:`other` is implicitly typecast to :code:`pointer.dtype.element_ty`.

    :param pointer: Pointers to the data to be loaded.
    :type pointer: Block of dtype=triton.PointerDType
    :param mask: if mask[idx] is false, do not load the data at address :code:`pointer[idx]`.
    :type mask: Block of triton.int1, optional
    :param other: if mask[idx] is false, return other[idx]
    :type other: Block, optional
    :param cache_modifier: changes cache option in nvidia ptx
    'type cache_modifier: str, optional
    """
    return frontend.load(pointer, mask, other, cache_modifier, eviction_policy, volatile, _builder)


@builtin
def store(pointer, value, mask=None, _builder=None):
    """
    Stores :code:`value` block of elements in memory, element-wise, at the memory locations specified by :code:`pointer`.

    :code:`value` is implicitly broadcast to :code:`pointer.shape` and typecast to :code:`pointer.dtype.element_ty`.

    :param pointer: The memory locations where the elements of :code:`value` are stored.
    :type pointer: Block of dtype=triton.PointerDType
    :param value: The block of elements to be stored.
    :type value: Block
    :param mask: If mask[idx] is false, do not store :code:`value[idx]` at :code:`pointer[idx]`.
    :type mask: Block of triton.int1, optional
    """
    return frontend.store(pointer, value, mask, _builder)


# -----------------------
# Atomic Memory Operations
# -----------------------

def _add_atomic_docstr(name):

    def _decorator(func):
        docstr = """
    Performs an atomic {name} at the memory location specified by :code:`pointer`.

    Return the data stored at :code:`pointer` before the atomic operation.

    :param pointer: The memory locations to compare-and-swap.
    :type pointer: Block of dtype=triton.PointerDType
    :param cmp: The values expected to be found in the atomic object
    :type cmp: Block of dtype=`pointer.dtype.element_ty`
    :param val: The values to copy in case the expected value matches the contained value.
    :type val: Block of dtype=`pointer.dtype.element_ty`
    """
        func.__doc__ = docstr.format(name=name)
        return func

    return _decorator


@builtin
@_add_atomic_docstr("compare-and-swap")
def atomic_cas(pointer, cmp, val, _builder=None):
    return frontend.atomic_cas(pointer, cmp, val, _builder)


@builtin
@_add_atomic_docstr("exchange")
def atomic_xchg(pointer, val, mask=None, _builder=None):
    return frontend.atomic_xchg(pointer, val, mask, _builder)


@builtin
@_add_atomic_docstr("add")
def atomic_add(pointer, val, mask=None, _builder=None):
    return frontend.atomic_add(pointer, val, mask, _builder)


@builtin
@_add_atomic_docstr("max")
def atomic_max(pointer, val, mask=None, _builder=None):
    return frontend.atomic_max(pointer, val, mask, _builder)


@builtin
@_add_atomic_docstr("min")
def atomic_min(pointer, val, mask=None, _builder=None):
    return frontend.atomic_min(pointer, val, mask, _builder)


@builtin
@_add_atomic_docstr("logical and")
def atomic_and(pointer, val, mask=None, _builder=None):
    return frontend.atomic_and(pointer, val, mask, _builder)


@builtin
@_add_atomic_docstr("logical or")
def atomic_or(pointer, val, mask=None, _builder=None):
    return frontend.atomic_or(pointer, val, mask, _builder)


@builtin
@_add_atomic_docstr("logical xor")
def atomic_xor(pointer, val, mask=None, _builder=None):
    return frontend.atomic_xor(pointer, val, mask, _builder)


# -----------------------
# Conditioning
# -----------------------


@builtin
def where(condition, x, y, _builder=None):
    """
    Returns a block of elements from either :code:`x` or :code:`y`, depending on :code:`condition`.

    Note that :code:`x` and :code:`y` are always evaluated regardless of the value of :code:`condition`.

    If you want to avoid unintented memory operations, use the :code:`mask` arguments in `triton.load` and `triton.store` instead.

    The shape of :code:`x` and :code:`y` are both broadcast to the shape of :code:`condition`.
    :code:`x` and :code:`y` must have the data type.

    :param condition: When True (nonzero), yield x, otherwise yield y.
    :type condition: Block of triton.bool
    :param x: values selected at indices where condition is True.
    :param y: values selected at indices where condition is False.
    """
    return frontend.where(condition, x, y, _builder)


# -----------------------
# Math
# -----------------------

@builtin
def umulhi(x, y, _builder=None):
    return frontend.umulhi(x, y, _builder)


@builtin
def fdiv(x, y, ieee_rounding=False, _builder=None):
    return frontend.fdiv(x, y, ieee_rounding, _builder)


def _add_math_1arg_docstr(name):

    def _decorator(func):
        docstr = """
    Computes the element-wise {name} of :code:`x`

    :param x: the input values
    :type x: Block
    """
        func.__doc__ = docstr.format(name=name)
        return func

    return _decorator


@builtin
@_add_math_1arg_docstr("exponential")
def exp(x, _builder=None):
    return frontend.exp(x, _builder)


@builtin
@_add_math_1arg_docstr("natural logarithm")
def log(x, _builder=None):
    return frontend.log(x, _builder)


@builtin
@_add_math_1arg_docstr("cosine")
def cos(x, _builder=None):
    return frontend.cos(x, _builder)


@builtin
@_add_math_1arg_docstr("sine")
def sin(x, _builder=None):
    return frontend.sin(x, _builder)


@builtin
@_add_math_1arg_docstr("square root")
def sqrt(x, _builder=None):
    return frontend.sqrt(x, _builder)


# -----------------------
# Reductions
# -----------------------

def _add_reduction_docstr(name):

    def _decorator(func):
        docstr = """
    Returns the {name} of all elements in the :code:`input` block along the provided :code:`axis`

    :param input: the input values
    :param axis: the dimension along which the reduction should be done
    """
        func.__doc__ = docstr.format(name=name)
        return func

    return _decorator


@builtin
@_add_reduction_docstr("maximum")
def max(input, axis, _builder=None):
    return frontend.max(input, axis, _builder)


@builtin
@_add_reduction_docstr("minimum")
def min(input, axis, _builder=None):
    return frontend.min(input, axis, _builder)


@builtin
@_add_reduction_docstr("sum")
def sum(input, axis, _builder=None):
    return frontend.sum(input, axis, _builder)


@builtin
@_add_reduction_docstr("xor sum")
def xor_sum(input, axis, _builder=None):
    return frontend.xor_sum(input, axis, _builder)

# -----------------------
# Utilities
# -----------------------


@builtin
def globaltimer(_builder=None):
    return frontend.globaltimer(_builder)


@builtin
def clock(_builder=None):
    return frontend.clock(_builder)

# -----------------------
# Internal for debugging
# -----------------------


@builtin
def debug_barrier(_builder=None):
    return frontend.debug_barrier(_builder)


@builtin
def multiple_of(input, value, _builder=None):
    """
    Let the compiler knows that the values in :code:`input` are all multiples of :code:`value`.
    """
    return frontend.multiple_of(input, value, _builder)


@builtin
def max_contiguous(input, value, _builder=None):
    """
    Let the compiler knows that the `value` first values in :code:`input` are contiguous.
    """
    return frontend.max_contiguous(input, value, _builder)


# -----------------------
# Standard library
# -----------------------

@triton.jit
def abs(x):
    return where(x >= 0, x, -x)


@triton.jit
def cdiv(x, div):
    """
    Computes the ceiling division of :code:`x` by :code:`div`

    :param x: the input number
    :type input: Block
    :param div: the divisor
    :param div: Block
    """
    return (x + div - 1) // div


@triton.jit
def minimum(x, y):
    """
    Computes the element-wise minimum of :code:`x` and :code:`y`.

    :param input: the first input block
    :type input: Block
    :param other: the second input block
    :type other: Block
    """
    return triton.language.where(x < y, x, y)


@triton.jit
def maximum(x, y):
    """
    Computes the element-wise maximum of :code:`x` and :code:`y`.

    :param input: the first input block
    :type input: Block
    :param other: the second input block
    :type other: Block
    """
    return triton.language.where(x > y, x, y)


@triton.jit
@_add_math_1arg_docstr("sigmoid")
def sigmoid(x):
    return 1 / (1 + triton.language.exp(-x))


@triton.jit
@_add_math_1arg_docstr("softmax")
def softmax(x, ieee_rounding: constexpr = False):
    z = x - triton.language.max(x, 0)
    num = triton.language.exp(z)
    den = triton.language.sum(num, 0)
    return fdiv(num, den, ieee_rounding)


@triton.jit
def ravel(x):
    """
    Returns a contiguous flattened view of :code:`x`

    :param x: the input block
    :type x: Block
    """
    return triton.language.reshape(x, [x.numel])


@triton.jit
def swizzle2d(i, j, size_i, size_j, size_g):
    """
    transformes indices of a row-major size_i*size_j matrix into those
    of one where indices are row major for each group of size_j rows.
    For example, for size_i = size_j = 4 and size_g = 2, it will transform
    [[0 , 1 , 2 , 3 ],
     [4 , 5 , 6 , 7 ],
     [8 , 9 , 10, 11],
     [12, 13, 14, 15]]
    into
    [[0, 2,  4 , 6 ],
     [1, 3,  5 , 7 ],
     [8, 10, 12, 14],
     [9, 11, 13, 15]]
    """
    # "unrolled index in array"
    ij = i * size_j + j
    # number of elements in `size_g` groups
    # of `size_j` columns
    size_gj = size_g * size_j
    # index of the group in which (i,j) is
    group_id = ij // size_gj
    # row-index of the first element of this group
    off_i = group_id * size_g
    # last group may have fewer rows
    size_g = minimum(size_i - off_i, size_g)
    # new row and column indices
    new_i = off_i + (ij % size_g)
    new_j = (ij % size_gj) // size_g
    return new_i, new_j


@triton.jit
def zeros_like(input):
    return zeros(input.shape, input.dtype)
# -----------------------
# Dynamic Parallelism
# -----------------------


class LaunchProxy:

    def __init__(self, fn, args, constants, grid, num_warps) -> None:
        self.args = args
        self.grid = grid
        self.constants = constants
        self.num_warps = num_warps
        self.fn = fn


@builtin
def launch(fn, args, grid, num_warps=None, _builder=None):
    constants = {i: x for i, x in enumerate(args) if isinstance(x, constexpr)}
    args = [_to_ir(x, builder=_builder) for x in args if not isinstance(x, constexpr)]
    grid = [_to_ir(x, builder=_builder) for x in grid]
    if num_warps is None:
        num_warps = _to_ir(4, builder=_builder)
    return LaunchProxy(fn, args, constants, grid, num_warps)
