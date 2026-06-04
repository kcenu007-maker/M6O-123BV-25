from src.db.backend.file import FileDatabase
from src.db.backend.memory import MemoryDatabase
from src.db.backend.errors import DatabaseError, StudentTableError


def main_menu():
    print("Выберите тип базы данных:")
    print("1. In-memory (Оперативная память)")
    print("2. File database (Файловое хранилище JSON)")

    db_choice = input("Введите номер: ").strip()
    if db_choice == "2":
        db = FileDatabase()
        print("Используется: Файловая БД.")
    else:
        db = MemoryDatabase()
        print("Используется: In-memory БД.")

    table_name = "students"

    try:
        db.create_table(
            table_name, ("student_id", "first_name", "second_name", "age", "sex")
        )
    except Exception:
        pass

    while True:
        print("\n1. Добавить 2. Показать 3. Обновить 4. Удалить 0. Выход")
        choice = input("Действие: ").strip()

        try:
            if choice == "1":
                record = {
                    "student_id": int(input("ID: ")),
                    "first_name": input("Имя: "),
                    "second_name": input("Фамилия: "),
                    "age": int(input("Возраст: ")),
                    "sex": input("Пол: "),
                }
                db.insert_record(table_name, record)
                print("Запись успешно добавлена.")
                if db_choice == "2":
                    print(f"Проверь файл по пути: {db._get_table_path(table_name)}")

            elif choice == "2":
                records = db.select_records(table_name)
                if not records:
                    print("Таблица пуста.")
                for r in records:
                    print(
                        (
                            r["student_id"],
                            r["first_name"],
                            r["second_name"],
                            r["age"],
                            r["sex"],
                        )
                    )

            elif choice == "3":
                student_id = int(input("ID для обновления: "))
                updated_data = {
                    "first_name": input("Новое имя: "),
                    "second_name": input("Новая фамилия: "),
                    "age": int(input("Возраст: ")),
                    "sex": input("Пол: "),
                }
                db.update_record(table_name, student_id, updated_data)
                print("Запись обновлена.")

            elif choice == "4":
                student_id = int(input("ID для удаления: "))
                db.delete_record(table_name, student_id)
                print("Запись удалена.")

            elif choice == "0":
                print("До свидания!")
                break
        except (ValueError, DatabaseError, StudentTableError) as e:
            print(f"Ошибка: {e}")


if __name__ == "__main__":
    main_menu()
