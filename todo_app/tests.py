import json

from django.test import TestCase
from django.core.urlresolvers import reverse

from models import Todo


class TodoTestData():

    def __init__(self):
        self.todo_list = [
            'End world hugner',
            'Hang out with kanye',
            'find missing socks'
        ]

        for todo in self.todo_list:
            t = Todo(task=todo)
            t.save()


class ModelTests(TestCase):

    def setUp(self):
        self.test_data = TodoTestData()

    def test_todo_models(self):
        # check if setup created all the models
        all_todos = Todo.objects.all()
        self.assertEqual(len(all_todos), 3)

        # check if tasks were properly assigned
        for orig_text, todo in zip(self.test_data.todo_list, all_todos):
            self.assertEqual(orig_text, todo.task)
            self.assertEqual(False, todo.complete)


class ViewTests(TestCase):

    def setUp(self):
        self.test_data = TodoTestData()

    def test_get_all_todos(self):
        """
        GET /todo
        """
        end_point = reverse('api_v1:todos')
        response = self.client.get(end_point)
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]['task'], self.test_data.todo_list[0])
        self.assertEqual(data[0]['complete'], False)
        self.assertEqual(data[2]['task'], self.test_data.todo_list[2])

    def test_get_one_todo(self):
        pass

    def test_update_todo(self):
        pass

    def test_delete_todo(self):
        pass
