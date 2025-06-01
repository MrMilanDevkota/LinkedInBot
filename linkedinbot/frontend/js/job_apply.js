document.addEventListener('DOMContentLoaded', () => {
    const resumeInput = document.getElementById('resume');
    const jsonEditor = document.getElementById('json-editor');
    const saveJsonBtn = document.getElementById('save-json-btn');
    const startAutoApplyBtn = document.getElementById('start-auto-apply');
    const backToLoginBtn = document.getElementById('back-to-login');

    // Function to generate initial JSON data similar to complete8.py
    function generateInitialJson() {
        return {
            personal_info: {
                name: "Your Name",
                email: "",
                phone: "",
                address: "Your Address",
                linkedin: "https://www.linkedin.com/in/your-profile",
                website: ""
            },
            education: [
                {
                    school: "Your University",
                    degree: "Your Degree",
                    field_of_study: "Your Field",
                    start_date: "MM/YYYY",
                    end_date: "MM/YYYY",
                    gpa: "4.0"
                }
            ],
            work_experience: [
                {
                    company: "Your Last Company",
                    title: "Your Title",
                    location: "City, State",
                    start_date: "MM/YYYY",
                    end_date: "MM/YYYY",
                    description: "Brief description of your role"
                }
            ],
            skills: ["Skill 1", "Skill 2", "Skill 3"],
            certifications: ["Certification 1", "Certification 2"],
            languages: ["English"],
            questions: {
                years_of_experience: "3",
                willing_to_relocate: "Yes",
                willing_to_travel: "Yes",
                preferred_work_setting: "Hybrid",
                salary_expectation: "$80,000 - $100,000",
                preferred_start_date: "As soon as possible",
                visa_sponsorship_required: "No",
                cleared_security_clearance: "No"
            }
        };
    }

    // Initialize the JSON editor with the generated data
    const initialJsonData = generateInitialJson();
    jsonEditor.value = JSON.stringify(initialJsonData, null, 2);

    // Event listener for resume input change
    resumeInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    // Attempt to parse the file content as JSON
                    const resumeJson = JSON.parse(e.target.result);
                    jsonEditor.value = JSON.stringify(resumeJson, null, 2);
                } catch (error) {
                    // If parsing as JSON fails, treat as text and create a basic JSON structure
                    const mockResumeData = {
                        "resumeText": e.target.result,
                        "name": "",
                        "contact": {
                            "email": "",
                            "phone": ""
                        },
                        "experience": [],
                        "education": [],
                        "skills": []
                    };
                    const jsonData = JSON.stringify(mockResumeData, null, 2);
                    jsonEditor.value = jsonData;
                }
            };
            reader.readAsText(file);
        }
    });

    // Event listener for save JSON button
    saveJsonBtn.addEventListener('click', () => {
        try {
            const jsonData = JSON.parse(jsonEditor.value);
            console.log('Parsed JSON Data:', jsonData);
            alert('JSON data saved!  Check console for the saved data.');
        } catch (error) {
            alert('Invalid JSON format. Please check your input.');
            console.error('Invalid JSON:', error);
        }
    });

    // Event listener for start auto apply button
    startAutoApplyBtn.addEventListener('submit', (event) => {
        event.preventDefault();

        const geminiKey = document.getElementById('gemini-api-key').value;
        const jobTitle = document.getElementById('job-title').value;
        const jobLocation = document.getElementById('job-location').value;
        const phoneNumber = document.getElementById('phone-number').value;
        const userWebsite = document.getElementById('user-website').value;
        const maxApplications = document.getElementById('max-applications').value;


        if (!geminiKey || !jobTitle || !jobLocation) {
            alert('Please fill in all required fields: Gemini API Key, Job Title, and Job Location.');
            return;
        }

        let resumeData;
        try {
            resumeData = JSON.parse(jsonEditor.value);
        } catch (e) {
            alert("Please upload a valid resume file, or ensure the JSON in the editor is valid.");
            return;
        }

        const applicationData = {
            geminiKey: geminiKey,
            jobTitle: jobTitle,
            jobLocation: jobLocation,
            phoneNumber: phoneNumber,
            userWebsite: userWebsite,
            maxApplications: maxApplications,
            resumeData: resumeData,
        };

        console.log('Application Data:', applicationData);
        alert('Starting auto job apply process... (Check console for application data)');

    });

    // Event listener for back to login button
    backToLoginBtn.addEventListener('click', () => {
        window.location.href = 'index.html';
    });
});