from django.test import TestCase, Client
from django.urls import reverse
from budget.models import Project, Category, Expense
import json


class TestViews(TestCase):

    #initializing arguments
    def setUp(self):
        self.client = Client()
        self.home_url = reverse('home')
        self.project_detail_url = reverse('detail', args=['project1'])
        """
        project1 is not created so, it will cause an 404 that's why our test fails, so first we need to
        create a 'project1' in Project
        """
        self.project = Project.objects.create(
            name='project1',
            budget='250000'
        )
        self.project_create_url = reverse('add')

    #home view
    def test_home_GET(self):
        response = self.client.get(self.home_url)
        self.assertEquals(response.status_code, 200, "Test Failed")
        self.assertTemplateUsed(response, 'budget/index.html', "Template Failed")

    """
    On the project_detail view method there's 3 methods using GET, POST, DELETE
    so, we need to check these three
    """
    #project detail - GET method
    def test_project_detail_GET(self):
        response = self.client.get(self.project_detail_url)
        self.assertEquals(response.status_code, 200, "Test Failed")
        self.assertTemplateUsed(response, 'budget/project-detail.html', "Template Failed")

    #project detail - POST method with data
    def test_project_detail_POST_adds_new_expense(self):
        #adding category first
        Category.objects.create(
            project=self.project,
            name='development'
        )

        response = self.client.post(self.project_detail_url, {
            'title':'expense1',
            'amount':1000,
            'category':'development'
        })

        self.assertEquals(response.status_code, 302, "Test Failed") #302 using because it's redirecting!!
        self.assertEquals(self.project.expenses.first().title, 'expense1', "Test Failed")

    #project detail - POST method without data
    def test_project_detail_POST_no_data(self):
        response = self.client.post(self.project_detail_url)
        self.assertEquals(response.status_code, 302, "Test Failed")
        self.assertEquals(self.project.expenses.count(), 0, "Test Failed")

    #project detail - DELETE method
    def test_project_detail_DELETE_deletes_expenses(self):
        category1 = Category.objects.create(
            project=self.project,
            name='development'
        )
        Expense.objects.create(
            project=self.project,
            title='expense1',
            amount='1000',
            category=category1
        )

        response = self.client.delete(self.project_detail_url,
                                      json.dumps({
                                          'id':1
                                      })) #on views we are using json to loads the data
        self.assertEquals(response.status_code, 204, "Test Failed") #204 on views
        self.assertEquals(self.project.expenses.count(), 0, "Test Failed")

    # project detail - DELETE method
    def test_project_detail_DELETE_with_no_id(self):
        category1 = Category.objects.create(
            project=self.project,
            name='development'
        )
        Expense.objects.create(
            project=self.project,
            title='expense1',
            amount='1000',
            category=category1
        )

        response = self.client.delete(self.project_detail_url)
        self.assertEquals(response.status_code, 404, "Test Failed") #it will cause an error so add try and except on views
        self.assertEquals(self.project.expenses.count(), 1, "Test Failed")

    #project create view - POST method last one
    def test_project_create_POST(self):
        response = self.client.post(self.project_create_url, {
            'name':'project2',
            'budget':250000,
            'categoriesString':'design,development'
        })

        #checking the project creates
        project2 = Project.objects.get(id=2)
        self.assertEquals(project2.name, 'project2', "Test Failed")

        #checking the categories created correctly
        #first_category
        category_1 = Category.objects.get(id=1)
        self.assertEquals(category_1.project, project2, "Test Failed")
        self.assertEquals(category_1.name, 'design', "Test Failed")

        #second_category
        category_2 = Category.objects.get(id=2)
        self.assertEquals(category_2.project, project2, "Test Failed")
        self.assertEquals(category_2.name, 'development', "Test Failed")


