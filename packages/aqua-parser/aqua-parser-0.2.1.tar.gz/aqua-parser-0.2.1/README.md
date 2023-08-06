# Aqua-parser

## Description

Aqua-parser is a package for extracting data from structured reports in pdf format.

## How to use

First of all, you need to install the package:

```bash
pip install aqua-parser
```
Next, the package must be imported into your project:
```python
import aquaparser
```
To extract the data, you just need to pass the file to the function:
```python
measurement = aquaparser.parse('document.pdf')
```
The function will return you the dataclass "Measurement" object:
```python
@dataclass
class Measurement:
    title: MeasurementTitle
    toc: list[MeasurementTOC]


@dataclass
class MeasurementTitle:
    measurement_object: str
    project: str
    report_date: datetime
    responsible_person: str


@dataclass
class MeasurementTOC:
    smd: str
    status: Optional[str]
    value_description: Optional[str]
    single_value: Optional[str]
    trial_object: Optional[str]
```

