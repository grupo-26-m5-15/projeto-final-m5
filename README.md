# BiblioteKa

### The application is a Restful API that aims to manage information related to the operation of various libraries.

To run the application, follow these steps.

1. Create your virtual environment:

```bash
python -m venv venv
```

2. Active your venv:

```bash
# Linux:
source venv/bin/activate

# Windows (Powershell):
.\venv\Scripts\activate

# Windows (Git Bash):
source venv/Scripts/activate
```

3. Install all requirements:

```bash
pip install -r requirements.txt
```

4. Run the migrations:

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

5. Run the server:

```bash
python manage.py runserver
```

6. Access the documentation to view and test all routes

```bash
localhost/api/docs/
```

## BiblioteKa Diagram

![Getting Started](./BiblioteKa.jpg)
