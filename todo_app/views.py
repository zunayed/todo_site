import json

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.http import require_http_methods
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from models import Todo


def index(request):
    return HttpResponse("Hello, world. You're at the api index.")


@csrf_exempt
@require_http_methods(['GET', 'POST'])
def todos(request):
    if request.method == 'GET':
        all_todos = Todo.objects.all()

        if all_todos:
            data = [todo.dict for todo in all_todos]
            return HttpResponse(
                json.dumps(data),
                content_type='application/json'
            )
        else:
            return HttpResponse('[]', content_type='application/json')

    if request.method == 'POST':
        post_data = json.loads(request.body)
        if 'task' in post_data.keys():
            todo = Todo(task=post_data['task'])
            todo.save()

            return HttpResponse(
                json.dumps(todo.dict),
                status=201,
                content_type='application/json'
            )
        else:
            return HttpResponseBadRequest(
                json.dumps({'errors': 'Missing fields'}),
                content_type='application/json'
            )


@csrf_exempt
@require_http_methods(['GET', 'PUT', 'DELETE'])
def get_todo(request, id):
    todo_instance = get_object_or_404(Todo, id=id)
    if request.method == 'GET':
        return HttpResponse(
            json.dumps(todo_instance.dict),
            content_type='application/json'
        )

    if request.method == 'PUT':
        put_data = json.loads(request.body)
        if set(['task', 'complete']).issubset(put_data.keys()):
            todo_instance.task = put_data['task']
            todo_instance.complete = put_data['complete']
            todo_instance.save()
            return HttpResponse(
                json.dumps({'message': 'resource successfully updated'}),
                content_type='application/json'
            )
        else:
            return HttpResponseBadRequest(
                json.dumps({'errors': 'Missing fields'}),
                content_type='application/json'
            )

    if request.method == 'DELETE':
        todo_instance.delete()
        return HttpResponse(
            json.dumps({'message': 'resource successfully deleted'}),
            content_type='application/json'
        )
