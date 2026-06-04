from abc import ABC, abstractmethod
from typing import Any
from .errors import TableAlreadyExistsError
from .table import Table


class Database(ABC):
    """Общий интерфейс СУБД."""

    def create_table(self, table_name: str, columns: tuple[str, ...]) -> None:
        if self._table_exists(table_name):
            raise TableAlreadyExistsError(f"Таблица '{table_name}' уже существует.")
        self._save_table(table_name, Table(columns))

    def insert_record(self, table_name: str, record: dict[str, Any]) -> None:
        table = self._load_table(table_name)
        table.insert_record(record)
        self._save_table(table_name, table)

    def select_records(self, table_name: str, **filters: Any) -> list[dict[str, Any]]:
        table = self._load_table(table_name)
        return table.select_records(**filters)

    def update_record(
        self, table_name: str, student_id: int, updated_data: dict[str, Any]
    ) -> dict[str, Any]:
        table = self._load_table(table_name)
        res = table.update_record(student_id, updated_data)
        self._save_table(table_name, table)
        return res

    def delete_record(self, table_name: str, student_id: int) -> dict[str, Any]:
        table = self._load_table(table_name)
        res = table.delete_record(student_id)
        self._save_table(table_name, table)
        return res

    @abstractmethod
    def _table_exists(self, table_name: str) -> bool:
        """Проверяет физическое или логическое существование таблицы."""
        pass

    @abstractmethod
    def _load_table(self, table_name: str) -> Table:
        """Загружает таблицу из источника данных."""
        pass

    @abstractmethod
    def _save_table(self, table_name: str, table: Table) -> None:
        """Сохраняет состояние таблицы в источник данных."""
        pass
