import os
import smtplib
from email.message import EmailMessage
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# SMTP Config
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")

@app.route("/")
def index():
    return send_file("all_airlines_web.html")

@app.route("/api/send_email", methods=["POST"])
def send_email():
    data = request.json
    target_email = data.get("email")
    airline_name = data.get("airline_name", "Airlines")
    departure_date = data.get("departure_date", "Unknown")
    ics_data = data.get("ics_data")
    
    if not all([target_email, ics_data]):
        return jsonify({"status": "error", "message": "前端未提供 Email 或 ICS 內容"}), 400
        
    if not SENDER_EMAIL or not SENDER_PASSWORD:
         return jsonify({"status": "error", "message": "伺服器未設定 SENDER_EMAIL 或應用程式密碼，請於 .env 完成設定。"}), 500

    try:
        msg = EmailMessage()
        msg["Subject"] = f"搶 {airline_name} 機票 ({departure_date}) 行事曆提醒"
        msg["From"] = SENDER_EMAIL
        msg["To"] = target_email
        msg.set_content(f"您好！\n\n附件為您剛才透過系統產生的：{airline_name} ({departure_date}) 自動放票提醒行事曆。\n\n請直接點擊匯入您的裝置或 Google 行事曆，並請於響鈴提醒時準時行動！\n\n- Global Airlines Award Hub 推算系統敬上")
        
        # 將前端編譯好的 ICS 字串附載成真正的 .ics 檔案
        msg.add_attachment(ics_data.encode('utf-8'), maintype='text', subtype='calendar', filename=f"award_reminder_{departure_date}.ics")
        
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            
        return jsonify({"status": "success", "message": "Email sent successfully!"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == "__main__":
    print("=" * 50)
    print("🌍 Global Airlines Hub Backend Service Started")
    print("=" * 50)
    print("🌐 網頁存取位址: http://127.0.0.1:5000")
    if not SENDER_EMAIL:
        print("⚠️ [警告] 尚未在此環境的 .env 檔案中配置 SENDER_EMAIL，Email 寄件功能將無法使用。")
    app.run(host="127.0.0.1", port=5000, debug=True)
