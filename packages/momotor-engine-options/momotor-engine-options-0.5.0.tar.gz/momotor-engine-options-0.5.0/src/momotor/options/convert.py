import typing
import warnings
import logging


logger = logging.getLogger(__name__)


def convert_duration(t: typing.Union[str, int, float, None]) -> typing.Optional[float]:
    """ Convert a string containing a duration into a float. The duration is defined as "hh:mm:ss"
    (hours, minutes, seconds).

    >>> convert_duration('1')
    1.0

    >>> convert_duration('10')
    10.0

    >>> convert_duration('100')
    100.0

    >>> convert_duration('1:00')
    60.0

    >>> convert_duration('10:00')
    600.0

    >>> convert_duration('100:00')
    6000.0

    >>> convert_duration('1:00:00')
    3600.0

    >>> convert_duration('1:00:00')
    3600.0

    >>> convert_duration('10:00:00')
    36000.0

    >>> convert_duration('100:00:00')
    360000.0

    >>> convert_duration(1)
    1.0

    >>> convert_duration(1.0)
    1.0

    :param t:
    :return:
    """
    if t is None:
        return t

    try:
        return float(t)
    except ValueError:
        pass

    # noinspection PyBroadException
    try:
        parts = t.split(':')
        if len(parts) > 3:
            raise ValueError

        result = 0.0
        for part in parts:
            result = result * 60.0 + float(part)

    except:
        msg = f'{t!r} is not a valid duration'
        warnings.warn(msg)
        raise ValueError(msg)

    return result


SIZE_FACTOR = {
    'k': 1,
    'm': 2,
    'g': 3,
    't': 4,
    'p': 5,
    'e': 6,
    'z': 7,
    'y': 8,
}


def convert_size(t: typing.Union[str, int, None]) -> typing.Optional[int]:
    """ Convert a size into an integer. If size ends with "i" or "ib", the value is assumed to be an
    IEC value, otherwise it is assumed to be a SI value. (See https://en.wikipedia.org/wiki/Binary_prefix)

    >>> convert_size('16')
    16

    >>> convert_size('16B')
    16

    >>> convert_size('16 B')
    16

    >>> convert_size('16k')
    16000

    >>> convert_size('16kb')
    16000

    >>> convert_size('16ki')
    16384

    >>> convert_size('16kib')
    16384

    >>> convert_size('16MiB')
    16777216

    >>> convert_size('16gib')
    17179869184

    >>> convert_size('16TIB')
    17592186044416

    :param t:
    :return: 
    """
    if t is None:
        return t

    base = 1000
    try:
        if isinstance(t, str):
            t = t.strip().lower()

            if t.endswith('b'):
                t = t[:-1]

            if t.endswith('i'):
                base = 1024
                t = t[:-1]

        try:
            return int(t)
        except ValueError:
            return int(t[:-1]) * (base ** SIZE_FACTOR[t[-1]])

    except:
        msg = f'{t!r} is not a valid size'
        warnings.warn(msg)
        raise ValueError(msg)
