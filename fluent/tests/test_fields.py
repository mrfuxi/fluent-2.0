
from django.db import models
from djangae.test import TestCase

from fluent.fields import (
    TranslatableField,
    TranslatableContent,
    find_all_translatable_fields
)
from fluent.models import MasterTranslation

from djangae.db.caching import disable_cache

class TestModel(models.Model):
    class Meta:
        app_label = "fluent"


    trans = TranslatableField()
    trans_with_hint = TranslatableField(hint="Test")
    trans_with_group = TranslatableField(group="Test")


class TranslatableFieldTests(TestCase):

    def test_unset_translations(self):
        m = TestModel.objects.create()

        self.assertEqual("", m.trans.text)
        self.assertEqual("", m.trans_with_hint.text)
        self.assertEqual("", m.trans_with_group.text)

        m.save()

        self.assertEqual("", m.trans.text)
        self.assertEqual("", m.trans_with_hint.text)
        self.assertEqual("", m.trans_with_group.text)

    def test_setting_translation_text(self):
        m = TestModel()
        m.trans.text = "Hello World!"
        m.trans_with_group.text = "Hello World!"
        m.trans_with_hint.text = "Hello World!"
        m.save()

    def test_finding_all_translations_for_a_group(self):
        TestModel.objects.create()
        translations = MasterTranslation.find_by_group("Test")
        self.assertEqual(0, translations.count())

        TestModel.objects.create(trans_with_group=TranslatableContent(text="Hello World!"))

        translations = MasterTranslation.find_by_group("Test")
        self.assertEqual(1, translations.count())


class TestLocatingTranslatableFields(TestCase):
    def test_find_all_translatable_fields(self):
        results = find_all_translatable_fields()

        # Just filter the results down to this app
        results = [ x for x in results if x[0]._meta.app_label == "fluent" ]

        # Should return the 3 fields of TestModel above
        self.assertEqual(3, len(results))
        self.assertEqual(TestModel, results[0][0])
        self.assertEqual(TestModel, results[1][0])
        self.assertEqual(TestModel, results[2][0])

        results = find_all_translatable_fields(with_group="Test")
        # Just filter the results down to this app
        results = [ x for x in results if x[0]._meta.app_label == "fluent" ]

        # Should return the one field with this group
        self.assertEqual(1, len(results))
        self.assertEqual(TestModel, results[0][0])
