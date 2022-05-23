from django.http import HttpRequest
from django.views.decorators.http import require_POST, require_GET, require_http_methods
from django.core.exceptions import ObjectDoesNotExist
from sympy import EvaluationFailed


from core.api.auth import jwt_auth
from core.api.utils import (ErrorCode, failed_api_response, parse_data,
                            response_wrapper, success_api_response)

from core.models import Demand, User, Evaluation
from core import logger

import json

@jwt_auth()
@require_POST
@response_wrapper
def create_evaluation(request: HttpRequest):
    """
    create evaluation

    [method]: POST

    [route]: /api/evaluation/create

    parms:
        - description: string
		- scholar_id: int
    """
    data: dict = parse_data(request)
    id = data['id']
    scholar = User.objects.get(id=id)
    Company: User = request.user
    description = data['description']
    evaluation = Evaluation(scholar=scholar, company=Company, content=description)
    evaluation.save()
    return success_api_response(None)

def evaluation2json(evaluation: Evaluation) -> dict:
    user = evaluation.company
    verified_user = user.verified_info.first()
    data = {
        'company_meta' : json.loads(verified_user.meta) if verified_user else None,
        'created_at': evaluation.created_at,
        'description': evaluation.content,
        "icon": str(user.get_icon())
    }
    return data

@jwt_auth()
@require_POST
@response_wrapper
def get_evaluation(request: HttpRequest):
    """
    get evaluation

    [method]: POST

    [route]: /api/evaluation/scholar

    parms:
		- id: int
    """
    data: dict = parse_data(request)
    id = data['id']
    scholar = User.objects.get(id=id)
    evaluations = scholar.evaluated_contents.all()
    data = {'evaluation_list': [evaluation2json(evaluation) for evaluation in evaluations]}
    return success_api_response(data)