import xlrd

from wikidata_exp.wdexp.communications.input.wikidata.interfaces import PropertyTracker
from wikidata_exp.wdexp.model.wikidata import WikidataProperty

__author__ = 'Dani'

_DEFAULT_FIRST_ROW = 1
_DEFAULT_SCORE_C = 3
_DEFAULT_ID_C = 0
_DEFAULT_LABEL_C = 1
_DEFAULT_DESC_C = 2

_FIRST_ROW = _DEFAULT_FIRST_ROW
_SCORE_C = _DEFAULT_SCORE_C
_ID_C = _DEFAULT_ID_C
_LABEL_C = _DEFAULT_LABEL_C
_DESC_C = _DEFAULT_DESC_C


class XsltClassPropertiesParser(PropertyTracker):
    def __init__(self, source_file, first_row=None, id_column=None, label_column=None,
                 desc_column=None, score_column=None):
        # In/out
        self._in_file = source_file

        # Const positions
        if id_column is not None:
            _ID_C = id_column
        if score_column is not None:
            _SCORE_C = score_column
        if label_column is not None:
            _LABEL_C = label_column
        if first_row is not None:
            _FIRST_ROW = first_row

    def yield_properties(self):
        for a_row in self._get_data_rows():
            if self._is_a_class(a_row):
                yield self._build_property_from_row(a_row)

    def _get_data_rows(self):
        book = xlrd.open_workbook(self._in_file)
        sheet = book.sheet_by_index(0)
        for row_index in range(_FIRST_ROW, sheet.nrows):
            yield sheet.row(row_index)

    def _build_property_from_row(self, row):
        return WikidataProperty(property_id=row[_ID_C].value,
                                label=row[_LABEL_C].value,
                                description=row[_DESC_C].value)

    def _is_a_class(self, row):
        if row[_SCORE_C].value == -2:
            return True
        return False
