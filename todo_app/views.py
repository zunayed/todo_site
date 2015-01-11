import json
import ast

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404

from models import Todo
from forms import TodoForm


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


@require_http_methods(["GET", "PUT", "DELETE"])
def get_todo(request, id):
    todo_instance = get_object_or_404(Todo, id=id)
    if request.method == 'GET':
        return HttpResponse(
            json.dumps(todo_instance.dict),
            content_type="application/json"
        )

    if request.method == 'PUT':
        form = TodoForm(ast.literal_eval(request.body), instance=todo_instance)
        if form.is_valid():
            form.save()
            return HttpResponse(
                'resource updated successfully',
                content_type="application/json"
            )
        else:
            return HttpResponseBadRequest(
                json.dumps(form.errors),
                content_type="application/json"
            )

    if request.method == 'DELETE':
        todo_instance.delete()
        return HttpResponse(
            'resource successfully deleted',
            content_type="application/json"
        )
