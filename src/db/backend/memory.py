_records = []

def create_record(student_id: int, first_name: str, second_name: str, age: int, sex: str) -> tuple:
    if any(r[0] == student_id for r in _records):
        raise ValueError(f"Студент с id {student_id} уже существует")
    record = (student_id, first_name, second_name, age, sex)
    _records.append(record)
    return record

def select_record(student_id=None, first_name=None, second_name=None, age=None, sex=None) -> list:
    result = _records
    if student_id is not None:
        result = [r for r in result if r[0] == student_id]
    if first_name is not None:
        result = [r for r in result if r[1].lower() == first_name.lower()]
    if second_name is not None:
        result = [r for r in result if r[2].lower() == second_name.lower()]
    if age is not None:
        result = [r for r in result if r[3] == age]
    if sex is not None:
        result = [r for r in result if r[4].lower() == sex.lower()]
    return result

def update_record(student_id: int, **kwargs) -> bool:
    for i, record in enumerate(_records):
        if record[0] == student_id:
            curr = list(record)
            if 'first_name' in kwargs: curr[1] = kwargs['first_name']
            if 'second_name' in kwargs: curr[2] = kwargs['second_name']
            if 'age' in kwargs: curr[3] = kwargs['age']
            if 'sex' in kwargs: curr[4] = kwargs['sex']
            _records[i] = tuple(curr)
            return True
    return False

def delete_record(student_id: int) -> bool:
    global _records
    old_len = len(_records)
    _records = [r for r in _records if r[0] != student_id]
    return len(_records) < old_len