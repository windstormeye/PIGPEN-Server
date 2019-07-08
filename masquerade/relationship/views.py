from django.shortcuts import render
from common import utils, decorator, masLogger


@decorator.request_method('GET')
@decorator.request_check_args(['phoneNumber', 'password', 'avatar', 'gender'])
def petRelationship(request):
    uid = request.GET.get('uid')
    pet_id = request.GET.get('pet_id')