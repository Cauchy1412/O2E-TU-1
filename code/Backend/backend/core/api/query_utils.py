"""query utils
Example of Usage:

@response_wrapper
@require_GET
@query_filter(fields=[("name", str), ("available", bool)])
@query_distinct(fields=["name"], model=Model)
@query_order_by(fields=["name", "available"])
@query_page(default=20)
def list_items(request: HttpRequest, *args, **kwargs):
    # filter
    item_filter = kwargs.get("filter")
    if item_filter is None:
        items = Model.objects.all()
    else:
        try:
            items = Model.objects.filter(item_filter)
        except FieldError:
            return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS,
                                        "Unsupported Filter Method.")
    # order_by
    orders = kwargs.get("order_by")
    if orders is not None:
        for order in orders:
            items = items.order_by(order)
    # page
    page = kwargs.get("page")
    page_size = kwargs.get("page_size")

    paginator = Paginator(items, page_size)
    total_count = paginator.count
    page_all = paginator.num_pages

    if page > page_all:
        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS,
                                    "Sorry, max page number is {}.".format(page_all))
    page_content = paginator.page(page).object_list
    item_details = list(page_content.values(...))
    # wrap ...
    data = {
        "total_count": total_count,
        "page_all": num_pages,
        "page_now": page,
        "items":item_details
    }
    return success_api_response(data)
"""
import ast
from typing import List, Tuple, Type, Dict, Callable

from django.db.models import Q
from django.http import HttpRequest

from core.api.utils import ErrorCode, failed_api_response

def query_page(default: int = 10):
    """parse page information in query string

    Args:
        default (int, optional): default value of page_size. Defaults to 10.

    Example of Usage:

        @response_wrapper
        @require_GET
        @query_page(default=20)
        def list_items(request: HttpRequest, *args, **kwargs):
            items = Model.objects.all()
            page = kwargs.get("page")
            page_size = kwargs.get("page_size")
            paginator = Paginator(items, page_size)
            page_all = paginator.num_pages
            total_count = paginator.count
            if page > page_all:
                return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS,
                                           "Sorry, max page number is {}.".format(page_all))
            data = {
                "total_count": total_count
                "page_all": num_pages,
                "page_now": page,
                "items":[...]
            }
            return success_api_response(data)

    Query String:

        pattern: page=int, page_size=int

        example: page=5&page_size=15, page=7, page_size=20

        example uri: ?page=1&page_size=114514
            corresponding dict:
            {
                'page': '1',
                'page_size': '114514'
            }
    """
    def decorator(func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            page = 1
            page_size = default
            query_dict = request.GET.dict()
            # parse page
            page_value = query_dict.get("page")
            if page_value is not None:
                try:
                    page = int(page_value)
                    if page <= 0:
                        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS,
                                                   "Sorry, page should be positive.")
                except ValueError:
                    return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS,
                                               "Sorry, page should be integer.")
            # parse page_size
            page_size_value = query_dict.get("page_size")
            if page_size_value is not None:
                try:
                    page_size = int(page_size_value)
                    if page_size <= 0:
                        return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS,
                                                   "Sorry, page_size should be positive.")
                except ValueError:
                    return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS,
                                               "Sorry, page_size should be integer.")
            kwargs.update({
                "page": page,
                "page_size": page_size
            })
            return func(request, *args, **kwargs)
        return wrapper
    return decorator

def query_filter(fields: List[Tuple[str, Type]], custom: Dict[str, Callable] = None):
    """parse filters in query string

    Args:
        fields (List[Tuple[str, Type]]): a list containing tuples of fields' name and types
        custom (List[str]): a list containing field names and corresponding handler

    Example of Usage:

        @response_wrapper
        @require_GET
        @query_filter(fields=[("student_id", str)])
        def list_items(request: HttpRequest, *args, **kwargs):
            item_filter = kwargs.get("filter")
            items = Model.objects.filter(student_filter)
            # wrap ...
            return data

    Query String:

        pattern: field__cmp=value

        example: name__exact, date__le, number__gt

        example uri: ?name__exact=abc&date__le=114514
            corresponding dict:
            {
                'name__exact': 'abc',
                'date__le': '114514'
            }
    """
    def decorator(func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            separator = "__"
            if custom is not None:
                custom_fields = custom.keys()
            else:
                custom_fields = []
            q_now = Q()
            query_dict = request.GET.dict()
            for field in fields:
                field_name = field[0]
                type_attr = field[1]
                querys = [(key, query_dict.get(key))
                          for key in query_dict.keys() if key.startswith(field_name + separator)]
                for query in querys:
                    key: str = query[0]
                    # type conversion
                    if type_attr is not str:
                        try:
                            value = type_attr(ast.literal_eval(query[1]))
                        except ValueError:
                            return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS,
                                                       "Sorry, {} should be {}.".format(field_name, type_attr.__name__))
                    else:
                        value = query[1]
                    # should be handled in func
                    if field[0] in custom_fields:
                        item_filter = custom.get(field[0])(key, value)
                    # ne support
                    else:
                        if key.endswith("ne"):
                            item_filter = ~Q(**{key[0:-2]+"exact": value})
                        else:
                            item_filter = Q(**{key: value})
                    q_now &= item_filter
            kwargs.update({"filter": q_now})
            return func(request, *args, **kwargs)
        return wrapper
    return decorator


def query_order_by(fields=List[str]):
    """parse order_by filter in query string

    '-' prefix means reverse.

    Example of Usage:

        @response_wrapper
        @require_GET
        @query_order_by(fields=["name"])
        def list_items(request: HttpRequest, *args, **kwargs):
            item_orders = kwargs.get("order_by")
            items = Model.objects.all()
            for item_order in item_orders:
                items = items.order_by(item_order)
            # wrap ...
            return data

    Query String:

        pattern: order_by=field

        example: order_by=name, order_by=-number

        example uri: ?order_by=name+date+-number
            corresponding dict:
            {
                'order_by': 'name date -number'
            }
    """
    def decorator(func):
        def wrapper(request: HttpRequest, *args, **kwargs):
            allowed_fields: set = {""}
            for field in fields:
                allowed_fields.add(field)
                allowed_fields.add("-" + field)
            query_dict = request.GET.dict()
            order_by = query_dict.get("order_by")
            if order_by is None:
                return func(request, *args, **kwargs)
            order_by_values = order_by.split(" ")
            for order_by_value in order_by_values:
                if not order_by_value in allowed_fields:
                    return failed_api_response(ErrorCode.INVALID_REQUEST_ARGS,
                                               "Sorry, it is not valid to order by {}.".format(order_by_value))
            kwargs.update({"order_by": order_by_values})
            return func(request, *args, **kwargs)
        return wrapper
    return decorator
