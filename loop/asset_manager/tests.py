import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import (Asset, Image, License, image_asset_storage_path,
                     image_asset_storage_subpath)


User = get_user_model()


class AssetSubClass(Asset):
    """
    Dummy Asset subclass for testing NotImplementedError exceptions.
    """
    pass


class AssetTestCase(TestCase):

    def setUp(self):
        self.assetSubClass = AssetSubClass()

    def test_asset_subclass_does_not_implement_asset_property(self):
        with self.assertRaises(NotImplementedError):
            self.assetSubClass.asset

    def test_asset_subclass_does_not_implement_get_absolute_url(self):
        with self.assertRaises(NotImplementedError):
            self.assetSubClass.get_absolute_url()


class ImageTestCase(TestCase):

    fixtures = ['test_data.json',]

    def setUp(self):
        self.image = Image.objects.create(caption="This is the caption.")
        self.now = datetime.datetime.now()

    def test_image_unicode(self):
        self.assertEqual(u"%s" % self.image, self.image.caption)

    def test_image_implements_asset_property(self):
        self.assertTrue(hasattr(self.image, 'asset'))

    def test_image_storage_path(self):
        filename = "redneck-family-tree_o_870746.jpg"
        path = "assets/images/%d/%d/%s" % (self.now.year, self.now.month,
                                           filename)
        test_image = Image.objects.get(pk=1)
        returned_path = image_asset_storage_path(test_image, filename)
        self.assertEqual(path, returned_path)

    def test_image_storage_subpath(self):
        subpath = "redneck-family-tree_o_870746"
        subpath_filename = "social.jpg"
        path = "assets/images/%d/%d/%s/%s" % (self.now.year, self.now.month,
                                              subpath, subpath_filename)
        test_image = Image.objects.get(pk=1)
        returned_path = image_asset_storage_subpath(test_image,
                                                    subpath_filename)
        self.assertEqual(path, returned_path)


class LicenseTestCase(TestCase):

    def setUp(self):
        self.license = License.objects.create(name=u"Creative Commons")

    def test_license_unicode(self):
        license_name = unicode(self.license)
        self.assertEqual(license_name, self.license.name)
