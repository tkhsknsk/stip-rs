# -*- coding: utf-8 -*-
from django.http.response import JsonResponse
from ctirs.core.common import get_text_field_value
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from ctirs.models.rs.models import STIPUser

def get_configuration_user_ajax_change_auth_username(request):
    return get_text_field_value(request,'username',default_value='')
def get_configuration_user_ajax_change_auth_key(request):
    return get_text_field_value(request,'key',default_value='')
def get_configuration_user_ajax_change_auth_value(request):
    return get_text_field_value(request,'value',default_value='')

@login_required
@csrf_protect
def change_auth(request):
    #GET以外はエラー
    if request.method != 'GET':
        r = {'status': 'NG',
             'message' : 'Invalid HTTP method'}
        return JsonResponse(r,safe=False)
    #activeユーザー以外はエラー
    if request.user.is_active == False:
        r = {'status': 'NG',
             'message' : 'You account is inactive.'}
        return JsonResponse(r,safe=False)
    #is_admin権限なしの場合はエラー
    if request.user.is_admin == False:
        r = {'status': 'NG',
             'message' : 'No permission.'}
        return JsonResponse(r,safe=False)

    try:
        username =  get_configuration_user_ajax_change_auth_username(request)
        key = get_configuration_user_ajax_change_auth_key(request)
        value  = True if get_configuration_user_ajax_change_auth_value(request) == u'true' else False

        u = STIPUser.objects.get(username = username)
        #keyに応じて属性の値を変更
        if(key == u'is_active'):
            u.is_active = value
        elif(key == u'is_admin'):
            u.is_admin = value
            u.is_superuser = value
        #変更を保存
        u.save()
        r = {'status': 'OK',
             'message' : 'Success'}
    except Exception as e:
        r = {'status': 'NG',
             'message' : str(e)}
    finally:
        return JsonResponse(r,safe=False)

