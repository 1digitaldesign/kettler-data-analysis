#!/usr/bin/env python3
"""
Anti-Bot Scraper with Random Timing and CAPTCHA Handling
Designed for accuracy and avoiding detection
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
    print("Warning: undetected_chromedriver not available. Install with: pip install undetected-chromedriver")

try:
    from twocaptcha import TwoCaptcha
    CAPTCHA_SERVICE_AVAILABLE = True
except ImportError:
    CAPTCHA_SERVICE_AVAILABLE = False
    print("Warning: 2captcha not available. Install with: pip install 2captcha-python")


class AntiBotScraper:
    """
    Scraper with built-in anti-bot detection, random timing, and CAPTCHA handling.
    Uses seed-based random timing for reproducibility while maintaining randomness.
    """
    
    def __init__(self, seed: Optional[int] = None, captcha_api_key: Optional[str] = None):
        """
        Initialize scraper with optional seed for reproducible random timing.
        
        Args:
            seed: Random seed for timing (if None, generates random seed)
            captcha_api_key: API key for 2captcha service (optional)
        """
        self.seed = seed or random.randint(1000, 9999)
        random.seed(self.seed)
        self.timing_base = random.uniform(2.0, 5.0)  # Base delay in seconds
        self.captcha_api_key = captcha_api_key
        
        if CAPTCHA_SERVICE_AVAILABLE and captcha_api_key:
            self.captcha_solver = TwoCaptcha(captcha_api_key)
        else:
            self.captcha_solver = None
        
        print(f"Initialized scraper with seed: {self.seed}, base timing: {self.timing_base:.2f}s")
    
    def random_delay(self, min_multiplier: float = 0.8, max_multiplier: float = 1.5) -> float:
        """
        Generate random delay based on seed.
        
        Args:
            min_multiplier: Minimum multiplier for base timing
            max_multiplier: Maximum multiplier for base timing
            
        Returns:
            Actual delay time used
        """
        delay = self.timing_base * random.uniform(min_multiplier, max_multiplier)
        time.sleep(delay)
        return delay
    
    def human_like_mouse_movement(self, driver: webdriver.Chrome):
        """Simulate human-like mouse movements to avoid bot detection."""
        try:
            body = driver.find_element(By.TAG_NAME, "body")
            actions = ActionChains(driver)
            
            # Random mouse movements
            num_movements = random.randint(2, 5)
            for _ in range(num_movements):
                x_offset = random.randint(-100, 100)
                y_offset = random.randint(-100, 100)
                actions.move_by_offset(x_offset, y_offset)
            
            actions.perform()
            self.random_delay(0.3, 0.8)
        except Exception as e:
            print(f"Mouse movement simulation failed: {e}")
    
    def human_like_scroll(self, driver: webdriver.Chrome):
        """Simulate human-like scrolling behavior."""
        try:
            # Random initial scroll
            initial_scroll = random.randint(200, 800)
            driver.execute_script(f"window.scrollTo(0, {initial_scroll});")
            self.random_delay(0.5, 2.0)
            
            # Scroll to middle
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
            self.random_delay(0.5, 1.5)
            
            # Scroll to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.random_delay(1.0, 2.5)
            
            # Scroll back up a bit (human behavior)
            scroll_back = random.randint(100, 400)
            driver.execute_script(f"window.scrollTo(0, document.body.scrollHeight - {scroll_back});")
            self.random_delay(0.3, 1.0)
        except Exception as e:
            print(f"Scroll simulation failed: {e}")
    
    def handle_captcha(self, driver: webdriver.Chrome) -> bool:
        """
        Handle CAPTCHA with random strategies.
        
        Args:
            driver: Selenium WebDriver instance
            
        Returns:
            True if CAPTCHA was handled, False otherwise
        """
        try:
            # Check for common CAPTCHA types
            captcha_selectors = [
                "iframe[src*='recaptcha']",
                "div[class*='captcha']",
                "iframe[src*='hcaptcha']",
                "div[id*='captcha']",
                "div[class*='g-recaptcha']"
            ]
            
            for selector in captcha_selectors:
                captcha_elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if captcha_elements:
                    print(f"CAPTCHA detected: {selector}")
                    
                    # Random delay before attempting to solve
                    self.random_delay(3.0, 6.0)
                    
                    # Try different strategies in random order
                    solve_strategies = [
                        self._try_audio_captcha,
                        self._try_captcha_service,
                        self._wait_for_auto_solve
                    ]
                    random.shuffle(solve_strategies)
                    
                    for strategy in solve_strategies:
                        if strategy(driver):
                            print("CAPTCHA solved successfully")
                            return True
                    
                    print("CAPTCHA could not be solved automatically")
                    return False
            
            return False
        except Exception as e:
            print(f"CAPTCHA handling error: {e}")
            return False
    
    def _try_audio_captcha(self, driver: webdriver.Chrome) -> bool:
        """Try audio CAPTCHA option."""
        try:
            audio_selectors = [
                "button[title*='audio']",
                "button[aria-label*='audio']",
                "a[href*='audio']",
                "button[id*='audio']"
            ]
            
            for selector in audio_selectors:
                try:
                    audio_button = driver.find_element(By.CSS_SELECTOR, selector)
                    if audio_button and audio_button.is_displayed():
                        audio_button.click()
                        self.random_delay(2.0, 4.0)
                        return True
                except:
                    continue
        except Exception as e:
            print(f"Audio CAPTCHA attempt failed: {e}")
        return False
    
    def _try_captcha_service(self, driver: webdriver.Chrome) -> bool:
        """Try using 2captcha service to solve CAPTCHA."""
        if not self.captcha_solver:
            return False
        
        try:
            # Find reCAPTCHA site key
            site_key_elem = driver.find_element(By.CSS_SELECTOR, "[data-sitekey]")
            if site_key_elem:
                site_key = site_key_elem.get_attribute("data-sitekey")
                page_url = driver.current_url
                
                # Solve CAPTCHA using service
                result = self.captcha_solver.recaptcha(
                    sitekey=site_key,
                    url=page_url
                )
                
                if result and result.get('code'):
                    # Inject solution
                    driver.execute_script(
                        f"document.getElementById('g-recaptcha-response').innerHTML='{result['code']}';"
                    )
                    self.random_delay(1.0, 2.0)
                    return True
        except Exception as e:
            print(f"CAPTCHA service attempt failed: {e}")
        return False
    
    def _wait_for_auto_solve(self, driver: webdriver.Chrome, max_wait: int = 30) -> bool:
        """Wait for CAPTCHA to be solved automatically."""
        waited = 0
        while waited < max_wait:
            # Check if CAPTCHA is gone
            captcha_elements = driver.find_elements(By.CSS_SELECTOR, "iframe[src*='recaptcha']")
            if not captcha_elements:
                return True
            time.sleep(1)
            waited += 1
        return False
    
    def create_stealth_driver(self) -> webdriver.Chrome:
        """Create undetected Chrome driver with anti-bot measures."""
        options = Options()
        
        # Anti-detection options
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        
        # Random user agent
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        ]
        options.add_argument(f'--user-agent={random.choice(user_agents)}')
        
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        # Use undetected_chromedriver if available
        if UC_AVAILABLE:
            try:
                driver = uc.Chrome(options=options, version_main=None)
            except:
                driver = webdriver.Chrome(options=options)
        else:
            driver = webdriver.Chrome(options=options)
        
        # Execute stealth script
        driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
            'source': '''
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['en-US', 'en']
                });
                window.chrome = {
                    runtime: {}
                };
            '''
        })
        
        return driver
    
    def scrape_page(self, url: str, page_num: int = 1) -> Dict:
        """
        Scrape a single page with anti-bot measures.
        
        Args:
            url: URL to scrape
            page_num: Page number for tracking
            
        Returns:
            Dictionary with scraping results
        """
        driver = self.create_stealth_driver()
        results = {
            'page': page_num,
            'url': url,
            'listings': [],
            'errors': [],
            'timing': {}
        }
        
        start_time = time.time()
        
        try:
            # Random delay before navigation
            nav_delay = self.random_delay(1.0, 3.0)
            results['timing']['navigation_delay'] = nav_delay
            
            driver.get(url)
            
            # Human-like mouse movement
            self.human_like_mouse_movement(driver)
            
            # Wait for page load with random variation
            wait_time = random.uniform(3.0, 6.0)
            WebDriverWait(driver, int(wait_time)).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            results['timing']['page_load'] = wait_time
            
            # Handle CAPTCHA if present
            captcha_start = time.time()
            if self.handle_captcha(driver):
                print(f"CAPTCHA handled on page {page_num}")
                self.random_delay(2.0, 4.0)
            results['timing']['captcha_time'] = time.time() - captcha_start
            
            # Human-like scrolling
            self.human_like_scroll(driver)
            
            # Wait for listings with random delay
            self.random_delay(1.0, 2.0)
            
            try:
                WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[data-testid="listing-card"]'))
                )
            except:
                results['errors'].append("Listings not found")
                return results
            
            # Parse with most accurate parser
            html = driver.page_source
            soup = BeautifulSoup(html, 'html5lib')
            
            listings = soup.select('[data-testid="listing-card"]')
            
            for listing in listings:
                title_elem = listing.select_one('h3')
                price_elem = listing.select_one('[data-testid="price"]')
                
                if title_elem and price_elem:
                    results['listings'].append({
                        'title': title_elem.get_text(strip=True),
                        'price': price_elem.get_text(strip=True),
                        'page': page_num
                    })
            
            # Verify results accuracy
            if len(results['listings']) == 0:
                results['errors'].append("No listings extracted")
            
        except Exception as e:
            results['errors'].append(str(e))
        finally:
            results['timing']['total_time'] = time.time() - start_time
            driver.quit()
        
        return results
    
    def scrape_pages_parallel(
        self,
        base_url: str,
        num_pages: int,
        max_workers: int = 3,
        delay_between_pages: float = 2.0
    ) -> List[Dict]:
        """
        Scrape multiple pages in parallel with random timing.
        
        Args:
            base_url: Base URL for scraping
            num_pages: Number of pages to scrape
            max_workers: Maximum parallel workers (keep low to avoid detection)
            delay_between_pages: Base delay between page requests
            
        Returns:
            List of scraping results
        """
        results = []
        
        # Generate URLs for all pages
        urls = [f"{base_url}&page={i}" if '?' in base_url else f"{base_url}?page={i}" 
                for i in range(1, num_pages + 1)]
        
        # Shuffle URLs to avoid sequential pattern
        random.shuffle(urls)
        
        # Process in parallel with limited workers to avoid detection
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit tasks with random delays
            futures = {}
            for i, url in enumerate(urls):
                # Random delay before submitting each task
                delay = random.uniform(0.5, delay_between_pages) * (i + 1)
                time.sleep(delay)
                
                # Create new scraper instance with different seed for each page
                page_seed = self.seed + i
                scraper = AntiBotScraper(seed=page_seed, captcha_api_key=self.captcha_api_key)
                future = executor.submit(scraper.scrape_page, url, i + 1)
                futures[future] = (url, i + 1)
            
            # Collect results as they complete
            for future in as_completed(futures):
                url, page_num = futures[future]
                try:
                    result = future.result()
                    results.append(result)
                    print(f"Page {page_num} completed: {len(result['listings'])} listings, "
                          f"time: {result['timing'].get('total_time', 0):.2f}s")
                    # Random delay between completions
                    self.random_delay(1.0, 3.0)
                except Exception as e:
                    print(f"Error scraping page {page_num}: {e}")
        
        return results


def scrape_airbnb_accurate(
    address: str,
    num_pages: int = 5,
    captcha_api_key: Optional[str] = None
) -> Dict:
    """
    Main scraping function with anti-bot measures.
    
    Args:
        address: Address to search for
        num_pages: Number of pages to scrape
        captcha_api_key: Optional 2captcha API key
        
    Returns:
        Dictionary with all scraping results
    """
    # Generate seed from address hash for reproducibility
    seed = int(hashlib.md5(address.encode()).hexdigest()[:8], 16) % 10000
    
    scraper = AntiBotScraper(seed=seed, captcha_api_key=captcha_api_key)
    base_url = f"https://www.airbnb.com/s/{address}"
    
    # Scrape pages in parallel with anti-bot measures
    results = scraper.scrape_pages_parallel(base_url, num_pages, max_workers=3)
    
    # Consolidate results
    all_listings = []
    total_errors = []
    for page_result in results:
        all_listings.extend(page_result['listings'])
        total_errors.extend(page_result.get('errors', []))
    
    return {
        'address': address,
        'seed': seed,
        'total_listings': len(all_listings),
        'pages_scraped': len(results),
        'listings': all_listings,
        'page_results': results,
        'errors': total_errors,
        'success_rate': len([r for r in results if not r.get('errors')]) / len(results) if results else 0
    }


if __name__ == "__main__":
    # Example usage
    result = scrape_airbnb_accurate("800 John Carlyle Street, Alexandria, VA", num_pages=3)
    print(f"\nScraping complete!")
    print(f"Total listings: {result['total_listings']}")
    print(f"Success rate: {result['success_rate']:.2%}")
    print(f"Errors: {len(result['errors'])}")
