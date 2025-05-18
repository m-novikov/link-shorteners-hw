from django.test import TestCase
from django.db import IntegrityError
from links.models import Link


class AnimalTestCase(TestCase):
    def setUp(self):
        Link.objects.create(link_hash="GOOGLE",url="https://google.com")
        Link.objects.create(link_hash="YOUTUB",url="https://youtube.com")

    def test_links_retived_by_hash(self):
        google_link = Link.objects.get(link_hash="GOOGLE")
        youtube_link = Link.objects.get(link_hash="YOUTUB")

        self.assertEqual(google_link.url, "https://google.com")
        self.assertEqual(youtube_link.url, "https://youtube.com")

    def test_no_duplicate_hashes_allowed(self):
        with self.assertRaises(IntegrityError):
            Link.objects.create(link_hash="GOOGLE", url="https://google.ru/")

    def test_no_duplicate_urls_allowed(self):
        google_link = Link.objects.get(link_hash="GOOGLE")
        with self.assertRaises(IntegrityError):
            Link.objects.create(link_hash="AFSFAA", url="https://google.com")

    def test_default_hit_count_is_0(self):
        google_link = Link.objects.get(link_hash="GOOGLE")

        self.assertEqual(google_link.hits, 0)