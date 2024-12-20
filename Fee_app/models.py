from django.db import models
from Student_app.models import Program, Branch, Student


class Fee(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='fees')
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, related_name='fees')
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, related_name='fees')
    semester = models.PositiveIntegerField()
    created_by = models.CharField(max_length=255)  # e.g., the username of the admin/teacher
    date = models.DateField(auto_now_add=True)
    total_fee = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=10)
    payment_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    # For cash payments
    cash_notes = models.TextField(blank=True, null=True, help_text="Details of cash notes, e.g., {'500': 2, '200': 3}")

    # For online payments
    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    screenshot = models.ImageField(upload_to='fee_screenshots/', blank=True, null=True)

    def __str__(self):
        return f"Fee record for {self.student.name} - {self.program.name} ({self.semester} semester)"

    class Meta:
        verbose_name = "Fee"
        verbose_name_plural = "Fees"
        ordering = ['-date']