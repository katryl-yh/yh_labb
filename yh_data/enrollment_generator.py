import csv
import random
from datetime import datetime
from pathlib import Path

# Get the parent folder of the current script
parent_folder = Path(__file__).resolve().parent  

# -------------------------------
# Configuration and lookup
# -------------------------------

# Grade options
grades = ["IG", "G", "VG"]
not_set_ids = {37, 38, 41, 45, 48, 49, 50, 51, 52, 53}
no_enrollment_ids = {54, 55}

# Student ID ranges per class
class_students = {
    1: range(1, 11),
    2: range(11, 21),
    3: range(21, 31),
    4: range(31, 41),
    5: range(41, 51),
}

# Special rule: course_id=37, offering_id=1 → students 5–24
special_course_37_students = range(5, 25)
# course_id=38, offering_id=17 → students 31–50
special_course_38_students = range(31, 51)

# -------------------------------
# Load Course Offerings from CSV
# -------------------------------

course_offerings = []

with open(parent_folder / 'Course_offering.csv', mode='r', newline='', encoding='utf-8') as file:
    reader = csv.DictReader(file, delimiter=',')
    for row in reader:
        course_offerings.append({
            'offering_id': int(row['offering_id']),
            'course_id': int(row['course_id']),
            'term': row['term'],
            'year': int(row['year']),
            'student_limit': int(row['student_limit']),
            'campus_id': int(row['campus_id']),
            'teacher_id': int(row['teacher_id']),
            'class_id': int(row['class_id'])
        })

# -------------------------------
# Generate Enrollments
# -------------------------------

enrollments = []

for offering in course_offerings:
    offering_id = offering['offering_id']
    course_id = offering['course_id']
    term = offering['term']
    year = offering['year']
    limit = offering['student_limit']
    campus_id = offering['campus_id']
    teacher_id = offering['teacher_id']
    class_id = offering['class_id']

    # Skip offerings that shouldn't have enrollments yet
    if offering_id in no_enrollment_ids:
        continue

    # Determine which students should be enrolled
    if offering_id == 1:
        student_ids = special_course_37_students
    elif offering_id == 17:
        student_ids = special_course_38_students
    elif class_id in class_students:
        student_ids = class_students[class_id]
    else:
        continue  # No valid students for this offering

    # Apply limit if needed (optional based on business rules)
    for student_id in student_ids:
        grade = "NOT SET" if offering_id in not_set_ids else random.choice(grades)
        grade_update = datetime.now().strftime("%Y-%m-%d")
        enrollments.append((student_id, offering_id, grade, grade_update))

# -------------------------------
# Write Enrollments to CSV
# -------------------------------

with open(parent_folder / 'Enrollment.csv', mode='w', newline='', encoding='utf-8') as file:
    fieldnames = ['student_id', 'offering_id', 'grade', 'grade_update']
    writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=',')

    writer.writeheader()
    for student_id, offering_id, grade, grade_update in enrollments:
        writer.writerow({
            'student_id': student_id,
            'offering_id': offering_id,
            'grade': grade,
            'grade_update': grade_update
        })

print("Enrollment.csv generated successfully.")
