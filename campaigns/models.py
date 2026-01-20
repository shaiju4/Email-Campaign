from django.db import models

class Campaign(models.Model):
    
    class Status(models.TextChoices):
        SCHEDULED = "SCHEDULED", "Scheduled"
        IN_PROGRESS = "IN_PROGRESS", "In Progress"
        COMPLETED = "COMPLETED", "Completed"
        
    name = models.CharField(max_length=200)
    subject = models.CharField(max_length=255)
    content = models.TextField()
    scheduled_time = models.DateTimeField()
    status = models.CharField(
        max_length = 20,
        choices =  Status.choices,
        default = Status.SCHEDULED
    )
    
    total_recipients = models.IntegerField(default=0)
    sent_count = models.IntegerField(default=0)
    failed_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    
class EmailLogs(models.Model):
    
    class Status(models.TextChoices):
        SENT = "SENT", "Sent"
        FAILED = "FAILED" , "Failed"
    
    campaign  = models.ForeignKey(Campaign,on_delete=models.CASCADE,related_name="email_logs")
    recipient_email = models.EmailField()
    status = models.CharField(max_length=10 , choices= Status.choices)
    failure_reason = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ("campaign", "recipient_email")
    
    def __str__(self):
        return f"{self.recipient_email} - {self.status}"
    
    
    
    
    