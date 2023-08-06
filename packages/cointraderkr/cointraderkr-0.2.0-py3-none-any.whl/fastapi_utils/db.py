# == Django Model Import ==#
import os
from asgiref.sync import sync_to_async
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")
application = get_wsgi_application()

import datetime
from db.models import Log, AccessToken
from django.contrib.auth import authenticate
from fastapi_utils.templates import LogTemplate, GetAccessTokenRequest


@sync_to_async
def get_django_access_token(user_request: GetAccessTokenRequest):
    user = authenticate(username=user_request.username, password=user_request.password)
    if user is not None:
        access_token = AccessToken.objects.filter(username=user.email).first()
        if access_token is not None:
            return access_token.token
        else:
            return None
    else:
        return None


@sync_to_async
def get_django_main_access_token():
    """
    AccessToken 테이블에 꼭 username=main의 토큰이 설저되어 있어야 한다.
    이 토큰과 유저의 토큰을 비교하여 일치하면 권한이 있는 것으로 판단한다.
    """
    access_token = AccessToken.objects.filter(username='main').first()
    if access_token is not None:
        return access_token.token
    else:
        return None


@sync_to_async
def get_all_django_logs():
    """
    로그가 너무 많을 수도 있기 때문에 최근 200 데이터만 불러온다.
    """
    cols = ['id', 'source', 'ip_address', 'log_level', 'timestamp', 'filename', 'message']
    # yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    # logs = list(Log.objects.filter(created__gte=yesterday))
    logs = Log.objects.order_by('-created')[:200]
    logs = list(reversed(logs.values(*cols)))
    return logs


@sync_to_async
def save_django_log(log: LogTemplate):
    try:
        log_inst = Log(source=log.source,
                       ip_address=log.ip_address,
                       log_level=log.log_level,
                       timestamp=log.timestamp,
                       filename=log.filename,
                       message=log.message)
        log_inst.save()
        return True, 'Successfully saved log data'
    except Exception as e:
        return False, str(e)