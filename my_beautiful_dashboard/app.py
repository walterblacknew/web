from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

# در این مثال، به سادگی از یک متغیر سراسری لیستی برای ذخیره داده‌ها استفاده شده.
# در عمل، بهتر است از دیتابیس (مثلاً SQLite/PostgreSQL) استفاده کنید.
ALL_RESPONSES = []

@app.route("/webhook", methods=["POST"])
def porsline_webhook():
    """
    وبهوکی که پرس‌لاین درخواست POST با داده‌های پاسخ‌های جدید را به آن ارسال می‌کند.
    """
    data = request.get_json()  # دریافت داده‌های JSON
    if not data:
        return jsonify({"error": "No JSON provided"}), 400
    
    # نمونه‌ای از داده‌هایی که ممکن است از پرس‌لاین دریافت کنید (بسته به مستندات):
    # {
    #   "form_id": 123,
    #   "response_id": "abc-xyz",
    #   "submitted_at": "2023-12-01T10:00:00Z",
    #   "answers": {
    #       "question_1": "پاسخ 1",
    #       "question_2": "پاسخ 2",
    #       ...
    #   }
    # }
    
    # داده را به لیست سراسری اضافه می‌کنیم
    ALL_RESPONSES.append(data)
    
    # پاسخ موفقیت‌آمیز به پرس‌لاین
    return jsonify({"status": "ok"}), 200

@app.route("/dashboard")
def dashboard():
    """
    نمایش یک داشبورد زیبا برای مشاهده و فیلتر کردن پاسخ‌ها.
    """
    # در اینجا می‌توانیم به صورت پویا ALL_RESPONSES را به قالب ارسال کنیم
    return render_template("dashboard.html", responses=ALL_RESPONSES)

@app.route("/")
def index():
    """
    صفحه اول را می‌توانیم ریدایرکت کنیم به داشبورد
    """
    return '''
    <h2>Welcome to the Beautiful Dashboard</h2>
    <p>برای مشاهده‌ی داشبورد <a href="/dashboard">کلیک کنید</a>.</p>
    '''

if __name__ == "__main__":
    app.run(debug=True, port=5000)
