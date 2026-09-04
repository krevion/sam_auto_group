# SAM Auto Group

Django car dealership website prepared for Vercel.

## Vercel setup

1. Import the GitHub repository into Vercel.
2. Use the project root as the Vercel root directory.
3. Add these environment variables in Vercel project settings:

```text
DJANGO_SECRET_KEY=<long-random-secret>
DJANGO_DEBUG=False
ALLOWED_HOSTS=<your-vercel-domain>.vercel.app
CSRF_TRUSTED_ORIGINS=https://<your-vercel-domain>.vercel.app
DATABASE_URL=<hosted-postgresql-connection-url>
```

Add the production domain to `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` if a custom domain is used.

## Database

SQLite is used only as a local fallback. Vercel needs a hosted PostgreSQL database for admin users, cars, bookings, and contact messages.

After setting `DATABASE_URL`, run migrations against the production database:

```powershell
py manage.py migrate
```

Create the production admin account with a strong password:

```powershell
py manage.py createsuperuser
```

## Local development

```powershell
py -m pip install -r requirements.txt
py manage.py migrate
py manage.py runserver
```

Static files are collected and served with WhiteNoise. Uploaded admin media is not persistent on Vercel; use object storage such as Cloudinary or S3 for car uploads in production.

## Render setup

The repository includes `render.yaml` for a Python web service. Create a PostgreSQL database in Render, then set its internal connection string as `DATABASE_URL` on the web service. Render will install dependencies, collect static files, run migrations, and start Gunicorn automatically.

For a manually configured Render service, use this start command:

```text
gunicorn sam.wsgi:application --bind 0.0.0.0:$PORT --access-logfile - --error-logfile -
```

For uploaded car images, use persistent object storage such as Cloudinary or Amazon S3 because the web service filesystem is not intended for permanent uploads.
