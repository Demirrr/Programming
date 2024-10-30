"""
In-memory database should support basic operations to manipulate
records, fields, and values within fields.

SET <key> <field> <value> — Insert a field-value pair to the record
associated with key.
If the field in the record already exists, replace the existing value with the specified value.
If the record does not exist, create a new one.
This operation should return an empty string.

GET <key> <field> — should return the value contained within field of the
record associated with key. If the record or the field doesn't exist, should return
an empty string

DELETE <key> <field> — should remove the field from the record associated
with key. Returns True
if the field was successfully deleted, and "false" if the key or the field do not exist in the database.

"""
class L1InMemoryDatabase:
    def __init__(self):
        self.database = {}

    def set(self, key, field, value):
        self.database.setdefault(key, dict())[field] = value
        return ""

    def get(self, key, field):
        return self.database.get(key, {}).get(field, "")

    def delete(self, key, field):
        if key in self.database and field in self.database[key]:
            del self.database[key][field]
            # Remove the record if it has no more fields
            if not self.database[key]:
                del self.database[key]
            return True
        return False

if __name__ == "__main__":

    # Example usage
    db = L1InMemoryDatabase()
    queries = [
        ["SET", "A", "B", "E"],
        ["SET", "A", "C", "F"],
        ["GET", "A", "B"],
        ["GET", "A", "D"],
        ["DELETE", "A", "B"],
        ["DELETE", "A", "D"]]

    # Execute queries and print the results
    for query in queries:
        print(query,end="\t")
        command = query[0]
        if command == "SET":
            print("Result:\t",db.set(query[1], query[2], query[3]),end="\t")
        elif command == "GET":
            print("Result:\t",db.get(query[1], query[2]),end="\t")
        elif command == "DELETE":
            print("Result:\t",db.delete(query[1], query[2]),end="\t")
        else:
            print("#")
        print("DATABASE STATE:",db.database)
