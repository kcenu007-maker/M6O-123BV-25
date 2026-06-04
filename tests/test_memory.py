import unittest
from src.db.backend.memory import MemoryDatabase, StudentTable
from src.db.backend.errors import (
    InvalidAgeError,
    DuplicateIDError,
    UnknownID,
    MissingColumnError,
    UnknownColumnError,
    TableAlreadyExistsError,
    TableNotFoundError,
)

class TestMemoryDatabaseAndCompatibility(unittest.TestCase):

    def setUp(self) -> None:
        
        self.student_table = StudentTable()
        self.db = MemoryDatabase()
        self.table_name = "students"
        self.columns = ("student_id", "first_name", "second_name", "age", "sex")
        self.db.create_table(self.table_name, self.columns)

    
    def test_create_record_success(self) -> None:
        record = self.student_table.create_record(1, "Ivan", "Ivanov", 20, "M")
        self.assertEqual(record, (1, "Ivan", "Ivanov", 20, "M"))

    def test_create_record_invalid_age(self) -> None:
        with self.assertRaises(InvalidAgeError):
            self.student_table.create_record(1, "Ivan", "Ivanov", -1, "M")

    def test_create_record_duplicate_id(self) -> None:
        self.student_table.create_record(1, "Ivan", "Ivanov", 20, "M")
        with self.assertRaises(DuplicateIDError):
            self.student_table.create_record(1, "Petr", "Petrov", 21, "M")

    def test_select_record_by_id(self) -> None:
        self.student_table.create_record(1, "Ivan", "Ivanov", 20, "M")
        records = self.student_table.select_record(student_id=1)
        self.assertEqual(records, [(1, "Ivan", "Ivanov", 20, "M")])

    def test_select_record_not_found(self) -> None:
        self.student_table.create_record(1, "Ivan", "Ivanov", 20, "M")
        records = self.student_table.select_record(student_id=2)
        self.assertEqual(records, [])

    def test_update_record_success(self) -> None:
        self.student_table.create_record(1, "Ivan", "Ivanov", 20, "M")
        updated = self.student_table.update_record(1, "Ivan", "Ivanov", 21, "M")
        self.assertEqual(updated, (1, "Ivan", "Ivanov", 21, "M"))

    def test_update_record_not_found(self) -> None:
        with self.assertRaises(UnknownID):
            self.student_table.update_record(999, "Ivan", "Ivanov", 21, "M")

    def test_delete_record_success(self) -> None:
        self.student_table.create_record(1, "Ivan", "Ivanov", 20, "M")
        deleted = self.student_table.delete_record(1)
        self.assertEqual(deleted, (1, "Ivan", "Ivanov", 20, "M"))

    def test_delete_record_not_found(self) -> None:
        with self.assertRaises(UnknownID):
            self.student_table.delete_record(999)

    def test_select_record_filter(self) -> None:
        test_datas = [
            (1, "Ivan", "Ivanov", 20, "M"),
            (2, "Petr", "Petrov", 21, "M"),
            (3, "Anna", "Sidorova", 20, "F"),
        ]
        for data in test_datas:
            self.student_table.create_record(*data)

        cases = [
            {"name": "filter by sex", "filters": {"sex": "M"}, "expected": [test_datas[0], test_datas[1]]},
            {"name": "filter by age", "filters": {"age": 20}, "expected": [test_datas[0], test_datas[2]]},
            {"name": "filter by both", "filters": {"age": 20, "sex": "F"}, "expected": [test_datas[2]]},
        ]

        for case in cases:
            with self.subTest(case=case["name"], filters=case["filters"]):
                records = self.student_table.select_record(**case["filters"])
                self.assertEqual(records, case["expected"])

    
    def test_create_table_already_exists(self) -> None:
        with self.assertRaises(TableAlreadyExistsError):
            self.db.create_table(self.table_name, self.columns)

    def test_operations_on_missing_table(self) -> None:
        with self.assertRaises(TableNotFoundError):
            self.db.select_records("non_existent_table")


    def test_insert_missing_column(self) -> None:
        incomplete_record = {"student_id": 5, "first_name": "Ivan"}
        with self.assertRaises(MissingColumnError):
            self.db.insert_record(self.table_name, incomplete_record)

    def test_insert_unknown_column(self) -> None:
        extra_record = {"student_id": 5, "first_name": "A", "second_name": "B", "age": 20, "sex": "M", "extra": 1}
        with self.assertRaises(UnknownColumnError):
            self.db.insert_record(self.table_name, extra_record)

    def test_select_unknown_filter(self) -> None:
        with self.assertRaises(UnknownColumnError):
            self.db.select_records(self.table_name, unknown_field="test")
