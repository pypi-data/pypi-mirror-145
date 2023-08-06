import string

DEFAULT_KEYSPACE = string.digits + string.ascii_letters


def encode_int(value: int, keyspace: str = DEFAULT_KEYSPACE) -> str:
    """
    Encode a positive integer into a variable-length string.

    By default, the keyspace is ascii-compatible.

    :param value: The integer to encode.
    :param keyspace: The keyspace string to use.
    :return: Encoded string.
    """
    if value < 0:
        raise ValueError("value must be positive")
    value = int(value)
    out = []
    n = len(keyspace)
    while value:
        value, digit = divmod(value, n)
        out.append(keyspace[digit])
    return "".join(out[::-1])


def decode_int(value: str, keyspace: str = DEFAULT_KEYSPACE) -> int:
    """
    Decode an integer previously encoded by `decode_int`.

    :param value: The encoded string.
    :param keyspace: The encoding keyspace. This will naturally
                     have to be the same used while encoding for
                     correct results.
    :return: an integer
    """
    out = 0
    n = len(keyspace)
    for char in value:
        out = out * n + keyspace.index(char)
    return out
