import csv
import random

def generate_enrollment_csv(filename="enrollment.csv"):
    """Generates enrollment data and saves it to a CSV file."""

    enrollments = []

    # DE23 (Class 1)
    for student_id in range(1, 11):
        for offering_id in range(1, 13):
            grade_id = random.choice([1, 2, 3])
            enrollments.append([student_id, offering_id, grade_id])

    # BIM23 (Class 3)
    for student_id in range(11, 21):
        for offering_id in range(13, 26):
            grade_id = random.choice([1, 2, 3])
            enrollments.append([student_id, offering_id, grade_id])

    # DE24 (Class 2)
    for student_id in range(1, 11):
        for offering_id in range(26, 32):
            grade_id = random.choice([1, 2, 3])
            enrollments.append([student_id, offering_id, grade_id])

    # BIM24 (Class 4)
    for student_id in range(16, 26): # corrected range
        for offering_id in range(32, 41):
            grade_id = random.choice([1, 2, 3])
            enrollments.append([student_id, offering_id, grade_id])

    # UX24 (Class 5)
    for student_id in range(21, 31): # corrected range
        for offering_id in range(41, 47):
            grade_id = random.choice([1, 2, 3])
            enrollments.append([student_id, offering_id, grade_id])

    # stand alone course 38, location 1 and 2
    for student_id in range(26,31):
        enrollments.append([student_id, 47, random.choice([1,2,3])])
    for student_id in range (36,41):
        enrollments.append([student_id,48, random.choice([1,2,3])])
    for student_id in range(46,51):
        enrollments.append([student_id,47, random.choice([1,2,3])])
    for student_id in range (41,46):
        enrollments.append([student_id,48, random.choice([1,2,3])])

    with open(filename, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["student_id", "offering_id", "grade_id"])  # Header
        writer.writerows(enrollments)

generate_enrollment_csv()
print(f"enrollment.csv generated successfully.")