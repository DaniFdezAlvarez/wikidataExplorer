from wikidata_exp.wdexp.communications.input.json.json_in import read_json_object
from wikidata_exp.wdexp.wikidata.commands.class_ranking_DUMP import KEY_ID, KEY_ACCUMULATED
from wikidata_exp.wdexp.wikidata.commands.agregated_class_summarizer_API import KEY_LABEL

KEY_RANKING_WITHIN_SOURCE = "int_rank"

KEY_NUMBER_ELEMS = "n_elems"
KEY_NUMBER_NOT_FOUND = "n_not_found"
KEY_NOT_FOUND_SOURCE_1 = "not_found_1"
KEY_NOT_FOUND_SOURCE_2 = "not_found_2"
KEY_ABSOLUTE_RANKING_VARIATION = "rank_variation_abs"
KEY_RELATIVE_RANKING_VARIATION = "rank_variation_rel"
KEY_RELATIVE_DEVIATION_SCORE = "rel_deviation"


class ResultComparatorCommand(object):
    def __init__(self, source1, source2, target_sectors, out_file=None):
        self._path_main = source1
        self._path_target = source2
        self._target_sectors = target_sectors
        self._out_file = out_file

        self._s_main = self._parse_source(source1)
        self._s_target = self._parse_source(source2)

        self._sector_summaries = []

    def exec_command(self, string_return=False):
        for a_sector in self._target_sectors:
            self._compare_results_in_sector(a_sector)
        self._serialize_results(string_return)

    def _compare_results_in_sector(self, end_of_sector):
        result_summary = {KEY_NUMBER_ELEMS: end_of_sector,
                          KEY_NUMBER_NOT_FOUND: 0,
                          KEY_NOT_FOUND_SOURCE_1: [],
                          KEY_NOT_FOUND_SOURCE_2: [],
                          KEY_ABSOLUTE_RANKING_VARIATION: 0,
                          KEY_RELATIVE_DEVIATION_SCORE: 0}

        main_subrange = self._extract_target_subrange(self._s_main, end_of_sector)
        target_subrange = self._extract_target_subrange(self._s_target, end_of_sector)

        shared_elements = self._find_shared_elements(main_subrange, target_subrange)

        self._compute_not_found(main_subrange, target_subrange, shared_elements, result_summary)
        self._compute_ranking_variation(main_subrange, target_subrange, shared_elements, result_summary)
        self._compute_relative_deviation(main_subrange, target_subrange, shared_elements, result_summary)
        self._sector_summaries.append(result_summary)

    def _extract_target_subrange(self, source, end_of_sector):
        return source[:end_of_sector]

    def _find_shared_elements(self, main_subrange, target_subrange):
        ids_in_main = []
        for elem in main_subrange:
            an_id = elem[KEY_ID]
            for target_elem in target_subrange:
                if target_elem[KEY_ID] == an_id:
                    ids_in_main.append(an_id)
                    break
        return ids_in_main

    def _compute_not_found(self, main_subrange, target_subrange, shared_elements, result_summary):
        result_summary[KEY_NUMBER_NOT_FOUND] = len(main_subrange) - len(shared_elements)
        for an_elem in main_subrange:
            if an_elem[KEY_ID] not in shared_elements:
                label = an_elem[KEY_LABEL] if an_elem[KEY_LABEL] is not None else "UNKNOWN"
                result_summary[KEY_NOT_FOUND_SOURCE_1].append(an_elem[KEY_ID] + ":" + label)

        for an_elem in target_subrange:
            if an_elem[KEY_ID] not in shared_elements:
                label = an_elem[KEY_LABEL] if an_elem[KEY_LABEL] is not None else "UNKNOWN"
                result_summary[KEY_NOT_FOUND_SOURCE_2].append(an_elem[KEY_ID] + ":" + label)

    def _compute_ranking_variation(self, main_subrange, target_subrange, shared_elements, result_summary):
        absolute = 0
        relative = 0
        for a_main in main_subrange:
            if a_main[KEY_ID] in shared_elements:
                a_target = self._get_elem_by_id(target_subrange, a_main[KEY_ID])
                absolute += abs(float(a_main[KEY_RANKING_WITHIN_SOURCE]) - a_target[KEY_RANKING_WITHIN_SOURCE])
                relative += abs(float(a_main[KEY_RANKING_WITHIN_SOURCE]) - a_target[KEY_RANKING_WITHIN_SOURCE]) / a_main[
                    KEY_RANKING_WITHIN_SOURCE]
        absolute /= len(shared_elements)
        relative /= len(shared_elements)
        result_summary[KEY_ABSOLUTE_RANKING_VARIATION] = absolute
        result_summary[KEY_RELATIVE_RANKING_VARIATION] = relative

    def _compute_relative_deviation(self, main_subrange, target_subrange, shared_elements, result_summary):
        relative = 0
        for a_main in main_subrange:
            if a_main[KEY_ID] in shared_elements:
                a_target = self._get_elem_by_id(target_subrange, a_main[KEY_ID])
                relative += abs(float(a_main[KEY_ACCUMULATED]) - float(a_target[KEY_ACCUMULATED])) / float(a_main[
                    KEY_ACCUMULATED])
        relative /= len(shared_elements)
        result_summary[KEY_RELATIVE_DEVIATION_SCORE] = relative

    def _get_elem_by_id(self, subrange, target_id):
        for elem in subrange:
            if target_id == elem[KEY_ID]:
                return elem
        return None

    def _parse_source(self, source_path):
        result = read_json_object(path=source_path)

        # Removing wikis
        i = 0
        indexes_to_remove = []
        for i in range(0, len(result)):
            if result[i][KEY_LABEL] is not None:
                if "wiki" in result[i][KEY_LABEL] or "Wiki" in result[i][KEY_LABEL]:
                    indexes_to_remove.append(i)
        for index in reversed(indexes_to_remove):
            del result[index]

        # Adding rank
        i = 1
        for an_elem in result:
            an_elem[KEY_RANKING_WITHIN_SOURCE] = i
            i += 1
        return result

    def _serialize_results(self, string_return):
        total_str_result = ""
        for a_sector_result in self._sector_summaries:
            total_str_result += self._generate_report_from_json_summary(a_sector_result)
            total_str_result += "\n\n\n-----------------------------------------------------\n\n\n"
        if string_return:
            print total_str_result
        else:
            with open(self._out_file, "w") as out_stream:
                out_stream.write(total_str_result)

    def _generate_report_from_json_summary(self, a_summary):
        result = ""
        result += "Report comparing documents " + self._path_main + " AND " + self._path_target
        result += "\n Sector considered:  top " + str(a_summary[KEY_NUMBER_ELEMS])
        result += "\n\n Number of shared elements: " + str(
            a_summary[KEY_NUMBER_ELEMS] - a_summary[KEY_NUMBER_NOT_FOUND]) + "/" + str(str(a_summary[KEY_NUMBER_ELEMS]))
        result += "\n Media of ABSOLUTE variations in RANKING: " + str(a_summary[KEY_ABSOLUTE_RANKING_VARIATION])
        result += "\n Media of RELATIVE variations in RANKING: " + str(a_summary[KEY_RELATIVE_RANKING_VARIATION])
        result += "\n Media of RELATIVE variations in SCORE: " + str(a_summary[KEY_RELATIVE_DEVIATION_SCORE])
        result += "\n\n Ordered elements of source 1 not found in source 2: "
        for an_elem in a_summary[KEY_NOT_FOUND_SOURCE_1]:
            result += "\n   " + an_elem
        result += "\n\n Ordered elements of source 2 not found in source 1: "
        for an_elem in a_summary[KEY_NOT_FOUND_SOURCE_2]:
            result += "\n   " + an_elem

        return result
        # result_summary = {KEY_NUMBER_ELEMS: end_of_sector,
        #                   KEY_NUMBER_NOT_FOUND: 0,
        #                   KEY_NOT_FOUND_SOURCE_1: [],
        #                   KEY_NOT_FOUND_SOURCE_2: [],
        #                   KEY_ABSOLUTE_RANKING_VARIATION:0,
        #                   KEY_RELATIVE_DEVIATION_SCORE:0}
