### Core Logic of the Data Model

- **Centralized Management**  
  The database is designed to centralize all core operations of YrkesCo, covering students, teachers, education managers, programs, courses, classes, and campus locations. This replaces the need for disconnected Excel files and fragmented data sources.

- **Role Separation**  
  Roles such as Student, Teacher, and Education Manager are represented as distinct entities, each linked to a shared `Person` entity. This structure supports clean data management, prevents role overlap, and facilitates role-specific permissions.

- **GDPR Compliance**  
  Sensitive personal information (e.g., personal number) is stored in separate `Private_*` entities for each role. This separation helps enforce GDPR compliance and simplifies access control for private data.

- **Abstract vs. Tangible Educational Units**  
  The model distinguishes between abstract entities (`Program`, `Course`) and their real-world implementations (`Class`, `Course_Offering`). This provides flexibility and scalability while supporting clear scheduling and tracking of actual teaching activities.

- **Class as the Student Anchor**  
  Every student must belong to a `Class`, establishing it as the core organizational unit. Even when enrolling in standalone courses, students must be linked to a class for administrative tracking and reporting.

- **Course Offering as the Operational Link**  
  The `Course_Offering` entity connects abstract `Course` definitions to specific terms (`HT`, `VT`, `ST`), years, physical or virtual locations (`Campus`), and assigned teachers. Course offerings can either be part of a program (linked to a `Class`) or standalone (with `linked_class_id = NULL`).

- **Enrollment and Grading**  
  The `Enrollment` entity captures student participation in specific `Course_Offering` instances. It tracks the current grade (with a default value of `NOT SET`) and the date of the most recent grade update.

- **Location and Address Management**  
  The physical infrastructure of the institution is managed using `Campus`, `Address`, and `City` entities. This enables flexible support for physical campuses (e.g., Gothenburg, Stockholm) and online delivery (via a "Virtual Campus").

- **Consultant and Company Integration**  
  External educators are modeled as consultants linked to a `Company` entity, which stores tax status, billing rate, and contact details. Permanent staff are linked to the school's own company record (with `hourly_rate = 0`).

- **Business Rule Enforcement**  
  Key business rules are enforced through database constraints and triggers. Examples include:
    - A person cannot hold multiple roles simultaneously (e.g., Teacher and Student).
    - Education Managers cannot teach.
    - Students must belong to a class.
    - Teachers assigned as permanent must be linked to YrkesCo’s company.

- **Third Normal Form (3NF) Compliance**  
  The model follows normalization best practices to eliminate redundancy, preserve data integrity, and ensure efficient querying. All non-key attributes are fully functionally dependent on the primary key of their respective tables.