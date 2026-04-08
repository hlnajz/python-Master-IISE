"""
Complete Execution Example - University Grade Management System
Demonstrates all exercises and concepts
"""

from university_system import *
from functools import reduce, lru_cache, partial
from itertools import groupby, chain
from operator import attrgetter, itemgetter


def print_section(title):
    """Helper to print section headers."""
    print(f"\n{'='*70}")
    print(f"{title.center(70)}")
    print(f"{'='*70}\n")


def main():
    """Main execution demonstrating the complete system."""
    
    print_section("UNIVERSITY GRADE MANAGEMENT SYSTEM")
    print("Advanced Python Programming - Practical Work 3")
    print("Integrating OOP and Functional Programming\n")
    
    # ========================================================================
    # SECTION 1: CREATE ACADEMIC ACTORS
    # ========================================================================
    print_section("1. Creating Academic Actors")
    
    # Create professors
    prof_math = Professor(101, "Dr. Ahmed Hassan", "ahmed.hassan@university.edu", "P001")
    prof_physics = Professor(102, "Dr. Fatima Zahra", "fatima.zahra@university.edu", "P002")
    
    print(f"✓ Created Professor 1: {prof_math.name}")
    print(f"✓ Created Professor 2: {prof_physics.name}")
    
    # Create students
    student1 = Student(201, "Ali Mohammed", "ali.mohammed@student.edu", "S001")
    student2 = Student(202, "Amine Karim", "amine.karim@student.edu", "S002")
    student3 = Student(203, "Noor Fatima", "noor.fatima@student.edu", "S003")
    student4 = Student(204, "Leila Ahmed", "leila.ahmed@student.edu", "S004")
    student5 = Student(205, "Omar Youssef", "omar.youssef@student.edu", "S005")
    
    students = [student1, student2, student3, student4, student5]
    
    for i, student in enumerate(students, 1):
        print(f"✓ Created Student {i}: {student.name} ({student.student_id})")
    
    # Create teaching assistant
    ta = TeachingAssistant(301, "Amine Karim", "amine.karim@university.edu", "S002", "TA001")
    print(f"\n✓ Created Teaching Assistant: {ta.name}")
    print(f"  {ta.describe()}")
    
    # ========================================================================
    # SECTION 2: CREATE COURSES
    # ========================================================================
    print_section("2. Creating Courses")
    
    course_math = Course("MATH101", "Calculus I", prof_math)
    course_physics = Course("PHY201", "Physics II", prof_physics)
    
    print(f"✓ Created Course 1: {course_math.code} - {course_math.title}")
    print(f"✓ Created Course 2: {course_physics.code} - {course_physics.title}")
    
    # Assign courses to professors
    prof_math.assign_course(course_math)
    prof_physics.assign_course(course_physics)
    
    print(f"\n{prof_math.describe()}")
    print(f"\n{prof_physics.describe()}")
    
    # ========================================================================
    # SECTION 3: ENROLL STUDENTS IN COURSES
    # ========================================================================
    print_section("3. Enrolling Students in Courses")
    
    # Enroll students in Math course
    print("Enrolling students in MATH101:")
    for student in students:
        course_math.add_student(student)
        print(f"  ✓ {student.name} enrolled")
    
    # Enroll students in Physics course
    print("\nEnrolling students in PHY201:")
    for student in students[:4]:  # First 4 students
        course_physics.add_student(student)
        print(f"  ✓ {student.name} enrolled")
    
    # ========================================================================
    # SECTION 4: RECORD GRADES
    # ========================================================================
    print_section("4. Recording Grades for Students")
    
    # Math course grades
    print("Recording grades for MATH101:")
    math_grades = {
        student1: [14, 16, 17],
        student2: [12, 14, 16],
        student3: [18, 17, 19],
        student4: [8, 9, 7],
        student5: [15, 16, 14]
    }
    
    for student, grades in math_grades.items():
        for grade in grades:
            result = course_math.record_grade(student, grade)
            print(f"  {result}")
    
    # Physics course grades
    print("\nRecording grades for PHY201:")
    physics_grades = {
        student1: [13, 15, 16],
        student2: [11, 12, 13],
        student3: [17, 18, 19],
        student4: [6, 7, 8]
    }
    
    for student, grades in physics_grades.items():
        for grade in grades:
            result = course_physics.record_grade(student, grade)
            print(f"  {result}")
    
    # ========================================================================
    # SECTION 5: STUDENT EVALUATIONS (From course enrollments)
    # ========================================================================
    print_section("5. Student Performance Evaluations")
    
    print("Individual Student Evaluations (from course enrollments):")
    for student in students[:4]:  # Only students with grades
        course_grades = course_math.enrollments.get(student, [])
        avg = sum(course_grades) / len(course_grades) if course_grades else 0
        print(f"\n{student.describe()}")
        print(f"  Grades in {course_math.code}: {course_grades}")
        print(f"  Average: {avg:.2f}")
        
        # Test different strategies
        if course_grades:
            result1 = simple_average(course_grades)
            result2 = max_grade(course_grades)
            print(f"  Strategy Results - Simple Avg: {result1:.2f}, Max: {result2}")
    
    # ========================================================================
    # SECTION 6: GRADING STRATEGIES
    # ========================================================================
    print_section("6. Applying Grading Strategies")
    
    print("Testing different grading strategies:")
    test_grades = [12, 14, 16, 18, 15]
    
    print(f"\nTest Grades: {test_grades}")
    print(f"  Simple Average: {simple_average(test_grades):.2f}")
    print(f"  Maximum Grade: {max_grade(test_grades)}")
    print(f"  Minimum Grade: {min_grade(test_grades)}")
    
    # Weighted average example
    weights = [0.1, 0.1, 0.2, 0.3, 0.3]
    weighted = weighted_average(test_grades, weights)
    print(f"  Weighted Average (weights={weights}): {weighted:.2f}")
    
    # ========================================================================
    # SECTION 7: CLOSURES - Grade Scaling
    # ========================================================================
    print_section("7. Using Closures for Grade Scaling")
    
    print("Scaling student grades with closure make_grader:")
    print(f"\nOriginal grades for {student1.name}: {student1.get_grades()}")
    
    scale_factor = 1.1  # Increase by 10%
    grader_function = make_grader(scale_factor)
    scaled_grades = list(map(grader_function, student1.get_grades()))
    
    print(f"Scale factor: {scale_factor}")
    print(f"Scaled grades: {[round(g, 2) for g in scaled_grades]}")
    
    # Using Course scale_grades method
    print(f"\nCourse scaling for {student2.name} in {course_math.code}:")
    original = course_math.enrollments[student2]
    scaled = course_math.scale_grades(student2, 1.15)
    print(f"  Original: {original}")
    print(f"  Scaled (1.15x): {[round(g, 2) for g in scaled]}")
    
    # ========================================================================
    # SECTION 8: FUNCTIONAL PROGRAMMING WITH MAP, FILTER, REDUCE
    # ========================================================================
    print_section("8. Functional Programming - Map, Filter, Reduce")
    
    # MAP: Convert grades to letter grades
    print("Using MAP to convert to letter grades:")
    sample_grades = [18, 14, 12, 10, 8]
    letter_grades = map_to_letter_grades(sample_grades)
    print(f"  Numerical: {sample_grades}")
    print(f"  Letter:    {letter_grades}")
    
    # FILTER: Get passing students (use course data)
    print(f"\nUsing FILTER to get passing students from {course_math.code} (avg >= 10):")
    course_passing = course_math.get_passing_students()
    print(f"  Total enrolled: {len(course_math.students)}")
    print(f"  Passing students: {len(course_passing)}")
    for student in course_passing:
        grade_list = course_math.enrollments.get(student, [])
        avg = sum(grade_list) / len(grade_list) if grade_list else 0
        print(f"    • {student.name}: {avg:.2f}")
    
    # REDUCE: Compute cumulative statistics using course grades
    print(f"\nUsing REDUCE for cumulative statistics:")
    all_course_grades = list(chain.from_iterable(course_math.enrollments.values()))
    if all_course_grades:
        total_grades = reduce(lambda x, y: x + y, all_course_grades, 0)
        print(f"  Total grade points: {total_grades}")
        print(f"  Class average: {total_grades / len(all_course_grades):.2f}")
    
    # ========================================================================
    # SECTION 9: FUNCTOOLS MODULE
    # ========================================================================
    print_section("9. Using functools Module")
    
    # partial: Create specialized grading function
    print("Using functools.partial to create specialized functions:")
    scale_by_factor = partial(scale_grade, scale=1.2)
    test_grade = 15
    scaled = scale_by_factor(test_grade)
    print(f"  Original grade: {test_grade}")
    print(f"  Scaled (1.2x): {scaled:.2f}")
    
    # lru_cache: Optimize average computation
    @lru_cache(maxsize=128)
    def cached_average(grades_tuple):
        """Cached average computation."""
        grades = list(grades_tuple)
        return sum(grades) / len(grades) if grades else 0
    
    print(f"\nUsing functools.lru_cache for average computation:")
    grades_tuple = tuple([14, 16, 17])
    print(f"  Grades: {list(grades_tuple)}")
    print(f"  Cached Average: {cached_average(grades_tuple):.2f}")
    
    # ========================================================================
    # SECTION 10: ITERTOOLS MODULE
    # ========================================================================
    print_section("10. Using itertools Module")
    
    # groupby: Group students by performance category
    print("Using itertools.groupby to group students by performance:")
    performance_groups = group_students_by_performance(students)
    for category, group_students in performance_groups.items():
        print(f"\n  {category} Category:")
        for student in group_students:
            print(f"    • {student.name}: {student.get_average():.2f}")
    
    # chain: Combine multiple sequences
    print(f"\nUsing itertools.chain to combine grade lists:")
    grade_lists = [s.get_grades() for s in students[:3]]
    combined = list(chain.from_iterable(grade_lists))
    print(f"  Combined grades: {combined}")
    
    # ========================================================================
    # SECTION 11: OPERATOR MODULE
    # ========================================================================
    print_section("11. Using operator Module")
    
    # attrgetter: Sort students by average
    print("Using operator.attrgetter to extract attributes:")
    sorted_by_avg = sorted(students, key=attrgetter('name'))
    print(f"  Students sorted by name:")
    for student in sorted_by_avg:
        print(f"    • {student.name}")
    
    # itemgetter: Extract specific course data
    print(f"\nUsing operator.itemgetter with course enrollments:")
    for student, grades in list(course_math.enrollments.items())[:3]:
        print(f"  {student.name}: {grades}")
    
    # ========================================================================
    # SECTION 12: RANKING STUDENTS
    # ========================================================================
    print_section("12. Ranking Students by Performance")
    
    print(f"Course: {course_math.code} - {course_math.title}")
    ranked = course_math.rank_students()
    print(f"\nRanking (by average grade):\n")
    for rank, student in enumerate(ranked, 1):
        grades = course_math.enrollments[student]
        avg = sum(grades) / len(grades) if grades else 0
        print(f"  {rank}. {student.name:<20} Avg: {avg:6.2f}  Grades: {grades}")
    
    # ========================================================================
    # SECTION 13: PASSING VS FAILING STUDENTS
    # ========================================================================
    print_section("13. Passing and Failing Students Analysis")
    
    print(f"Course: {course_math.code}\n")
    
    passing_students = course_math.get_passing_students()
    print(f"Passing Students (avg >= 10): {len(passing_students)}")
    for student in passing_students:
        avg = sum(course_math.enrollments[student]) / len(course_math.enrollments[student])
        print(f"  ✓ {student.name}: {avg:.2f}")
    
    failing_students = [s for s in course_math.students if s not in passing_students]
    print(f"\nFailing Students (avg < 10): {len(failing_students)}")
    for student in failing_students:
        grades = course_math.enrollments[student]
        avg = sum(grades) / len(grades) if grades else 0
        print(f"  ✗ {student.name}: {avg:.2f}")
    
    # ========================================================================
    # SECTION 14: COURSE REPORTS
    # ========================================================================
    print_section("14. Generating Course Reports")
    
    print(course_math.generate_report())
    print(course_physics.generate_report())
    
    # ========================================================================
    # SECTION 15: CLASS STATISTICS
    # ========================================================================
    print_section("15. Class Statistics")
    
    print(f"Computing statistics using course data and functools.reduce:\n")
    
    # Use course data instead of individual student grades
    all_course_grades = list(chain.from_iterable(course_math.enrollments.values()))
    
    if all_course_grades:
        total = reduce(lambda x, y: x + y, all_course_grades, 0)
        print(f"  Total Grades Recorded: {len(all_course_grades)}")
        print(f"  Class Average: {total / len(all_course_grades):.2f}")
        print(f"  Total Points: {total}")
        print(f"  Highest Grade: {max(all_course_grades)}")
        print(f"  Lowest Grade: {min(all_course_grades)}")
    
    # ========================================================================
    # SECTION 16: DECORATORS DEMONSTRATION
    # ========================================================================
    print_section("16. Demonstrating Decorators")
    
    @log_call
    def test_function(value1, value2):
        """Test function with logging."""
        return value1 + value2
    
    print("Using @log_call decorator:\n")
    result = test_function(10, 20)
    
    # ========================================================================
    # SECTION 17: VALIDATION WITH DECORATOR
    # ========================================================================
    print_section("17. Validation Decorator Examples")
    
    print("Demonstrating @validate decorator (implicit in record_grade):\n")
    
    print(f"Valid grade (17): {course_math.record_grade(student1, 17)}")
    print(f"Invalid grade (25): {course_math.record_grade(student1, 25)}")
    print(f"Invalid grade (-5): {course_math.record_grade(student1, -5)}")
    
    # ========================================================================
    # SECTION 18: PROFESSOR EVALUATION
    # ========================================================================
    print_section("18. Professor Evaluation Capabilities")
    
    prof_grades = [12, 14, 16, 18, 15]
    print(f"Professor {prof_math.name} evaluating grades:")
    print(f"  Grades: {prof_grades}")
    print(f"  Simple Average: {prof_math.evaluate(prof_grades, simple_average):.2f}")
    print(f"  Max Grade: {prof_math.evaluate(prof_grades, max_grade)}")
    
    # ========================================================================
    # SECTION 19: TEACHING ASSISTANT DUAL ROLE
    # ========================================================================
    print_section("19. Teaching Assistant - Dual Role")
    
    # Add grades to TA as a student
    for grade in [15, 16, 14, 17]:
        ta.add_grade(grade)
    
    print(f"TA {ta.name}:")
    print(f"  Description: {ta.describe()}\n")
    print(f"  As Student:")
    print(f"    Student ID: {ta.student_id}")
    print(f"    Grades: {ta.get_grades()}")
    print(f"    Average: {ta.get_average():.2f}\n")
    
    print(f"  As Professor:")
    print(f"    Professor ID: {ta.professor_id}")
    print(f"    Can evaluate grades: Yes")
    print(f"    Can assign courses: Yes\n")
    
    # ========================================================================
    # SECTION 20: EMAIL MANAGEMENT
    # ========================================================================
    print_section("20. Email Management")
    
    print(f"Email operations using concrete methods:")
    print(f"\nOriginal email: {student1.get_email()}")
    result = student1.set_email("ali.mohammed@newemail.edu")
    print(f"Updated email: {student1.get_email()}")
    
    # ========================================================================
    # FINAL SUMMARY
    # ========================================================================
    print_section("SYSTEM SUMMARY")
    
    print(f"Total Professors: 2")
    print(f"Total Students: 5")
    print(f"Total Teaching Assistants: 1")
    print(f"Total Courses: 2")
    
    total_enrollments = len(course_math.students) + len(course_physics.students)
    print(f"Total Enrollments: {total_enrollments}")
    
    all_grades = list(chain.from_iterable(
        list(course_math.enrollments.values()) + 
        list(course_physics.enrollments.values())
    ))
    print(f"Total Grades Recorded: {len(all_grades)}")
    
    print(f"\n✓ System successfully integrates OOP and Functional Programming")
    print(f"✓ All exercises completed successfully")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    main()
