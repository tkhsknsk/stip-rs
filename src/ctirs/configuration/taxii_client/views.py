# -*- coding: utf-8 -*-
from django.shortcuts import render
from ctirs.core.common import get_text_field_value, get_common_replace_dict
from ctirs.error.views import error_page,error_page_no_view_permission, error_page_free_format, error_page_inactive
from django.contrib.auth.decorators import login_required
from ctirs.models.rs.models import STIPUser
from ctirs.core.mongo.documents import TaxiiClients, Communities

def get_taxii_client_create_display_name(request):
    return get_text_field_value(request,'display_name',default_value='')

def get_taxii_client_create_address(request):
    return get_text_field_value(request,'address',default_value='')

def get_taxii_client_create_port(request):
    return int(get_text_field_value(request,'port',default_value='-1'))

def get_taxii_client_create_path(request):
    return get_text_field_value(request,'path',default_value='')

def get_taxii_client_create_collection(request):
    return get_text_field_value(request,'collection',default_value='')

def get_taxii_client_create_login_id(request):
    return get_text_field_value(request,'login_id',default_value='')

def get_taxii_client_create_login_password(request):
    return get_text_field_value(request,'login_password',default_value='')

def get_taxii_client_create_ssl(request):
    return request.POST.has_key('ssl')

def get_taxii_client_create_ca(request):
    return request.POST.has_key('ca')

def get_taxii_client_create_certificate(request):
    return get_text_field_value(request,'certificate',default_value=None)

def get_taxii_client_create_private_key(request):
    return get_text_field_value(request,'private_key',default_value=None)

def get_taxii_client_create_community_id(request):
    return get_text_field_value(request,'community_id',default_value='')

def get_taxii_client_create_protocol_version(request):
    return get_text_field_value(request,'protocol_version',default_value='')

def get_taxii_client_create_push(request):
    return request.POST.has_key('push')

def get_taxii_client_create_uploader_id(request):
    return get_text_field_value(request,'uploader_id',default_value='')

def get_taxii_client_delete_display_name(request):
    return get_text_field_value(request,'display_name',default_value='')

@login_required
def top(request):
    #activeユーザー以外はエラー
    if request.user.is_active == False:
        return error_page_inactive(request)
    #is_admin権限なしの場合はエラー
    if request.user.is_admin == False:
        return error_page_no_view_permission(request)
    try:
        replace_dict = get_taxii_client_common_replace_dict(request)
        #レンダリング
        return render(request,'taxii_client.html',replace_dict)
    except Exception:
        #エラーページ
        return error_page(request)

@login_required
def create(request):
    if request.method != 'POST':
        return error_page_free_format(request,'invalid method')
    #activeユーザー以外はエラー
    if request.user.is_active == False:
        return error_page_inactive(request)
    try:
        setting_name = get_taxii_client_create_display_name(request)
        if(setting_name == None or len(setting_name) == 0):
            return error_page_free_format(request,'No Display Name.')
        address = get_taxii_client_create_address(request)
        if(address == None or len(address) == 0):
            return error_page_free_format(request,'No Address.')
        try:
            port = get_taxii_client_create_port(request)
            if(port < 0 or port > 65535):
                return error_page_free_format(request,'Invalid port.')
        except ValueError:
                return error_page_free_format(request,'Invalid port.')
        path = get_taxii_client_create_path(request)
        if(path == None or len(path) == 0):
            return error_page_free_format(request,'No Path.')
        collection = get_taxii_client_create_collection(request)
        if(collection == None or len(collection) == 0):
            return error_page_free_format(request,'No Collection.')
        login_id = get_taxii_client_create_login_id(request)
        login_password = get_taxii_client_create_login_password(request)
        ssl = get_taxii_client_create_ssl(request)
        community_id = get_taxii_client_create_community_id(request)
        ca = get_taxii_client_create_ca(request)
        certificate = get_taxii_client_create_certificate(request)
        private_key = get_taxii_client_create_private_key(request)
        protocol_version = get_taxii_client_create_protocol_version(request)
        push = get_taxii_client_create_push(request)
        uploader_id = int(get_taxii_client_create_uploader_id(request))
        if(ca == True):
            if certificate is None:
                return error_page_free_format(request,'No Certificate.')
            if private_key is None:
                return error_page_free_format(request,'No Private Key.')
            if ssl is not True:
                return error_page_free_format(request,'Use SSL.')
        else:
            if(login_id == None or len(login_id) == 0):
                return error_page_free_format(request,'No Login ID.')

        #taxii作成
        TaxiiClients.create(setting_name ,
                             address=address,
                             port=port,
                             ssl=ssl,
                             path=path,
                             collection=collection,
                             login_id=login_id,
                             login_password=login_password,
                             community_id=community_id,
                             ca=ca,
                             cert_file=certificate,
                             key_file=private_key,
                             protocol_version=protocol_version,
                             push = push,
                             uploader_id = uploader_id)
        replace_dict = get_taxii_client_common_replace_dict(request)
        replace_dict['info_msg'] = 'Create or Modify Success!!'
        #レンダリング
        return render(request,'taxii_client.html',replace_dict)
    except Exception:
        #エラーページ
        return error_page(request)


@login_required
def delete(request):
    if request.method != 'GET':
        return error_page_free_format(request,'invalid method')
    #activeユーザー以外はエラー
    if request.user.is_active == False:
        return error_page_inactive(request)
    try:
        display_name = get_taxii_client_delete_display_name(request)
        if(display_name == None or len(display_name) == 0):
            return error_page_free_format(request,'No Display Name.')
        taxii = TaxiiClients.objects.get(name=display_name)
        taxii.delete()
        replace_dict = get_taxii_client_common_replace_dict(request)
        replace_dict['info_msg'] = 'Delete Success!!'
        #レンダリング
        return render(request,'taxii_client.html',replace_dict)
    except Exception:
        #エラーページ
        return error_page(request)
    
def get_taxii_client_common_replace_dict(request):
    replace_dict = get_common_replace_dict(request)
    replace_dict['taxii_clients'] = TaxiiClients.objects.all()
    replace_dict['protocol_versions'] = TaxiiClients.get_protocol_versions()
    replace_dict['communities'] = Communities.objects.all()
    replace_dict['users'] = STIPUser.objects.all()
    return replace_dict
