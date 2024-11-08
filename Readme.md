# Automated Business Data Processing Tool

## Overview
This project is an automation tool that streamlines and optimizes the retrieval and analysis of large-scale transactional data in a business application. Traditional methods require users to manually input major codes and process tables one by one, taking 1-2 hours for 80 transactions. With this tool, users can access processed data for 80 transactions within **10 seconds**, enhancing efficiency and decision-making.

## Key Features

- **Automated Data Retrieval**: Initiates multithreaded browser sessions to extract data concurrently using **BeautifulSoup**.
- **Data Transformation and Analysis**: Converts raw data into meaningful insights and displays only relevant information for better user consumption.
- **Fast Processing**: Reduces data processing time from hours to seconds.
- **User Authentication and Security**: Implements **JWT-based security protocols** for secure access.
- **Subscription and Team Plans**: Supports team organization plans and premium user subscriptions for tailored experiences.
- **User-Friendly Interface**: Provides an elegant UI for seamless, single-click data retrieval.

## Tech Stack

- **Backend**: **Django**, **AWS EC2** for hosting, **Memcache** for caching, **Celery** for task management.
- **Frontend**: **Next.js**, deployed via **Netlify**.
- **Data Parsing**: **BeautifulSoup** for screen scraping and data extraction.
- **Hosting & Infrastructure**:
  - **Website Hosting**: Hosted on **Hostinger** with domain registration via **GoDaddy**.
  - **Edge Computing**: **Cloudflare** for proxy and caching solutions.
- **Security**: **JWT** for secure user sessions.

## Getting Started

1. Clone the repository: `git clone https://github.com/thisisjayakumar/ncs-nomopix-automation`
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables for authentication, database connection, etc.
4. Make migrations and run the migrations to your database.
5. Run the Django development server: `python manage.py runserver`
6. In a separate terminal, start the Celery worker: `celery -A project_name worker --beat --loglevel=info`
7. Navigate to `http://localhost:8000` in your web browser to access the application.

## Contributing

We welcome contributions from the community! If you find any issues or have suggestions for improvements, please [submit an issue](https://github.com/thisisjayakumar/ncs-nomopix-automation/issues/new/) or [create a pull request](https://github.com/thisisjayakumar/ncs-nomopix-automation/compare).

## License

This project is licensed under the [MIT License](LICENSE).