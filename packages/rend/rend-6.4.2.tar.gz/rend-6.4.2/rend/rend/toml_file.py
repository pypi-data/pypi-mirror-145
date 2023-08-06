import toml

import rend.exc


__virtualname__ = "toml"


def render(hub, data, params=None):
    """
    Render the given toml data
    """
    if isinstance(data, bytes):
        data = data.decode()
    try:
        ret = toml.loads(data)
    except toml.TomlDecodeError as exc:
        raise rend.exc.RenderException(f"Toml render error: {exc.msg}")
    return ret
