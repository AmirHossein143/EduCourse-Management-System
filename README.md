# سامانه مدیریت دوره‌های آموزشی — فاز اول

پروژه درس برنامه‌نویسی وب، موضوع «مدیریت دوره‌های آموزشی» (بند ۳.۸ فایل پروژه).

در فاز اول اپ‌ها، فرایندها و مدل‌ها تعریف شده‌اند. صفحه‌های سایت، ثبت‌نام و ورود کاربران، جستجو و فرم‌های دانشجو و مدرس مربوط به فاز دوم هستند. فعلاً داده‌ها را می‌توان از پنل آماده ادمین وارد کرد.

## فایل‌های مهم

- [گزارش فاز اول و نمودار فرایندها](docs/phase1.md)؛ نمودارهای Mermaid را در GitHub یا Markdown Preview نسخه‌های جدید VS Code ببینید. در ویرایشگر متنی فقط کد نمودارها دیده می‌شود.
- [مدل پروفایل](accounts/models.py)
- [مدل موضوع، دوره و جلسه](courses/models.py)
- [مدل ثبت‌نام و نمره](enrollments/models.py)
- [بکاپ PostgreSQL فاز اول](backups/phase1.sql)

## ابزارهای لازم

- Python 3.10 تا 3.14 (اینجا با Python 3.12 اجرا شده است؛ Python 3.14 نیز با نسخه‌های فعلی وابستگی‌ها سازگار است).
- Django 5.2.18؛ نسخه 5.2 برای هماهنگی با اسلاید مدل‌ها و مثال‌های کلاس انتخاب شده است.
- PostgreSQL 16؛ در این پروژه از SQLite استفاده نمی‌شود.
- Docker و Docker Compose فقط برای روش ساده اجرای دیتابیس؛ اگر PostgreSQL نصب دارید، Docker لازم نیست.

## راه‌اندازی

دستورها را در پوشه‌ای اجرا کنید که `manage.py` در آن است.

```bash
python -m venv .venv
```

فعال کردن محیط در لینوکس و مک:

```bash
source .venv/bin/activate
```

در PowerShell ویندوز:

```powershell
.venv\Scripts\Activate.ps1
```

سپس:

```bash
python -m pip install -r requirements.txt
```

از فایل `.env.example` یک کپی با نام `.env` بسازید. در لینوکس و مک:

```bash
cp .env.example .env
```

در PowerShell:

```powershell
Copy-Item .env.example .env
```

داخل `.env`، مقدار `DB_PASSWORD` را با رمز دیتابیس محلی خود و `DJANGO_SECRET_KEY` را با یک رشته تصادفی جایگزین کنید. برای ساخت رشته تصادفی:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

این فایل محلی است و نباید وارد گیت شود. تنظیمات فعلی برای توسعه هستند.

برای اجرای محلی با `runserver`، مقدار `DJANGO_DEBUG=True` را نگه دارید تا فایل‌های static، از جمله CSS و JavaScript ادمین، سرو شوند. در استقرار واقعی باید `DEBUG=False` باشد و سرو فایل‌های static جداگانه تنظیم شود.

### روش اول: دیتابیس با Docker

```bash
docker compose up -d --wait db
```

این دستور کاربر و دیتابیس را با مقادیر `.env` می‌سازد و منتظر آماده شدن PostgreSQL می‌ماند. داده‌ها در volume نگهداری می‌شوند. بعد از اولین اجرا، تغییر رمز در `.env` رمز کاربر داخل دیتابیس را تغییر نمی‌دهد؛ برای تغییر رمز باید از خود PostgreSQL استفاده کنید.

### روش دوم: PostgreSQL نصب‌شده

در pgAdmin یا ابزار مدیریت PostgreSQL، یک کاربر و یک دیتابیس متعلق به همان کاربر بسازید و نام، رمز، میزبان و پورت را در `.env` وارد کنید. مثلاً در `psql` با حساب مدیر:

```sql
CREATE USER educourse;
\password educourse
CREATE DATABASE educourse OWNER educourse;
```

دستور `\password` رمز را تعاملی می‌گیرد. برای اجرای تست‌های دیتابیسی در فازهای بعد ممکن است لازم باشد به کاربر اجازه ساخت دیتابیس بدهید؛ برای اجرای عادی پروژه لازم نیست.

### ساخت جدول‌ها و اجرای پروژه

```bash
python manage.py migrate
python manage.py check
python manage.py createsuperuser
python manage.py runserver
```

در مرورگر مسیر `/admin/` روی سرور توسعه را باز کنید. مسیر اصلی سایت هنوز صفحه‌ای ندارد، چون ساخت صفحه‌ها در فاز دوم است.

ترتیب ورود دستی اطلاعات در ادمین:

1. در بخش کاربران، یک کاربر مدرس و یک کاربر دانشجو بسازید. رمزها را از فرم ساخت کاربر تعیین کنید.
2. در بخش پروفایل‌ها، برای هر کاربر پروفایل بسازید و نقش مناسب را انتخاب کنید. پروفایل در این فاز خودکار ساخته نمی‌شود.
3. موضوع و سپس دوره را با یک مدرس بسازید.
4. جلسه‌های دوره را وارد کنید.
5. برای دانشجو ثبت‌نام بسازید. نمره و ارزیابی می‌توانند فعلاً خالی بمانند.

نقش مدرس یا دانشجو با مجوز ادمین فرق دارد. برای کار با پنل مدیریت از حساب superuser استفاده کنید. حساب‌های عادی هنوز صفحه ورود و داشبورد ندارند.

## بررسی مدل‌ها

```bash
python manage.py check --database default
python manage.py makemigrations --check --dry-run
python manage.py showmigrations
```

اعتبارسنجی مقدارها در ادمین انجام می‌شود. اگر در shell داده می‌سازید، قبل از `save()`، متد `full_clean()` را صدا بزنید؛ خود `save()` آن را اجرا نمی‌کند. یکتایی ثبت‌نام و شماره جلسه علاوه بر اعتبارسنجی، در دیتابیس هم اعمال می‌شود.

## بکاپ دیتابیس

فایل `backups/phase1.sql` بکاپ دیتابیس همین فاز است؛ جدول‌های پروژه و اطلاعات داخلی migrationها و مجوزهای Django را دارد، ولی کاربر، رمز یا داده شخصی ندارد. برای ساخت یک دیتابیس تازه، روش پیشنهادی `migrate` است.

برای ساخت بکاپ کامل از دیتابیس خودتان با Docker، فایل را داخل کانتینر بسازید و سپس کپی کنید. این روش در PowerShell ویندوز و لینوکس و مک قابل استفاده است:

```bash
docker compose exec -T db sh -c 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc -f /tmp/educourse.dump'
docker compose cp db:/tmp/educourse.dump backups/educourse.dump
```

در Windows PowerShell 5.1 و PowerShell قدیمی‌تر از 7.4، هدایت خروجی باینری با `>` می‌تواند بکاپ `-Fc` را خراب کند. از نسخه 7.4 به بعد، خروجی برنامه‌های native به صورت بایت حفظ می‌شود؛ دستورهای بالا به این تفاوت نسخه‌ها وابسته نیستند.

این بکاپ ممکن است شامل حساب‌ها و داده‌های شخصی باشد، پس به صورت پیش‌فرض از گیت کنار گذاشته شده است. برای تحویل فاز یک، بکاپ بدون داده کاربری در مخزن قرار دارد.

بازیابی بکاپ فاز اول در یک دیتابیس **خالی** با Docker (پس از راه‌اندازی سرویس `db`):

```bash
docker compose cp backups/phase1.sql db:/tmp/phase1.sql
docker compose exec -T db sh -c 'psql -X -v ON_ERROR_STOP=1 -U "$POSTGRES_USER" -d "$POSTGRES_DB" -f /tmp/phase1.sql'
python manage.py migrate
```

این روش در PowerShell نیز کار می‌کند و به ورودی `<` نیاز ندارد. فایل `phase1.sql` شامل دستورهای مخصوص `psql` مانند `\restrict` و داده‌های `COPY ... FROM stdin` است؛ آن را با Query Tool در pgAdmin اجرا نکنید. برای PostgreSQL 16، از کلاینت به‌روز `psql` (حداقل 16.10) استفاده کنید تا `\restrict` را بشناسد.

اگر PostgreSQL را محلی نصب کرده‌اید و `psql` در PATH است:

```bash
psql -X -v ON_ERROR_STOP=1 -h 127.0.0.1 -p 5432 -U educourse -d educourse -f backups/phase1.sql
python manage.py migrate
```

نام کاربر و دیتابیس، میزبان و پورت را مطابق `.env` خود تغییر دهید؛ `psql` فایل `.env` پروژه را خودکار نمی‌خواند و در صورت نیاز رمز را تعاملی می‌پرسد. روی دیتابیس دارای جدول بازیابی را اجرا نکنید؛ برای این مسیر، قبل از بازیابی `migrate` نزنید و فقط پس از موفقیت بازیابی آن را اجرا کنید.

توقف دیتابیس بدون پاک شدن داده‌ها:

```bash
docker compose stop db
```
