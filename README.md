# Learnify Test Automation Suite

Automated Selenium test suite for Learnify e-learning platform with CI/CD integration.

## Quick Start

### Prerequisites
- Python 3.8+
- Chrome browser
- pip

### Installation

```bash
pip install -r requirements.txt
```

### Running Tests

**Step 1: Start your Learnify app**
```bash
cd "C:\Users\muneeb aslam\Desktop\Learnify-Skillup"
npm run dev
```

Wait for: `VITE ... Local: http://localhost:5173/`

**Step 2: Run tests**
```bash
cd C:\selenium-tests
python -m unittest test_learnify_automation -v
```

## Test Cases (10+)

1. **test_01_auth_page_displays_login_form** - Auth page validation
2. **test_02_invalid_route_displays_not_found** - 404 page testing
3. **test_03_sidebar_visibility_when_authenticated** - Sidebar check
4. **test_04_loading_spinner_during_page_load** - Loading state
5. **test_05_course_page_navigation** - Course navigation
6. **test_06_search_courses_by_name** - Search functionality
7. **test_07_quiz_page_loads** - Quiz page validation
8. **test_08_profile_page_accessible** - Profile page access
9. **test_09_sidebar_toggle_on_mobile_view** - Responsive design
10. **test_10_main_page_elements_exist** - Page elements check
11. **test_admin_dashboard_loads** - Admin dashboard test

## Key Features

- ✅ Headless Chrome mode (EC2/Jenkins ready)
- ✅ App connectivity detection
- ✅ Graceful error handling
- ✅ 10+ test cases covering major features

## Environment Variables

Set custom app URL:
```bash
$env:APP_URL = "http://your-url:port"
python -m unittest test_learnify_automation -v
```

## Docker

Build and run tests in Docker:
```bash
docker build -t learnify-tests .
docker run --rm learnify-tests
```

## Jenkins Integration (Part II)

1. Create GitHub repo: `learnify-test-automation`
2. Push all files to GitHub
3. In Jenkins, create pipeline from `Jenkinsfile`
4. Configure GitHub webhook for auto-trigger

## Files

- `test_learnify_automation.py` - 10+ test cases
- `requirements.txt` - Python dependencies
- `Dockerfile` - Docker image
- `docker-compose.yml` - Docker compose setup
- `Jenkinsfile` - Jenkins pipeline
- `.gitignore` - Git configuration
- `README.md` - This file

## Troubleshooting

**Tests fail with ERR_CONNECTION_REFUSED**
→ Make sure app is running: `npm run dev` in another terminal

**Chrome not found**
→ Install Chrome or run: `pip install --upgrade webdriver-manager`

**Python not found**
→ Install Python 3.8+ from python.org

## Status

✅ Ready for local testing
✅ Ready for Docker
✅ Ready for Jenkins CI/CD
✅ Ready for GitHub integration
