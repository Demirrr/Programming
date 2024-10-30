"""
Time-to-Live Support
Time should always flow forward, so timestamps are guaranteed to strictly
increase as operations are executed.


Each test cannot contain both versions of operations (with and without
timestamp). However, you should maintain backward compatibility, so all
previously defined methods should work in the same way as before.


SET_AT <key> <field> <value> <timestamp> — should insert a field-value pair
or updates the value of the field in the record associated with key. This
operation should return an empty string.

SET_AT_WITH_TTL <key> <field> <value> <timestamp> <ttl> — should insert a
field-value pair or update the value of the field in the record associated with
key. Also sets its Time-To-Live starting at timestamp to be ttl. The ttl is the
amount of time that this field-value pair should exist in the database, meaning it
will be available during this interval: [timestamp, timestamp + ttl). This operation
should return an empty string.

DELETE_AT <key> <field> <timestamp> — the same as DELETE, but with
timestamp of the operation specified. Should return "true" if the field existed
and was successfully deleted and "false" if the key didn't exist.

GET_AT <key> <field> <timestamp> — the same as GET, but with timestamp of
the operation specified.

SCAN_AT <key> <timestamp> — the same as SCAN, but with timestamp of the
operation specified.

SCAN_BY_PREFIX_AT <key> <prefix> <timestamp> — the same as

SCAN_BY_PREFIX, but with timestamp of the operation specified.
"""
from level2 import L2InMemoryDatabase
class L3InMemoryDatabase(L2InMemoryDatabase):
    def __init__(self):
        super().__init__()
        self.ttl_data = {}

    def __str__(self):
        return f"Database:{self.database}\tTTL:{self.ttl_data}"
    def _clean_expired(self, key, timestamp):
        """Remove expired fields based on TTL."""
        if key in self.ttl_data:
            expired_fields = [
                field for field, expiry in self.ttl_data[key].items() if expiry <= timestamp
            ]
            for field in expired_fields:
                self.database[key].pop(field, None)
                self.ttl_data[key].pop(field, None)
            if not self.database[key]:
                del self.database[key]
            if not self.ttl_data[key]:
                del self.ttl_data[key]

    def set_at(self, key, field, value, timestamp):
        self._clean_expired(key, timestamp)
        if key not in self.database:
            self.database[key] = {}
        self.database[key][field] = (value, timestamp)
        return ""

    def set_at_with_ttl(self, key, field, value, timestamp, ttl):
        self.set_at(key, field, value, timestamp)
        if key not in self.ttl_data:
            self.ttl_data[key] = {}
        self.ttl_data[key][field] = timestamp + ttl
        return ""

    def get_at(self, key, field, timestamp):
        self._clean_expired(key, timestamp)
        if key in self.database and field in self.database[key]:
            value, set_time = self.database[key][field]
            return value
        return ""

    def delete_at(self, key, field, timestamp):
        self._clean_expired(key, timestamp)
        if key in self.database and field in self.database[key]:
            del self.database[key][field]
            if field in self.ttl_data.get(key, {}):
                del self.ttl_data[key][field]
            if not self.database[key]:
                del self.database[key]
            return "true"
        return "false"

    def scan_at(self, key, timestamp):
        self._clean_expired(key, timestamp)
        if key not in self.database:
            return ""
        fields = sorted((field, value[0]) for field, value in self.database[key].items())
        return ", ".join(f"{field}({value})" for field, value in fields)

    def scan_by_prefix_at(self, key, prefix, timestamp):
        self._clean_expired(key, timestamp)
        if key not in self.database:
            return ""
        fields = sorted(
            (field, value[0])
            for field, value in self.database[key].items()
            if field.startswith(prefix)
        )
        return ", ".join(f"{field}({value})" for field, value in fields)


if __name__ == "__main__":
    # Example usage
    examples= [[
        ["SET_AT_WITH_TTL", "A", "BC", "E", "1", "9"],
        ["SET_AT_WITH_TTL", "A", "BC", "E", "5", "10"],
        ["SET_AT", "A", "BD", "F", "5"],
        ["SCAN_BY_PREFIX_AT", "A", "B", "14"],
        ["SCAN_BY_PREFIX_AT", "A", "B", "15"]], [["SET_AT", "A", "B", "C", "1"],
                                                 ["SET_AT_WITH_TTL", "X", "Y", "Z", "2", "15"],
                                                 ["GET_AT", "X", "Y", "3"],
                                                 ["SET_AT_WITH_TTL", "A", "D", "E", "4", "10"],
                                                 ["SCAN_AT", "A", "13"],
                                                 ["SCAN_AT", "X", "16"],
                                                 ["SCAN_AT", "X", "17"],
                                                 ["DELETE_AT", "X", "Y", "20"]]]

    for queries in examples:
        db = L3InMemoryDatabase()

        # Execute queries and print the results
        for query in queries:
            command = query[0]
            print(query,end="\t")
            if command == "SET_AT":
                print(db.set_at(query[1], query[2], query[3], int(query[4])),end="\t")  # returns ""
            elif command == "SET_AT_WITH_TTL":
                print(db.set_at_with_ttl(query[1], query[2], query[3], int(query[4]), int(query[5])),end="\t")  # returns ""
            elif command == "GET_AT":
                print(db.get_at(query[1], query[2], int(query[3])),end="\t")  # returns value or ""
            elif command == "DELETE_AT":
                print(db.delete_at(query[1], query[2], int(query[3])),end="\t")  # returns "true" or "false"
            elif command == "SCAN_AT":
                print(db.scan_at(query[1], int(query[2])),end="\t")  # returns fields as a string or ""
            elif command == "SCAN_BY_PREFIX_AT":
                print(db.scan_by_prefix_at(query[1], query[2], int(query[3])),end="\t")  # returns fields with prefix as a string or ""

            print("DATABASE STATE:", db)
        print("\n\n")
