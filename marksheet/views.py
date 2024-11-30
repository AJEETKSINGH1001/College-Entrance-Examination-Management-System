from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.db.models import Sum
from .models import Student, Marks, Class
from .forms import MarksheetForm  # Form we will create
from reportlab.pdfgen import canvas  # For generating PDFs

# Helper function to calculate grades based on marks
def calculate_grade(marks):
    if marks >= 90:
        return 'A'
    elif marks >= 80:
        return 'B'
    elif marks >= 70:
        return 'C'
    elif marks >= 60:
        return 'D'
    else:
        return 'F'


# Homepage View (List of classes and sections)
def homepage(request):
    if request.method == 'POST':
        form = MarksheetForm(request.POST)
        if form.is_valid():
            roll_number = form.cleaned_data['roll_number']
            class_name = form.cleaned_data['student_class']  # This refers to the class_name field in Student model

            # Try to fetch the student based on roll number and class
            try:
                student = Student.objects.get(roll_number=roll_number, class_name=class_name)  # Corrected field name
                # Redirect to the student's marksheet page
                return redirect('marksheet:student_marksheet', student_id=student.id)
            except Student.DoesNotExist:
                form.add_error('roll_number', 'Student not found for the given roll number and class.')
    else:
        form = MarksheetForm()

    classes = Class.objects.all()
    return render(request, 'marksheet/homepage.html', {'form': form, 'classes': classes})


# View to see students of a specific class and section
def class_students(request, class_id):
    try:
        class_obj = Class.objects.get(id=class_id)
        students = class_obj.students.all()  # Assuming reverse relationship "students" exists in Class model
    except Class.DoesNotExist:
        raise Http404("Class does not exist")
    return render(request, 'marksheet/class_students.html', {'class_obj': class_obj, 'students': students})


# Generate and View Marksheets for Students
def student_marksheet(request, student_id):
    try:
        # Fetch the student and their marks
        student = Student.objects.get(id=student_id)
        marks = Marks.objects.filter(student=student)

        # Calculate total marks, maximum marks, and percentage
        total_marks = marks.aggregate(Sum('marks_obtained'))['marks_obtained__sum'] or 0
        total_subjects = marks.count()
        max_marks = total_subjects * 100  # Assuming each subject has max marks of 100
        percentage = (total_marks / max_marks) * 100 if max_marks > 0 else 0

        # Calculate average marks and overall grade
        average_marks = total_marks / total_subjects if total_subjects > 0 else 0
        overall_grade = calculate_grade(average_marks)

        # Add grades for each subject
        marks_with_grades = [
            {
                'subject': mark.subject.name,
                'marks_obtained': mark.marks_obtained,
                'grade': calculate_grade(mark.marks_obtained),
            }
            for mark in marks
        ]

        # Rank calculation within the class
        same_class_students = Student.objects.filter(class_name=student.class_name)  # Corrected field name
        ranks = (
            Marks.objects
            .filter(student__in=same_class_students)
            .values('student')
            .annotate(total=Sum('marks_obtained'))
            .order_by('-total')
        )

        student_rank = 0
        for idx, rank in enumerate(ranks, start=1):
            if rank['student'] == student.id:
                student_rank = idx
                break

    except Student.DoesNotExist:
        raise Http404("Student does not exist")

    return render(request, 'marksheet/student_marksheet.html', {
        'student': student,
        'marks_with_grades': marks_with_grades,
        'total_marks': total_marks,
        'max_marks': max_marks,
        'percentage': percentage,
        'average_marks': average_marks,
        'overall_grade': overall_grade,
        'student_rank': student_rank,
        'signature': 'Authorized Signature (Principal)',  # Add signature to marksheet
    })


# Download Marksheet as PDF
def download_pdf(request, student_id):
    try:
        # Fetch the student and their marks
        student = Student.objects.get(id=student_id)
        marks = Marks.objects.filter(student=student)

        # Create a PDF response
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{student.first_name}_{student.last_name}_marksheet.pdf"'

        # Generate PDF using ReportLab
        p = canvas.Canvas(response)
        p.drawString(100, 800, f"Marksheet for {student.first_name} {student.last_name}")
        p.drawString(100, 780, f"Roll Number: {student.roll_number}")
        p.drawString(100, 760, f"Class: {student.class_name}")

        y_position = 740
        for mark in marks:
            p.drawString(100, y_position, f"{mark.subject.name}: {mark.marks_obtained} ({calculate_grade(mark.marks_obtained)})")
            y_position -= 20

        p.drawString(100, y_position - 40, "Authorized Signature: Principal")
        p.showPage()
        p.save()

        return response
    except Student.DoesNotExist:
        raise Http404("Student does not exist")
