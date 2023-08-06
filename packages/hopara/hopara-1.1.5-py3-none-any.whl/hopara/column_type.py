from enum import Enum, auto


class ColumnType(Enum):
    """hopara.Table support all the following types for its columns:
     - ``STRING``, ``INTEGER``, ``DECIMAL``, ``BOOLEAN``
     - ``DATETIME``: python datetime format
     - ``AUTO_INCREMENT``: auto-increment integer
     - ``MONEY``: currency values
     - ``JSON``: json column, can be used for regular Json or a (GeoJson)(https://geojson.org/)
     - ``STRING_ARRAY``: string array column: ``['value1', 'value2']``
     - ``POLYGON``: a string representing a Polygon ``POLYGON ((40 40, 20 45, 45 30, 40 40))`` in [WKT format](https://en.wikipedia.org/wiki/Well-known_text_representation_of_geometry)
     - ``MULTIPOINT``: a string representing a MultiPoint ``MULTIPOINT ((10 40), (40 30), (20 20), (30 10))`` in WKT format
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
    POLYGON = auto()
    MULTIPOINT = auto()
    IMAGE = auto()
