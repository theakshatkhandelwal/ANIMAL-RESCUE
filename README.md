# AI-Enabled Animal Rescue & Adoption Web App

A full-stack web application that helps users report stray or lost animals, search for adoptable pets, and connect with local shelters. The system includes AI image recognition that identifies animals from uploaded photos to assist in faster reporting.

## Features

- 🐾 **Animal Adoption**: Browse and search for adoptable pets
- 📸 **AI Image Recognition**: Automatic animal identification from uploaded photos
- 📍 **Location-Based Reports**: Report and find animals near you
- 🏠 **Shelter Management**: Dashboard for shelters to manage animals and adoption requests
- 👤 **User Dashboard**: Track your reports and adoption requests
- 📱 **Responsive Design**: Works seamlessly on mobile and desktop devices

## Tech Stack

- **Backend**: Python, Django
- **Database**: MySQL
- **Frontend**: HTML, CSS, JavaScript
- **AI/ML**: OpenCV, TensorFlow (for image recognition)

## Prerequisites

- Python 3.8 or higher
- MySQL Server 5.7 or higher
- pip (Python package manager)

## Installation

### 1. Clone the Repository

```bash
cd "animal rescue"
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up MySQL Database

1. Create a MySQL database:
```sql
CREATE DATABASE animal_rescue CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. Create a `.env` file in the project root (copy from `.env.example`):
```env
SECRET_KEY=your-secret-key-here-change-this
DEBUG=True
DB_NAME=animal_rescue
DB_USER=root
DB_PASSWORD=your-mysql-password
DB_HOST=localhost
DB_PORT=3306
```

**Note**: For Windows, you may need to install `mysqlclient` separately. If you encounter issues, try:
```bash
pip install --upgrade pip
pip install mysqlclient
```

Alternatively, you can use `pymysql` as a workaround:
```bash
pip install pymysql
```

Then add this to your `animal_rescue/__init__.py`:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Admin)

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### 7. Collect Static Files

```bash
python manage.py collectstatic
```

### 8. Run the Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## Usage

### For Regular Users

1. **Register/Login**: Create an account or login
2. **Browse Animals**: View available animals for adoption
3. **Report Animals**: Report stray, lost, or found animals with photos
4. **Request Adoption**: Submit adoption requests for available animals
5. **View Dashboard**: Track your reports and adoption requests

### For Shelters

1. **Create Shelter Profile**: Register as a shelter from your dashboard
2. **Add Animals**: Add animals available for adoption
3. **Manage Requests**: Approve or reject adoption requests
4. **Post Updates**: Share updates about animals

### AI Image Recognition

When uploading a photo with a report:
- The system automatically attempts to identify the animal type
- Results are displayed with confidence percentage
- Helps speed up the reporting process

## Project Structure

```
animal rescue/
├── animal_rescue/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── rescue/                 # Main application
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── forms.py            # Django forms
│   ├── urls.py             # URL routing
│   ├── admin.py            # Admin configuration
│   └── ai_recognition.py   # AI image recognition
├── templates/              # HTML templates
│   ├── base.html
│   └── rescue/
├── static/                 # Static files
│   ├── css/
│   └── js/
├── media/                  # User uploaded files (created automatically)
├── manage.py
├── requirements.txt
└── README.md
```

## Database Models

- **User**: Django's built-in user model
- **Shelter**: Shelter/organization information
- **Animal**: Animal profiles with details
- **Report**: Reports of stray/lost/found animals
- **AdoptionRequest**: Adoption requests from users
- **Update**: Updates on animals or reports

## AI Recognition Notes

The current AI recognition implementation uses basic image processing as a placeholder. For production use:

1. Train or use a pre-trained model for animal classification
2. Save the model file (`.h5` or similar format)
3. Update `rescue/ai_recognition.py` to load the trained model
4. The current implementation provides a framework for integration

## Troubleshooting

### MySQL Connection Issues

If you encounter MySQL connection errors:
- Verify MySQL is running
- Check database credentials in `.env`
- Ensure the database exists
- Try using `pymysql` as mentioned in installation

### Static Files Not Loading

```bash
python manage.py collectstatic --noinput
```

### Migration Issues

```bash
python manage.py makemigrations rescue
python manage.py migrate
```

## Development

### Running Tests

```bash
python manage.py test
```

### Accessing Admin Panel

1. Navigate to `http://127.0.0.1:8000/admin/`
2. Login with superuser credentials
3. Manage all models from the admin interface

## Production Deployment

For production deployment:

1. Set `DEBUG=False` in settings
2. Update `SECRET_KEY` with a secure random key
3. Configure proper database credentials
4. Set up proper static file serving (e.g., WhiteNoise, AWS S3)
5. Configure media file storage
6. Set up proper security headers
7. Use a production WSGI server (e.g., Gunicorn)
8. Configure reverse proxy (e.g., Nginx)

## License

This project is open source and available for educational purposes.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For issues or questions, please open an issue in the repository.

---

**Built with ❤️ for animal rescue and adoption**


