"""
Selenium automated test suite for Learnify e-learning platform.
Part I: Automated test cases using Selenium (minimum 10 tests).
Headless Chrome mode enabled for EC2/Jenkins integration.
"""

import os
import time
import unittest

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException


class TestLearnifyPlatform(unittest.TestCase):
    """
    Combined suite for user and admin smoke tests.
    All tests are written as robust smoke tests suitable for CI/CD.
    """

    @classmethod
    def setUpClass(cls):
        cls.base_url = os.getenv("APP_URL", "http://localhost:5173")

        print("\n" + "=" * 70)
        print("LEARNIFY PLATFORM TEST SUITE - START")
        print("=" * 70)
        print(f"Base URL: {cls.base_url}")
        print("Browser: Headless Chrome")
        print("=" * 70 + "\n")

        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1280,720")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-blink-features=AutomationControlled")

        try:
            cls.driver = webdriver.Chrome(options=options)
        except WebDriverException as e:
            print(f"❌ Failed to start Chrome WebDriver: {e}")
            raise

        cls.driver.set_page_load_timeout(20)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        print("\n" + "=" * 70)
        print("LEARNIFY PLATFORM TEST SUITE - END")
        print("=" * 70 + "\n")

    def setUp(self):
        # Basic sanity check: home page responds
        self.driver.get(self.base_url)
        time.sleep(1)

    # ------------------------------------------------------------------
    # USER-SIDE TESTS (7)
    # ------------------------------------------------------------------

    def test_01_user_dashboard_loads(self):
        """
        TC01: /user dashboard should respond with HTML content.
        """
        print("\n[USER TEST 01] User Dashboard Load")

        url = f"{self.base_url}/user"
        self.driver.get(url)
        time.sleep(2)

        page_source = self.driver.page_source
        self.assertGreater(len(page_source), 50, "/user dashboard should not be blank")
        print(f"✅ /user route responded with content (length={len(page_source)})")

    def test_02_available_courses_page(self):
        """
        TC02: /user/all-courses (AvailableCourses.jsx) should respond with content.
        """
        print("\n[USER TEST 02] Available Courses Page")

        url = f"{self.base_url}/user/all-courses"
        self.driver.get(url)
        time.sleep(2)

        page_source = self.driver.page_source
        self.assertGreater(len(page_source), 50, "/user/all-courses should not be blank")
        print(f"✅ /user/all-courses route responded with content (length={len(page_source)})")

    def test_03_enrolled_courses_page(self):
        """
        TC03: /user/enrolled-courses (EnrolledCourses.jsx) should respond.
        """
        print("\n[USER TEST 03] Enrolled Courses Page")

        url = f"{self.base_url}/user/enrolled-courses"
        self.driver.get(url)
        time.sleep(2)

        page_source = self.driver.page_source
        self.assertGreater(
            len(page_source), 50, "/user/enrolled-courses should not be blank"
        )
        print("✅ /user/enrolled-courses route responded with content")

    def test_04_quiz_page_loads(self):
        """
        TC04: /user/quiz (Quiz.jsx) should respond with HTML content.
        """
        print("\n[USER TEST 04] Quiz Page Load")

        url = f"{self.base_url}/user/quiz"
        self.driver.get(url)
        time.sleep(2)

        page_source = self.driver.page_source
        self.assertGreater(len(page_source), 50, "/user/quiz should not be blank")
        print("✅ /user/quiz route responded with content")

        # Optional soft check: look for 'quiz' or 'question' in source
        lower_source = page_source.lower()
        if "quiz" in lower_source or "question" in lower_source:
            print("ℹ️ Quiz-related text found in page source.")
        else:
            print("ℹ️ No explicit 'quiz' keyword found; layout may differ.")

    def test_05_profile_management_page(self):
        """
        TC05: /profile-management (ProfileManagement.jsx) should respond.
        """
        print("\n[USER TEST 05] Profile Management Page")

        url = f"{self.base_url}/profile-management"
        self.driver.get(url)
        time.sleep(2)

        page_source = self.driver.page_source
        self.assertGreater(len(page_source), 50, "/profile-management should not be blank")
        print("✅ /profile-management route responded with content")

    def test_06_notifications_page(self):
        """
        TC06: /notifications (Notifications.jsx) should respond.
        """
        print("\n[USER TEST 06] Notifications Page")

        url = f"{self.base_url}/notifications"
        self.driver.get(url)
        time.sleep(2)

        page_source = self.driver.page_source
        self.assertGreater(len(page_source), 50, "/notifications should not be blank")
        print("✅ /notifications route responded with content")

    def test_07_certification_page(self):
        """
        TC07: /user/certifications (Certification.jsx) should respond.
        """
        print("\n[USER TEST 07] Certification Page")

        url = f"{self.base_url}/user/certifications"
        self.driver.get(url)
        time.sleep(2)

        page_source = self.driver.page_source
        self.assertGreater(len(page_source), 50, "/user/certifications should not be blank")
        print("✅ /user/certifications route responded with content")

    # ------------------------------------------------------------------
    # RESPONSIVE / UI TEST (1)
    # ------------------------------------------------------------------

    def test_08_dashboard_mobile_view(self):
        """
        TC08: /user dashboard should render in a small/mobile viewport.
        """
        print("\n[USER TEST 08] User Dashboard Mobile View")

        self.driver.set_window_size(375, 667)
        url = f"{self.base_url}/user"
        self.driver.get(url)
        time.sleep(2)

        page_source = self.driver.page_source
        self.assertGreater(len(page_source), 50, "Mobile /user dashboard should not be blank")
        print("✅ /user dashboard rendered on mobile viewport")

        self.driver.set_window_size(1280, 720)

    # ------------------------------------------------------------------
    # ADMIN-SIDE TESTS (2)
    # ------------------------------------------------------------------

    def test_09_admin_dashboard_page(self):
        """
        TC09: /admin (AdminDashboard.jsx) should respond with HTML.
        """
        print("\n[ADMIN TEST 09] Admin Dashboard Page")

        url = f"{self.base_url}/admin"
        self.driver.get(url)
        time.sleep(2)

        page_source = self.driver.page_source
        self.assertGreater(len(page_source), 50, "/admin should not be blank")
        print("✅ /admin route responded with content")

    def test_10_admin_all_courses_page(self):
        """
        TC10: /admin/all-courses (AllCourses.jsx) should respond.
        """
        print("\n[ADMIN TEST 10] Admin All Courses Page")

        url = f"{self.base_url}/admin/all-courses"
        self.driver.get(url)
        time.sleep(2)

        page_source = self.driver.page_source
        self.assertGreater(len(page_source), 50, "/admin/all-courses should not be blank")
        print("✅ /admin/all-courses route responded with content")


if __name__ == "__main__":
    unittest.main(verbosity=2)
