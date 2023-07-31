## ConverGente: Where ideas become representation.

ConverGente is an innovative and powerful platform that drives citizen participation and real democratic representation. Designed to collect and consolidate proposals from members of various territorial assemblies, ConverGente enables representatives to build accurate and representative summaries of their communities' ideas.

Utilizing advanced built-in artificial intelligence, our virtual advisors guide representatives through the representation process, ensuring that each proposal faithfully reflects the concerns and aspirations of citizens.

The process doesn't end there. Once the consolidated summary is crafted, it undergoes voting among the members, ensuring that the final document is a true reflection of collective will.

The certification of representativeness bestowed upon the final document provides a seal of legitimacy, supporting decision-making and proposals in higher assemblies. With ConverGente, representatives have effective tools to advocate for the voices of their communities and carry out a more transparent and robust democratic process.

Join the revolution of citizen representation. Discover how ConverGente empowers communities and leaders to build a fairer and more participatory future.

## Features

- Collect and consolidate proposals from various territorial assemblies.
- Virtual advisors assist representatives in building accurate summaries.
- Members can vote on the consolidated summary to ensure true representation.
- Certification of representativeness lends legitimacy to decision-making processes.

## Getting Started

Follow these instructions to get a copy of the ConverGente project up and running 
on your local machine for development and testing purposes.

### Prerequisites

- Python (version 3.10.9)
- PostgreSQL (version 15.3)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/your_username/convergente.git
   ```

2. Create `.env` files:
Example file: 
```
DEBUG=1
SECRET_KEY=whatever
DJANGO_ALLOWED_HOSTS=0.0.0.0 localhost 127.0.0.1 [::1]
SQL_ENGINE=django.db.backends.postgresql_psycopg2
SQL_DATABASE=convergente
SQL_USER=postgres
SQL_PASSWORD=your_password
SQL_HOST=db
SQL_PORT=5432
DATABASE=postgres
```

3. Setup the virtual environment:  

```bash
cd convergente
python -m venv venv
source venv/bin/activate  # On Windows, use "venv\Scripts\activate"
```

4. Install dependencies:  
```bash
pip install -r requirements.txt

```

5. Configure the database:

- Create a PostgreSQL database for ConverGente. Database name should be `convergente`
- Update the database settings in convergente/settings.py with your database credentials.

6. Apply migrations to database:  

```bash
python manage.py makemigrations
python manage.py migrate
```

7. Create initial data:  
```bash
python manage.py populate_data
```

8. Run the project:  
```bash
python manage.py runserver 0.0.0.0:8000
```

9. Execution via Docker:  

```
docker-compose up
```

### Hints:  
- Stop keeping database data: `docker-compose down`
- Stop deleting database data: `docker-compose down -v`  

10. Example of `api` use:  

Getting all users from api with `jwt` token authentication:  

```bash
python api/utilities/get_all_users_from_api.py
```
Other `api`endpoints under development.  