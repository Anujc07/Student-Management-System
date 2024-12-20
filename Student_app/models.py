from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User 
import uuid





class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile' ,null=True, blank=True)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100) 
    email = models.EmailField(unique=True) 
    contact_number = models.CharField(max_length=15) 
    subject = models.CharField(max_length=100) 
    hire_date = models.DateField() 
    address = models.TextField(blank=True, null=True)
    qualification = models.CharField(max_length=200, blank=True, null=True) 
    status = models.IntegerField(default=1)
    assigned_branch = models.ForeignKey(
        'Branch', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='teachers'
    )  

    def __str__(self):
        return self.name

 
    
class Program(models.Model):
    name = models.CharField(max_length=100, unique=True) 
    duration = models.DecimalField(max_digits=4, decimal_places=1) 
    semsters = models.IntegerField(default=0)
    status = models.IntegerField(default=1)

    def __str__(self):
        return self.name
    

class Branch(models.Model):
    name = models.CharField(max_length=100)  
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="branches")
    status = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.name} ({self.program.name})"
    

class Student(models.Model):

    id = models.AutoField(primary_key=True)  
    name = models.CharField(max_length=100)
    class_name = models.TextField(max_length=50)
    roll_no = models.TextField(max_length=20) 
    dob = models.DateField()  
    parent_contact = models.CharField(max_length=15) 
    adhaar_no = models.TextField(max_length=255, unique=True)
    father_name = models.CharField(max_length=100)
    address = models.TextField()  
    tenth_marksheet = models.FileField(upload_to='10th_marksheet', blank=True)
    twelfth_marksheet = models.FileField(upload_to='12th_marksheet', blank=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name='program_model', null=True, blank=True)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branches_model', null=True, blank=True)
    semester = models.PositiveIntegerField(verbose_name="Semester", default=1)
    status = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.name} - {self.roll_no}"

# student_phone, email, SSSM id, family id, caste certificate, adhar_card_img





class Subject(models.Model):
    # Core fields
    name = models.CharField(max_length=200, unique=True, verbose_name="Subject Name")
    code = models.CharField(max_length=50, unique=True, verbose_name="Subject Code")  # Unique identifier for the subject
    description = models.TextField(blank=True, null=True, verbose_name="Description")  # Optional field for details
    teachers = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Teacher", related_name="subjects")


    # Relationships
    branch = models.ForeignKey(
        'Branch',
        on_delete=models.CASCADE,
        related_name='subjects',
        verbose_name="Branch"
    )
    program = models.ForeignKey(
        'Program',
        on_delete=models.CASCADE,
        related_name='subjects',
        verbose_name="Program"
    )
    
    # Additional fields
    semester = models.PositiveIntegerField(verbose_name="Semester")  # Semester in which the subject is taught
    credits = models.PositiveIntegerField(default=0, verbose_name="Credits")  # Credits for the subject
    is_elective = models.BooleanField(default=False, verbose_name="Is Elective?")  # Whether the subject is elective

    # Audit fields
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    status = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.name} ({self.code})"




class Attendance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    marked_by = models.ForeignKey(
        'Teacher',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='attendance_marked'
    )


    student_data = models.JSONField(
        default=dict, 
        verbose_name="Student Attendance Data",
        help_text="Stores student IDs and their attendance status in JSON format"
    )
    
    date = models.PositiveIntegerField(verbose_name="Date")
    month = models.PositiveIntegerField(verbose_name="Month", default=None)
    year = models.PositiveIntegerField(verbose_name="Year",  default=None)

    program = models.ForeignKey(
        'Program',
        on_delete=models.CASCADE,
        related_name='attendance_program',
         default=None
    )
    branch = models.ForeignKey(
        'Branch',
        on_delete=models.CASCADE,
        related_name='attendance_branch',
        default=None
    )
    subject = models.ForeignKey(
        'Subject',
        on_delete=models.CASCADE,
        related_name='attendance_subject',
         default=None
    )
    status = models.IntegerField(default=1)
    

    class Meta:
        verbose_name = "Attendance Record"
        verbose_name_plural = "Attendance Records"
        unique_together = ('date', 'month', 'year', 'subject', 'branch')

    def __str__(self):
        return f"Attendance {self.id} by {self.marked_by} on {self.date}-{self.month}-{self.year}"

class Book_Type(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, related_name="books", default='')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name="books", default='')
    book_type = models.CharField(max_length=100)
    subject = models.CharField(max_length=200)
    status = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.book_type} - {self.subject}"