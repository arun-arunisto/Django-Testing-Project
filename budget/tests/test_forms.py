from django.test import SimpleTestCase
from budget.forms import ExpenseForm


class TestForms(SimpleTestCase):
    #form with valid data
    def test_expense_forms_valid_data(self):
        form = ExpenseForm(data={
            'title':'expense1',
            'amount':1000,
            'category':'development'
        })

        self.assertTrue(form.is_valid(), "Test Failed")

    #form without data
    def test_expense_forms_no_data(self):
        form = ExpenseForm(data={})
        self.assertFalse(form.is_valid(), "Test Failed")
        self.assertEquals(len(form.errors), 3, "Test Failed")


