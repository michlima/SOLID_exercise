from typing import Protocol
from dataclasses import dataclass, field
import json

@dataclass
class ParseResult:
    records: list[dict]
    errors: list[str] = field(default_factory=list)

class Parser(Protocol):
    def parse(self, raw: str) -> ParseResult: ...


class Reporter(Protocol):
    def report(self, result: ParseResult) -> str:
        ...

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
    def validate(self, result: ParseResult) -> ParseResult:
        cleaned = []
        try: 
            for record in result.records:
                if record:
                    valid = True
                    for field in record:
                        if field == "":
                            valid = False
                    if valid:
                        cleaned.append(record)
            result.records = cleaned
        except Exception as e:
            result.errors = str(e)
        return result
    
class ReporterText(Protocol):
    def report(self, result: ParseResult) -> str:
        return "\n".join([str(record) for record in result.records])
    
class ReporterHTML(Protocol):
    def report(self, result: ParseResult) -> str:
        output = "<ul>"
        for record in result.records:
            output += "<li>" + str(record) + "</li>"
        output += "</ul>"
        return output

class Pipeline:
    def __init__(self, parser: Parser, validator: Validator, reporter: Reporter) -> None: ...
    def run(self, raw: str) -> str: ...

