import tempfile
import unittest
from src.db.backend.errors import TableNotFoundError
from src.db.backend.file import FileDatabase


class TestFileDatabase(unittest.TestCase):

    def test_data_is_saved_between_instances(self) -> None:
        """Проверка главного свойства: данные сохраняются между инстансами классов."""
        with tempfile.TemporaryDirectory() as directory:
            first_db = FileDatabase(directory)
            first_db.create_table("students", ("student_id", "name"))
            first_db.insert_record("students", {"student_id": 1, "name": "Ксения"})

            # Создаем второй инстанс, указывающий на ту же директорию
            second_db = FileDatabase(directory)
            records = second_db.select_records("students")

            self.assertEqual(records, [{"student_id": 1, "name": "Ксения"}])

    def test_select_with_filters(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db = FileDatabase(directory)
            db.create_table("students", ("student_id", "name"))
            db.insert_record("students", {"student_id": 1, "name": "Иван"})
            db.insert_record("students", {"student_id": 2, "name": "Мария"})

            records = db.select_records("students", name="Мария")
            self.assertEqual(records, [{"student_id": 2, "name": "Мария"}])

    def test_select_from_missing_table(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            db = FileDatabase(directory)
            with self.assertRaises(TableNotFoundError):
                db.select_records("non_existent_table")
