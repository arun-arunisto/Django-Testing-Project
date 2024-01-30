from django.test import SimpleTestCase
from django.urls import reverse, resolve
from budget.views import home, ProjectCreateView, project_detail

class TestUrls(SimpleTestCase):

    #first url for home
    def test_home_url_is_resolved(self):
        url = reverse('home')
        #print(resolve(url))
        self.assertEquals(resolve(url).func, home, "Test Failed")

    # second url for add #class view
    def test_add_url_is_resolved(self):
        url = reverse('add')
        #print(resolve(url))
        self.assertEquals(resolve(url).func.view_class, ProjectCreateView, "Test Failed")

    # third url for detail
    def test_detail_url_is_resolved(self):
        url = reverse('detail', args=['some-slug']) #adding this because we need slug to run
        print(resolve(url))
        #self.assertEquals(resolve(url).func.view_class, ProjectCreateView, "Test Failed")