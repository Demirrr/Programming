"""
BACKUP <timestamp> — should save the database state at the specified
timestamp, including the remaining ttl for all records and fields. Remaining ttl is
the difference between their initial ttl and their current lifespan (the duration
between the timestamp of this operation and their initial timestamp). Returns a
string representing the number of non-empty non-expired records in the
database.
RESTORE <timestamp> <timestampToRestore> — should restore the database
from the latest backup before or at timestampToRestore. It's guaranteed that a
backup before or at timestampToRestore will exist. Expiration times for restored
records and fields should be recalculated according to the timestamp of this
operation - since the database timeline always flows forward, restored records
and fields should expire after the timestamp of this operation, depending on
their remaining ttls at backup. This operation should return an empty string.
"""
from level3 import L3InMemoryDatabase
class L4InMemoryDatabase(L3InMemoryDatabase):
    def __init__(self):
        super().__init__()
        self.backups = {}

    def backup(self, timestamp):
        self._clean_expired(None, timestamp)
        backup_state = {}
        for key, fields in self.database.items():
            backup_state[key] = {
                field: (value[0], timestamp - set_time)  # Store value and remaining TTL
                for field, (value, set_time) in fields.items()
            }
        self.backups[timestamp] = (backup_state, {k: v.copy() for k, v in self.ttl_data.items()})
        return str(len([k for k in self.database if self.database[k]]))

    def restore(self, timestamp, timestamp_to_restore):
        restore_time = max(t for t in self.backups if t <= timestamp_to_restore)
        backup_state, backup_ttl = self.backups[restore_time]

        # Restore database state
        self.database = {
            key: {
                field: (value, timestamp)
                for field, (value, remaining_ttl) in fields.items()
            }
            for key, fields in backup_state.items()
        }

        # Restore TTL with recalculated expiration times
        self.ttl_data = {}
        for key, fields in backup_ttl.items():
            for field, expiry in fields.items():
                remaining_ttl = expiry - restore_time
                if key not in self.ttl_data:
                    self.ttl_data[key] = {}
                self.ttl_data[key][field] = timestamp + remaining_ttl
        return ""


if __name__ == '__main__':
    # Example usage
    db = L4InMemoryDatabase()
    queries = [
        ["SET_AT_WITH_TTL", "A", "B", "C", "1", "10"],
        ["BACKUP", "3"],
        ["SET_AT", "A", "D", "E", "4"],
        ["BACKUP", "5"],
        ["DELETE_AT", "A", "B", "8"],
        ["BACKUP", "9"],
        ["RESTORE", "10", "7"],
        ["BACKUP", "11"],
        ["SCAN_AT", "A", "15"],
        ["SCAN_AT", "A", "16"]]

    # Execute queries and print the results
    for query in queries:
        command = query[0]
        print(query, end="\t")
        if command == "SET_AT":
            print("Result:\t",db.set_at(query[1], query[2], query[3], int(query[4])),end="\t")  # returns ""
        elif command == "SET_AT_WITH_TTL":
            print("Result:\t",db.set_at_with_ttl(query[1], query[2], query[3], int(query[4]), int(query[5])),end="\t")  # returns ""
        elif command == "GET_AT":
            print("Result:\t",db.get_at(query[1], query[2], int(query[3])),end="\t")  # returns value or ""
        elif command == "DELETE_AT":
            print("Result:\t",db.delete_at(query[1], query[2], int(query[3])),end="\t")  # returns "true" or "false"
        elif command == "SCAN_AT":
            print("Result:\t",db.scan_at(query[1], int(query[2])),end="\t")  # returns fields as a string or ""
        elif command == "SCAN_BY_PREFIX_AT":
            print("Result:\t",db.scan_by_prefix_at(query[1], query[2], int(query[3])),end="\t")  # returns fields with prefix as a string or ""
        elif command == "BACKUP":
            print("Result:\t",db.backup(int(query[1])),end="\t")  # returns number of non-empty records
        elif command == "RESTORE":
            print("Result:\t",db.restore(int(query[1]), int(query[2])),end="\t")  # returns ""

        print("DATABASE STATE:", db.database)