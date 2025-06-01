def load_resume_data():
    """Load resume data from JSON file or create if not exists"""
    try:
        if os.path.exists(RESUME_DATA_FILE):
            with open(RESUME_DATA_FILE, 'r') as file:
                return json.load(file)
        else:
            # Create a basic resume data template
            resume_data = {
                "personal_info": {
                    "name": "Your Name",
                    "email": LINKEDIN_EMAIL,
                    "phone": PHONE_NUMBER,
                    "address": "Your Address",
                    "linkedin": f"https://www.linkedin.com/in/your-profile",
                    "website": USER_WEBSITE
                },
                "education": [
                    {
                        "school": "Your University",
                        "degree": "Your Degree",
                        "field_of_study": "Your Field",
                        "start_date": "MM/YYYY",
                        "end_date": "MM/YYYY",
                        "gpa": "4.0"
                    }
                ],
                "work_experience": [
                    {
                        "company": "Your Last Company",
                        "title": "Your Title",
                        "location": "City, State",
                        "start_date": "MM/YYYY",
                        "end_date": "MM/YYYY",
                        "description": "Brief description of your role"
                    }
                ],
                "skills": ["Skill 1", "Skill 2", "Skill 3"],
                "certifications": ["Certification 1", "Certification 2"],
                "languages": ["English"],
                "questions": {
                    "years_of_experience": "3",
                    "willing_to_relocate": "Yes",
                    "willing_to_travel": "Yes",
                    "preferred_work_setting": "Hybrid",
                    "salary_expectation": "$80,000 - $100,000",
                    "preferred_start_date": "As soon as possible",
                    "visa_sponsorship_required": "No",
                    "cleared_security_clearance": "No"
                }
            }
            
            # Save template to file
            with open(RESUME_DATA_FILE, 'w') as file:
                json.dump(resume_data, file, indent=4)
            
            print(f"Created template resume data file at {RESUME_DATA_FILE}. Please update with your information.")
            return resume_data
    except Exception as e:
        print(f"Error loading resume data: {e}")
        return None