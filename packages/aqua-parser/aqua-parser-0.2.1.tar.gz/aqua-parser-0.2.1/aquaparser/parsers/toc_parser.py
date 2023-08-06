from typing import Any

import pdfplumber

from aquaparser.schemas import MeasurementTOC

SMD_ERROR = ('SMD', None, '')


class TocParser:

    def parse(self, doc: pdfplumber, start: int = 2, finish: int = 3):
        return self._get_toc(
            doc=doc,
            start_page=start,
            finish_page=finish,
        )

    def _clean_toc(self, table: list[list[Any]]) -> list[MeasurementTOC]:
        new_table = []

        for row in table:
            smd, status, description, value, obj = row
            if smd in SMD_ERROR:
                continue

            measurement_toc = MeasurementTOC(
                smd=smd,
                status=status,
                value_description=description,
                single_value=value,
                trial_object=obj,
            )
            new_table.append(measurement_toc)

        return new_table

    def _get_toc(self, doc: pdfplumber, start_page: int, finish_page: int) -> list[MeasurementTOC]:
        pages = doc.pages[start_page:finish_page]
        toc_list = []

        for page in pages:
            table = page.extract_table({
                'edge_min_length': 200,  # this param get clean toc table default 3
            })

            valid_table = self._clean_toc(table)
            toc_list.extend(valid_table)

        return toc_list
