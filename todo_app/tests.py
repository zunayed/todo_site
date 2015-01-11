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
        """
        GET /todo/<id>
        """
        end_point = reverse('api_v1:get_todo', kwargs={'id': '2'})
        response = self.client.get(end_point)
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)

        self.assertEqual(data['task'], self.test_data.todo_list[1])
        self.assertEqual(data['complete'], False)

        # test with bad id
        end_point = reverse('api_v1:get_todo', kwargs={'id': '99'})
        response = self.client.get(end_point)
        self.assertEqual(response.status_code, 404)

    def test_create_one_todo(self):
        """
        POST /todos
        """
        end_point = reverse('api_v1:todos')
        post_data = {
            'task': 'new test post',
            'complete': 'True',
        }
        # import ipdb; ipdb.set_trace()

        response = self.client.post(
            end_point,
            post_data
        )

        new_post = Todo.objects.get(task='new test post')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(new_post.task, post_data['task'])
        self.assertEqual(new_post.complete, bool(post_data['complete']))

        # test with bad post data
        bad_post_data = {
            'task': 'new test post',
        }

        response = self.client.post(
            end_point,
            bad_post_data
        )

        self.assertEqual(response.status_code, 400)

    def test_update_todo(self):
        """
        PUT /todo/<id>
        """
        end_point = reverse('api_v1:get_todo', kwargs={'id': '1'})
        put_data = {
            'task': 'test changes',
            'complete': 'True',
        }
        response = self.client.put(
            end_point,
            json.dumps(put_data)
        )
        updated_object = Todo.objects.get(id=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(updated_object.task, put_data['task'])
        self.assertEqual(updated_object.complete, bool(put_data['complete']))

        # put request with bad data
        bad_put_data = {
            'task': 'test changes',
        }
        response = self.client.put(
            end_point,
            json.dumps(bad_put_data)
        )

        self.assertEqual(response.status_code, 400)

    def test_delete_todo(self):
        """
        DELETE /todo/<id>
        """
        end_point = reverse('api_v1:get_todo', kwargs={'id': '1'})

        response = self.client.delete(end_point)
        all_todos = Todo.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(all_todos), 2)
