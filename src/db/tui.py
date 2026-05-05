from .backend.memory import create_record, select_record, update_record, delete_record

def _print_menu() -> None:
    print("\n=== База студентов ===")
    print("1. Добавить запись")
    print("2. Показать все записи")
    print("3. Найти записи по фильтру")
    print("4. Обновить запись")
    print("5. Удалить запись")
    print("0. Выход")

def _read_int(prompt: str) -> int:
    while True:
        raw = input(prompt).strip()
        try:
            return int(raw)
        except ValueError:
            print("Ошибка: введите целое число.")

def _read_optional_int(prompt: str) -> int | None:
    while True:
        raw = input(prompt).strip()
        if not raw: return None
        try:
            return int(raw)
        except ValueError:
            print("Ошибка: введите число или Enter.")

def _add_student() -> None:
    print("\nДобавление")
    sid = _read_int("id: ")
    fn = input("Имя: ").strip()
    sn = input("Фамилия: ").strip()
    age = _read_int("Возраст: ")
    sex = input("Пол: ").strip()
    try:
        rec = create_record(sid, fn, sn, age, sex)
        print(f"Добавлено: {rec}")
    except ValueError as e:
        print(f"Ошибка: {e}")

def _show_all_students() -> None:
    recs = select_record()
    if not recs:
        print("Пусто")
    for r in recs:
        print(r)

def _find_students_by_filter() -> None:
    print("\nПоиск (Enter = пропустить)")
    sid = _read_optional_int("id: ")
    fn = input("Имя: ").strip() or None
    sn = input("Фамилия: ").strip() or None
    age = _read_optional_int("Возраст: ")
    sex = input("Пол: ").strip() or None
    recs = select_record(sid, fn, sn, age, sex)
    for r in recs: print(r)

def _update_student() -> None:
    sid = _read_int("\nid для изменения: ")
    print("Новые данные (Enter = пропустить)")
    fn = input("Имя: ").strip()
    sn = input("Фамилия: ").strip()
    age = _read_optional_int("Возраст: ")
    sex = input("Пол: ").strip()
    data = {}
    if fn: data['first_name'] = fn
    if sn: data['second_name'] = sn
    if age: data['age'] = age
    if sex: data['sex'] = sex
    if update_record(sid, **data):
        print("Обновлено")
    else:
        print("Не найден")

def _delete_student() -> None:
    sid = _read_int("\nid для удаления: ")
    if delete_record(sid):
        print("Удалено")
    else:
        print("Не найден")

def run() -> None:
    while True:
        _print_menu()
        cmd = input("Действие: ").strip()
        if cmd == "1": _add_student()
        elif cmd == "2": _show_all_students()
        elif cmd == "3": _find_students_by_filter()
        elif cmd == "4": _update_student()
        elif cmd == "5": _delete_student()
        elif cmd == "0": break
        else: print("Ошибка команды")