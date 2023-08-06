from enum import Enum, auto


class ColumnType(Enum):
    """hopara.Table support all the following types for its columns:
     - ``STRING``, ``INTEGER``, ``DECIMAL``, ``BOOLEAN``
     - ``DATETIME``: python datetime format
     - ``AUTO_INCREMENT``: auto-increment integer
     - ``MONEY``: currency values
     - ``JSON``: json column, can be used for regular JSON or a (GeoJson)(https://geojson.org/)
     - ``STRING_ARRAY``: string array column: ``['value1', 'value2']``
     - ``GEOMETRY``: a coordinates array representing a Geometry ``[[0, 0], [1, 0], [1, 1], [0, 1], [0, 0]]``
     - ``IMAGE``: a string that representing an image ``data:[<mediatype>][;base64],<data>`` in [Data URIs format](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URIs)
    """
    STRING = auto()
    INTEGER = auto()
    DECIMAL = auto()
    BOOLEAN = auto()
    DATETIME = auto()
    AUTO_INCREMENT = auto()
    MONEY = auto()
    JSON = auto()
    STRING_ARRAY = auto()
    GEOMETRY = auto()
    IMAGE = auto()
