// document.addEventListener("DOMContentLoaded", () => {
//     const loginForm = document.getElementById("loginForm");
//     const cvScrapeBtn = document.getElementById("cvScrapeBtn");
//     const jobApplyBtn = document.getElementById("jobApplyBtn");

//     let action = null;

//     // Set the action depending on which button is clicked
//     cvScrapeBtn.addEventListener("click", (event) => {
//         event.preventDefault();
//         action = "cv_scrape";
//         loginForm.requestSubmit(); // Trigger form submit programmatically
//     });

//     jobApplyBtn.addEventListener("click", (event) => {
//         event.preventDefault();
//         action = "job_apply";
//         loginForm.requestSubmit();
//     });

//     // Form submission handler
//     loginForm.addEventListener("submit", async (event) => {
//         event.preventDefault();

//         const username = document.getElementById("username").value.trim();
//         const password = document.getElementById("password").value.trim();
//         const status = document.getElementById("status");

//         // Basic validation
//         if (!username || !password) {
//             status.textContent = "Please fill in both fields.";
//             status.className = "error";
//             return;
//         }

//         // Show loading state
//         status.textContent = "Logging in...";
//         status.className = "loading";

//         try {
//             // Make API call to your backend
//             const response = await fetch('/api/login', {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json',
//                 },
//                 body: JSON.stringify({
//                     username: username,
//                     password: password,
//                     action: action
//                 })
//             });

//             const data = await response.json();

//             if (response.ok) {
//                 // Login successful
//                 status.textContent = "Login successful!";
//                 status.className = "success";

//                 // Store token if your backend returns one
//                 if (data.token) {
//                     localStorage.setItem('authToken', data.token);
//                 }

//                 // Redirect based on which button was clicked
//                 setTimeout(() => {
//                     if (action === "cv_scrape") {
//                         window.location.href = "cv_scrape.html";
//                     } else if (action === "job_apply") {
//                         window.location.href = "job-apply";
//                     }
//                 }, 1000);

//             } else {
//                 // Login failed
//                 status.textContent = data.message || "Login failed. Please try again.";
//                 status.className = "error";
//             }

//         } catch (error) {
//             // Network or other error
//             console.error('Login error:', error);
//             status.textContent = "Network error. Please check your connection and try again.";
//             status.className = "error";
//         }
//     });
// });

document.addEventListener("DOMContentLoaded", () => {
    const loginForm = document.getElementById("loginForm");
    const cvScrapeBtn = document.getElementById("cvScrapeBtn");
    const jobApplyBtn = document.getElementById("jobApplyBtn");

    let action = null;

    // Set the action depending on which button is clicked
    cvScrapeBtn.addEventListener("click", (event) => {
        event.preventDefault();
        action = "cv_scrape";
        loginForm.requestSubmit(); // Trigger form submit programmatically
    });

    jobApplyBtn.addEventListener("click", (event) => {
        event.preventDefault();
        action = "job_apply";
        loginForm.requestSubmit();
    });

    // Form submission handler
    loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const usernameField = document.getElementById("username");
        const passwordField = document.getElementById("password");
        const status = document.getElementById("status");

        // Check if elements exist
        if (!usernameField || !passwordField || !status) {
            console.error("Required form elements not found");
            return;
        }

        const username = usernameField.value.trim();
        const password = passwordField.value.trim();

        // Basic validation
        if (!username || !password) {
            status.textContent = "Please fill in both fields.";
            status.className = "error";
            return;
        }

        // Ensure an action was selected
        if (!action) {
            status.textContent = "Please select an action (CV Scrape or Job Apply).";
            status.className = "error";
            return;
        }

        // Show loading state and disable form
        status.textContent = "Logging in...";
        status.className = "loading";
        setFormDisabled(true);

        try {
            // Make API call to your backend
            const response = await fetch('/api/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    username: username,
                    password: password,
                    action: action
                })
            });

            // Check if response is JSON
            const contentType = response.headers.get('content-type');
            if (!contentType || !contentType.includes('application/json')) {
                throw new Error('Server returned non-JSON response');
            }

            const data = await response.json();

            if (response.ok) {
                // Login successful
                status.textContent = data.message || "Login successful!";
                status.className = "success";

                // Store token if your backend returns one
                if (data.token) {
                    localStorage.setItem('authToken', data.token);
                }

                // Redirect based on which button was clicked
                setTimeout(() => {
                    if (action === "cv_scrape") {
                        window.location.href = "cv_scrape.html";
                    } else if (action === "job_apply") {
                        window.location.href = "job_apply.html"; // Fixed: consistent naming
                    }
                }, 1000);

            } else {
                // Login failed
                status.textContent = data.message || "Login failed. Please try again.";
                status.className = "error";
            }

        } catch (error) {
            // Network or other error
            console.error('Login error:', error);
            
            if (error.name === 'TypeError' && error.message.includes('fetch')) {
                status.textContent = "Cannot connect to server. Please check your connection.";
            } else if (error.message.includes('JSON')) {
                status.textContent = "Server error. Please try again later.";
            } else {
                status.textContent = "An unexpected error occurred. Please try again.";
            }
            status.className = "error";
        } finally {
            // Re-enable form
            setFormDisabled(false);
            // Reset action after processing
            action = null;
        }
    });

    // Helper function to disable/enable form elements
    function setFormDisabled(disabled) {
        const elements = [
            document.getElementById("username"),
            document.getElementById("password"),
            cvScrapeBtn,
            jobApplyBtn
        ];
        
        elements.forEach(el => {
            if (el) el.disabled = disabled;
        });
    }
});