#!/usr/bin/env python3
"""
Anti-Bot Scraper with Random Timing and CAPTCHA Handling
Designed for accuracy and avoiding bot detection
"""

import random
import time
import hashlib
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import html5lib

try:
    import undetected_chromedriver as uc
    UC_AVAILABLE = True
except ImportError:
    UC_AVAILABLE = False
    print("Warning: undetected-chromedriver not available. Install with: pip install undetected-chromedriver")

try:
    from python_anticaptcha import AnticaptchaClient, ImageToTextTask
    ANTICAPTCHA_AVAILABLE = True
except ImportError:
    ANTICAPTCHA_AVAILABLE = False
    print("Warning: python-anticaptcha not available. CAPTCHA solving disabled.")


class AntiBotScraper:
    """Scraper with anti-bot detection, random timing, and CAPTCHA handling"""

    def __init__(self, captcha_api_key: Optional[str] = None):
        self.captcha_api_key = captcha_api_key
        self.master_seed = self._generate_seed_from_time()
        self.session_count = 0

    def _generate_seed_from_time(self) -> int:
        """Generate seed value from current time for reproducible randomness"""
        current_time = int(time.time())
        # Use hash of time for seed (ensures different seed each run but reproducible)
        seed = int(hashlib.md5(str(current_time).encode()).hexdigest()[:8], 16)
        return seed

    def _random_delay(self, min_seconds: float = 2.0, max_seconds: float = 8.0, seed: Optional[int] = None):
        """Random delay with seed-based randomness to avoid bot detection"""
        if seed is not None:
            local_random = random.Random(seed)
            delay = local_random.uniform(min_seconds, max_seconds)
        else:
            delay = random.uniform(min_seconds, max_seconds)

        # Add human-like variation (slight pauses)
        time.sleep(delay)
        # Additional micro-delays to mimic human behavior
        time.sleep(random.uniform(0.1, 0.5))

    def _human_like_mouse_movement(self, driver):
        """Simulate human-like mouse movements"""
        try:
            body = driver.find_element(By.TAG_NAME, "body")
            actions = ActionChains(driver)
            # Random mouse movements
            move_count = random.randint(1, 3)
            for _ in range(move_count):
                x_offset = random.randint(-100, 100)
                y_offset = random.randint(-100, 100)
                actions.move_by_offset(x_offset, y_offset).perform()
                time.sleep(random.uniform(0.1, 0.3))
        except Exception as e:
            pass  # Ignore errors in mouse movement

    def _human_like_scroll(self, driver, seed: Optional[int] = None):
        """Simulate human-like scrolling behavior"""
        if seed is not None:
            local_random = random.Random(seed)
        else:
            local_random = random

        # Random scroll positions
        scroll_positions = [
            local_random.randint(200, 800),
            local_random.randint(1000, 2000),
            "document.body.scrollHeight"  # Bottom
        ]

        for pos in scroll_positions:
            if isinstance(pos, int):
                driver.execute_script(f"window.scrollTo(0, {pos});")
            else:
                driver.execute_script(f"window.scrollTo(0, {pos});")
            self._random_delay(0.5, 1.5, seed)

    def _detect_captcha(self, driver) -> Optional[str]:
        """Detect if CAPTCHA is present"""
        captcha_selectors = [
            ("iframe[src*='recaptcha']", "reCAPTCHA"),
            ("div[class*='captcha']", "Generic CAPTCHA"),
            ("iframe[src*='hcaptcha']", "hCaptcha"),
            ("div[id*='captcha']", "Generic CAPTCHA"),
            ("div[class*='recaptcha']", "reCAPTCHA"),
        ]

        for selector, captcha_type in captcha_selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if elements:
                    return captcha_type
            except:
                continue

        return None

    def _solve_captcha(self, driver, captcha_type: str) -> bool:
        """Attempt to solve CAPTCHA using service"""
        if not self.captcha_api_key or not ANTICAPTCHA_AVAILABLE:
            return False

        try:
            if captcha_type == "reCAPTCHA":
                # Use 2captcha or AntiCaptcha service
                # This is a placeholder - implement based on chosen service
                print("CAPTCHA solving service integration needed")
                return False
            elif captcha_type == "hCaptcha":
                # Similar implementation for hCaptcha
                print("hCaptcha solving service integration needed")
                return False
        except Exception as e:
            print(f"Error solving CAPTCHA: {e}")
            return False

        return False

    def _handle_captcha(self, driver, seed: Optional[int] = None) -> bool:
        """Handle CAPTCHA with random approaches"""
        captcha_type = self._detect_captcha(driver)

        if captcha_type:
            print(f"CAPTCHA detected: {captcha_type}")
            # Random delay before handling
            self._random_delay(3.0, 6.0, seed)

            # Try to solve automatically if service available
            if self._solve_captcha(driver, captcha_type):
                return True

            # If solving fails, wait and retry
            print("Waiting for CAPTCHA resolution...")
            self._random_delay(10.0, 20.0, seed)

            # Check if CAPTCHA still present
            if self._detect_captcha(driver):
                raise Exception(f"CAPTCHA still present: {captcha_type}. Requires manual intervention or CAPTCHA solving service.")

            return True

        return False

    def _create_driver(self) -> webdriver.Chrome:
        """Create Chrome driver with anti-detection settings"""
        options = Options()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)

        # Randomize user agent
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        ]
        options.add_argument(f'user-agent={random.choice(user_agents)}')

        # Use undetected-chromedriver if available
        if UC_AVAILABLE:
            try:
                driver = uc.Chrome(options=options, version_main=None)
                return driver
            except Exception as e:
                print(f"Warning: Could not use undetected-chromedriver: {e}")

        # Fallback to regular Chrome driver
        return webdriver.Chrome(options=options)

    def scrape_page(self, url: str, page_num: int = 1, seed: Optional[int] = None) -> List[Dict]:
        """Scrape a single page with anti-bot protection"""
        if seed is None:
            seed = self.master_seed + page_num + self.session_count

        # Use seed for reproducible randomness
        local_random = random.Random(seed)
        self.session_count += 1

        driver = self._create_driver()

        try:
            # Random delay before starting
            self._random_delay(1.0, 3.0, seed)

            driver.get(url)

            # Human-like mouse movement
            self._human_like_mouse_movement(driver)

            # Random delay after page load
            self._random_delay(2.0, 5.0, seed)

            # Check and handle CAPTCHA
            self._handle_captcha(driver, seed)

            # Wait for complete page load
            WebDriverWait(driver, 30).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )

            # Additional random delay to mimic reading time
            self._random_delay(1.5, 4.0, seed)

            # Human-like scrolling
            self._human_like_scroll(driver, seed)

            # Get page source and parse
            html = driver.page_source
            soup = BeautifulSoup(html, 'html5lib')

            # Extract data (customize selectors based on target site)
            results = self._extract_data(soup, page_num)

            return results

        finally:
            driver.quit()

    def _extract_data(self, soup: BeautifulSoup, page_num: int) -> List[Dict]:
        """Extract data from parsed HTML (override for specific sites)"""
        # Placeholder - implement based on target site
        return []

    def scrape_parallel(self, urls: List[str], max_workers: int = 3) -> List[Dict]:
        """Scrape multiple URLs in parallel with rate limiting"""
        master_seed = self._generate_seed_from_time()
        print(f"Using master seed: {master_seed}")

        all_results = []

        # Limit workers to avoid detection (3-5 workers max)
        workers = min(max_workers, len(urls), 5)

        with ThreadPoolExecutor(max_workers=workers) as executor:
            # Submit all scraping tasks
            future_to_url = {
                executor.submit(
                    self.scrape_page,
                    url,
                    idx + 1,
                    master_seed + idx
                ): (url, idx + 1)
                for idx, url in enumerate(urls)
            }

            # Process completed tasks with delays between them
            completed = 0
            for future in as_completed(future_to_url):
                url, page_num = future_to_url[future]
                try:
                    results = future.result()
                    all_results.extend(results)
                    completed += 1
                    print(f"Completed page {page_num}: {len(results)} items")

                    # Random delay between page completions (rate limiting)
                    if completed < len(urls):
                        self._random_delay(3.0, 8.0, master_seed + completed)

                except Exception as e:
                    print(f"Error scraping page {page_num} ({url}): {e}")
                    # If CAPTCHA detected, wait longer before retry
                    if "CAPTCHA" in str(e):
                        print("CAPTCHA detected - waiting 60 seconds before retry...")
                        time.sleep(60)

        print(f"Total items scraped: {len(all_results)}")
        return all_results


# Example usage for Airbnb scraping
class AirbnbScraper(AntiBotScraper):
    """Specialized scraper for Airbnb"""

    def _extract_data(self, soup: BeautifulSoup, page_num: int) -> List[Dict]:
        """Extract Airbnb listing data"""
        listings = soup.select('[data-testid="listing-card"]')
        results = []

        for listing in listings:
            title_elem = listing.select_one('h3')
            price_elem = listing.select_one('[data-testid="price"]')

            if title_elem and price_elem:
                results.append({
                    'title': title_elem.get_text(strip=True),
                    'price': price_elem.get_text(strip=True),
                    'page': page_num
                })

        return results

    def scrape_airbnb(self, address: str, max_pages: int = 5, max_workers: int = 3) -> List[Dict]:
        """Scrape Airbnb listings for an address"""
        urls = []
        for page_num in range(1, max_pages + 1):
            if page_num > 1:
                url = f"https://www.airbnb.com/s/{address}/homes?items_offset={(page_num-1)*20}"
            else:
                url = f"https://www.airbnb.com/s/{address}"
            urls.append(url)

        return self.scrape_parallel(urls, max_workers)


if __name__ == "__main__":
    # Example usage
    scraper = AirbnbScraper(captcha_api_key=None)  # Add API key if using CAPTCHA service

    # Scrape Airbnb listings
    results = scraper.scrape_airbnb("800 John Carlyle Street, Alexandria, VA", max_pages=3, max_workers=2)

    print(f"\nScraped {len(results)} listings")
    for result in results[:5]:  # Print first 5
        print(result)
