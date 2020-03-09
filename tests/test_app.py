import unittest

from flaskapp.app import app


class BasicTestCase(unittest.TestCase):
    def test_home(self):
        tester = app.test_client(self)
        response = tester.get("/", content_type="html/text")
        self.assertEqual(response.status_code, 200)

    def test_other(self):
        tester = app.test_client(self)

        response = tester.get("/showSignUp", content_type="html/text")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
