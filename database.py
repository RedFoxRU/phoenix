import sqlite3


def get_table_schema(cursor, table_name):
    cursor.execute(f"PRAGMA table_info({table_name});")
    return [row[1] for row in cursor.fetchall()]

def find_duplicates(cursor, table_name, tgid_column):
    cursor.execute(f"SELECT {tgid_column}, COUNT(*) as count FROM {table_name} GROUP BY {tgid_column} HAVING COUNT(*) > 1;")
    return cursor.fetchall()

def merge_duplicates(cursor, table_name, tgid_column, columns_to_merge):
    for tgid_value, _ in find_duplicates(cursor, table_name, tgid_column):
        cursor.execute(f"SELECT * FROM {table_name} WHERE {tgid_column} = ?;", (tgid_value,))
        rows_to_merge = cursor.fetchall()

        if len(rows_to_merge) > 1:
            first_row = rows_to_merge[0]
            for row in rows_to_merge[1:]:
                merged_row = [row[i] if row[i] is not None else first_row[i] for i in range(len(row))]
                cursor.execute(f"DELETE FROM {table_name} WHERE {tgid_column} = ?;", (tgid_value,))
                cursor.execute(f"INSERT OR REPLACE INTO {table_name} VALUES ({', '.join(['?']*len(merged_row))});", merged_row)

def main(database_path):
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()
    
    table_name = "user"  # Имя таблицы "user"
    tgid_column = "tgid"  # Замените на имя столбца tgid в вашей таблице
    columns_to_merge = get_table_schema(cursor, table_name)

    duplicates = find_duplicates(cursor, table_name, tgid_column)
    if duplicates:
        print(f"Found {len(duplicates)} duplicates in {table_name}.")
        merge_duplicates(cursor, table_name, tgid_column, columns_to_merge)
        print(f"Merged duplicates in {table_name}.")
    else:
        print(f"No duplicates found in {table_name}.")
    
    connection.commit()
    connection.close()

if __name__ == "__main__":
    database_path = "database.db"  # Замените на путь к вашей базе данных SQLite
    main(database_path)
