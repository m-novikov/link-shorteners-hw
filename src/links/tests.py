from django.db import IntegrityError
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from links.models import Link, LinkHit


class LinkTestCase(TestCase):
    def setUp(self):
        Link.objects.create(link_hash="GOOGLE", url="https://google.com")
        Link.objects.create(link_hash="YOUTUB", url="https://youtube.com")

    def test_links_retived_by_hash(self):
        google_link = Link.objects.get(link_hash="GOOGLE")
        youtube_link = Link.objects.get(link_hash="YOUTUB")

        self.assertEqual(google_link.url, "https://google.com")
        self.assertEqual(youtube_link.url, "https://youtube.com")

    def test_no_duplicate_hashes_allowed(self):
        with self.assertRaises(IntegrityError):
            Link.objects.create(link_hash="GOOGLE", url="https://google.ru/")

    def test_no_duplicate_urls_allowed(self):
        with self.assertRaises(IntegrityError):
            Link.objects.create(link_hash="AFSFAA", url="https://google.com")

    def test_default_hit_count_is_0(self):
        google_link = Link.objects.get(link_hash="GOOGLE")

        self.assertEqual(google_link.hits, 0)


class LinkAPITestCase(TestCase):
    def setUp(self):
        self.api_client = APIClient()
        self.api_client.force_authenticate()
        self.link = Link.objects.create(link_hash="LINKAA", url="https://linkaa.com")
        self.other_link = Link.objects.create(
            link_hash="LINKBB", url="https://linkbb.com"
        )

    def test_create_link(self):
        url = "https://link01.com"
        resp = self.api_client.post("/links/", {"url": url}, format="json")

        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(resp.data["link_hash"]), 6)
        self.assertEqual(resp.data["url"], url)

    def test_retrieve_link(self):
        url = "https://yandex.com"
        link_hash = "YANDEX"
        Link.objects.create(link_hash=link_hash, url=url)

        resp = self.api_client.get(f"/links/{link_hash}/", format="json")

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(resp.data["link_hash"], link_hash)
        self.assertEqual(resp.data["url"], url)

    def test_404_on_missing_missing_link(self):
        link_hash = "OTHER0"

        resp = self.api_client.get(f"/links/{link_hash}/", format="json")

        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

        resp = self.api_client.get(f"/{link_hash}", format="json", follow=False)
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_redirection_link(self):
        resp = self.api_client.get(
            f"/{self.link.link_hash}", format="json", follow=False
        )
        self.assertEqual(resp.status_code, status.HTTP_302_FOUND)

    def test_using_redirection_link_increases_hit_counter(self):
        self.assertEqual(self.link.hits, 0)
        resp = self.api_client.get(
            f"/{self.link.link_hash}", format="json", follow=False
        )
        self.assertEqual(resp.status_code, status.HTTP_302_FOUND)

        self.link.refresh_from_db()
        self.assertAlmostEqual(self.link.hits, 1)

        for _ in range(30):
            resp = self.api_client.get(
                f"/{self.link.link_hash}", format="json", follow=False
            )
            self.assertEqual(resp.status_code, status.HTTP_302_FOUND)

        self.link.refresh_from_db()
        self.assertAlmostEqual(self.link.hits, 31)

        all_hits = self.link.link_hits.all()
        self.assertEqual(len(all_hits), 31)

    def test_hits_api(self):
        for _ in range(100):
            LinkHit.objects.create(link=self.link)

        for _ in range(70):
            LinkHit.objects.create(link=self.other_link)

        resp = self.api_client.get(f"/links/{self.link.link_hash}/hits/", format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 100)

        resp = self.api_client.get(
            f"/links/{self.other_link.link_hash}/hits/", format="json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 70)

        resp = self.api_client.get("/hits/", format="json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 170)
