from django.test import TestCase, Client
from forum.models import Author, Category, Post, Comment, Reply
from django.contrib.auth.models import User
from django.urls import reverse
from team.models import Coach, Athlete
import json


class TestForumModels(TestCase):

    @classmethod
    def setUpTestData(cls):    
        testuser = User.objects.create_user(
            username='testuser', password='12345'
        )
        testauthor = Author.objects.create(
            fullname="Test Author", bio="some bio", slug="django", user=testuser
        )
        cls.fullname=Author.objects.create(fullname="Test User1", user=testuser)
        cls.category = Category.objects.create(title="Django Testing")
        cls.post = Post.objects.create(
            title="test post1", user=testauthor)
        cls.comment = Comment.objects.create(
            content ="test comment ", user=testauthor)
        cls.reply = Reply.objects.create(
            content="test reply ", user=testauthor)
        
    def test_model_Author_str(self):
        
        self.assertEqual(str(self.fullname), "Test User1")

    def test_model_category_str(self):    
        self.assertEqual(str(self.category), "Django Testing")

    def test_model_Post_str(self):
        self.assertEqual(str(self.post), "test post1")

    def test_model_Comment_str(self):
        self.assertEqual(str(self.comment.content), "test comment ")

    def test_model_Reply_str(self):
        self.assertEqual(str(self.reply.content), "test reply ")


class TestForumViews(TestCase):

    def test_forum_list(self):
        client = Client()

        response = client.get(reverse('posts'))

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'forum/posts.html' )


class TestTeamModels(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.testcoach = Coach.objects.create(name="testCoach")
        cls.testathlete = Athlete.objects.create(name="testAthlete", DOB="1984-07-28")

    def test_model_Athlete_str(self):
        print('test2')
        self.assertEqual(str(self.testathlete.name), "testAthlete")

    def test_model_Coach_str(self):
        self.assertEqual(str(self.testcoach.name), "testCoach")