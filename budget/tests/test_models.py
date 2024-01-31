from django.test import TestCase
from budget.models import Project, Category, Expense

class TestModels(TestCase):

    def setUp(self):
        self.project1 = Project.objects.create(
            name='Project 1',
            budget=100000
        )

    #first checking the slug creation wrks correctly
    def test_project_is_assigned_slug_on_creation(self):
        self.assertEquals(self.project1.slug, 'project-1', "Test Failed")

    #next we are going to check budget left
    def test_budget_left(self):
        category1 = Category.objects.create(
            project=self.project1,
            name='development'
        )
        Expense.objects.create(
            project=self.project1,
            title='expense1',
            amount=2000,
            category=category1
        )
        Expense.objects.create(
            project=self.project1,
            title='expense2',
            amount=2000,
            category=category1
        )

        self.assertEquals(self.project1.budget_left, 96000, "Test Failed")

    #checking total_expenses
    def test_total_expenses(self):
        project2 = Project.objects.create(
            name='project2',
            budget=10000
        )
        category1 = Category.objects.create(
            project=project2,
            name='development'
        )
        Expense.objects.create(
            project=self.project1,
            title='expense1',
            amount=1000,
            category=category1
        )
        Expense.objects.create(
            project=project2,
            title='expense2',
            amount=2000,
            category=category1
        )

        self.assertEquals(project2.total_transactions, 1, "Test Failed")


