# marksheet/models.py
from django.db import models
from django.contrib.auth.models import User  # Assuming you're using the built-in User model


# Class model to store class name and section
class Class(models.Model):
    name = models.CharField(max_length=100)  # E.g., '10th', '12th'
    section = models.CharField(max_length=1)  # E.g., A, B, C

    def __str__(self):
        return f"{self.name} - {self.section}"  # Returns like '10th - A'

# Student model to store student information
class Student(models.Model):

    first_name = models.CharField(max_length=100)  # First name of the student
    last_name = models.CharField(max_length=100)  # Last name of the student
    roll_number = models.CharField(max_length=10, unique=True)  # Unique roll number for each student
    dob = models.DateField()  # Date of birth of the student
    class_name = models.ForeignKey(Class, related_name='students', on_delete=models.CASCADE)  # Foreign key linking to Class model

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.roll_number})"  # Returns student name and roll number

# Subject model to store subject names
class Subject(models.Model):
    name = models.CharField(max_length=100)  # Subject name, e.g., 'Maths', 'Science'

    def __str__(self):
        return self.name  # Returns the subject name

# Marks model to store marks for each student in each subject
class Marks(models.Model):
    student = models.ForeignKey(Student, related_name='marks', on_delete=models.CASCADE)  # Foreign key linking to Student
    subject = models.ForeignKey(Subject, related_name='marks', on_delete=models.CASCADE)  # Foreign key linking to Subject
    marks_obtained = models.IntegerField()  # Marks obtained by the student in the subject

    def __str__(self):
        return f"{self.student.first_name} - {self.subject.name}: {self.marks_obtained}"  # Returns student name, subject, and marks
