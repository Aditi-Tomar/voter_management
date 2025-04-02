from django.shortcuts import render
from django.http import JsonResponse
from .models import Voter, VoterField

def voter_list(request):
    voters = Voter.objects.all()
    return JsonResponse({
        'count': voters.count(),
        'fields': list(VoterField.objects.values('name', 'field_type'))
    })