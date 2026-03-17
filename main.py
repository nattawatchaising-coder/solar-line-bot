from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import requests
import json
import os

# 1. ดึงกุญแจจาก GitHub Secrets (เดี๋ยวเราจะไปตั้งค่ากันใน GitHub ครับ)
LINE_ACCESS_TOKEN = os.environ.get("LINE_ACCESS_TOKEN")
LINE_USER_ID = os.environ.get("LINE_USER_ID")

# ฟังก์ชันสำหรับส่งข้อความผ่าน LINE Messaging API
def send_line_message(message_text):
    url = 'https://api.line.me/v2/bot/message/push'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {LINE_ACCESS_TOKEN}'
    }
    data = {
        "to": LINE_USER_ID,
        "messages": [{"type": "text", "text": message_text}]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 200:
        print("✅ ส่งข้อความเข้า LINE สำเร็จ!")
    else:
        print(f"❌ ส่งข้อความไม่สำเร็จ Error: {response.text}")

# 2. ตั้งค่าเบราว์เซอร์แบบไร้หน้าจอ (สำหรับรันบนเซิร์ฟเวอร์)
chrome_options = Options()
chrome_options.add_argument("--headless=new")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

print("🚀 เริ่มการทำงาน: เปิดเบราว์เซอร์...")
driver = webdriver.Chrome(options=chrome_options)

try:
    # 3. ล็อกอินเข้าเว็บ
    driver.get("http://147.50.93.142:81/default.aspx")
    time.sleep(2)
    driver.find_element(By.ID, "txtUsername").send_keys("Admin")
    driver.find_element(By.ID, "txtPassword").send_keys("1234" + Keys.RETURN)
    
    # 4. ดึงข้อมูล
    print("⏳ กำลังรอโหลดข้อมูล 5 วินาที...")
    time.sleep(5)
    energy_labels = driver.find_elements(By.XPATH, "//label[@style='color: gray; font-size: x-large;']")
    
    if len(energy_labels) >= 2:
        this_month = energy_labels[0].text
        today = energy_labels[1].text
        
        # 5. สรุปข้อความ
        msg = f"📊 สรุปยอดพลังงานโซล่าเซลล์\n⚡ ยอดวันนี้: {today} kWh\n📅 ยอดเดือนนี้: {this_month} kWh"
        print(msg)
        
        # 6. สั่งให้ฟังก์ชันส่งข้อความทำงาน
        if LINE_ACCESS_TOKEN and LINE_USER_ID:
            send_line_message(msg)
        else:
            print("⚠️ หาตัวกุญแจ LINE ไม่พบ (ข้ามการส่งข้อความ)")
    else:
        print("❌ ดึงข้อมูลไม่สำเร็จ หาตัวเลขไม่พบ")

except Exception as e:
    print(f"❌ เกิดข้อผิดพลาด: {e}")

finally:
    driver.quit()
    print("🏁 จบการทำงานเบราว์เซอร์")
