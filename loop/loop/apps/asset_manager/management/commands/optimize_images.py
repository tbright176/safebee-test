import subprocess
import urllib

from boto.s3.connection import S3Connection

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.create_s3_connection()
        origin_bucket = self.get_origin_bucket()
        keys = origin_bucket.list()
        for img in keys:
            if img.name.find('.jpg') >= 0 or img.name.find('.JPG') >= 0:
                print img.name
                self.optimize_image(img)
            else:
                print "Skipping ", img.name

    def create_s3_connection(self):
        self.conn = S3Connection(settings.AWS_ACCESS_KEY_ID,
                                 settings.AWS_SECRET_ACCESS_KEY)

    def get_origin_bucket(self):
        bucket_name = settings.AWS_STORAGE_BUCKET_NAME
        print bucket_name
        return self.conn.get_bucket(bucket_name)

    def optimize_image(self, img):
        url = img.generate_url(expires_in=0, query_auth=False, force_http=True)
        filename, headers = urllib.urlretrieve(url)
        try:
            proc = subprocess.check_output("/usr/local/bin/jpegoptim %s" % filename,
                                           shell=True)
        except subprocess.CalledProcessError:
            print "ERROR: ", img.name
            return
        fp = open(filename)
        output = fp.read()
        headers = dict()
        headers['Content-Type'] = 'image/jpeg'
        headers['Content-Length'] = str(len(output))
        headers['Cache-Control'] = 'max-age=2592000'
        headers['Expires'] = 'Fri, 31 Dec 2031 23:59:59 GMT'
        img.set_contents_from_string(output, headers=headers,
                                     policy='public-read')
        fp.close()
