import xlrd
import os
import json


_KEY_RANK = "rank"
_KEY_LABEL = "label"
_KEY_DESC = "desc"
_KEY_ID = "id"
_KEY_SCORES = "scores"
_KEY_AVERAGE = "average"
_KEY_STD_DEVIATION = "deviation"
_KEY_MAX_GAP = "max_gap"
_KEY_CLASSIFICATION = "class"

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

_CLEAR_TOPIC = "TOPIC (clear)"
_LIKELY_TOPIC = "Topic (likely)"
_UNDEFINED = "Unknown"
_LIKELY_INSTANCE = "Instance (likely)"
_CLEAR_INSTANCE = "INSTANCE (Clear)"


class XsltSurveyProcessor(object):
    def __init__(self, source_folder, out_file=None, first_row=None, id_column=None, label_column=None,
                 desc_column=None,
                 score_column=None):
        # In/out
        self._in_folder = source_folder
        self._out_file = out_file

        # Const positions
        if id_column is not None:
            _ID_C = id_column
        if score_column is not None:
            _SCORE_C = score_column
        if label_column is not None:
            _LABEL_C = label_column
        if first_row is not None:
            _FIRST_ROW = first_row

        # Internal estructures
        self._props_dict = {}  # expected: {_KEY_ID : { model dict returned by template_dict()} }

    def process_survey(self):
        self._collect_data()
        self._process_data()
        self._serialize_results()

    def _collect_data(self):
        for a_file in self._get_file_names():
            rank = 0
            for a_row in self._get_data_rows(a_file):
                rank += 1
                if a_row[_SCORE_C].ctype == xlrd.XL_CELL_NUMBER:
                    if a_row[_ID_C].value not in self._props_dict:
                        self._create_new_dict_for_scores(a_row, rank)
                    else:
                        self._complete_dict_with_score(a_row)

    def _process_data(self):
        for a_key in self._props_dict:
            self._calc_average(self._props_dict[a_key])
            self._calc_std_deviation(self._props_dict[a_key])  # Call always after calc_average
            self._calc_max_gap(self._props_dict[a_key])
            self._calc_classification(self._props_dict[a_key])  # Call always after calc_average

    def _calc_average(self, a_dict):
        print a_dict[_KEY_SCORES]
        a_dict[_KEY_AVERAGE] = sum(a_dict[_KEY_SCORES]) / len(a_dict[_KEY_SCORES])

    def _calc_std_deviation(self, a_dict):
        average = a_dict[_KEY_AVERAGE]
        a_dict[_KEY_STD_DEVIATION] = sum([abs(x - average) for x in a_dict[_KEY_SCORES]]) / len(a_dict[_KEY_SCORES])

    def _calc_max_gap(self, a_dict):
        max_gap = 0
        for i in range(0, len(a_dict[_KEY_SCORES]) - 1):
            for j in range(i + 1, len(a_dict[_KEY_SCORES])):
                gap = abs(a_dict[_KEY_SCORES][i] - a_dict[_KEY_SCORES][j])
                if gap > max_gap:
                    max_gap = gap
        a_dict[_KEY_MAX_GAP] = max_gap

    def _calc_classification(self, a_dict):
        average = a_dict[_KEY_AVERAGE]
        if average < -1:
            a_dict[_KEY_CLASSIFICATION] = _CLEAR_TOPIC
        elif average > 1:
            a_dict[_KEY_CLASSIFICATION] = _CLEAR_INSTANCE
        elif average < -0.4:
            a_dict[_KEY_CLASSIFICATION] = _LIKELY_TOPIC
        elif average > 0.4:
            a_dict[_KEY_CLASSIFICATION] = _LIKELY_INSTANCE
        else:
            a_dict[_KEY_CLASSIFICATION] = _UNDEFINED

    def _serialize_results(self):
        conflictive_deviations = set()
        conflictive_gaps = set()
        clear_results = set()
        clear_classes = set()
        clear_instances = set()
        likely_instances = set()
        likely_classes = set()
        undefined = set()

        wrost_possible_combo = 0
        horrible_combo = 0


        unclear_but_agreed_results = set()
        for a_key in self._props_dict:
            target = self._props_dict[a_key]
            if target[_KEY_AVERAGE] < -1:
                clear_results.add(target[_KEY_RANK])
                clear_classes.add(target[_KEY_RANK])
            if target[_KEY_AVERAGE] > 1:
                clear_results.add(target[_KEY_RANK])
                clear_instances.add(target[_KEY_RANK])
            if target[_KEY_STD_DEVIATION] > 0.5:
                conflictive_deviations.add(target[_KEY_RANK])
            if target[_KEY_STD_DEVIATION] <= 1 and target[_KEY_AVERAGE] > - 0.5 and target[_KEY_AVERAGE] < -0.5:
                unclear_but_agreed_results.add(target[_KEY_RANK])
            if target[_KEY_MAX_GAP] >= 3:
                conflictive_gaps.add(target[_KEY_RANK])

            if -2 in target[_KEY_SCORES] and 2 in target[_KEY_SCORES] and 0 in target[_KEY_SCORES]:
                wrost_possible_combo += 1

            if -2 in target[_KEY_SCORES] and 2 in target[_KEY_SCORES]:
                horrible_combo += 1

            if target[_KEY_CLASSIFICATION] == _CLEAR_INSTANCE:
                clear_results.add(target[_KEY_RANK])
                clear_instances.add(target[_KEY_RANK])
            elif target[_KEY_CLASSIFICATION] == _CLEAR_TOPIC:
                clear_results.add(target[_KEY_RANK])
                clear_classes.add(target[_KEY_RANK])
            elif target[_KEY_CLASSIFICATION] == _LIKELY_INSTANCE:
                likely_instances.add(target[_KEY_RANK])
            elif target[_KEY_CLASSIFICATION] == _LIKELY_TOPIC:
                likely_classes.add(target[_KEY_RANK])
            else:
                undefined.add(target[_KEY_RANK])

        # conflictive_deviations = set()
        # conflictive_gaps = set()
        # clear_results = set()
        # clear_classes = set()
        # clear_instances = set()
        # n_c_classes = 0
        # n_c_instances = 0
        # n_l_classes = 0
        # n_l_instances = 0
        # n_undefined = 0

        print "TOTAL ELEMS: ", len(self._props_dict)

        print "Clear classes:", len(clear_classes), clear_classes
        print "Likely classes:", len(likely_classes), likely_classes
        print "Undefined:", len(undefined), undefined
        print "likely instances:", len(likely_instances), likely_instances
        print "Clear instances:", len(clear_instances), clear_instances

        print "----------"
        print "Wrong deviations", len(conflictive_deviations)
        print "Dangerous gaps", len(conflictive_gaps), conflictive_gaps
        print "Unclear but agreed", len(unclear_but_agreed_results)
        print "------------"
        print "CLEAR RESULTS: " , len(clear_results)
        print "Horrible combo: ", horrible_combo
        print "Worst possible combo: ", wrost_possible_combo

        with open(self._out_file, "w") as out_stream:
            json.dump(self._props_dict, out_stream, indent=4)

        # print clear_classes
        # print clear_instances

    def _create_new_dict_for_scores(self, row, rank):
        target_dict = self._get_template_dict()
        target_dict[_KEY_LABEL] = row[_LABEL_C].value
        target_dict[_KEY_DESC] = row[_DESC_C].value
        target_dict[_KEY_SCORES].append(row[_SCORE_C].value)
        target_dict[_KEY_RANK] = rank

        self._props_dict[row[_ID_C].value] = target_dict

    def _complete_dict_with_score(self, row):
        self._props_dict[row[_ID_C].value][_KEY_SCORES].append(row[_SCORE_C].value)

    def _get_file_names(self):
        for (dirpath, dirnames, filenames) in os.walk(self._in_folder):
            for filename in filenames:
                if filename.endswith(".xlsx"):
                    yield os.sep.join([dirpath, filename])

    @staticmethod
    def _get_data_rows(file_path):
        book = xlrd.open_workbook(file_path)
        sheet = book.sheet_by_index(0)
        for row_index in range(_FIRST_ROW, sheet.nrows):
            yield sheet.row(row_index)

    @staticmethod
    def _get_template_dict():
        return {_KEY_LABEL: None,
                _KEY_DESC: None,
                _KEY_AVERAGE: None,
                _KEY_MAX_GAP: None,
                _KEY_RANK: None,
                _KEY_SCORES: [],
                _KEY_STD_DEVIATION: None}
