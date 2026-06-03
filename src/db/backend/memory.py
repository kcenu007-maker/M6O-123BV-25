from .database import Database
from .errors import TableNotFoundError
from .table import Table
from typing import Any


class MemoryDatabase(Database):
    """База данных в оперативной памяти."""

    def __init__(self) -> None:
        self.tables: dict[str, Table] = {}

    def _table_exists(self, table_name: str) -> bool:
        return table_name in self.tables

    def _load_table(self, table_name: str) -> Table:
        if table_name not in self.tables:
            raise TableNotFoundError(f"Таблица '{table_name}' не существует.")
        return self.tables[table_name]

    def _save_table(self, table_name: str, table: Table) -> None:
        self.tables[table_name] = table


# КЛАСС-ОБЕРТКА ДЛЯ СОВМЕСТИМОСТИ С СТАРЫМИ ТЕСТАМИ ИЗ ЛАБОРАТОРНОЙ №3
class StudentTable:
    def __init__(self):
        self.db = MemoryDatabase()
        self.table_name = "students"
        self.db.create_table(
            self.table_name, ("student_id", "first_name", "second_name", "age", "sex")
        )

    def create_record(self, student_id, first_name, second_name, age, sex):
        record = {
            "student_id": student_id,
            "first_name": first_name,
            "second_name": second_name,
            "age": age,
            "sex": sex,
        }
        self.db.insert_record(self.table_name, record)
        return (student_id, first_name, second_name, age, sex)

    def select_record(
        self, student_id=None, first_name=None, second_name=None, age=None, sex=None
    ):
        filters = {}
        if student_id is not None:
            filters["student_id"] = student_id
        if first_name is not None:
            filters["first_name"] = first_name
        if second_name is not None:
            filters["second_name"] = second_name
        if age is not None:
            filters["age"] = age
        if sex is not None:
            filters["sex"] = sex

        records = self.db.select_records(self.table_name, **filters)
        return [
            (r["student_id"], r["first_name"], r["second_name"], r["age"], r["sex"])
            for r in records
        ]

    def update_record(self, student_id, first_name, second_name, age, sex):
        updated_data = {
            "first_name": first_name,
            "second_name": second_name,
            "age": age,
            "sex": sex,
        }
        r = self.db.update_record(self.table_name, student_id, updated_data)
        return (r["student_id"], r["first_name"], r["second_name"], r["age"], r["sex"])

    def delete_record(self, student_id):
        r = self.db.delete_record(self.table_name, student_id)
        return (r["student_id"], r["first_name"], r["second_name"], r["age"], r["sex"])
