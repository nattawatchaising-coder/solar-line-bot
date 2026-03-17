from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests
import json
import os

# ==============================
# 🔐 1. LINE CONFIG (จาก GitHub Secrets)
# ==============================
LINE_ACCESS_TOKEN = os.environ.get("LINE_ACCESS_TOKEN")

# ==============================
# 📤 ฟังก์ชัน Broadcast
# ==============================
def send_line_broadcast(message_text):
    url = 'https://api.line.me/v2/bot/message/broadcast'
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_ACCESS_TOKEN}'
    }

    data = {
        "messages": [
            {
                "type": "text",
                "text": message_text
            }
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        print("✅ Broadcast ส่งสำเร็จ!")
    else:
        print(f"❌ Broadcast ไม่สำเร็จ: {response.text}")


# ==============================
# 🌐 2. ตั้งค่า Chrome (Headless)
# ==============================
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

print("🚀 เริ่มการทำงาน: เปิดเบราว์เซอร์...")
driver = webdriver.Chrome(options=chrome_options)

try:
    # ==============================
    # 🔑 3. ล็อกอินเว็บ
    # ==============================
    driver.get("http://147.50.93.142:81/default.aspx")
    time.sleep(2)

    driver.find_element(By.ID, "txtUsername").send_keys("Admin")
    driver.find_element(By.ID, "txtPassword").send_keys("1234" + Keys.RETURN)

    # ==============================
    # ⏳ 4. รอโหลดข้อมูล
    # ==============================
    print("⏳ กำลังรอโหลดข้อมูล 5 วินาที...")
    time.sleep(5)

    # ==============================
    # 📊 5. ดึงข้อมูลพลังงาน
    # ==============================
    energy_labels = driver.find_elements(By.XPATH, "//label[@style='color: gray; font-size: x-large;']")

    if len(energy_labels) >= 2:
        this_month = energy_labels[0].text
        today = energy_labels[1].text

        # ==============================
        # 📝 6. สร้างข้อความ
        # ==============================
        msg = f"""📊 สรุปพลังงานโซล่าเซลล์
⚡ วันนี้: {today} kWh
📅 เดือนนี้: {this_month} kWh"""

        print(msg)

        # ==============================
        # 📤 7. Broadcast
        # ==============================
        if LINE_ACCESS_TOKEN:
            send_line_broadcast(msg)
        else:
            print("⚠️ ไม่พบ LINE_ACCESS_TOKEN")

    else:
        print("❌ ดึงข้อมูลไม่สำเร็จ")

except Exception as e:
    print(f"❌ เกิดข้อผิดพลาด: {e}")

finally:
    driver.quit()
    print("🏁 ปิดเบราว์เซอร์เรียบร้อย")
