from django.db import models


class VoterField(models.Model):
    name = models.CharField(max_length=255, unique=True)
    field_type = models.CharField(
        max_length=50,
        choices=[
            ('text', 'Text'),
            ('number', 'Number'),
            ('decimal', 'Decimal'),
            ('datetime', 'Date/Time'),
            ('boolean', 'Boolean'),
        ],
        default='text'
    )
    is_required = models.BooleanField(default=False)

    class Meta:
        db_table = 'voter_fields'
        verbose_name = 'Voter Field'
        verbose_name_plural = 'Voter Fields'
        ordering = ['name']

    def __str__(self):
        return self.name


class Voter(models.Model):
    data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'voters'
        verbose_name = 'Voter'
        verbose_name_plural = 'Voters'
        ordering = ['-created_at']

    def __str__(self):
        return f"Voter {self.id}"