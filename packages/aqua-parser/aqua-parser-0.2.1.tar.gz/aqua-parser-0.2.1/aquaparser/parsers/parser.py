import logging

import pdfplumber

from aquaparser.parsers import title_parser, toc_parser
from aquaparser.schemas import Measurement, MeasurementTOC

logger = logging.getLogger(__name__)


def parse(filename: str):
    title = title_parser.TitleParser()
    toc = toc_parser.TocParser()

    doc = pdfplumber.open(filename)
    measurement = Measurement(
        title=title.parse(doc),
        toc=toc.parse(doc),
    )
    logger.info(measurement.title)
    log_toc(measurement.toc)
    return measurement


def log_toc(table: list[MeasurementTOC]):
    for num, row in enumerate(table):
        smd = row.smd.replace('\n', ' ')
        row_num = num + 1
        control_string = f'{row_num}: smd = {smd}; status = {row.status}'
        logger.info(control_string)
