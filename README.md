# yoonas12.github.io
IDOR Testing Flask Application

This repository contains a Flask application intentionally designed with Insecure Direct Object Reference (IDOR) vulnerabilities for educational purposes. It includes a simple frontend and a Python script for automated testing, allowing security enthusiasts to practice IDOR testing with tools like Burp Suite.

Warning: This application is vulnerable by design. Do not deploy it in a production environment.

Features

Vulnerable endpoints for testing basic and advanced IDOR issues:
/profile/<user_id>: Access user profiles (basic IDOR).
/document/<encoded_doc_id>: Access documents with base64-encoded IDs.
/project/<project_id>/files: Access project files (indirect IDOR).
/admin/users: Admin-only endpoint (secure, requires admin role).
Simple HTML frontend (index.html) for user interaction.

Python script (idor_test.py) for automated IDOR testing.
Designed for testing with Burp Suite or similar tools.

Prerequisites: Python 3.8+ Flask (pip install flask)
Requests library (pip install requests) for idor_test.py
Burp Suite (optional, for manual testing)
A web browser configured with Burp Suite proxy (if using Burp)

Setup
Clone the Repository:

git clone https://github.com/<your-username>/idor-testing-flask.git
cd idor-testing-flask
Install Dependencies:
 pip install flask requests

Verify File Structure:

idor-testing-flask/
├── vulnerable_app.py
├── idor_test.py
└── templates/
    └── index.html

Running the Application
  Start the Flask App:

python vulnerable_app.py
The app runs on http://127.0.0.1:5000.
Access the frontend at http://127.0.0.1:5000 in a browser.
Interact with the Frontend:
Login: Enter a user ID (1, 2, or 3) and click "Login".
   User 1: Alice (user role)
   User 2: Bob (user role)
   User 3: Charlie (admin role)

Test endpoints via the frontend forms (profile, document, project files, admin).

Testing for IDOR Vulnerabilities

Option 1: Automated Testing with Python Script

Run the testing script:

python idor_test.py

The script:
Logs in as user 3 (Charlie, admin).

Tests IDOR vulnerabilities by accessing other users' profiles, documents, and project files.
Attempts to access the admin endpoint.

Check the output for 200 status codes indicating unauthorized access (IDOR vulnerabilities).
 
Option 2: Manual Testing with Burp Suite

Configure Burp Suite:

Set up the proxy (127.0.0.1:8080).

Configure your browser to use the proxy.

Interact and Intercept:

Access http://127.0.0.1:5000 and log in (e.g., as user 2).



Use the frontend to trigger requests (e.g., access /profile/2).



Intercept requests in Burp Suite’s Proxy tab.



Test IDOR:

Modify parameters in Repeater or Intruder:

Change /profile/2 to /profile/1.



Change /document/ZG9jMg== (doc2) to /document/ZG9jMQ== (doc1).



Change /project/2/files to /project/1/files.



Look for 200 responses with unauthorized data.



Use Burp’s Decoder to encode/decode base64 document IDs (e.g., doc1 → ZG9jMQ==).



Admin Endpoint:





Test /admin/users as user 3 (admin) for 200.



Non-admins (e.g., user 2) should get 403.

Expected Vulnerabilities





Basic IDOR: Access other users’ profiles (e.g., /profile/1 as user 2).



Encoded IDOR: Access documents via base64-encoded IDs (e.g., /document/ZG9jMQ==).



Indirect IDOR: Access project files not owned by the user (e.g., /project/1/files).



Admin Endpoint: Secure (only user 3 can access).

Troubleshooting





404 Not Found:





Ensure the Flask app is running and URLs are correct (e.g., /profile/1, not /profiles/1).



Verify index.html is in the templates folder.



401 Unauthorized:





Log in first via the frontend or POST to /login with {"user_id": 2}.



Ensure Burp Suite includes the session cookie.



Frontend Not Loading:





Check Flask terminal for errors (e.g., TemplateNotFound).



Confirm file structure and Flask version (pip show flask).

Security Note

This app is for learning purposes only. It contains intentional vulnerabilities to demonstrate IDOR issues. To mitigate IDOR in real applications:





Validate resource ownership (e.g., check session['user_id'] against resource owner).



Use unpredictable IDs (e.g., UUIDs).



Implement role-based access control (RBAC).



Apply rate limiting to prevent enumeration.

License

MIT License. See LICENSE for details.

Contributing

Feel free to open issues or submit pull requests for improvements or additional vulnerabilities.
