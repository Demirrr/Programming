#include <iostream>
#include <string>
#include <unordered_map>
#include <vector>
#include <algorithm>
#include <sstream>
#include <map>

class L1InMemoryDatabase {
public:
    // Insert a field-value pair into the record associated with key.
    // If the record or field does not exist, create them.
    // Returns an empty string.
    std::string set(const std::string &key, const std::string &field, const std::string &value) {
        database[key][field] = value;
        return "";
    }

    // Retrieve the value of a specific field within a record.
    // Returns an empty string if the record or field doesn't exist.
    std::string get(const std::string &key, const std::string &field) const {
        auto record = database.find(key);
        if (record != database.end()) {
            auto field_it = record->second.find(field);
            if (field_it != record->second.end()) {
                return field_it->second;
            }
        }
        return "";
    }

    // Delete a specific field from a record.
    // Returns true if the field was successfully deleted,
    // false if the record or field doesn't exist.
    bool delete_field(const std::string &key, const std::string &field) {
        auto record = database.find(key);
        if (record != database.end()) {
            auto field_it = record->second.find(field);
            if (field_it != record->second.end()) {
                record->second.erase(field_it);
                // Remove the record if it has no more fields.
                if (record->second.empty()) {
                    database.erase(record);
                }
                return true;
            }
        }
        return false;
    }

    // Method to print the database state for debugging purposes
    void printDatabaseState() const {
        std::cout << "DATABASE STATE:\n";
        for (const auto &record : database) {
            std::cout << "Key: " << record.first << "\n";
            for (const auto &field : record.second) {
                std::cout << "  Field: " << field.first << " => Value: " << field.second << "\n";
            }
        }
        std::cout << "\n";
    }

protected:
    std::unordered_map<std::string, std::unordered_map<std::string, std::string>> database;
};

class L2InMemoryDatabase : public L1InMemoryDatabase {
public:
    // Return lexicographically sorted fields and values of a record
    std::string scan(const std::string &key) const {
        auto record = database.find(key);
        if (record == database.end()) {
            return "";
        }

        std::vector<std::pair<std::string, std::string>> fields(record->second.begin(), record->second.end());
        std::sort(fields.begin(), fields.end());

        std::ostringstream result;
        for (const auto &field : fields) {
            result << field.first << "(" << field.second << "), ";
        }

        std::string output = result.str();
        if (!output.empty()) {
            output.pop_back();
            output.pop_back();  // Remove trailing ", "
        }
        return output;
    }

    // Return lexicographically sorted fields and values of a record starting with a given prefix
    std::string scan_by_prefix(const std::string &key, const std::string &prefix) const {
        auto record = database.find(key);
        if (record == database.end()) {
            return "";
        }

        std::vector<std::pair<std::string, std::string>> fields;
        for (const auto &field : record->second) {
            if (field.first.find(prefix) == 0) {
                fields.emplace_back(field.first, field.second);
            }
        }
        std::sort(fields.begin(), fields.end());

        std::ostringstream result;
        for (const auto &field : fields) {
            result << field.first << "(" << field.second << "), ";
        }

        std::string output = result.str();
        if (!output.empty()) {
            output.pop_back();
            output.pop_back();  // Remove trailing ", "
        }
        return output;
    }
};

class L3InMemoryDatabase : public L2InMemoryDatabase{
public:
    // Clean expired fields based on TTL
    void clean_expired(const std::string &key, int timestamp) {
        if (ttl_data.find(key) != ttl_data.end()) {
            std::vector<std::string> expired_fields;
            for (const auto &field : ttl_data[key]) {
                if (field.second <= timestamp) {
                    expired_fields.push_back(field.first);
                }
            }
            for (const auto &field : expired_fields) {
                database[key].erase(field);
                ttl_data[key].erase(field);
            }
            if (database[key].empty()) {
                database.erase(key);
            }
            if (ttl_data[key].empty()) {
                ttl_data.erase(key);
            }
        }
    }

    std::string set_at(const std::string &key, const std::string &field, const std::string &value, int timestamp) {
        clean_expired(key, timestamp);
        database[key][field] = {value, timestamp};
        return "";
    }

    std::string set_at_with_ttl(const std::string &key, const std::string &field, const std::string &value, int timestamp, int ttl) {
        set_at(key, field, value, timestamp);
        ttl_data[key][field] = timestamp + ttl;
        return "";
    }

    std::string get_at(const std::string &key, const std::string &field, int timestamp) {
        clean_expired(key, timestamp);
        if (database.find(key) != database.end() && database[key].find(field) != database[key].end()) {
            return database[key][field].first;
        }
        return "";
    }

    std::string delete_at(const std::string &key, const std::string &field, int timestamp) {
        clean_expired(key, timestamp);
        if (database.find(key) != database.end() && database[key].find(field) != database[key].end()) {
            database[key].erase(field);
            if (ttl_data[key].find(field) != ttl_data[key].end()) {
                ttl_data[key].erase(field);
            }
            if (database[key].empty()) {
                database.erase(key);
            }
            return "true";
        }
        return "false";
    }

    std::string scan_at(const std::string &key, int timestamp) {
        clean_expired(key, timestamp);
        if (database.find(key) == database.end()) {
            return "";
        }

        std::vector<std::pair<std::string, std::string>> fields;
        for (const auto &field : database[key]) {
            fields.push_back({field.first, field.second.first});
        }
        std::sort(fields.begin(), fields.end());

        std::ostringstream result;
        for (const auto &field : fields) {
            result << field.first << "(" << field.second << "), ";
        }
        std::string output = result.str();
        if (!output.empty()) {
            output.pop_back();
            output.pop_back(); // Remove trailing ", "
        }
        return output;
    }

    std::string scan_by_prefix_at(const std::string &key, const std::string &prefix, int timestamp) {
        clean_expired(key, timestamp);
        if (database.find(key) == database.end()) {
            return "";
        }

        std::vector<std::pair<std::string, std::string>> fields;
        for (const auto &field : database[key]) {
            if (field.first.find(prefix) == 0) {
                fields.push_back({field.first, field.second.first});
            }
        }
        std::sort(fields.begin(), fields.end());

        std::ostringstream result;
        for (const auto &field : fields) {
            result << field.first << "(" << field.second << "), ";
        }
        std::string output = result.str();
        if (!output.empty()) {
            output.pop_back();
            output.pop_back(); // Remove trailing ", "
        }
        return output;
    }

    // Display current state for debugging
    void display() const {
        std::cout << "Database: ";
        for (const auto &record : database) {
            std::cout << "{" << record.first << ": ";
            for (const auto &field : record.second) {
                std::cout << "{" << field.first << ": " << field.second.first << "@" << field.second.second << "} ";
            }
            std::cout << "} ";
        }
        std::cout << "\nTTL Data: ";
        for (const auto &record : ttl_data) {
            std::cout << "{" << record.first << ": ";
            for (const auto &field : record.second) {
                std::cout << "{" << field.first << ": " << field.second << "} ";
            }
            std::cout << "} ";
        }
        std::cout << std::endl;
    }

public:
    std::unordered_map<std::string, std::unordered_map<std::string, std::pair<std::string, int>>> database;
    std::unordered_map<std::string, std::unordered_map<std::string, int>> ttl_data;
};


class L4InMemoryDatabase : public L3InMemoryDatabase {
private:
    std::map<int, std::pair<std::map<std::string, std::map<std::string, std::pair<std::string, int>>>,
                            std::map<std::string, std::map<std::string, int>>>> backups;

public:
    std::string backup(int timestamp) {
        clean_expired("", timestamp);  // Clean expired entries

        std::map<std::string, std::map<std::string, std::pair<std::string, int>>> backup_state;
        for (const auto& [key, fields] : database) {
            std::map<std::string, std::pair<std::string, int>> field_backup;
            for (const auto& [field, value_and_time] : fields) {
                int remaining_ttl = timestamp - value_and_time.second;  // Calculate remaining TTL
                field_backup[field] = {value_and_time.first, remaining_ttl};
            }
            backup_state[key] = field_backup;
        }

        // Convert ttl_data to map for storing in backups
        std::map<std::string, std::map<std::string, int>> backup_ttl;
        for (const auto& [key, fields] : ttl_data) {
            backup_ttl[key] = {fields.begin(), fields.end()};
        }

        backups[timestamp] = {backup_state, backup_ttl};

        // Return count of non-empty, non-expired records
        int count = 0;
        for (const auto& [key, fields] : database) {
            if (!fields.empty()) count++;
        }
        return std::to_string(count);
    }

    std::string restore(int timestamp, int timestamp_to_restore) {
        // Find the most recent backup before or at timestamp_to_restore
        auto restore_it = backups.lower_bound(timestamp_to_restore);
        if (restore_it == backups.end() || restore_it->first > timestamp_to_restore) {
            if (restore_it == backups.begin()) return ""; // No valid backup
            --restore_it;
        }

        const auto& [backup_state, backup_ttl] = restore_it->second;

        // Restore database from backup state
        database.clear();
        for (const auto& [key, fields] : backup_state) {
            for (const auto& [field, value_and_remaining] : fields) {
                database[key][field] = {value_and_remaining.first, timestamp};
            }
        }

        // Restore TTLs with recalculated expiration times
        ttl_data.clear();
        for (const auto& [key, fields] : backup_ttl) {
            for (const auto& [field, initial_expiry] : fields) {
                int remaining_ttl = initial_expiry - restore_it->first;
                ttl_data[key][field] = timestamp + remaining_ttl;
            }
        }

        return "";
    }
};
void level1() {
    L1InMemoryDatabase db;

    // Example queries
    std::vector<std::vector<std::string>> queries = {
        {"SET", "A", "B", "E"},
        {"SET", "A", "C", "F"},
        {"GET", "A", "B"},
        {"GET", "A", "D"},
        {"DELETE", "A", "B"},
        {"DELETE", "A", "D"}
    };

    // Execute and display query results
    for (const auto &query : queries) {
        std::cout << query[0] << " " << query[1] << " " << query[2];
        if (query[0] == "SET") {
            std::cout << " " << query[3] << "\t" << db.set(query[1], query[2], query[3]) << "\n";
        } else if (query[0] == "GET") {
            std::cout << "\t" << db.get(query[1], query[2]) << "\n";
        } else if (query[0] == "DELETE") {
            std::cout << "\t" << (db.delete_field(query[1], query[2]) ? "true" : "false") << "\n";
        }
        db.printDatabaseState();

    }

}
void level2() {
    L2InMemoryDatabase db;

    // Example queries
    std::vector<std::vector<std::string>> queries = {
        {"SET", "A", "BC", "E"},
        {"SET", "A", "BD", "F"},
        {"SET", "A", "C", "G"},
        {"SCAN_BY_PREFIX", "A", "B"},
        {"SCAN", "A"},
        {"SCAN_BY_PREFIX", "B", "B"}
    };

    // Execute and display query results
    for (const auto &query : queries) {
        std::cout << "Query: ";
        for (const auto &arg : query) {
            std::cout << arg << " ";
        }
        std::cout << "\t";

        std::string command = query[0];
        if (command == "SET") {
            std::cout << "Result: " << db.set(query[1], query[2], query[3]) << "\t";
        } else if (command == "GET") {
            std::cout << "Result: " << db.get(query[1], query[2]) << "\t";
        } else if (command == "DELETE") {
            std::cout << "Result: " << (db.delete_field(query[1], query[2]) ? "true" : "false") << "\t";
        } else if (command == "SCAN") {
            std::cout << "Result: " << db.scan(query[1]) << "\t";
        } else if (command == "SCAN_BY_PREFIX") {
            std::cout << "Result: " << db.scan_by_prefix(query[1], query[2]) << "\t";
        }
        std::cout << "\n";
    }
}
void level3() {
    L3InMemoryDatabase db;

    // Example queries
    std::vector<std::vector<std::string>> queries = {
        {"SET_AT_WITH_TTL", "A", "BC", "E", "1", "9"},
        {"SET_AT_WITH_TTL", "A", "BC", "E", "5", "10"},
        {"SET_AT", "A", "BD", "F", "5"},
        {"SCAN_BY_PREFIX_AT", "A", "B", "14"},
        {"SCAN_BY_PREFIX_AT", "A", "B", "15"},
        {"SET_AT", "A", "B", "C", "1"},
        {"SET_AT_WITH_TTL", "X", "Y", "Z", "2", "15"},
        {"GET_AT", "X", "Y", "3"},
        {"SET_AT_WITH_TTL", "A", "D", "E", "4", "10"},
        {"SCAN_AT", "A", "13"},
        {"SCAN_AT", "X", "16"},
        {"SCAN_AT", "X", "17"},
        {"DELETE_AT", "X", "Y", "20"}
    };

    // Execute and display query results
    for (const auto &query : queries) {
        std::string command = query[0];
        std::cout << "Query: ";
        for (const auto &arg : query) {
            std::cout << arg << " ";
        }
        std::cout << "\t";

        if (command == "SET_AT") {
            std::cout << db.set_at(query[1], query[2], query[3], std::stoi(query[4])) << "\t";
        } else if (command == "SET_AT_WITH_TTL") {
            std::cout << db.set_at_with_ttl(query[1], query[2], query[3], std::stoi(query[4]), std::stoi(query[5])) << "\t";
        } else if (command == "GET_AT") {
            std::cout << db.get_at(query[1], query[2], std::stoi(query[3])) << "\t";
        } else if (command == "DELETE_AT") {
            std::cout << db.delete_at(query[1], query[2], std::stoi(query[3])) << "\t";
        } else if (command == "SCAN_AT") {
            std::cout << db.scan_at(query[1], std::stoi(query[2])) << "\t";
        } else if (command == "SCAN_BY_PREFIX_AT") {
            std::cout << db.scan_by_prefix_at(query[1], query[2], std::stoi(query[3])) << "\t";
        }
        db.display();
    }
}

void level4() {
    L4InMemoryDatabase db;
    std::vector<std::vector<std::string>> queries = {
        {"SET_AT_WITH_TTL", "A", "B", "C", "1", "10"},
        {"BACKUP", "3"},
        {"SET_AT", "A", "D", "E", "4"},
        {"BACKUP", "5"},
        {"DELETE_AT", "A", "B", "8"},
        {"BACKUP", "9"},
        {"RESTORE", "10", "7"},
        {"BACKUP", "11"},
        {"SCAN_AT", "A", "15"},
        {"SCAN_AT", "A", "16"}
    };

    for (const auto& query : queries) {
        const std::string& command = query[0];
        if (command == "SET_AT_WITH_TTL") {
            std::cout << db.set_at_with_ttl(query[1], query[2], query[3], std::stoi(query[4]), std::stoi(query[5])) << "\n";
        } else if (command == "BACKUP") {
            std::cout << db.backup(std::stoi(query[1])) << "\n";
        } else if (command == "RESTORE") {
            std::cout << db.restore(std::stoi(query[1]), std::stoi(query[2])) << "\n";
        } else if (command == "SCAN_AT") {
            std::cout << db.scan_at(query[1], std::stoi(query[2])) << "\n";
        }
    }
}

int main() {
    //level1();
    //level2();
    //level3();
    level4();
    return 0;
}
