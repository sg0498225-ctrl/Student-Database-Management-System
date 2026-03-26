import json
import os

DATA_FILE = 'students.json'

def load_students():
    """Load students from JSON file."""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_students(students):
    """Save students to JSON file."""
    with open(DATA_FILE, 'w') as f:
        json.dump(students, f, indent=4)

def add_student(name, age, grade):
    """Add a new student."""
    students = load_students()
    student_id = max([s.get('id', 0) for s in students] or [0]) + 1
    student = {'id': student_id, 'name': name, 'age': age, 'grade': grade}
    students.append(student)
    save_students(students)
    return student_id

def get_all_students():
    """Get all students."""
    return load_students()

def delete_student(student_id):
    """Delete a student by ID."""
    students = load_students()
    students = [s for s in students if s['id'] != student_id]
    save_students(students)
    return True

def update_student(student_id, name, age, grade):
    """Update a student by ID."""
    students = load_students()
    for student in students:
        if student['id'] == student_id:
            student['name'] = name
            student['age'] = age
            student['grade'] = grade
            save_students(students)
            return True
    return False

def search_students(query):
    """Search students by name or ID."""
    students = load_students()
    query_lower = query.lower()
    return [s for s in students if query_lower in s['name'].lower() or str(s['id']) == query]
