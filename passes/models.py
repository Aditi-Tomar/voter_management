from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class PassRequest(models.Model):
    TEMPLE_CHOICES = [
        ('Mahakaaleshwar', 'Sri Mahakaaleshwar Mandir'),
        ('Tirupati', 'Tirumala Tirupati Devasthanam'),
        ('Dwaraka', 'Dwaraka Tirumala Devasthanam'),
        ('Padmanabha', 'Sree Padmanabha Swamy Devasthanam'),
        ('Bhramaramba', 'Sri Bhramaramba Mallikarjuna Swamy Varla Devasthanam'),
        ('Kalahasti', 'Sri Gnanaprasunambika Sametha Srikalahasteeswara Temple'),
        ('Shirdi', 'Shri Shirdi Sayee Samsthan'),
        ('Sabarimala', 'Sabarimala Sree Ayyappa Devasthanam'),
        ('Jagannath', 'Shree Jagannath Temple'),
        ('Kashi', 'Shri Kashi Vishwanath Temple'),
        ('Vinayaka', 'Swayambhu Sri Varasiddhi Vinayaka Swamy'),
        ('Kamakshi', 'Sri Kamakshi Ambal Devasthanam'),
        ('RamLala', 'Ram Lala Ayodha'),
        ('Arunachaleswarar', 'Arulmigu Arunachaleswarar Temple'),
    ]

    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    temple = models.CharField(max_length=50, choices=TEMPLE_CHOICES)
    persons = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)]
    )
    visit_date = models.DateField()
    id_proof = models.CharField(max_length=50)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='PENDING'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Pass Request'
        verbose_name_plural = 'Pass Requests'
        unique_together = ['temple', 'visit_date']

    def __str__(self):
        return f"{self.name} - {self.temple} - {self.visit_date}"