# llm and gemini logic here 
from langchain_google_genai import GoogleGenerativeAI
import os
from dotenv import load_dotenv

from app_process import question, resume_data, job_title, company, question_lower, llm, PromptTemplate
# Import the Config class from  config.py file
from app.config.config import Config

class LLMController:
    def __init__(self):
        self.config = Config()
        os.environ["GOOGLE_API_KEY"] = self.config.GEMINI_API_KEY


    def setup_llm(self):
        llm = GoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.environ["GOOGLE_API_KEY"], 
            temperature=0.7
        )
        return llm
    
    def generate_answer_with_llm(llm, question, resume_data, job_title, company):
        """Generate an appropriate answer to a custom question using the LLM with improved error handling"""
        try:
            print(f"Generating answer for question: {question}")
            
            # Check if question is empty or too short
            if not question or len(question) < 5:
                print("Question text too short, skipping LLM generation")
                return ""
                
            # Extract skills and experience from resume data for use in the prompt
            skills = ", ".join(resume_data["skills"][:5]) if "skills" in resume_data else ""
            experience_summary = ""
            if "work_experience" in resume_data and resume_data["work_experience"]:
                latest_job = resume_data["work_experience"][0]
                experience_summary = f"{latest_job.get('title', '')} at {latest_job.get('company', '')} - {latest_job.get('description', '')}"
            
            # Build a more focused prompt template
            prompt_template = PromptTemplate(
                input_variables=["question", "job_title", "company", "skills", "experience", "profile"],
                template="""
                You are helping a job applicant answer a question on a LinkedIn job application form.
                
                JOB: {job_title} at {company}
                
                QUESTION: {question}
                
                APPLICANT INFO:
                - Skills: {skills}
                - Recent Experience: {experience}
                - Additional Profile Info: {profile}
                
                Write a concise, professional response that directly answers the question. 
                Make it specific to the job position and highlight relevant skills or experience.
                Keep it under 100 words, using first-person perspective.Just write the very short answer directly, and if the answer is numbers then answer in digits.
                Don't start with phrases like "As a [job title]" or "Based on my experience" - just answer directly.
                Only output the answer text with no quotation marks or additional commentary.
                """
            )
            
            # Extract a compact profile summary for the prompt
            profile_summary = f"Education: {resume_data['education'][0]['degree'] if 'education' in resume_data and resume_data['education'] else 'Not specified'}, "
            profile_summary += f"Years of experience: {resume_data['questions'].get('years_of_experience', 'Not specified')}, "
            profile_summary += f"Willing to relocate: {resume_data['questions'].get('willing_to_relocate', 'Not specified')}"
            
            # Format the prompt with our data
            formatted_prompt = prompt_template.format(
                question=question,
                job_title=job_title,
                company=company,
                skills=skills,
                experience=experience_summary,
                profile=profile_summary
            )
            print(formatted_prompt)
            
            # Generate the answer with timeout handling
            try:
                response = llm.invoke(formatted_prompt)
                answer = response.strip()
                
                # Handle common edge cases
                if "As an AI assistant" in answer or "As an AI language model" in answer:
                    answer = answer.split("\n", 1)[1] if "\n" in answer else ""
                
                # Remove any quotation marks around the answer
                answer = answer.strip('"\'')
                
                print(f"Generated answer: {answer[:100]}...")
                return answer
            except Exception as e:
                print(f"LLM timeout or error: {e}")
                # Fall through to backup answers
            
        except Exception as e:
            print(f"Error generating answer with LLM: {e}")
        
        # Enhanced fallback answers for common questions - more tailored to the job
        # These will be used if the LLM fails
        
        # Extract key resume info for fallbacks
        skills_list = resume_data.get('skills', ['problem-solving', 'communication', 'teamwork'])
        top_skills = ', '.join(skills_list[:3])
        experience_years = resume_data.get('questions', {}).get('years_of_experience', '3+')
        
        # Pattern match the question for better fallbacks
        question_lower = question.lower()
        
        if any(phrase in question_lower for phrase in ["tell us about yourself", "introduce yourself", "background"]):
            return f"I'm a dedicated professional with {experience_years} years of experience and expertise in {top_skills}. Throughout my career, I've focused on delivering excellent results while continuously expanding my skill set. I'm particularly interested in this {job_title} role at {company} as it aligns with my professional goals and strengths."
        
        elif any(phrase in question_lower for phrase in ["why do you want to work", "why are you interested", "why join"]):
            return f"I'm drawn to {company} because of its reputation for innovation and impact in the industry. The {job_title} position particularly excites me as it leverages my skills in {top_skills}. I believe my background would allow me to contribute effectively while growing professionally in this role."
        
        elif any(phrase in question_lower for phrase in ["salary", "compensation", "pay", "expected"]):
            return resume_data.get('questions', {}).get('salary_expectation', "My salary expectations are flexible and based on the total compensation package, but I'm looking in the range typical for this role considering my experience level.")
        
        elif any(phrase in question_lower for phrase in ["start", "when can you start", "availability"]):
            return resume_data.get('questions', {}).get('preferred_start_date', "I can be available to start within two weeks after receiving an offer, though I'm flexible and can adjust based on your needs.")
        
        elif any(phrase in question_lower for phrase in ["strength", "greatest strength"]):
            return f"My greatest strength is my ability to {skills_list[0] if skills_list else 'quickly adapt to new challenges'}. This has enabled me to consistently deliver results in previous roles, particularly when working on complex projects requiring {skills_list[1] if len(skills_list) > 1 else 'attention to detail'}."
        
        elif any(phrase in question_lower for phrase in ["weakness", "area for improvement"]):
            return "I tend to be very detail-oriented, which sometimes means I spend extra time ensuring everything is perfect. I've learned to balance this by setting clear timelines and checkpoints to ensure I maintain both quality and efficiency."
        
        elif any(phrase in question_lower for phrase in ["challenge", "difficult situation", "overcome"]):
            return f"In a previous role, I faced a significant challenge when working on a time-sensitive project with changing requirements. By maintaining clear communication with stakeholders and leveraging my skills in {top_skills}, I was able to adapt quickly and deliver successfully despite the obstacles."
        
        elif any(phrase in question_lower for phrase in ["remote", "work from home", "hybrid"]):
            preferred_setting = resume_data.get('questions', {}).get('preferred_work_setting', 'flexible')
            return f"I'm comfortable working in a {preferred_setting} environment. I have experience collaborating effectively both remotely and on-site, and value maintaining strong communication and productivity regardless of the work setting."
        
        elif any(phrase in question_lower for phrase in ["relocate", "relocation", "move"]):
            willing = resume_data.get('questions', {}).get('willing_to_relocate', 'Yes')
            return f"{'I am willing to relocate for the right opportunity.' if willing.lower() == 'yes' else 'I prefer positions in my current location, but am open to discussing options for exceptional opportunities.'}"
        
        elif any(phrase in question_lower for phrase in ["visa", "sponsorship", "work authorization"]):
            need_visa = resume_data.get('questions', {}).get('visa_sponsorship_required', 'No')
            return f"{'I am authorized to work in the United States without sponsorship.' if need_visa.lower() == 'no' else 'I would require visa sponsorship to work in the United States.'}"
        
        # Generic fallback for other questions
        return f"Based on my {experience_years} years of experience with {top_skills}, I believe I would be able to make strong contributions to this {job_title} role. I'm excited about the opportunity to bring my skills to {company} and help achieve your team's goals."