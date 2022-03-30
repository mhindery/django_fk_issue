from django.test import TestCase
from poc_models.models import Object, RemoteObject


class FKTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        Object.objects.create(remote_object_id=1234)

    # All of the test methods below try to fetch the same object which was created in setUpTestData

    def test_remote_object_does_exist_object_should_be_found(self):
        RemoteObject.objects.create(remote_id=1234)

        db_objects = Object.objects.filter(remote_object_id=1234)
        self.assertIsNotNone(db_objects.first())

    def test_remote_object_does_exist_object_select_related_should_be_found(self):
        RemoteObject.objects.create(remote_id=1234)

        db_objects = Object.objects.filter(
            remote_object_id=1234).select_related('remote_object')
        self.assertIsNotNone(db_objects.first())

    def test_remote_object_does_not_exist_object_should_be_found(self):

        db_objects = Object.objects.filter(remote_object_id=1234)
        self.assertIsNotNone(db_objects.first())

    def test_remote_object_does_not_exist_object_with_select_related_should_be_found(self):
        ''' This one fails while it should not, due to the select_related addition '''

        # Note that the only difference here versus the test above (test_remote_object_does_not_exist_object_should_be_found) is the
        # addition of the select_related call, which breaks the lookup. Note the query below which incorrectly uses an INNER JOIN statement.
        # Since the remote object does not exist, this join will remove the row from the results, which is incorrect behaviour.
        db_objects = Object.objects.filter(remote_object_id=1234).select_related('remote_object')

        # print(db_objects._query)
        # SELECT "poc_models_object"."id", "poc_models_object"."remote_object_id", "poc_models_remoteobject"."id", "poc_models_remoteobject"."remote_id"
        # FROM "poc_models_object"
        #     INNER JOIN "poc_models_remoteobject" ON ("poc_models_object"."remote_object_id" = "poc_models_remoteobject"."remote_id")
        # WHERE "poc_models_object"."remote_object_id" = 1234

        self.assertIsNotNone(db_objects.first())

    def test_remote_object_does_not_exist_object_no_filter_with_select_related_should_be_found(self):
        ''' This one works, even with select_related, because we don't filter the QS '''

        # Difference from the test above (test_remote_object_does_not_exist_object_with_select_related_should_be_found) is that we don't filter the qs here.
        # Looking at the query which is generated, it uses a LEFT OUTER JOIN, which is correct. A missing remote object (which is the case here) won't
        # cause the row to be dropped from the results.
        db_objects = Object.objects.filter().select_related('remote_object')

        # print(db_objects._query)
        # SELECT "poc_models_object"."id", "poc_models_object"."remote_object_id", "poc_models_remoteobject"."id", "poc_models_remoteobject"."remote_id"
        # FROM "poc_models_object"
        #     LEFT OUTER JOIN "poc_models_remoteobject" ON("poc_models_object"."remote_object_id"="poc_models_remoteobject"."remote_id")

        self.assertIsNotNone(db_objects.first())

    def test_remote_object_does_not_exist_object_with_prefetch_related_should_be_found(self):

        # Use prefetch_related instead of select_related, then it works
        db_objects = Object.objects.filter(remote_object_id=1234).prefetch_related('remote_object')

        # print(db_objects._query)
        # SELECT "poc_models_object"."id", "poc_models_object"."remote_object_id"
        # FROM "poc_models_object"
        # WHERE "poc_models_object"."remote_object_id" = 1234

        self.assertIsNotNone(db_objects.first())
