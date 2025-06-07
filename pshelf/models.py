from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    USER_TYPES = (
        ('creator', 'Creator'),
        ('visitor', 'Visitor'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPES)

    def __str__(self):
        return f"{self.user.username} - {self.user_type}"
    
class CreatorProject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    stats = models.CharField(max_length=20, choices=[('student', 'Student'), ('professional', 'Professional')])
    project_name = models.CharField(max_length=200)
    project_description = models.TextField()
    project_image = models.URLField()
    project_link = models.URLField()
    project_date = models.DateField()
    project_technologies = models.CharField(max_length=200)
    project_outcomes = models.TextField(blank=True, null=True)
    case_study = models.TextField(blank=True, null=True)

class VisitorActivity(models.Model):
    visitor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='visits')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator_visited')
    project = models.ForeignKey(CreatorProject, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    clicked = models.BooleanField(default=False)  # Did they click a link?
    
    def __str__(self):
        return f"{self.visitor.username} visited {self.project.project_name} by {self.creator.username}"