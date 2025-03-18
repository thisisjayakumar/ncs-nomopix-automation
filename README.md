# Medical Billing Automation Web App

A Django-based web application designed to streamline and automate redundant processes for medical billing companies. This tool reduces the time-consuming task of querying data across multiple API calls from over 5 minutes to just **10 seconds** with a single click. It handles API requests, result generation, data cleaning, filtering, and optimization to provide a seamless user experience.

## Overview

In the medical billing industry, professionals often deal with repetitive tasks involving multiple API requests, data processing, and querying subsequent tasks based on previous results. This application automates the entire workflow, enabling users to:
- Trigger multiple API calls from the frontend with one click.
- Process, clean, and filter data automatically.
- Pass processed data to subsequent tasks for further querying.
- Deliver optimized results in a user-friendly format.

The result? A drastic reduction in manual effort and processing time, empowering medical billing teams to focus on higher-value tasks.

## Features
- **One-Click Automation**: Execute a chain of API requests and data processing with a single action.
- **Time Efficiency**: Reduces a 5-minute manual process to just 10 seconds.
- **Data Handling**: Cleans, filters, and optimizes API response data for ease of use.
- **Scalable Design**: Built with Django for robustness and extensibility.
- **Real-World Impact**: Tailored for medical billing companies to improve operational efficiency.

## Tech Stack
- **Framework**: Django 5.1.2
- **Backend**: Python, Gunicorn
- **API Automation**: Selenium, Trio, WebSocket
- **Dependencies**: See [requirements.txt](#dependencies) for the full list.

## Installation

### Prerequisites
- Python 3.8+
- Git
- Virtualenv (recommended)

### Steps
1. **Clone the Repository**
   ```bash
   git clone https://github.com/thisisjayakumar/medical-billing-automation.git
   cd medical-billing-automation
   ```

2. **Set Up a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment**
   - Create a `.env` file in the root directory (if applicable) for sensitive configurations like API keys or database credentials.
   - Example `.env`:
     ```
     SECRET_KEY=your_django_secret_key
     DEBUG=True
     API_KEY=your_api_key
     ```

5. **Run Database Migrations**
   ```bash
   python manage.py migrate
   ```

6. **Start the Development Server**
   ```bash
   python manage.py runserver
   ```
   Visit `http://127.0.0.1:8000/` in your browser to see the app in action.

7. **Deploy with Gunicorn (Optional)**
   ```bash
   gunicorn cgsmedicare.wsgi:application
   ```

## Dependencies
The project relies on the following Python packages (listed in `requirements.txt`):
```
asgiref==3.8.1
attrs==24.2.0
certifi==2024.8.30
cffi==1.17.1
Django==5.1.2
gevent==24.10.2
greenlet==3.1.1
gunicorn==23.0.0
h11==0.14.0
idna==3.10
MarkupSafe==3.0.1
outcome==1.3.0.post0
packaging==24.1
pycparser==2.22
PySocks==1.7.1
selenium==4.25.0
serverless-wsgi==3.0.4
setuptools==75.1.0
sniffio==1.3.1
sortedcontainers==2.4.0
sqlparse==0.5.1
trio==0.26.2
trio-websocket==0.11.1
typing_extensions==4.12.2
tzdata==2024.2
urllib3==2.2.3
webdriver-manager
websocket-client==1.8.0
Werkzeug==3.0.6
wsproto==1.2.0
zope.event==5.0
zope.interface==7.1.0
```

## Usage
1. **Access the Web App**: Open the app in your browser after starting the server.
2. **Input Data**: Provide any necessary inputs (e.g., billing codes, patient IDs) via the frontend interface.
3. **Click to Process**: Hit the "Process" button (or equivalent) to trigger the automation.
4. **View Results**: The app will display cleaned and optimized results within seconds.

## Project Structure
```
medical-billing-automation/
│
├── cgsmedicare/
│   ├── settings.py  
│   ├── urls.py  
│   ├── wsgi.py  
│   └── ...
├── app/
│   ├── views.py 
│   ├── models.py  
│   ├── templates/
│   └── ...
├── requirements.txt
└── README.md
```

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a pull request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
For questions or feedback, reach out to jayagma032@gmail.com or open an issue on GitHub.

---
