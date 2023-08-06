import inspect
import re
import types
from typing import Iterator, Any, Union, AsyncIterator


def _make_iterencode(markers, _default, _encoder, _indent, _floatstr,
        _key_separator, _item_separator, _sort_keys, _skipkeys, _one_shot,
        ## HACK: hand-optimized bytecode; turn globals into locals
        ValueError=ValueError,
        dict=dict,
        float=float,
        id=id,
        int=int,
        isinstance=isinstance,
        list=list,
        str=str,
        tuple=tuple,
        _intstr=int.__repr__,
    ):

    if _indent is not None and not isinstance(_indent, str):
        _indent = ' ' * _indent

    async def _iterencode_iter(it: Union[Iterator[Any], AsyncIterator[Any]], _current_indent_level, _async):
        # if markers is not None:
        #     markerid = id(it)
        #     if markerid in markers:
        #         raise ValueError("Circular reference detected")
        #     markers[markerid] = it

        buf = '['
        if _indent is not None:
            _current_indent_level += 1
            newline_indent = '\n' + _indent * _current_indent_level
            separator = _item_separator + newline_indent
            buf += newline_indent
        else:
            newline_indent = None
            separator = _item_separator

        first = True
        while True:
            try:
                value = await it.__anext__() if _async else next(it)
            except (StopIteration, StopAsyncIteration):
                break

            if first:
                first = False
            else:
                buf = separator
            yield buf

            if inspect.isawaitable(value):
                value = await value

            if isinstance(value, str):
                yield _encoder(value)
            elif value is None:
                yield 'null'
            elif value is True:
                yield 'true'
            elif value is False:
                yield 'false'
            elif isinstance(value, int):
                # Subclasses of int/float may override __repr__, but we still
                # want to encode them as integers/floats in JSON. One example
                # within the standard library is IntEnum.
                yield _intstr(value)
            elif isinstance(value, float):
                # see comment above for int
                yield _floatstr(value)
            else:
                if isinstance(value, (list, tuple, types.GeneratorType)):
                    chunks = _iterencode_iter(iter(value), _current_indent_level, False)
                elif isinstance(value, dict):
                    chunks = _iterencode_dict(value, _current_indent_level)
                elif inspect.isasyncgen(value):
                    chunks = _iterencode_iter(value.__aiter__(), _current_indent_level, True)
                else:
                    chunks = _iterencode(value, _current_indent_level)

                async for chunk in chunks:
                    yield chunk

        if newline_indent is not None:
            _current_indent_level -= 1
            yield '\n' + _indent * _current_indent_level
        yield ']'
        # if markers is not None:
        #     del markers[markerid]

    async def _iterencode_dict(dct: dict, _current_indent_level):
        if not dct:
            yield '{}'
            return
        # if markers is not None:
        #     markerid = id(dct)
        #     if markerid in markers:
        #         raise ValueError("Circular reference detected")
        #     markers[markerid] = dct
        yield '{'
        if _indent is not None:
            _current_indent_level += 1
            newline_indent = '\n' + _indent * _current_indent_level
            item_separator = _item_separator + newline_indent
            yield newline_indent
        else:
            newline_indent = None
            item_separator = _item_separator

        first = True
        if _sort_keys:
            items = sorted(dct.items())
        else:
            items = dct.items()

        for key, value in items:
            if inspect.isawaitable(key):
                key = await key

            if isinstance(key, str):
                pass
            # JavaScript is weakly typed for these, so it makes sense to
            # also allow them.  Many encoders seem to do something like this.
            elif isinstance(key, float):
                # see comment for int/float in _make_iterencode
                key = _floatstr(key)
            elif key is True:
                key = 'true'
            elif key is False:
                key = 'false'
            elif key is None:
                key = 'null'
            elif isinstance(key, int):
                # see comment for int/float in _make_iterencode
                key = _intstr(key)
            elif inspect.isgenerator(key):
                key = ''.join(str(x) for x in key)
            elif inspect.isasyncgen(key):
                key = ''.join([str(x) async for x in key])
            elif _skipkeys:
                continue
            else:
                raise TypeError(f'keys must be str, int, float, bool, None, awaitable object, '
                                f'async or sync generator, not {key.__class__.__name__}')

            if first:
                first = False
            else:
                yield item_separator
            yield _encoder(key)
            yield _key_separator

            if inspect.isawaitable(value):
                value = await value

            if isinstance(value, str):
                yield _encoder(value)
            elif value is None:
                yield 'null'
            elif value is True:
                yield 'true'
            elif value is False:
                yield 'false'
            elif isinstance(value, int):
                # Subclasses of int/float may override __repr__, but we still
                # want to encode them as integers/floats in JSON. One example
                # within the standard library is IntEnum.
                yield _intstr(value)
            elif isinstance(value, float):
                # see comment above for int
                yield _floatstr(value)
            else:
                if isinstance(value, (list, tuple, types.GeneratorType)):
                    chunks = _iterencode_iter(iter(value), _current_indent_level, False)
                elif isinstance(value, dict):
                    chunks = _iterencode_dict(value, _current_indent_level)
                elif inspect.isasyncgen(value):
                    chunks = _iterencode_iter(value.__aiter__(), _current_indent_level, True)
                else:
                    chunks = _iterencode(value, _current_indent_level)

                async for chunk in chunks:
                    yield chunk

        if newline_indent is not None:
            _current_indent_level -= 1
            yield '\n' + _indent * _current_indent_level
        yield '}'
        # if markers is not None:
        #     del markers[markerid]

    # def _iterencode(o, _current_indent_level):
    #     if isinstance(o, str):
    #         yield _encoder(o)
    #     elif o is None:
    #         yield 'null'
    #     elif o is True:
    #         yield 'true'
    #     elif o is False:
    #         yield 'false'
    #     elif isinstance(o, int):
    #         # see comment for int/float in _make_iterencode
    #         yield _intstr(o)
    #     elif isinstance(o, float):
    #         # see comment for int/float in _make_iterencode
    #         yield _floatstr(o)
    #     elif isinstance(o, (list, tuple)):
    #         yield from _iterencode_list(o, _current_indent_level)
    #     elif isinstance(o, dict):
    #         yield from _iterencode_dict(o, _current_indent_level)
    #     else:
    #         # if markers is not None:
    #         #     markerid = id(o)
    #         #     if markerid in markers:
    #         #         raise ValueError("Circular reference detected")
    #         #     markers[markerid] = o
    #         o = _default(o)
    #         yield from _iterencode(o, _current_indent_level)
    #         # if markers is not None:
    #         #     del markers[markerid]


    async def _iterencode(value, _current_indent_level):
        if inspect.isawaitable(value):
            value = await value

        if isinstance(value, str):
            yield _encoder(value)
        elif value is None:
            yield 'null'
        elif value is True:
            yield 'true'
        elif value is False:
            yield 'false'
        elif isinstance(value, int):
            # Subclasses of int/float may override __repr__, but we still
            # want to encode them as integers/floats in JSON. One example
            # within the standard library is IntEnum.
            yield _intstr(value)
        elif isinstance(value, float):
            # see comment above for int
            yield _floatstr(value)
        else:
            if isinstance(value, (list, tuple, types.GeneratorType)):
                chunks = _iterencode_iter(iter(value), _current_indent_level, False)
            elif isinstance(value, dict):
                chunks = _iterencode_dict(value, _current_indent_level)
            elif inspect.isasyncgen(value):
                chunks = _iterencode_iter(value.__aiter__(), _current_indent_level, True)
            else:
                value = _default(value)
                chunks = _iterencode(value, _current_indent_level)

            async for chunk in chunks:
                yield chunk

    return _iterencode


markers = {}


def default(val):
    raise RuntimeError('default()')


item_separator = ', '
key_separator = ': '
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


def py_encode_basestring(s):
    """Return a JSON representation of a Python string

    """
    def replace(match):
        return ESCAPE_DCT[match.group(0)]
    return '"' + ESCAPE.sub(replace, s) + '"'


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


iterencode = _make_iterencode(
    markers, default, py_encode_basestring, '    ', floatstr,
    key_separator, item_separator, False,
    False, False)

