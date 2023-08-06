from datetime import datetime
from typing import Any

import pdfplumber

from aquaparser.schemas import MeasurementTitle


class TitleParser:

    def parse(self, doc: pdfplumber):
        page = doc.pages[:1]
        table = page[0].extract_tables({
            'edge_min_length': 15,  # this param get clean title table default 3
        })
        return self._clean_title(table)

    def _clean_title(self, table: list[list[Any]]) -> MeasurementTitle:
        measure_title, measure_description = table

        measure_date = datetime.strptime(measure_description[2][1], '%d.%m.%Y %H:%M')

        return MeasurementTitle(
            measurement_object=measure_title[1][1],
            project=measure_description[0][1],
            report_date=measure_date,
            responsible_person=measure_description[3][1],
        )
