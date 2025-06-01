# selenium , automation logic 
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def navigate_to_jobs_and_search(driver, job_title, location):
    """Navigate to LinkedIn Jobs and search using the specific input elements"""
    try:
        # Navigate to Jobs page
        print("Navigating to LinkedIn Jobs page...")
        driver.get("https://www.linkedin.com/jobs/")
        time.sleep(3)  # Give page time to fully load
        
        # Try to find the job title input field using multiple selectors
        print("Looking for job title input field...")
        job_title_input = None
        
        # Try several methods to find the job title input
        try:
            # Try finding by CSS that matches job title input
            job_title_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[aria-label='Search by title, skill, or company']"))
            )
        except:
            try:
                # Try finding by CSS class
                job_title_input = driver.find_element(By.CSS_SELECTOR, ".jobs-search-box__text-input.jobs-search-box__keyboard-text-input")
            except:
                try:
                    # Try finding by partial ID
                    inputs = driver.find_elements(By.CSS_SELECTOR, "input[id*='jobs-search-box-keyword']")
                    if inputs:
                        job_title_input = inputs[0]
                except:
                    pass
        
        if not job_title_input:
            print("Could not find job title input field")
            return False
        
        # Clear and fill the job title field
        print(f"Entering job title: {job_title}")
        job_title_input.clear()
        time.sleep(1)
        job_title_input.send_keys(job_title)
        time.sleep(1)
        
        # Find location input field
        print("Looking for location input field...")
        location_input = None
        
        try:
            # Try finding by CSS that matches location input
            location_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[aria-label='City, state, or zip code']"))
            )
        except:
            try:
                # Try alternative ID pattern
                inputs = driver.find_elements(By.CSS_SELECTOR, "input[id*='jobs-search-box-location']")
                if inputs:
                    location_input = inputs[0]
            except:
                pass
        
        if not location_input:
            print("Could not find location input field")
            return False
        
        # Clear and fill the location field
        print(f"Entering location: {location}")
        location_input.clear()
        time.sleep(1)
        location_input.send_keys(location)
        time.sleep(1)
        
        # Press Enter to submit the search
        print("Submitting search...")
        location_input.send_keys(Keys.RETURN)
        
        # Wait for search results to load
        print("Waiting for search results...")
        time.sleep(5)  # Initial wait for page load
        
        try:
            # Try to detect if search results have loaded by looking for common elements
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".jobs-search-results-list, .jobs-search__job-details"))
            )
            print("Job search completed successfully")
            return True
        except:
            # If specific elements aren't found, check if URL contains job search parameters
            current_url = driver.current_url
            if "keywords=" in current_url and ("location=" in current_url or "geoId=" in current_url):
                print("Job search URL detected, search appears successful")
                return True
            else:
                print("Could not confirm if job search was successful")
                return False
            
    except Exception as e:
        print(f"Error during job search: {e}")
        return False
    





def click_easy_apply_filter(driver):
    """Click the Easy Apply filter button"""
    try:
        print("Looking for Easy Apply filter button...")
        
        # Try multiple methods to find and click the Easy Apply filter
        try:
            # Try by ID first as provided
            easy_apply_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "searchFilter_applyWithLinkedin"))
            )
            print("Found Easy Apply filter by ID")
        except:
            try:
                # Try by aria-label
                easy_apply_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Easy Apply filter.']")
                print("Found Easy Apply filter by aria-label")
            except:
                try:
                    # Try by text content
                    buttons = driver.find_elements(By.TAG_NAME, "button")
                    for button in buttons:
                        if "Easy Apply" in button.text:
                            easy_apply_button = button
                            print("Found Easy Apply filter by text content")
                            break
                except:
                    # Try one more CSS selector approach
                    try:
                        easy_apply_button = driver.find_element(By.CSS_SELECTOR, ".artdeco-pill--choice:contains('Easy Apply')")
                        print("Found Easy Apply filter by CSS class")
                    except:
                        easy_apply_button = None
        
        if not easy_apply_button:
            print("Could not find Easy Apply filter button")
            return False
        
        # Click the Easy Apply button
        print("Clicking Easy Apply filter button...")
        driver.execute_script("arguments[0].click();", easy_apply_button)
        time.sleep(3)  # Wait for filter to apply
        
        # Check if filter is applied
        try:
            # Look for visual indication of filter being selected (is this filter selected/active?)
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "button[aria-checked='true'][aria-label='Easy Apply filter.']"))
            )
            print("Easy Apply filter was successfully applied")
            
            # Verify job listings are updated
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".jobs-search-results-list"))
            )
            print("Job listings updated with Easy Apply filter")
            return True
        except:
            print("Could not confirm if Easy Apply filter was applied")
            return False
        
    except Exception as e:
        print(f"Error clicking Easy Apply filter: {e}")
        return False
    

def process_job_listings(driver, llm, max_applications=10):
    """Process through the list of jobs and apply to them"""
    print("Processing job listings...")
    applied_count = 0
    jobs_viewed = 0
    applied_jobs = []
    
    # Load resume data for application responses
    resume_data = load_resume_data()
    if not resume_data:
        print("Failed to load resume data, cannot proceed with applications")
        return False
    
    try:
        # Wait for the job list to load with improved selector
        print("Waiting for job listings to load...")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".jobs-search-results-list, .scaffold-layout__list"))
        )
        time.sleep(3)  # Additional wait to ensure full loading
        
        print("Identifying job cards...")
        # Try multiple selectors for job cards
        job_cards = []
        for selector in [
            ".job-card-container",
            ".jobs-search-results__list-item",
            "li.jobs-search-results__list-item",
            ".artdeco-list__item"
        ]:
            job_cards = driver.find_elements(By.CSS_SELECTOR, selector)
            if job_cards:
                print(f"Found {len(job_cards)} job cards using selector: {selector}")
                break
        
        if not job_cards:
            print("No job cards found. Attempting alternative approach...")
            # Try to get all job cards by their parent container
            containers = driver.find_elements(By.CSS_SELECTOR, ".jobs-search-results-list")
            if containers:
                print("Found jobs container, looking for cards within it...")
                job_cards = containers[0].find_elements(By.XPATH, "./div")
                print(f"Found {len(job_cards)} job cards using container approach")
        
        if not job_cards:
            print("Could not locate job cards. Please check LinkedIn's layout or try another search.")
            return False
        
        # Process job cards
        while applied_count < max_applications and jobs_viewed < len(job_cards):
            try:
                # Close any open modals before proceeding
                try:
                    close_buttons = driver.find_elements(By.CSS_SELECTOR, "button[aria-label='Dismiss']")
                    for button in close_buttons:
                        if button.is_displayed():
                            driver.execute_script("arguments[0].click();", button)
                            time.sleep(1)
                except:
                    pass
                
                # Get the current job card
                current_job = job_cards[jobs_viewed]
                jobs_viewed += 1
                
                print(f"Processing job {jobs_viewed}/{len(job_cards)}...")
                
                # Scroll the job card into view
                driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", current_job)
                time.sleep(1)
                
                # Click on the job card with retry mechanism
                job_clicked = False
                attempts = 0
                while not job_clicked and attempts < 3:
                    try:
                        driver.execute_script("arguments[0].click();", current_job)
                        job_clicked = True
                    except:
                        try:
                            # Alternative click method
                            action = webdriver.ActionChains(driver)
                            action.move_to_element(current_job).click().perform()
                            job_clicked = True
                        except:
                            attempts += 1
                            time.sleep(1)
                
                if not job_clicked:
                    print("Failed to click job card, skipping to next job")
                    continue
                
                # Wait for job details to load
                time.sleep(2)
                
                # Get job details
                try:
                    job_title_element = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".jobs-unified-top-card__job-title, .job-details-jobs-unified-top-card__job-title"))
                    )
                    job_title = job_title_element.text.strip()
                    
                    company_element = driver.find_element(By.CSS_SELECTOR, ".jobs-unified-top-card__company-name, .job-details-jobs-unified-top-card__company-name")
                    company = company_element.text.strip()
                    
                    print(f"Viewing: {job_title} at {company}")
                except:
                    print("Could not extract job details, but continuing anyway")
                    job_title = "Unknown Position"
                    company = "Unknown Company"
                
                # Check for Easy Apply button with comprehensive selectors
                easy_apply_found = False
                for selector in [
                    ".jobs-apply-button",
                    "button[aria-label='Easy Apply']",
                    "button.jobs-apply-button",
                    ".jobs-apply-button--top-card",
                    "button[data-control-name='jobdetails_topcard_inapply']"
                ]:
                    try:
                        easy_apply_button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                        )
                        print(f"Found Easy Apply button using selector: {selector}")
                        easy_apply_found = True
                        break
                    except:
                        continue
                
                if not easy_apply_found:
                    print("No Easy Apply button found for this job, skipping")
                    continue
                
                # Click Easy Apply button
                try:
                    # Scroll to ensure button is in view
                    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", easy_apply_button)
                    time.sleep(1)
                    
                    # Try clicking
                    driver.execute_script("arguments[0].click();", easy_apply_button)
                    time.sleep(2)
                    
                    # Handle the application process
                    if handle_application_process(driver, llm, resume_data, job_title, company):
                        applied_count += 1
                        applied_jobs.append({"company": company, "title": job_title})
                        print(f"Successfully applied to: {job_title} at {company}")
                        print(f"Application {applied_count}/{max_applications} completed")
                        
                        # Add random delay between applications
                        delay = random.uniform(5, 10)
                        print(f"Waiting {delay:.1f} seconds before next application...")
                        time.sleep(delay)
                    else:
                        print(f"Failed to complete application for: {job_title} at {company}")
                        
                        # Try to close any open dialogs
                        try:
                            close_buttons = driver.find_elements(By.CSS_SELECTOR, "button[aria-label='Dismiss'], button[aria-label='Close']")
                            for button in close_buttons:
                                if button.is_displayed():
                                    driver.execute_script("arguments[0].click();", button)
                                    time.sleep(1)
                        except:
                            pass
                except Exception as e:
                    print(f"Error clicking Easy Apply button: {e}")
                    continue
                
                # Check if we've reached our application limit
                if applied_count >= max_applications:
                    print(f"Reached maximum applications limit ({max_applications})")
                    break
                
            except Exception as e:
                print(f"Error processing job card: {e}")
                continue
            
            # After processing each job, check if more job cards are available
            if jobs_viewed >= len(job_cards) and applied_count < max_applications:
                print("Looking for more job cards...")
                
                # Scroll down to load more jobs
                job_list_container = driver.find_element(By.CSS_SELECTOR, ".jobs-search-results-list, .scaffold-layout__list")
                driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", job_list_container)
                time.sleep(3)
                
                # Get updated job cards
                old_count = len(job_cards)
                for selector in [
                    ".job-card-container",
                    ".jobs-search-results__list-item",
                    "li.jobs-search-results__list-item",
                    ".artdeco-list__item"
                ]:
                    job_cards = driver.find_elements(By.CSS_SELECTOR, selector)
                    if len(job_cards) > old_count:
                        print(f"Found {len(job_cards) - old_count} additional job cards")
                        break
                
                if len(job_cards) <= old_count:
                    print("No more job cards found. Ending job search.")
                    break
        
        print(f"Application process completed. Applied to {applied_count} jobs.")
        
        # Save the list of jobs we applied to
        with open("applied_jobs.json", "w") as file:
            json.dump(applied_jobs, file, indent=4)
            
        return True
        
    except Exception as e:
        print(f"Error processing job listings: {e}")
        return False