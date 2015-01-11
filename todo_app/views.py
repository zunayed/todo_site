import json

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from models import Todo


def index(request):
    return HttpResponse("Hello, world. You're at the api index.")


@require_http_methods(["GET"])
def todos(request):
    all_todos = Todo.objects.all()

    if all_todos:
        data = [todo.dict for todo in all_todos]
        return HttpResponse(
            json.dumps(data),
            content_type="application/json"
        )
    else:
        return HttpResponse('[]', content_type="application/json")
