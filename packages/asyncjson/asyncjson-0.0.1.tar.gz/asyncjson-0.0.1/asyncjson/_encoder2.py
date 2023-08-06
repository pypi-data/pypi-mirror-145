__all__ = ['encode']
import inspect
import re
import types
from typing import AsyncGenerator, Any, Tuple

SENTINEL = object()
INFINITY = float('inf')
ESCAPE = re.compile(r'[\x00-\x1f\\"\b\f\n\r\t]')
ESCAPE_DCT = {
    '\\': '\\\\',
    '"': '\\"',
    '\b': '\\b',
    '\f': '\\f',
    '\n': '\\n',
    '\r': '\\r',
    '\t': '\\t',
}
for i in range(0x20):
    ESCAPE_DCT.setdefault(chr(i), '\\u{0:04x}'.format(i))


def floatstr(o, allow_nan=True,
             _repr=float.__repr__, _inf=INFINITY, _neginf=-INFINITY):
    # Check for specials.  Note that this type of test is processor
    # and/or platform-specific, so do tests which don't depend on the
    # internals.

    if o != o:
        text = 'NaN'
    elif o == _inf:
        text = 'Infinity'
    elif o == _neginf:
        text = '-Infinity'
    else:
        return _repr(o)

    if not allow_nan:
        raise ValueError(
            "Out of range float values are not JSON compliant: " +
            repr(o))

    return text


def py_encode_basestring(s):
    """Return a JSON representation of a Python string

    """
    def replace(match):
        return ESCAPE_DCT[match.group(0)]
    return '"' + ESCAPE.sub(replace, s) + '"'


async def encode(obj: Any, pretty: bool = False):
    stack = []
    enc = encoder()
    await enc.asend(None)

    ittyp, obj = await enc.asend(obj)
    it = None
    if ittyp == 'list' or ittyp == 'gen':
        yield '['
        it = iter(obj)
    elif ittyp == 'agen':
        yield '['
        it = obj.__aiter__()
    elif ittyp == 'dict':
        yield '{'
        it = iter(obj.items())
    elif ittyp == 'str':
        yield obj
        await close_encoder(enc)
        return

    if pretty:
        yield '\n'
    stack.append((ittyp, it))
    begun = False
    while stack:
        if ittyp == 'list' or ittyp == 'gen' or ittyp == 'agen':
            while True:
                try:
                    value = await it.__anext__() if ittyp == 'agen' else next(it)
                    if begun:
                        yield ','
                    if pretty:
                        yield '\n'
                    begun = True
                except (StopIteration, StopAsyncIteration):
                    stack.pop()
                    if pretty and begun:
                        yield '\n' + '    ' * len(stack)
                    yield ']'
                    if stack:
                        ittyp, it = stack[-1]
                    begun = True
                    break

                vtyp, vobj = await enc.asend(value)
                if pretty:
                    yield '    ' * len(stack)

                if vtyp != 'str':
                    ittyp, obj = vtyp, vobj
                    if ittyp == 'list' or ittyp == 'gen':
                        yield '['
                        it = iter(obj)
                    elif ittyp == 'agen':
                        yield '['
                        it = obj.__aiter__()
                    elif ittyp == 'dict':
                        yield '{'
                        it = iter(obj.items())
                    stack.append((ittyp, it))
                    begun = False
                    break

                yield vobj

        elif ittyp == 'dict':
            while True:
                try:
                    key, value = await it.__anext__() if ittyp == 'agen' else next(it)
                    if begun:
                        yield ','
                    if pretty:
                        yield '\n'
                    begun = True
                except (StopIteration, StopAsyncIteration):
                    stack.pop()
                    if pretty and begun:
                        yield '\n' + '    ' * len(stack)
                    yield '}'
                    if stack:
                        ittyp, it = stack[-1]
                    begun = True
                    break

                if pretty:
                    yield '    ' * len(stack)

                # KEY
                ktyp, kobj = await enc.asend(key)
                if ktyp == 'list' or ktyp == 'gen':
                    yield py_encode_basestring(''.join(str(x) for x in kobj))
                elif ktyp == 'agen':
                    k = ""
                    async for x in kobj:
                        k += str(x)
                    yield py_encode_basestring(k)
                elif ktyp == 'str':
                    yield kobj
                else:
                    raise TypeError(f'Dict key cannot be {ktyp}')
                yield ':'
                if pretty:
                    yield ' '

                # VALUE
                vtyp, vobj = await enc.asend(value)
                if vtyp != 'str':
                    ittyp, obj = vtyp, vobj
                    if ittyp == 'list' or ittyp == 'gen':
                        yield '['
                        it = iter(obj)
                    elif ittyp == 'agen':
                        yield '['
                        it = obj.__aiter__()
                    elif ittyp == 'dict':
                        yield '{'
                        it = iter(obj.items())
                    stack.append((ittyp, it))
                    begun = False
                    break

                yield vobj

    await close_encoder(enc)


async def close_encoder(gen):
    try:
        await gen.asend(SENTINEL)
    except StopAsyncIteration:
        pass


async def encoder() -> AsyncGenerator[Tuple[str, Any], Any]:
    typ, obj = None, None
    _intstr = int.__repr__

    while True:
        item = yield typ, obj
        if item is SENTINEL:
            break

        if inspect.isawaitable(item):
            item = await item

        if isinstance(item, str):
            typ, obj = 'str', py_encode_basestring(item)
        elif item is None:
            typ, obj = 'str', 'null'
        elif item is True:
            typ, obj = 'str', 'true'
        elif item is False:
            typ, obj = 'str', 'false'
        elif isinstance(item, int):
            # Subclasses of int/float may override __repr__, but we still
            # want to encode them as integers/floats in JSON. One example
            # within the standard library is IntEnum.
            typ, obj = 'str', _intstr(item)
        elif isinstance(item, float):
            # see comment above for int
            typ, obj = 'str', floatstr(item)
        else:
            if isinstance(item, (list, tuple)):
                typ, obj = 'list', item
            elif isinstance(item, dict):
                typ, obj = 'dict', item
            elif isinstance(item, types.GeneratorType):
                typ, obj = 'gen', item
            elif inspect.isasyncgen(item):
                typ, obj = 'agen', item
