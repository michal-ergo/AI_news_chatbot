import unittest
from unittest.mock import patch
from news_api_client import NewsAPIClient

class TestnewsAPIClient(unittest.TestCase):
    def setUp(self):
        self.client = NewsAPIClient("dummy_api_key")
        self.articles = [
            {
                "title": "Test Article",
                "author": None,
                "source": {"name": "Test Source"},
                "description": "Test Description",
                "content": "content",
                "url": "http://testurl.com"

            }
        ]

    def test_format_articles(self):
        formatted_articles = self.client.format_articles(self.articles)
        expected_articles = [
            {
                "title": "Test Article",
                "author": "Unknown",
                "source name": "Test Source",
                "description": "Test Description",
                "content": "content",
                "url": "http://testurl.com"
            }
        ]
        self.assertDictEqual(formatted_articles[0], expected_articles[0])

    def test_build_request_parameters(self):
        url, params = self.client.build_requests("technology", 10)
        expected_url = "https://newsapi.org/v2/everything"
        expected_params = {"q": "technology", "apiKey": "dummy_api_key", "pageSize": 10}
        self.assertEqual(url, expected_url)
        self.assertDictEqual(params, expected_params)

    # mocking, @odekorování další funkcí (patch)
    @patch("news_api_client.NewsAPIClient.make_api_call")
    def test_fetch_news(self, mock_make_api_call):
        mock_make_api_call.return_value = {"articles": self.articles}
        articles = self.client.fetch_news("technology", 10)

        expected_articles = [{
                "title": "Test Article",
                "author": "Unknown",
                "source": {"name": "Test Source"},
                "description": "Test Description",
                "content": "content",
                "url": "http://testurl.com"            
        }]

        self.assertEqual(len(articles), 1)
        self.assertDictEqual(articles[0], expected_articles[0])

if __name__ == "__main__":
    unittest.main()