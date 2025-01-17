import mysql.connector
import json
from datetime import datetime
import Levenshtein

class MySQLDatabase:
    def __init__(self, host, user, password, database):
        # Инициализация объекта базы данных
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None

    def connect(self):
        # Подключение к базе данных MySQL
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor(dictionary=True)

    def close(self):
        # Закрытие соединения с базой данных MySQL
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()

    def create_table(self, table_name, columns):
        # Создание таблицы с указанными столбцами
        self.connect()
        columns_with_types = ", ".join([f"{column} {data_type}" for column, data_type in columns.items()])
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_with_types})"
        self.cursor.execute(query)
        self.connection.commit()
        self.close()

    def insert_record(self, table_name, record):
        # Вставка новой записи в таблицу
        self.connect()
        placeholders = ", ".join(["%s"] * len(record))
        columns = ", ".join([f"`{column}`" for column in record.keys()])  # Добавляем обратные кавычки для экранирования колонок
        values = tuple(json.dumps(v) if isinstance(v, (list, dict)) else v for v in record.values())
        query = f"INSERT INTO `{table_name}` ({columns}) VALUES ({placeholders})"
        self.cursor.execute(query, values)
        self.connection.commit()
        self.close()


    def update_record(self, table_name, conditions, updates):
        # Обновление записи в таблице по указанным условиям
        self.connect()
        # Добавляем экранирование обратными кавычками для всех колонок
        set_clause_parts = [f"`{column}` = %s" for column, value in updates.items() if value is not None]
        set_clause = ", ".join(set_clause_parts)
        condition_clause = " AND ".join([f"`{column}` = %s" for column in conditions.keys()])
        
        values = tuple(json.dumps(v) if isinstance(v, (list, dict)) else v for v in updates.values() if v is not None)
        condition_values = tuple(conditions.values())
        
        query = f"UPDATE `{table_name}` SET {set_clause} WHERE {condition_clause}"
        
        self.cursor.execute(query, values + condition_values)
        self.connection.commit()
        self.close()
    def get_all_records(self, table_name):
        self.connect()
        query = f"SELECT * FROM {table_name}"
        self.cursor.execute(query)
        results = self.cursor.fetchall()
        self.close()

        return results
    def get_records_between_dates(self, table_name, start_date, end_date):
        self.connect()
        # Формируем SQL-запрос для поиска записей между двумя датами
        query = f"""
        SELECT * FROM {table_name} 
        WHERE `date_check` BETWEEN %s AND %s
        """
        
        # Выполняем запрос с параметрами (start_date и end_date)
        self.cursor.execute(query, (start_date, end_date))
        
        # Получаем результаты
        results = self.cursor.fetchall()
        
        self.close()

        return results
    def update_record_none(self, table_name, conditions, updates):
        # Обновление записи в таблице с обновлением всех полей
        self.connect()
        set_clause_parts = [f"{column} = %s" for column in updates.keys()]
        set_clause = ", ".join(set_clause_parts)
        condition_clause = " AND ".join([f"{column} = %s" for column in conditions.keys()])
        values = tuple(json.dumps(v) if isinstance(v, (list, dict)) else v for v in updates.values())
        condition_values = tuple(conditions.values())
        query = f"UPDATE {table_name} SET {set_clause} WHERE {condition_clause}"
        self.cursor.execute(query, values + condition_values)
        self.connection.commit()
        self.close()

    def find_record_by_single_field(self, table_name, field, value):
        # Поиск записи в таблице по одному полю
        self.connect()
        query = f"SELECT * FROM {table_name} WHERE {field} = %s"
        self.cursor.execute(query, (value,))
        results = self.cursor.fetchall()
        self.close()
        
        if results:
            return results
        else:
            return False

    def find_record_by_multiple_fields(self, table_name, conditions):
        # Поиск записи в таблице по нескольким полям
        self.connect()
        condition_clause = " AND ".join([f"{column} = %s" for column in conditions.keys()])
        values = tuple(conditions.values())
        query = f"SELECT * FROM {table_name} WHERE {condition_clause}"
        self.cursor.execute(query, values)
        results = self.cursor.fetchall()
        self.close()

        if results:
            return results
        else:
            return False

    def find_record_by_array_field(self, table_name, field, value):
        # Поиск записи в таблице по значению в массиве (JSON)
        self.connect()
        query = f"SELECT * FROM {table_name} WHERE JSON_CONTAINS({field}, %s)"
        self.cursor.execute(query, (json.dumps(value),))
        results = self.cursor.fetchall()
        self.close()

        if results:
            return results
        else:
            return False

    def get_array_field(self, table_name, field, conditions):
        # Получение значения массива (JSON) по указанным условиям
        self.connect()
        condition_clause = " AND ".join([f"{column} = %s" for column in conditions.keys()])
        values = tuple(conditions.values())
        query = f"SELECT {field} FROM {table_name} WHERE {condition_clause}"
        self.cursor.execute(query, values)
        results = self.cursor.fetchall()
        self.close()

        arrays = []
        if results:
            for result in results:
                if result[field]:
                    arrays.append(json.loads(result[field]))
        return arrays

    def find_record_by_value_in_array(self, table_name, field, value):
        # Поиск записи по значению в массиве (JSON) с использованием JSON_CONTAINS
        self.connect()
        query = f"SELECT * FROM {table_name} WHERE JSON_CONTAINS({field}, %s)"
        self.cursor.execute(query, (json.dumps(value),))
        results = self.cursor.fetchall()
        self.close()

        if results:
            return results
        else:
            return False

    def find_similar_records(self, table_name, search_criteria, threshold=0.8):
        """
        Поиск записей, схожих по нескольким критериям.

        :param table_name: Название таблицы.
        :param search_criteria: Словарь {поле: значение} для поиска.
        :param threshold: Порог схожести (по умолчанию 0.8).
        :return: Список схожих записей.
        """
        self.connect()
        query = f"SELECT * FROM {table_name}"
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        self.close()

        similar_records = []
        for record in records:
            similarity_scores = []
            for field, search_value in search_criteria.items():
                if field in record and isinstance(record[field], str) and isinstance(search_value, str):
                    similarity = Levenshtein.ratio(record[field], search_value)
                    similarity_scores.append(similarity)

            # Calculate the average similarity score for all criteria
            if similarity_scores:
                average_similarity = sum(similarity_scores) / len(similarity_scores)
                if average_similarity > threshold:
                    similar_records.append(record)
        return similar_records

    def delete_record_by_id(self, table_name, record_id):
        # Удаление записи по идентификатору (id)
        self.connect()
        query = f"DELETE FROM {table_name} WHERE id = %s"
        self.cursor.execute(query, (record_id,))
        self.connection.commit()
        self.close()

    def update_teams_main(self, teamlist_id, index1, index2):
        # Обновление массива teams_main в записи по идентификатору, меняя значения местами
        self.connect()
        
        # Шаг 1: Получение текущего массива teams_main
        query = "SELECT teams_main FROM teamlists WHERE id = %s"
        self.cursor.execute(query, (teamlist_id,))
        result = self.cursor.fetchone()

        if not result:
            print(f"No record found with id {teamlist_id}")
            self.close()
            return

        teams_main = json.loads(result['teams_main'])

        # Шаг 2: Замена значений местами
        if 0 <= index1 < len(teams_main) and 0 <= index2 < len(teams_main):
            teams_main[index1], teams_main[index2] = teams_main[index2], teams_main[index1]
        else:
            print(f"Invalid indices {index1} or {index2} for teams_main array")
            self.close()
            return

        # Шаг 3: Обновление записи в базе данных
        query = "UPDATE teamlists SET teams_main = %s WHERE id = %s"
        self.cursor.execute(query, (json.dumps(teams_main), teamlist_id))
        self.connection.commit()

        self.close()
db = MySQLDatabase(host="localhost", user="loer", password="Vfn21450-", database="application")
db.connect()