
import email
from requests import request

from exam.models import ToDouser
from .test_setup import TestSetUp
from django.test import Client
from rest_framework.test import force_authenticate
#Task 5 Unit Test 

class TestViews(TestSetUp):


    def test_user_cannot_register_with_no_data(self):
        res = self.client.post(self.register_url)
        # import pdb
        # pdb.set_trace()
        self.assertEqual(res.status_code,400)


    def test_user_can_register_correctly(self):
        res = self.client.post(self.register_url, self.user_data, format="json")
       

        self.assertEqual(res.status_code,201)

    def test_user_login(self):

        self.client.post(self.register_url, self.user_data, format="json")
        res = self.client.post(self.login_url, self.user_data, format="json")
      
        self.assertEqual(res.status_code, 200)

    
    def test_unauthorized_user_cannot_add_todo(self):
        
        res = self.client.post(self.addtodo_url, self.todo_data, format="json")
       
        
        self.assertEqual(res.status_code,401)

   
