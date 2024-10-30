"""
SCAN <key>

should return a string representing the fields of a record
associated with key. The returned string should be in the following format
"<field1>(<value1>), <field2>(<value2>), ... where fields are sorted lexicographically.

If the specified record does not exist, returns an empty string.


SCAN_BY_PREFIX <key> <prefix> — should return a string representing some
fields of a record associated with key.

Specifically, only fields that start with
prefix should be included.
The returned string should be in the same format as
in the SCAN operation with fields sorted in lexicographical order.
"""
from level1 import L1InMemoryDatabase

class L2InMemoryDatabase(L1InMemoryDatabase):
    def __init__(self):
        super().__init__()

    def scan(self, key):
        if key not in self.database:
            return ""
        # Sort lexicographically by field names
        fields = sorted(self.database[key].items())
        return ", ".join(f"{field}({value})" for field, value in fields)

    def scan_by_prefix(self, key, prefix):
        if key not in self.database:
            return ""
        fields = sorted(
            (field, value) for field, value in self.database[key].items()
            if field.startswith(prefix)
        )
        return ", ".join(f"{field}({value})" for field, value in fields)

if __name__ == "__main__":
    # Example usage
    db = L2InMemoryDatabase()
    queries = [
        ["SET", "A", "BC", "E"],
        ["SET", "A", "BD", "F"],
        ["SET", "A", "C", "G"],
        ["SCAN_BY_PREFIX", "A", "B"],
        ["SCAN", "A"],
        ["SCAN_BY_PREFIX", "B", "B"]
    ]

    # Execute queries and print the results
    for query in queries:
        print(f"Query:{query}",end="\t")
        command = query[0]
        if command == "SET":
            print("Result:",db.set(query[1], query[2], query[3]),end="\t")  # returns ""
        elif command == "GET":
            print("Result:",db.get(query[1], query[2]),end="\t")  # returns the value or ""
        elif command == "DELETE":
            print("Result:",db.delete(query[1], query[2]),end="\t")  # returns "true" or "false"
        elif command == "SCAN":
            print("Result:",db.scan(query[1]),end="\t")  # returns fields as a string or ""
        elif command == "SCAN_BY_PREFIX":
            print("Result:",db.scan_by_prefix(query[1], query[2]),end="\t")  # returns fields with prefix as a string or ""

        print("DATABASE STATE:",db.database)