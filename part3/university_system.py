"""
Advanced Python Programming - Practical Work 3
University Grade Management System
Combining OOP and Functional Programming

Author: Student
Date: 2025/2026
"""

from abc import ABC, abstractmethod
from functools import reduce, lru_cache, partial
from itertools import groupby, chain
from operator import attrgetter, itemgetter
import statistics


# ============================================================================
# EXERCISE 1-5: Abstract Base Class - Person
# ============================================================================
class Person(ABC):
    """
    Abstract base class representing a person in the university system.
    Defines common attributes and behaviors for all academic actors.
    """
    
    def __init__(self, id_person, name, email):
        """
        Initialize a Person with basic attributes.
        
        Args:
            id_person: Unique identifier
            name: Full name
            email: Email address
        """
        self.id_person = id_person
        self.name = name
        self.email = email
    
    @abstractmethod
    def describe(self):
        """
        Returns a textual description of the person and their role.
        Must be implemented by subclasses.
        """
        pass
    
    @abstractmethod
    def evaluate(self):
        """
        Defines how the person participates in academic evaluation.
        Must be implemented by subclasses.
        """
        pass
    
    def get_email(self):
        """Returns the email address of the person."""
        return self.email
    
    def set_email(self, new_email):
        """Updates the email address of the person."""
        self.email = new_email
        return f"Email updated to: {new_email}"


# ============================================================================
# EXERCISE 6-8: Abstract Base Class - Evaluator
# ============================================================================
class Evaluator(ABC):
    """
    Abstract base class for evaluation and ranking operations.
    Defines methods for computing scores and ranking students.
    """
    
    @abstractmethod
    def compute_score(self, grades):
        """
        Computes a final score based on a list of grades.
        Must be implemented by subclasses.
        
        Args:
            grades: List of grades
            
        Returns:
            Computed score
        """
        pass
    
    @abstractmethod
    def rank_students(self, students):
        """
        Ranks students according to their academic performance.
        Must be implemented by subclasses.
        
        Args:
            students: List of Student objects
            
        Returns:
            Ordered list of students
        """
        pass
    
    def is_valid_score(self, score):
        """
        Verifies that a score is valid (between 0 and 20).
        
        Args:
            score: Score to validate
            
        Returns:
            True if valid, False otherwise
        """
        return 0 <= score <= 20


# ============================================================================
# EXERCISE 9-11: Student Class
# ============================================================================
class Student(Person, Evaluator):
    """
    Concrete class representing a student in the university.
    Inherits from Person and Evaluator.
    """
    
    def __init__(self, id_person, name, email, student_id):
        """
        Initialize a Student.
        
        Args:
            id_person: Unique identifier for the person
            name: Full name
            email: Email address
            student_id: Unique student identifier
        """
        super().__init__(id_person, name, email)
        self.student_id = student_id
        self.grades = []
        self.courses = []
    
    def describe(self):
        """Returns a description of the student."""
        return f"Student: {self.name} (ID: {self.student_id})"
    
    def add_grade(self, grade):
        """
        Adds a new grade to the student's grades.
        Validates the grade before storing.
        
        Args:
            grade: Grade to add
            
        Returns:
            Success message or error
        """
        if self.is_valid_score(grade):
            self.grades.append(grade)
            return f"Grade {grade} added successfully"
        else:
            return f"Error: Grade {grade} is invalid (must be 0-20)"
    
    def get_average(self):
        """
        Computes the average of all grades.
        
        Returns:
            Average grade or 0 if no grades
        """
        if not self.grades:
            return 0
        return sum(self.grades) / len(self.grades)
    
    def get_grades(self):
        """Returns the list of grades."""
        return self.grades.copy()
    
    def evaluate(self, strategy):
        """
        Evaluates the student's performance using a strategy function.
        Demonstrates first-class functions.
        
        Args:
            strategy: Function that takes grades and returns a score
            
        Returns:
            Result of applying the strategy
        """
        if not self.grades:
            return "No grades available"
        return strategy(self.grades)
    
    def compute_score(self, grades):
        """
        Computes average score from grades.
        Implementation of abstract method.
        
        Args:
            grades: List of grades
            
        Returns:
            Average grade
        """
        return sum(grades) / len(grades) if grades else 0
    
    def rank_students(self, students):
        """
        Ranks students by their average grade.
        Implementation of abstract method.
        
        Args:
            students: List of Student objects
            
        Returns:
            Sorted list of students (descending by average)
        """
        return sorted(students, key=lambda s: s.get_average(), reverse=True)
    
    def __repr__(self):
        """String representation of student."""
        return f"Student({self.name}, Avg: {self.get_average():.2f})"


# ============================================================================
# EXERCISE 12-14: Professor Class
# ============================================================================
class Professor(Person, Evaluator):
    """
    Concrete class representing a professor in the university.
    Inherits from Person and Evaluator.
    """
    
    def __init__(self, id_person, name, email, professor_id):
        """
        Initialize a Professor.
        
        Args:
            id_person: Unique identifier for the person
            name: Full name
            email: Email address
            professor_id: Unique professor identifier
        """
        super().__init__(id_person, name, email)
        self.professor_id = professor_id
        self.courses = []
    
    def describe(self):
        """Returns a description of the professor."""
        courses_str = ", ".join([c.title for c in self.courses]) if self.courses else "No courses"
        return f"Professor: {self.name} (ID: {self.professor_id})\nCourses: {courses_str}"
    
    def assign_course(self, course):
        """
        Assigns a course to the professor.
        
        Args:
            course: Course object to assign
            
        Returns:
            Success message
        """
        if course not in self.courses:
            self.courses.append(course)
            return f"Course '{course.title}' assigned to {self.name}"
        return f"Course '{course.title}' already assigned"
    
    def evaluate(self, grades, strategy):
        """
        Evaluates grades using a strategy function.
        
        Args:
            grades: List of grades
            strategy: Function to evaluate grades
            
        Returns:
            Evaluation result
        """
        if not grades:
            return "No grades to evaluate"
        return strategy(grades)
    
    def compute_score(self, grades):
        """
        Computes average score from grades.
        Implementation of abstract method.
        
        Args:
            grades: List of grades
            
        Returns:
            Average grade
        """
        return sum(grades) / len(grades) if grades else 0
    
    def rank_students(self, students):
        """
        Ranks students by their average grade.
        Implementation of abstract method.
        
        Args:
            students: List of Student objects
            
        Returns:
            Sorted list of students (descending by average)
        """
        return sorted(students, key=lambda s: s.get_average(), reverse=True)
    
    def __repr__(self):
        """String representation of professor."""
        return f"Professor({self.name})"


# ============================================================================
# EXERCISE 15-17: Course Class
# ============================================================================
class Course:
    """
    Represents a course in the university with students and grading.
    """
    
    def __init__(self, code, title, professor):
        """
        Initialize a Course.
        
        Args:
            code: Course code
            title: Course title
            professor: Professor responsible for the course
        """
        self.code = code
        self.title = title
        self.students = []
        self.professor = professor
        self.enrollments = {}  # {student: [grades]}
    
    def add_student(self, student):
        """
        Adds a student to the course enrollment.
        
        Args:
            student: Student to enroll
            
        Returns:
            Success message
        """
        if student not in self.students:
            self.students.append(student)
            self.enrollments[student] = []
            return f"Student {student.name} enrolled in {self.title}"
        return f"Student {student.name} already enrolled"
    
    def record_grade(self, student, grade):
        """
        Records a grade for a student.
        
        Args:
            student: Student object
            grade: Grade to record (validated)
            
        Returns:
            Success or error message
        """
        if student not in self.enrollments:
            return f"Student {student.name} not enrolled in {self.title}"
        
        if not (0 <= grade <= 20):
            return f"Error: Grade {grade} is invalid (must be 0-20)"
        
        self.enrollments[student].append(grade)
        return f"Grade {grade} recorded for {student.name}"
    
    def apply_grading_strategy(self, student, strategy):
        """
        Applies a grading strategy to compute final score.
        
        Args:
            student: Student object
            strategy: Function to compute score
            
        Returns:
            Final score
        """
        if student not in self.enrollments:
            return None
        grades = self.enrollments[student]
        return strategy(grades) if grades else 0
    
    def scale_grades(self, student, scale):
        """
        Scales grades using a closure.
        
        Args:
            student: Student object
            scale: Scaling factor
            
        Returns:
            List of scaled grades
        """
        if student not in self.enrollments:
            return []
        
        def scaler(grade):
            return grade * scale
        
        return list(map(scaler, self.enrollments[student]))
    
    def get_passing_students(self):
        """
        Returns students with average >= 10.
        
        Returns:
            List of passing students
        """
        def passes(item):
            student, grades = item
            avg = sum(grades) / len(grades) if grades else 0
            return avg >= 10
        
        return [student for student, grades in filter(passes, self.enrollments.items())]
    
    def rank_students(self):
        """
        Ranks students by average grade (descending).
        
        Returns:
            List of students sorted by average
        """
        def get_average(student):
            grades = self.enrollments.get(student, [])
            return sum(grades) / len(grades) if grades else 0
        
        return sorted(self.students, key=get_average, reverse=True)
    
    def generate_report(self):
        """
        Generates a comprehensive report for the course.
        
        Returns:
            Formatted report string
        """
        report = f"\n{'='*70}\n"
        report += f"COURSE REPORT\n"
        report += f"{'='*70}\n"
        report += f"Code: {self.code}\n"
        report += f"Title: {self.title}\n"
        report += f"Professor: {self.professor.name}\n"
        report += f"Total Students: {len(self.students)}\n"
        report += f"\n{'-'*70}\n"
        
        # Student grades and averages
        report += f"{'Student':<25} {'Grades':<30} {'Average':<10}\n"
        report += f"{'-'*70}\n"
        
        for student in self.rank_students():
            grades = self.enrollments.get(student, [])
            avg = sum(grades) / len(grades) if grades else 0
            grades_str = str(grades)[:28]
            report += f"{student.name:<25} {grades_str:<30} {avg:.2f}\n"
        
        # Statistics
        report += f"\n{'-'*70}\n"
        report += "STATISTICS\n"
        report += f"{'-'*70}\n"
        
        all_grades = list(chain.from_iterable(self.enrollments.values()))
        if all_grades:
            report += f"Total Grades: {len(all_grades)}\n"
            report += f"Average Grade: {sum(all_grades)/len(all_grades):.2f}\n"
            report += f"Highest Grade: {max(all_grades)}\n"
            report += f"Lowest Grade: {min(all_grades)}\n"
            report += f"Passing Students: {len(self.get_passing_students())}\n"
        
        report += f"{'='*70}\n"
        return report
    
    def __repr__(self):
        """String representation of course."""
        return f"Course({self.code} - {self.title})"


# ============================================================================
# EXERCISE 18-19: TeachingAssistant Class (Multiple Inheritance)
# ============================================================================
class TeachingAssistant(Student, Professor):
    """
    Class representing a Teaching Assistant.
    Inherits from both Student and Professor (Multiple Inheritance + MRO).
    """
    
    def __init__(self, id_person, name, email, student_id, professor_id):
        """
        Initialize a Teaching Assistant.
        
        Args:
            id_person: Unique identifier
            name: Full name
            email: Email address
            student_id: Student identifier
            professor_id: Professor identifier
        """
        # Initialize both parent classes properly
        Person.__init__(self, id_person, name, email)
        self.student_id = student_id
        self.professor_id = professor_id
        self.grades = []
        self.courses = []
    
    def describe(self):
        """
        Returns a description explaining dual role.
        
        Returns:
            Description string
        """
        return f"{self.name} is both a student and a teaching assistant assisting the professor."
    
    def evaluate(self, *args, **kwargs):
        """
        Can evaluate in both student and professor capacities.
        
        Returns:
            Evaluation result
        """
        if len(args) >= 2:  # Professor evaluation with grades and strategy
            return Professor.evaluate(self, args[0], args[1])
        elif len(args) == 1:  # Student evaluation with strategy
            return Student.evaluate(self, args[0])
        return "Evaluation not specified"
    
    def __repr__(self):
        """String representation."""
        return f"TeachingAssistant({self.name})"


# ============================================================================
# EXERCISE 20: Grading Strategy Functions (First-Class Functions)
# ============================================================================
def simple_average(grades):
    """
    Computes the simple average of grades.
    
    Args:
        grades: List of grades
        
    Returns:
        Average grade
    """
    if not grades:
        return 0
    return sum(grades) / len(grades)


def max_grade(grades):
    """
    Returns the maximum grade.
    
    Args:
        grades: List of grades
        
    Returns:
        Maximum grade
    """
    return max(grades) if grades else 0


def min_grade(grades):
    """
    Returns the minimum grade.
    
    Args:
        grades: List of grades
        
    Returns:
        Minimum grade
    """
    return min(grades) if grades else 0


def weighted_average(grades, weights=None):
    """
    Computes weighted average of grades.
    
    Args:
        grades: List of grades
        weights: List of weights (default: equal weights)
        
    Returns:
        Weighted average
    """
    if not grades:
        return 0
    
    if weights is None:
        weights = [1] * len(grades)
    
    return sum(g * w for g, w in zip(grades, weights)) / sum(weights)


# ============================================================================
# EXERCISE 21: Closure - make_grader
# ============================================================================
def make_grader(scale):
    """
    Creates a grader function with a scaling factor (closure).
    
    Args:
        scale: Scaling factor
        
    Returns:
        Function that scales grades
    """
    def grader(grade):
        """Inner function that scales a grade."""
        return grade * scale
    
    return grader


# Alternative using partial
def scale_grade(grade, scale):
    """Helper function for partial application."""
    return grade * scale


# ============================================================================
# EXERCISE 22: Decorator - log_call
# ============================================================================
def log_call(func):
    """
    Decorator that logs function calls with arguments and results.
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function
    """
    def wrapper(*args, **kwargs):
        args_str = ", ".join(str(arg) for arg in args[1:])  # Skip 'self'
        kwargs_str = ", ".join(f"{k}={v}" for k, v in kwargs.items())
        all_args = ", ".join(filter(None, [args_str, kwargs_str]))
        
        print(f"Calling {func.__name__}({all_args})")
        result = func(*args, **kwargs)
        print(f"Result: {result}")
        return result
    
    return wrapper


# ============================================================================
# EXERCISE 23: Decorator with Parameters - validate
# ============================================================================
def validate(min_val=0, max_val=20):
    """
    Decorator that validates grade values before recording.
    
    Args:
        min_val: Minimum valid value
        max_val: Maximum valid value
        
    Returns:
        Decorator function
    """
    def decorator(func):
        def wrapper(self, student, grade):
            if not (min_val <= grade <= max_val):
                return f"Error: Invalid grade {grade} (must be {min_val}-{max_val})"
            return func(self, student, grade)
        return wrapper
    return decorator


# ============================================================================
# UTILITY FUNCTIONS for functional programming demonstrations
# ============================================================================
def group_students_by_performance(students):
    """
    Groups students by performance category using itertools.groupby.
    
    Args:
        students: List of Student objects
        
    Returns:
        Dictionary with categories as keys and students as values
    """
    # Sort first to enable groupby
    sorted_students = sorted(students, key=lambda s: s.get_average())
    
    groups = {}
    for avg, group in groupby(sorted_students, key=lambda s: s.get_average() // 10):
        category_map = {0: "Fail", 1: "Fail", 2: "Pass", 3: "Pass", 4: "Pass"}
        category = category_map.get(avg, "Excellent")
        groups[category] = list(group)
    
    return groups


def compute_class_statistics(students):
    """
    Computes statistics for a group of students using functools.reduce.
    
    Args:
        students: List of Student objects
        
    Returns:
        Dictionary with statistics
    """
    all_grades = list(chain.from_iterable(s.get_grades() for s in students))
    
    if not all_grades:
        return {"count": 0, "average": 0, "total": 0}
    
    return {
        "count": len(all_grades),
        "average": sum(all_grades) / len(all_grades),
        "total": sum(all_grades),
        "max": max(all_grades),
        "min": min(all_grades)
    }


def filter_by_performance(students, threshold=10):
    """
    Filters students by performance threshold using functional filter.
    
    Args:
        students: List of Student objects
        threshold: Minimum average grade
        
    Returns:
        List of students meeting threshold
    """
    return list(filter(lambda s: s.get_average() >= threshold, students))


def map_to_letter_grades(grades):
    """
    Maps numerical grades to letter grades using functional map.
    
    Args:
        grades: List of numerical grades
        
    Returns:
        List of letter grades
    """
    def grade_mapper(grade):
        if grade >= 16:
            return 'A'
        elif grade >= 14:
            return 'B'
        elif grade >= 12:
            return 'C'
        elif grade >= 10:
            return 'D'
        else:
            return 'F'
    
    return list(map(grade_mapper, grades))
