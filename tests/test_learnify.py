"""
Selenium automated test suite for Learnify e-learning platform.

"""

import unittest
import time
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoSuchElementException,
    WebDriverException,
)


# ======================================================================
# USER-FACING TESTS
# ======================================================================

class TestLearnifyPlatform(unittest.TestCase):
    """Test suite for Learnify user-facing features."""

    @classmethod
    def setUpClass(cls):
        """Set up a single headless Chrome driver for all user tests."""
        cls.base_url = os.getenv("APP_URL", "http://localhost:5173")

        print("\n" + "=" * 70)
        print("LEARNIFY PLATFORM TEST SUITE - USER TESTS")
        print("=" * 70)
        print(f"Base URL: {cls.base_url}")
        print("Browser: Headless Chrome")
        print("=" * 70 + "\n")

        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1280,720")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-blink-features=AutomationControlled")

        try:
            cls.driver = webdriver.Chrome(options=options)
        except WebDriverException as e:
            print(f"❌ Error starting Chrome driver: {e}")
            raise

        cls.driver.set_page_load_timeout(20)
        cls.wait = WebDriverWait(cls.driver, 10)

    @classmethod
    def tearDownClass(cls):
        """Close the browser once user tests are done."""
        try:
            cls.driver.quit()
        except Exception:
            pass
        print("\n" + "=" * 70)
        print("USER TESTS COMPLETED - DRIVER CLOSED")
        print("=" * 70 + "\n")

    def setUp(self):
        """Navigate to the base URL before each user test."""
        self.driver.get(self.base_url)
        time.sleep(1)

    # ------------------------------------------------------------------
    # TC01 - Auth Page
    # ------------------------------------------------------------------
    def test_01_auth_page_structure(self):
        """
        TC01: Auth page (Auth.jsx) should display auth container, role select,
        email/password inputs, and login button.
        """
        print("\n[USER TEST 01] Auth Page Structure")

        self.driver.get(self.base_url)
        time.sleep(2)

        page_source = self.driver.page_source
        self.assertGreater(len(page_source), 100, "Auth page should have HTML content")

        # Main container .auth-container
        auth_container = self.driver.find_element(By.CLASS_NAME, "auth-container")
        self.assertTrue(auth_container.is_displayed(), "auth-container should be visible")
        print("✅ auth-container found and displayed")

        # Role select
        role_select = self.driver.find_element(By.TAG_NAME, "select")
        self.assertTrue(role_select.is_displayed(), "Role <select> should be visible")
        print("✅ Role <select> found on auth page")

        # Email / Password inputs
        inputs = self.driver.find_elements(By.TAG_NAME, "input")
        self.assertGreater(len(inputs), 0, "There should be at least one input on auth page")
        print(f"ℹ️ {len(inputs)} <input> elements found on auth page")

        email_found = any(
            (inp.get_attribute("placeholder") or "").lower() == "email" for inp in inputs
        )
        password_found = any(
            (inp.get_attribute("placeholder") or "").lower() == "password" for inp in inputs
        )
        self.assertTrue(email_found, "Email input with placeholder 'Email' should exist")
        self.assertTrue(password_found, "Password input with placeholder 'Password' should exist")
        print("✅ Email and Password inputs detected")

        # Login button text
        buttons = self.driver.find_elements(By.TAG_NAME, "button")
        button_texts = [b.text.strip() for b in buttons if b.text.strip()]
        print("ℹ️ Buttons on auth page:", button_texts)

        self.assertTrue(
            any("login" in t.lower() for t in button_texts),
            "There should be a Login button on auth page",
        )
        print("✅ Login button text found among buttons")

    # ------------------------------------------------------------------
    # TC02 - NotFound Page
    # ------------------------------------------------------------------
    def test_02_not_found_page(self):
        """
        TC02: Invalid route should render NotFound.jsx with '404 - Not Found'
        and explanatory text.
        """
        print("\n[USER TEST 02] 404 Not Found Page")

        invalid_url = f"{self.base_url}/this-route-does-not-exist"
        self.driver.get(invalid_url)
        time.sleep(2)

        page_source = self.driver.page_source
        self.assertGreater(len(page_source), 50, "404 page should not be blank")

        heading_404 = self.driver.find_element(By.XPATH, "//*[text()='404 - Not Found']")
        self.assertTrue(heading_404.is_displayed(), "'404 - Not Found' heading should be visible")
        print("✅ '404 - Not Found' heading displayed")

        text_p = self.driver.find_element(
            By.XPATH,
            "//*[contains(text(),'The page you are looking for does not exist.')]",
        )
        self.assertTrue(text_p.is_displayed(), "NotFound explanatory text should be visible")
        print("✅ NotFound explanatory text displayed")

    # ------------------------------------------------------------------
    # TC03 - User Dashboard Page
    # ------------------------------------------------------------------
    def test_03_user_dashboard_loads(self):
        """TC03: /user dashboard should respond with HTML content."""
        print("\n[USER TEST 03] User Dashboard Load")

        self.driver.get(f"{self.base_url}/user")
        time.sleep(2)

        page_source = self.driver.page_source
        self.assertGreater(len(page_source), 100, "User dashboard page should return some HTML")
        print("✅ /user route responded with content")

    # ------------------------------------------------------------------
    # TC04 - Available Courses Page
    # ------------------------------------------------------------------
    def test_04_available_courses_page(self):
        """TC04: /user/all-courses (AvailableCourses.jsx) should respond with content."""
        print("\n[USER TEST 04] Available Courses Page")

        self.driver.get(f"{self.base_url}/user/all-courses")
        time.sleep(2)

        page_source = self.driver.page_source
        self.assertGreater(len(page_source), 100, "Available courses page should return some HTML")
        print("✅ /user/all-courses route responded with content")

    # ------------------------------------------------------------------
    # TC05 - Enrolled Courses Page
    # ------------------------------------------------------------------
    def test_05_enrolled_courses_page(self):
        """TC05: /user/enrolled-courses (EnrolledCourses.jsx) should respond."""
        print("\n[USER TEST 05] Enrolled Courses Page")

        self.driver.get(f"{self.base_url}/user/enrolled-courses")
        time.sleep(2)

        page_source = self.driver.page_source
        self.assertGreater(len(page_source), 80, "Enrolled courses page should return HTML")
        print("✅ /user/enrolled-courses route responded with content")

    # ------------------------------------------------------------------
    # TC06 - Quiz Page
    # ------------------------------------------------------------------
    def test_06_quiz_page_loads(self):
        """TC06: /user/quiz (Quiz.jsx) should respond with HTML content."""
        print("\n[USER TEST 06] Quiz Page Load")

        self.driver.get(f"{self.base_url}/user/quiz")
        time.sleep(2)

        page_source = self.driver.page_source
        self.assertGreater(len(page_source), 80, "Quiz page should return HTML")
        print("✅ /user/quiz route responded with content")

    # ------------------------------------------------------------------
    # TC07 - Profile Management Page
    # ------------------------------------------------------------------
    def test_07_profile_management_page(self):
        """TC07: /profile-management (ProfileManagement.jsx) should respond."""
        print("\n[USER TEST 07] Profile Management Page")

        self.driver.get(f"{self.base_url}/profile-management")
        time.sleep(2)

        page_source = self.driver.page_source
        self.assertGreater(len(page_source), 80, "Profile management page should return HTML")
        print("✅ /profile-management route responded with content")

    # ------------------------------------------------------------------
    # TC08 - Notifications Page
    # ------------------------------------------------------------------
    def test_08_notifications_page(self):
        """TC08: /notifications (Notifications.jsx) should respond."""
        print("\n[USER TEST 08] Notifications Page")

        self.driver.get(f"{self.base_url}/notifications")
        time.sleep(2)

        page_source = self.driver.page_source
        self.assertGreater(len(page_source), 50, "Notifications page should return HTML")
        print("✅ /notifications route responded with content")

    # ------------------------------------------------------------------
    # TC09 - Certification Page
    # ------------------------------------------------------------------
    def test_09_certification_page(self):
        """TC09: /user/certifications (Certification.jsx) should respond."""
        print("\n[USER TEST 09] Certification Page")

        self.driver.get(f"{self.base_url}/user/certifications")
        time.sleep(2)

        page_source = self.driver.page_source
        self.assertGreater(len(page_source), 50, "Certification page should return HTML")
        print("✅ /user/certifications route responded with content")

    # ------------------------------------------------------------------
    # TC10 - Mobile View Dashboard
    # ------------------------------------------------------------------
    def test_10_dashboard_mobile_view(self):
        """TC10: /user dashboard should render in a small/mobile viewport."""
        print("\n[USER TEST 10] User Dashboard Mobile View")

        self.driver.set_window_size(375, 667)
        self.driver.get(f"{self.base_url}/user")
        time.sleep(2)

        page_source = self.driver.page_source
        self.assertGreater(len(page_source), 100, "Dashboard should render in mobile viewport")
        print("✅ /user dashboard rendered on mobile viewport")

        # Restore
        self.driver.set_window_size(1280, 720)


# ======================================================================
# ADMIN-FACING TESTS
# ======================================================================

class TestLearnifyAdminFeatures(unittest.TestCase):
    """Test suite for Learnify admin features."""

    @classmethod
    def setUpClass(cls):
        """Set up a single headless Chrome driver for all admin tests."""
        cls.base_url = os.getenv("APP_URL", "http://localhost:5173")

        print("\n" + "=" * 70)
        print("LEARNIFY PLATFORM TEST SUITE - ADMIN TESTS")
        print("=" * 70)
        print(f"Base URL: {cls.base_url}")
        print("Browser: Headless Chrome")
        print("=" * 70 + "\n")

        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1280,720")
        options.add_argument("--disable-gpu")

        try:
            cls.driver = webdriver.Chrome(options=options)
        except WebDriverException as e:
            print(f"❌ Error starting Chrome driver (admin tests): {e}")
            raise

        cls.driver.set_page_load_timeout(20)
        cls.wait = WebDriverWait(cls.driver, 10)

    @classmethod
    def tearDownClass(cls):
        try:
            cls.driver.quit()
        except Exception:
            pass
        print("\n" + "=" * 70)
        print("ADMIN TESTS COMPLETED - DRIVER CLOSED")
        print("=" * 70 + "\n")

    def setUp(self):
        self.driver.get(self.base_url)
        time.sleep(1)

    # ------------------------------------------------------------------
    # TC11 - Admin Dashboard Page
    # ------------------------------------------------------------------
    def test_11_admin_dashboard_page(self):
        """TC11: /admin (AdminDashboard.jsx) should respond with HTML."""
        print("\n[ADMIN TEST 11] Admin Dashboard Page")

        self.driver.get(f"{self.base_url}/admin")
        time.sleep(2)

        page_source = self.driver.page_source
        self.assertGreater(len(page_source), 80, "Admin dashboard page should return HTML")
        print("✅ /admin route responded with content")

    # ------------------------------------------------------------------
    # TC12 - Admin All Courses Page
    # ------------------------------------------------------------------
    def test_12_admin_all_courses_page(self):
        """TC12: /admin/all-courses (AllCourses.jsx) should respond."""
        print("\n[ADMIN TEST 12] Admin All Courses Page")

        self.driver.get(f"{self.base_url}/admin/all-courses")
        time.sleep(2)

        page_source = self.driver.page_source
        self.assertGreater(len(page_source), 80, "Admin all-courses page should return HTML")
        print("✅ /admin/all-courses route responded with content")


if __name__ == "__main__":
    # Run all tests with verbose output
    unittest.main(verbosity=2)
