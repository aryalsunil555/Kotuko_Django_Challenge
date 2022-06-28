from rest_framework.test import APITestCase
from django.urls import reverse


class TestSetUp(APITestCase):
    
    def setUp(self):
        self.register_url=reverse('register')
        self.login_url=reverse('login')
        self.addtodo_url = reverse('addtodo')
        
        self.user_data ={
            'fullname':"Sunil Aryal",
            'email':"email@gmail.com",
            'password':"password",
            'password2':"password"
        }

        self.todo_data ={
            'name':"Read Books",
            'description':"to read book",
            'image':"image.jpg",
            
        }
        self.cred_data ={
         
            'email':"email@gmail.com",
            'password':"password"
         
        }

     
    def tearDown(self):
        return super().tearDown()

