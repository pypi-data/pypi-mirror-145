from django.test import TestCase
from softdelete.tests.models import TestModel


class TestDeletionModel(TestCase):

    def setUp(self):
        self.obj = TestModel.objects.create(title='new model')
        self.obj2 = TestModel.objects.create(title='new model 2')

    def test_delete_function(self):
        """Test that delete function don't delete the from db and modify deleted_at from None to now time"""
        obj = self.obj
        self.assertEquals(obj.deleted_at, None)
        obj.delete()
        self.assertNotEqual(obj.deleted_at, None)

    def test_double_deletion(self):
        """Test that if object that deleted once cant delete it again and throw an exception"""
        obj = self.obj
        obj.delete()
        with self.assertRaises(ValueError):
            obj.delete()

    def test_query_set_had_wright_objects(self):
        """Test that after soft deletion query set returns with the values that didn't deleted"""
        obj_1 = self.obj
        obj_2 = self.obj2
        self.assertEquals(len(TestModel.objects.all()), 2)
        obj_1.delete()
        self.assertEquals(len(TestModel.objects.all()), 1)
        self.assertEquals(TestModel.objects.all()[0], obj_2)

    def test_all_objects_returns_all_objects_in_db(self):
        """Test that all_objects returns all objects in the db with deleted ones"""
        obj_1 = self.obj
        obj_1.delete()
        self.assertEquals(len(TestModel.all_objects.all()), 2)

    def test_alive_function_returns_not_deleted_objects(self):
        """Test that alive function returns all objects that didn't deleted yet"""
        obj_1 = self.obj
        obj_2 = self.obj2

        obj_1.delete()
        returned_object = TestModel.all_objects.all().alive()[0]
        self.assertEquals(returned_object, obj_2)

    def test_dead_function_returns_deleted_objects(self):
        obj_1 = self.obj
        obj_1.delete()
        returned_object = TestModel.all_objects.all().dead()[0]
        self.assertEquals(returned_object, obj_1)

    def test_hard_delete_deletes_objects_from_db(self):
        """Test that hard delete objects from database permanently"""
        obj = self.obj
        obj2 = self.obj2
        obj.hard_delete()
        obj2.hard_delete()
        self.assertEquals(0, TestModel.all_objects.all().count())
