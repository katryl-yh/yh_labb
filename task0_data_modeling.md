## YrkesCo - Database Design and Data Modeling Lab

---
### Background

YrkesCo currently relies on spreadsheets and decentralized systems to track students, educators, programs, and operational units. 
This results in data fragmentation, redundancy, and limited reporting capabilities. 
A centralized relational database ensures better control, GDPR compliance, and scalable access to accurate information.

---

### Problem Description

YrkesCo needs to manage:

- Student and staff personal data
- Courses and program structures
- Teacher roles and consultant contracts
- Campus and location data
- Enrollments and grading
- Data privacy (GDPR)
- Role exclusivity within the organization

---


Below are final requirements, based on provided description and other rulers that I identified:

**Student**
- First name, last name, email, and personal identification number.
- Each student must belong to a class (even if applying for a standalone course).
- School does not track the historical changes of classes that the student belonged to. 

**Teacher**
- Can be a permanent employee (BONUS) or an external consultant.
- Permanent instructor is always directly employed by YrkesCo.

**Education Manager**
- Has the same base info as instructors (name, email, personal number).
- Is always permanent staff, hired directly by the school.
- Each manager can manage up to 3 classes.
- A manager does not teach!

**Courses & Programs**
- A program consists of multiple courses and is an abstract educational unit.
- Program may be offered across multiple school locations.
- When a program is approved, it always has an allowed number of program iterations, each resulting in a class.
- A class is a tangible instance of a program and inherits all its courses.
- Course has a name, course code, number of credits, and a short description.
- Standalone courses are also available (BONUS), but students must belong to a class to enroll.

**Consultant**
- Their company details are stored, including organization number, F-tax status, address, and hourly rate.

**Campus**
- YrkesCo currently operates in Gothenburg and Stockholm, with potential expansion.
- Online classes/courses are also available and assigned to a “virtual campus”.

### Other Business Rules

1. **Programs and Courses are Abstract**
   - Programs can be offered at multiple school locations.
   - Courses linked to a program are also abstract; course offerings make them tangible.

2. **Class = Tangible Program Instance**
   - Each class inherits its program's courses and is tied to a specific location.

3. **Course Offering = Specific Teaching Instance**
   - Can belong to a program or be standalone.
   - Linked to a class, if it belongs to a program.
   - Linked to a location and a teacher.

4. **Student Enrollment**
   - Students must belong to a class, even when applying for standalone courses.

5. **Private Information**
   - Stored in separate entities for students, education managers, and teachers in order to comply with GDPR rules.
   - Personal number is linked to a government register; address is retrieved from there.

6. **Role Restrictions**
   - Education managers can’t teach classes.
   - Teachers cannot be class managers.
   - Enforced using database triggers.
   - A person cannot have several positions within the school: Student / Education Manager / Teacher

### Entity Overview (with Attributes) and Design Rationale 

#### 🧍 Person
Stores general identity information for all individuals.
- `person_id` (PK)
- `first_name`
- `last_name`
- `school_email` (UNIQUE)
- `personal_email` (UNIQUE)

> 🔒 Note: Role exclusivity enforced with constraints/triggers.
> Note 2: MVP will exclude `personal_email` for simpliciy 


#### 🧑‍🎓 Student
Represents students at YrkesCo.
- `student_id` (PK)
- `person_id` (FK → Person)
- `class_id` (FK → Class) **NOT NULL**



#### 🔒 Private_Student
Holds GDPR-sensitive information for students.
- `student_id` (PK, FK → Student)
- `personal_number` (UNIQUE)


#### 👩‍🏫 Teacher
Captures both consultants and permanent teachers.
- `teacher_id` (PK)
- `person_id` (FK → Person)
- `company_id` (FK → Company)
- `employment_type`: `'permanent: full-time'`, `'permanent: part-time'`, `'consultant'`, `'temporary'`


#### 🔒 Private_Teacher
- `teacher_id` (PK, FK → Teacher)
- `personal_number` (UNIQUE)


#### 👩‍💼 Education_Manager
Non-teaching role with class management duties.
- `manager_id` (PK)
- `person_id` (FK → Person)
- `company_id` (FK → Company)
- `employment_type`: Always `'permanent'`


#### 🔒 Private_Education_Manager
- `manager_id` (PK, FK → Education_Manager)
- `personal_number` (UNIQUE)


#### 🏢 Company
Represents both YrkesCo itself and external partners.
- `company_id` (PK)
- `company_name`
- `organization_number`
- `is_F_tax` (BOOLEAN)
- `hourly_rate`
- `address_id` (FK → Address)

> 💡 Check constraint: internal companies must have hourly_rate = 0.


#### 🏠 Address
Normalized address data reused across entities.
- `address_id` (PK)
- `street`
- `building_number`
- `postal_code`
- `city_id` (FK → City)


#### 🏙️ City
Reusable geographical info.
- `city_id` (PK)
- `city_name`
- `country_name`


#### 🎓 Program
Abstract representation of a study track.
- `program_id` (PK)
- `program_name`
- `program_duration_years`
- `total_credits`
- `approved_iterations`


#### 🧑‍🏫 Class
Tangible instance of a Program offering.
- `class_id` (PK)
- `class_name`
- `program_id` (FK → Program)
- `iteration_number`
- `manager_id` (FK → Education_Manager)
- `campus_id` (FK → Campus)
- `status`: `'to open'`, `'ongoing'`, `'graduated'`, `'cancelled'`

> ⚠️ A manager can only manage 3 classes – enforced with a constraint.


#### 📘 Course
Abstract unit of study.
- `course_id` (PK)
- `course_name`
- `course_code` (UNIQUE)
- `course_credits`
- `course_description`


#### 📅 Course_Offering
A course taught in a specific term/year/location.
- `offering_id` (PK)
- `course_id` (FK → Course)
- `term`: ENUM `'VT'`, `'HT'`, `'ST'`
- `year`: INT (YYYY)
- `student_limit`
- `campus_id` (FK → Campus)
- `linked_class_id` (FK → Class) — `NULL` if standalone
- `teacher_id` (FK → Teacher)


#### 🏫 Campus
Location or virtual site of education delivery.
- `campus_id` (PK)
- `campus_name`
- `address_id` (FK → Address)


#### 📎 program_course
Join table to associate programs with their courses.
- `program_id` (PK, FK → Program)
- `course_id` (PK, FK → Course)


#### 📄 Enrollment
Represents a student's participation in a course.
- `student_id` (PK, FK → Student)
- `course_offering_id` (PK, FK → Course_Offering)
- `grade`: ENUM `'NOT SET'`, `'IG'`, `'G'`, `'VG'`
- `grade_update`: TIMESTAMP (nullable)


### Entity Relationship Notes

- Every student must belong to a class in order to be enrolled into course_offering.
- Every course_offering links a teacher and optionally a class.
- GDPR-sensitive data is stored in private tables.
- Teachers and managers must be exclusive roles.
- Course offerings and enrollments enforce teaching and performance logic.
- Programs and courses are abstract. Classes and offerings make them real.



### Normalization (3NF)

- All tables use atomic values (1NF)
- No partial dependency on composite PKs (2NF)
- No transitive dependencies (3NF)
- Role-specific private tables eliminate duplication
- NOTE: Clear separation between abstract and tangible entities


### Conceptual ERD

<img src = "/assets/ex2_0_ezecream_ERD.png">

### Logical ERD

<img src = "/assets/YH_v7_logical ERD.png">

### Entity Relationships 

| #  | Relationship Name                | Relationship Statement                                                                 | Cardinality    | Implementation                                                                                         |
|----|-----------------------------------|-----------------------------------------------------------------------------------------|----------------|-------------------------------------------------------------------------------------------------------|
| 1  | Person ↔ Student                 | Each Person can be linked to one Student, and each Student is linked to one Person.     | One-to-One     | The foreign key is `person_id` in the `Student` table, which is unique, ensuring a one-to-one relationship. |
| 2  | Student ↔ Private_Student         | Each Student can have one Private_Student record, and each Private_Student is linked to one Student. | One-to-One     | The `student_id` in `Private_Student` is a primary key, enforcing a one-to-one relationship.         |
| 3  | Person ↔ Teacher                 | Each Person can be a Teacher, and each Teacher is linked to one Person.                 | One-to-One     | The `person_id` in the `Teacher` table is unique, enforcing the one-to-one relationship.             |
| 4  | Teacher ↔ Private_Teacher        | Each Teacher can have one Private_Teacher record, and each Private_Teacher is linked to one Teacher. | One-to-One     | The `teacher_id` in `Private_Teacher` is a primary key, ensuring a one-to-one relationship.          |
| 5  | Person ↔ Education_Manager       | Each Person can be an Education_Manager, and each Education_Manager is linked to one Person. | One-to-One     | The `person_id` in the `Education_manager` table is unique, enforcing the one-to-one relationship.    |
| 6  | Education_Manager ↔ Private_Education_Manager | Each Education_Manager can have one Private_Education_Manager record, and each Private_Education_Manager is linked to one Education_Manager. | One-to-One     | The `manager_id` in `Private_Education_Manager` is a primary key, ensuring a one-to-one relationship. |
| 7  | Company ↔ Education_Manager      | A Company can have multiple Education_Managers, but each Education_Manager belongs to one Company. | One-to-Many    | The `company_id` in `Education_manager` references `Company(company_id)`.                             |
| 8  | Company ↔ Teacher                | A Company can employ multiple Teachers, but each Teacher belongs to one Company.         | One-to-Many    | The `company_id` in `Teacher` references `Company(company_id)`.                                        |
| 9  | City ↔ Address                   | A City is associated with many Addresses, but each Address is associated with exactly one City. | One-to-Many    | The `city_id` in `Address` references `City(city_id)`.                                                |
| 10 | Address ↔ Company                | An Address can be associated with multiple Companies, but each Company has exactly one Address. | One-to-Many    | The `address_id` in `Company` references `Address(address_id)`.                                        |
| 11 | Address ↔ Campus                 | An Address can be associated with multiple Campuses, but each Campus has zero or one Address. | One-to-Many    | The `address_id` in `Campus` references `Address(address_id)`.                                         |
| 12 | Program ↔ Class                  | A Program can have multiple Classes, but each Class belongs to one Program.               | One-to-Many    | The `program_id` in `Class` references `Program(program_id)`.                                          |
| 13 | Class ↔ Education_Manager        | A Class can be managed by one or more Education_Managers, but each Education_Manager can manage multiple Classes. | One-to-Many    | The `manager_id` in `Class` references `Education_manager(manager_id)`.                                |
| 14 | Campus ↔ Class                   | A Campus can have multiple Classes, but each Class is held at one Campus.                 | One-to-Many    | The `campus_id` in `Class` references `Campus(campus_id)`.                                             |
| 15 | Class ↔ Student                  | A Class can have multiple Students, but each Student belongs to one Class.                | One-to-Many    | The `class_id` in `Student` references `Class(class_id)`.                                              |
| 16 | Program ↔ ProgramCourse          | A Program can offer multiple ProgramCourses, and each ProgramCourse links one Program to one Course. | One-to-Many    | The `program_id` in `ProgramCourse` references `Program(program_id)`.                                  |
| 17 | Course ↔ ProgramCourse           | A Course can be included in multiple ProgramCourses, but each ProgramCourse links one Course to one Program. | One-to-Many    | The `course_id` in `ProgramCourse` references `Course(course_id)`.                                     |
| 18 | Course ↔ Course_Offering         | A Course can have multiple CourseOfferings, but each CourseOffering is for one Course.   | One-to-Many    | The `course_id` in `Course_offering` references `Course(course_id)`.                                   |
| 19 | Campus ↔ Course_Offering         | A Campus can offer multiple CourseOfferings, but each CourseOffering can be held at one Campus. | One-to-Many    | The `campus_id` in `Course_offering` references `Campus(campus_id)`.                                   |
| 20 | Teacher ↔ Course_Offering        | A Teacher can be assigned to multiple CourseOfferings, but each CourseOffering can have one Teacher. | One-to-Many    | The `teacher_id` in `Course_offering` references `Teacher(teacher_id)`.                                |
| 21 | Class ↔ Course_Offering          | A Class can have multiple CourseOfferings, but each CourseOffering can be linked to one Class. | One-to-Many    | The `linked_class_id` in `Course_offering` references `Class(class_id)`.                               |

