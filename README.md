# Online Shop

Online Shop is an e-commerce web application built with Django, offering users a seamless shopping experience. This
project incorporates various features and technologies to facilitate product browsing, purchasing, and management.

## Features

- **User Authentication and Authorization**: Users can create accounts, log in, and securely access features like order
  placement and profile management.

- **Product Browsing and Search**: Browse products by categories and use a robust search feature to find items quickly.

- **Shopping Cart Management**: Add, remove, and adjust quantities of products in the shopping cart.

- **Streamlined Checkout Process**: Guided steps for entering shipping details, selecting payment methods, and reviewing
  orders.

- **Asynchronous Task Processing**: Celery handles tasks like sending order confirmation emails without impacting
  application responsiveness.

- **Caching for Performance**: Redis caches frequently accessed data to improve performance and reduce database load.

- **Responsive Design**: Ensures a consistent user experience across devices.

## List of technologies, frameworks, libraries, and tools Used

- **Python**: High-level programming language known for its simplicity and versatility.

- **Django**: Web framework for rapid development of secure and maintainable websites.

- **Django Rest Framework**: Toolkit for building Web APIs quickly and efficiently.

- **python-decouple**: Library for separating settings from code for better configuration management.

- **Pillow**: Python Imaging Library for image processing tasks.

- **Django-Jazzmin**: Customizable admin panel for Django projects.

- **Psycopg2-Binary**: PostgreSQL adapter for Python.

- **Pytz**: Library for working with time zones in Python.

- **Selenium**: Browser automation framework for web application testing.

- **Isort**: Python import sorter for organizing import statements.

- **Ruff**: Tool for fixing linting errors in Python code.

- **Pre-Commit**: Framework for managing pre-commit hooks in Git repositories.

- **Docker**: Containerization platform for packaging and deploying applications.

- **Redis**: In-memory data structure store commonly used for caching and message queuing.

- **Celery**: Distributed task queue for asynchronous task processing in web applications.

- **Tailwind CSS**: Utility-first CSS framework for building responsive and customizable user interfaces.

- **AJAX Fetch**: Technique for making asynchronous HTTP requests from web pages using JavaScript.

## Entity-Relationship Diagram for Online Shop

![ERD](ERD/ERD_Online_Shop.pdf)

## Setup

### Prerequisites

- Python (version >= 3.6)
- Django (version >= 3.0)
- Django Rest Framework (version >= 3.0)
- python-decouple (version >= 3.8)
- pillow (version >= 10.3.0)
- django-jazzmin (version >= 2.6.1)
- psycopg2-binary (version >= 2.9.9)
- pytz (version >= 2024.1)
- selenium (version >= 4.19.0)
- isort (version >= 5.13.2)
- ruff (version >= 0.3.7)
- pre-commit (version >= 3.7.0)

### Installation and Usage

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/pedramkarimii/Online-Shop.git
    ```

2. **Navigate to the Project Directory**:

    ```bash
    cd Online-Shop
    ```

3. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Set Up Django Environment**:

    ```bash
    . utility/cleaner.sh
    ```

5. **Start the Development Server**:

    ```bash
    python manage.py runserver
    ```

6. **Access the Application**:

   Visit `http://127.0.0.1:8000/` in your web browser.

## How to Fork the Project

To fork the Tiny Instagram project and contribute to it:

1. **Fork the Repository**: Click the "Fork" button at the top right of the GitHub repository page to create a copy of
   the project in your GitHub account.
2. **Clone Your Forked Repository**: Clone your forked repository to your local machine using Git.
3. **Make Changes and Improvements**: Make changes and improvements to the project as needed, such as adding new
   features, fixing bugs, or enhancing documentation.
4. **Commit and Push Changes**: Commit your changes to your forked repository and push them to GitHub.
5. **Create a Pull Request**: Create a pull request to propose your changes and merge them into the main repository.

## Contributors

- Pedram Karimi (@pedramkarimii) - Owner

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

