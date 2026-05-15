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