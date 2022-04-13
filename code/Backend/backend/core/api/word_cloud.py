import pytz
from datetime import datetime, timedelta
from django.db.models import Count
from django.http import HttpRequest
from django.views.decorators.http import require_GET
from core.api.auth import jwt_auth
from core.api.utils import response_wrapper, success_api_response, failed_api_response, ErrorCode
from core.models.tag import Tag


@response_wrapper
@jwt_auth()
@require_GET
def word_cloud(request: HttpRequest):
    num = int(request.GET.dict().get('num', 100))
    timezone = pytz.timezone('UTC')
    now = timezone.localize(datetime.now())
    begin = now - timedelta(days=30)
    tag_hot = list(Tag.objects.filter(tag_to_mk__created_at__gte=begin, tag_to_mk__created_at__lte=now)\
        .annotate(hot=Count('tag_to_mk')).order_by('-hot').values('name', 'hot', 'id')[:num])
    return success_api_response(tag_hot)