from typing import Protocol
from dataclasses import dataclass, field
import json

@dataclass
class ParseResult:
    records: list[dict]
    errors: list[str] = field(default_factory=list)

class ParseCSV(Protocol):
    def parse(self, raw: str) -> ParseResult:
        newParse = ParseResult()
        lines = raw.split("\n")
        records = [line.split(",") for line in lines if line]
        with open("output.log", "a") as f:
            f.write(str(records) + "\n")
        newParse.records = records
        return newParse
    
class ParseJSON(Protocol):
    def parse(self, raw:str) -> ParseResult:
        
        newParse = ParseResult()
        try:
            records = json.loads(raw)
            print(records)
            newParse.records = records
            return newParse
        except Exception as e:
            newParse.errors = e
            return newParse

class ParseXML(Protocol):
    def parse(self,raw: str) -> ParseResult:
        newParse = ParseResult()
        try:
            records = []
            for chunk in raw.split("<record>"):
                if "</record>" in chunk:
                    value = chunk.split("</record>")[0]
                    records.append(value.split("<field>"))
            newParse.records = records
        except Exception as e:
            newParse.errors = str(e)
        
        return newParse

class Validator(Protocol):
    def validate(self, result: ParseResult) -> ParseResult: ...

class Reporter(Protocol):
    def report(self, result: ParseResult) -> str: ...

class Pipeline:
    def __init__(self, parser: Parser, validator: Validator, reporter: Reporter) -> None: ...
    def run(self, raw: str) -> str: ...

class DataProcessor:
    def process(self, raw_data, format, validate=False):
        if format == "csv":
            lines = raw_data.split("\n")
            records = [line.split(",") for line in lines if line]
            with open("output.log", "a") as f:
                f.write(str(records) + "\n")
        elif format == "json":
            import json
            records = json.loads(raw_data)
            print(records)
        elif format == "xml":
            records = []
            for chunk in raw_data.split("<record>"):
                if "</record>" in chunk:
                    value = chunk.split("</record>")[0]
                    records.append(value.split("<field>"))
        else:
            records = []

        if validate:
            cleaned = []
            for record in records:
                if record:
                    valid = True
                    for field in record:
                        if field == "":
                            valid = False
                    if valid:
                        cleaned.append(record)
            records = cleaned

        return records

    def to_report(self, records, format):
        if format == "text":
            return "\n".join([str(record) for record in records])
        elif format == "html":
            output = "<ul>"
            for record in records:
                output += "<li>" + str(record) + "</li>"
            output += "</ul>"
            return output
        else:
            return str(records)