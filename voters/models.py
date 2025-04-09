from django.db import models
from django.utils import timezone


class VoterField(models.Model):
    FIELD_TYPES = [
        ('text', 'Text'),
        ('number', 'Number'),
        ('date', 'Date'),
        ('datetime', 'DateTime'),
        ('boolean', 'Boolean'),
        ('email', 'Email'),
        ('phone', 'Phone'),
        ('select', 'Select'),
    ]

    name = models.CharField(max_length=255, unique=True)
    field_type = models.CharField(max_length=50, choices=FIELD_TYPES, default='text')
    is_required = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)  # Changed from auto_now_add
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'voters_voterfield'
        verbose_name = 'Voter Field'
        verbose_name_plural = 'Voter Fields'
        ordering = ['name']

    def __str__(self):
        return self.name


class Voter(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other')
    ]

    VERIFY_STATUS_CHOICES = [
        ('Verified', 'Verified'),
        ('Pending', 'Pending'),
        ('Rejected', 'Rejected')
    ]

    # All fields with default values to handle existing data
    mlc_constituency = models.CharField('MLC CONSTITUENCY', max_length=255, default='')
    assembly = models.CharField('ASSEMBLY', max_length=255, default='')
    mandal = models.CharField('MANDAL', max_length=255, default='')
    town = models.CharField('TOWN', max_length=255, blank=True, null=True)
    village = models.CharField('VILLAGE', max_length=255, blank=True, null=True)
    psno = models.CharField('PSNO', max_length=50, default='')
    location = models.CharField('LOCATION', max_length=255, default='')
    ps_address = models.TextField('PS ADDRESS', default='')
    street = models.CharField('STREET', max_length=255, default='')
    hno = models.CharField('HNO', max_length=50, default='')
    sno = models.CharField('SNO', max_length=50, default='')
    card_no = models.CharField('CARD NO', max_length=50, default='')
    voter_name = models.CharField('VOTER NAME', max_length=255, default='')
    mobile_no = models.CharField('MOBILE NO', max_length=15, default='')
    age = models.IntegerField('AGE', default=0)  # Adding default=0 for age
    gender = models.CharField('GENDER', max_length=1, choices=GENDER_CHOICES, default='M')
    rel_name = models.CharField('REL NAME', max_length=255, default='')
    relation = models.CharField('RELATION', max_length=255, default='')
    voter_status = models.CharField('VOTER STATUS', max_length=50, default='')
    party = models.CharField('PARTY', max_length=100, default='')
    caste = models.CharField('CASTE', max_length=100, default='')
    category = models.CharField('CATEGORY', max_length=100, default='')
    verify_status = models.CharField('VERIFY STATUS', max_length=20, choices=VERIFY_STATUS_CHOICES, default='Pending')

    # Keep the data field temporarily for migration
    data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'voters_voter'
        verbose_name = 'Voter'
        verbose_name_plural = 'Voters'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.voter_name} - {self.card_no}"