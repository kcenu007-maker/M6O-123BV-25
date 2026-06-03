from typing import Any
from .errors import (
    MissingColumnError,
    UnknownColumnError,
    InvalidAgeError,
    DuplicateIDError,
    UnknownID,
)


class Table:
    """Таблица с фиксированным набором колонок и валидацией бизнес-логики."""

    def __init__(
        self, columns: tuple[str, ...], records: list[dict[str, Any]] | None = None
    ) -> None:
        self.columns = columns
        self.records: list[dict[str, Any]] = []

        if records is not None:
            for record in records:
                self.insert_record(record)

    def insert_record(self, record: dict[str, Any]) -> None:
        """Добавляет запись, если она соответствует схеме и правилам валидации."""
        # Валидация схемы колонок
        missing_columns = [column for column in self.columns if column not in record]
        if missing_columns:
            raise MissingColumnError(
                f"Отсутствует поле '{missing_columns[0]}' в записи."
            )

        extra_columns = [column for column in record if column not in self.columns]
        if extra_columns:
            raise UnknownColumnError(
                f"Поле '{extra_columns[0]}' не определено в структуре."
            )

        # Специфичная валидация из лабораторной №3 (Проверка возраста и дубликатов ID)
        if "age" in record and record["age"] < 0:
            raise InvalidAgeError("Поле age не может быть отрицательным.")

        if "student_id" in record:
            if any(r.get("student_id") == record["student_id"] for r in self.records):
                raise DuplicateIDError(
                    f"Запись с id={record['student_id']} уже существует."
                )

        self.records.append(record.copy())

    def select_records(self, **filters: Any) -> list[dict[str, Any]]:
        """Возвращает список записей, удовлетворяющих фильтрам."""
        unknown_filters = [key for key in filters if key not in self.columns]
        if unknown_filters:
            raise UnknownColumnError(
                f"Поле '{unknown_filters[0]}' не определено в фильтрах."
            )

        if not filters:
            return [record.copy() for record in self.records]

        result: list[dict[str, Any]] = []
        for record in self.records:
            if all(record.get(key) == value for key, value in filters.items()):
                result.append(record.copy())
        return result

    def update_record(
        self, student_id: int, updated_data: dict[str, Any]
    ) -> dict[str, Any]:
        """Обновляет запись по её student_id."""
        if "age" in updated_data and updated_data["age"] < 0:
            raise InvalidAgeError("Поле age не может быть отрицательным.")

        for i, record in enumerate(self.records):
            if record.get("student_id") == student_id:
                # Формируем новую запись
                new_record = {"student_id": student_id}
                for col in self.columns:
                    if col != "student_id":
                        new_record[col] = updated_data.get(col, record.get(col))
                self.records[i] = new_record
                return self.records[i].copy()

        raise UnknownID(f"Поле с ID {student_id} не найдено")

    def delete_record(self, student_id: int) -> dict[str, Any]:
        """Удаляет запись по её student_id."""
        for i, record in enumerate(self.records):
            if record.get("student_id") == student_id:
                return self.records.pop(i)

        raise UnknownID(f"Поле с ID {student_id} не найдено")
