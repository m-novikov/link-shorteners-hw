from django.test import TestCase
from django.db import IntegrityError
from links.models import Link
from rest_framework.test import APIClient
from rest_framework import status




class LinkTestCase(TestCase):
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


class LinkAPITestCase(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        self.api_client.force_authenticate()

    def test_create_link(self):
        url = 'https://link01.com'
        resp = self.api_client.post('/links/', {'url': url}, format='json')

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(resp.data['link_hash']), 6)
        self.assertEqual(resp.data['url'], url)

    def test_retrieve_link(self):
        url = "https://yandex.com"
        link_hash = "YANDEX"
        Link.objects.create(link_hash=link_hash, url=url)

        resp = self.api_client.get(f'/links/{link_hash}/', format='json')

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data['link_hash'], link_hash)
        self.assertEqual(resp.data['url'], url)

    def test_404_on_missing_missing_link(self):
        link_hash = "OTHER0"

        resp = self.api_client.get(f'/links/{link_hash}/', format='json')

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

        resp = self.api_client.get(f'/{link_hash}', format='json', follow=False)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_redirection_link(self):
        url = "https://yandex.com"
        link_hash = "YANDEX"
        Link.objects.create(link_hash=link_hash, url=url)
        resp = self.api_client.get(f'/{link_hash}', format='json', follow=False)
        self.assertEqual(resp.status_code, status.HTTP_302_FOUND)