from rest_framework import serializers
from .models import JobApplication
#Day 6 Advanced Serializer
from django.utils import timezone

class JobApplicationSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source = 'owner.username')
    salary_formatted = serializers.SerializerMethodField()
    applied_since = serializers.SerializerMethodField()
    status_display  = serializers.SerializerMethodField()
    class Meta:
        model = JobApplication

        fields = ['id','owner', 'company', 'role',
                'salary_formatted', 'applied_since','status_display',
                    'salary', 'status', 'date_applied', 'notes']
        # obj = current JobApplication instance
    def get_salary_formatted(self, obj):
        return f"₹{obj.salary:,}"
        
    def get_applied_since(self, obj):
        x = timezone.now().date() - obj.date_applied
        return x.days
        
    def get_status_display(self, obj):
        stats = {
                'applied':   '📝 Applied',
                'interview': '🎯 Interview Scheduled',
                'rejected':  '❌ Rejected',
                'offer':     '🎉 Offer Received',
        }
        return stats.get(obj.status, obj.status)