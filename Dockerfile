# نختار صورة بايثون رسمية
FROM python:3.11-slim

# نحدد مكان العمل داخل الحاوية
WORKDIR /app

# ننسخ الملفات من الجهاز للحاوية
COPY . .

# نثبت المتطلبات لو فيه requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# نحدد الأمر اللي يتنفذ لما يبدأ الكونتينر
CMD ["python", "main.py"]
