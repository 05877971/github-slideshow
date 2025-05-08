import requests
import json
import re
from datetime import datetime
import time
import os  # לסביבה

'''

כל הזכויות שמורות לאלי כהן ©
פיתוח ותכנות (פייתון, וגוגל סקריפט-ג'אווה סקריפט וכו' וכו')
ליצירת קשר ופרטים נוספים:
8582511c@gmail.com
אין להעתיק, לשכפל בלי קנייה או קבלת אישור לשימוש בקוד
כל המעתיק, משכפל עובר על אישור גזל
''' 
# הגדרות
FOLDER_ID = '1DUCfXOMJnWB62INhajm_irJPPKDnFqsV'



TELEGRAM_CHANNELS = [
    {"url": "https://t.me/s/divuhim1234"},  # דיווחים חמים מהשטח
    {"url": "https://t.me/s/PikudHaOref_all"},  # פיקוד העורף - כל ההודעות
    {"url": "https://t.me/s/abualiexpress"},  # אבו עלי אקספרס
    {"url": "https://t.me/s/amitsegal"},  # עמית סגל
    {"url": "https://t.me/s/merkaz"},  # מרכז החדשות
    {"url": "https://t.me/s/lieldaphna"},  # ליאל דפנה
    {"url": "https://t.me/s/News_cabinet_news"},  # חדשות הממשלה
    {"url": "https://t.me/s/ynetalerts"},  # ynet - עדכונים
    {"url": "https://t.me/s/ramreports"},  # רם ברנדס - דיווחים
    {"url": "https://t.me/s/news00009"},  # חדשות 00009
    {"url": "https://t.me/s/yedidya_epshteyn"},  # ידידיה אפשטיין
    {"url": "https://t.me/s/HallelBittonRosen"},  # הלל ביטון רוזן
    {"url": "https://t.me/s/yediyot_bnei_brak"},  # ידיעות בני ברק
    {"url": "https://t.me/s/kolahadasot"},  # קול החדשות
    {"url": "https://t.me/s/yinonews"},  # ידיעות און ליין
    {"url": "https://t.me/s/Newss0nline"},  # חדשות און ליין
    {"url": "https://t.me/s/pkpoi"},  # פוקוס פוינט
    {"url": "https://t.me/s/Now14israel"},  # עכשיו 14
    {"url": "https://t.me/s/firstreportsnews"},  # דיווחים ראשוניים
    {"url": "https://t.me/s/TheBigBadShadow"},  # הצל
    {"url": "https://t.me/s/tzviye"},  # צבי יחזקאלי
    {"url": "https://t.me/s/NTD_Hebrew"},  # NTD עברית
    {"url": "https://t.me/s/bnetanyahu"},  # בנימין נתניהו
    {"url": "https://t.me/s/YLapid"},  # יאיר לפיד
    {"url": "https://t.me/s/yarivlevin"},  # יריב לוין
    {"url": "https://t.me/s/ayeletshaked1"},  # איילת שקד
    {"url": "https://t.me/s/yairsherkinews"},  # יאיר שרקי
    {"url": "https://t.me/s/mivzakibitahon"},  # מבזקי ביטחון - ישראל היום
    {"url": "https://t.me/s/N12_News"},  # חדשות 12
    {"url": "https://t.me/s/behadrei_harebim_bhol"},  # חדרי חרדים
    {"url": "https://t.me/s/idf_telegram"},  # צבא ההגנה לישראל
    {"url": "https://t.me/s/JewishFist"},  # האגרוף היהודי
    {"url": "https://t.me/s/arabworld301news"},  # העולם הערבי - חדשות
    {"url": "https://t.me/s/israel_news_telegram"},  # חדשות ישראל
    {"url": "https://t.me/s/GLOBAL_Telegram_MOKED"},  # מוקד החדשות - גלובל
    {"url": "https://t.me/s/knessettv"},  # ערוץ הכנסת
    {"url": "https://t.me/s/hadasot10"},  # חדשות 10
    {"url": "https://t.me/s/New_security8200"},  # חדשות ביטחון 8200
    {"url": "https://t.me/s/hazfon1"},  # חדשות הצפון 1
    {"url": "https://t.me/s/Yotamzimritelegram"},  # יותם זמרי
    {"url": "https://t.me/s/elisha_yered"},  # אלישע ירד
    {"url": "https://t.me/s/filbers"},  # פילבר
    {"url": "https://t.me/s/amirbohbot"},  # אמיר בוחבוט
    {"url": "https://t.me/s/realelchangr"},  # אלחנן גרונר
    {"url": "https://t.me/s/FidYamin"},  # פיד ימין
    {"url": "https://t.me/s/nilchamim"},  # נלחמים על הבית
    {"url": "https://t.me/s/tamirmorag14"},  # תמיר מורג
    {"url": "https://t.me/bengvir"},  # איתמר בן גביר
    {"url": "https://t.me/s/ZakaHQ"},  # זק"א
    {"url": "https://t.me/s/mdaisrael"},  # מגן דוד אדום
    {"url": "https://t.me/s/uh1221"},  # איחוד הצלה
    {"url": "https://t.me/s/techisrael"},  # טק ישראל
    {"url": "https://t.me/s/tzap1"}  # צאפ מגזין
]
GOOGLE_CHAT_WEBHOOK_URL = "https://chat.googleapis.com/v1/spaces/AAQA1-801Ro/messages?key=AIzaSyDdI0hCZtE6vySjMm-WEfRq3CPzqKqqsHI&token=_yfpt_D9lg7RZhofYRmrlPSseHbx6YeEnrbMgq4RwIk"
DELAY_BETWEEN_MESSAGES_MS = 1  # בפייתון, זמן ожидания הוא בשניות

# אחסון מידע על ההודעה האחרונה (ניתן להשתמש במסד נתונים או קובץ)
last_message_ids = {}
def fetch_url(url):
    try:
        response = requests.get(url, verify=False)  # הוספנו verify=False כאן
        response.raise_for_status()  # העלה חריגה עבור קודי סטטוס שגיאה
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"שגיאה בשליפת דף הטלגרם: {url} - {e}")
        return None

def get_channel_info(html_content):
    name_match = re.search(r'<meta property="og:title" content="([^"]+)"', html_content)
    image_match = re.search(r'<meta property="og:image" content="([^"]+)"', html_content)
    return {
        "name": name_match.group(1) if name_match else "ערוץ לא ידוע",
        "imageUrl": image_match.group(1) if image_match else ""
    }

def clean_text(text):
    text = re.sub(r'<br\s*\/?>', '\n', text)
    text = re.sub(r'<[^>]+>', '', text)
    text = text.replace('&quot;', '"').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    text = re.sub(r'https?:\/\/chat\.whatsapp\.com\/[^\s]+', '', text)
    text = re.sub(r'https?:\/\/wa\.link\/[^\s]+', '', text)
    text = re.sub(r'\s*להצטרפות בוואטסאפ:\s*\n?', '', text)
    text = re.sub(r'\s*בסטטוס:\s*\n?', '', text)
    text = re.sub(r'https?:\/\/t\.me\/[^\s]+', '', text)
    text = re.sub(r'https?:\/\/telegram\.me\/[^\s]+', '', text)
    text = re.sub(r'\s*הצטרפו לערוץ הטלגרם שלנו:\s*\n?', '', text)
    text = re.sub(r'פיד ימין - The Right Way בטלגרם: [^\s]*', '', text)
    text = re.sub(r'פיד ימין - The Right Way בוואטסאפ: [^\s]*', '', text)
    text = re.sub(r'https?:\/\/did\.li\/FidYamin', '', text)
    text = re.sub(r'לשיתוף בWhatsApp 💬.:', '', text)
    text = re.sub(r"עקבו אחרי 'חדשות אונליין ללא צנזורה' בכל הפלטפורמות: אינסטגרם \| טיקטוק \| טלגרם", '', text)
    text = re.sub(r'ללא צנזורה חדשות ישראל בטלגרם: [^\s]*', '', text)
    text = re.sub(r'לקבוצת הוואטסאפ: [^\s]*', '', text)
    return text.strip()

def parse_messages_from_html(html_content):
    messages = []
    message_blocks = re.findall(r'<div class="tgme_widget_message_wrap js-widget_message_wrap"[\s\S]*?<\/div><\/div>', html_content)
    for block in message_blocks:
        id_match = re.search(r'data-post="[^"]*?\/(\d+)"', block)
        if not id_match:
            continue
        message_id = int(id_match.group(1))
        text_match = re.search(r'<div class="tgme_widget_message_text js-message_text"[^>]*>([\s\S]*?)<\/div>', block)
        text = clean_text(text_match.group(1)) if text_match else ""
        text = re.sub(r'https:\/\/drive\.google\.com\/file\/d\/([^\/]+)\/view\?usp=[^&]+', r'https://drive.google.com/file/d/\1/view?usp=drivesdk', text)
        text = re.sub(r'(https?:\/\/[^\s]+)', r'<a href="\1">\1</a>', text)
        image_match = re.search(r'background-image:url\([\'"]?([^\'"\)]+)[\'"]?\)', block)
        image_url = image_match.group(1) if image_match else ""
        video_match = re.search(r'<video[^>]+src="([^"]+)"', block)
        video_url = video_match.group(1) if video_match else ""
        time_match = re.search(r'<time datetime="([^"]+)"', block)
        timestamp_str = time_match.group(1) if time_match else None
        timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else datetime.now()
        messages.append({
            "id": message_id,
            "text": text,
            "imageUrl": image_url,
            "videoUrl": video_url,
            "timestamp": timestamp.isoformat()
        })
    return sorted(messages, key=lambda x: x["id"])  # <-- השורה הזו צריכה להיות מוזחת פנימה
# פונקציה להעלאת סרטון לדרייב (דורשת אינטגרציה עם Google Drive API)
def upload_video_to_drive(url):
    print(f"הפונקציה upload_video_to_drive קיבלה את הקישור: {url}. יש לממש אינטגרציה עם Google Drive API כאן.")
    # כאן תצטרכי להשתמש בספריית google-api-python-client כדי לבצע העלאה לדרייב
    # זה כולל הרשאות, יצירת שירות דרייב וכו'.
    # כרגע, נחזיר None כ placeholder.
    return None

def send_card_to_google_chat(message, channel_info):
    formatted_date = datetime.fromisoformat(message["timestamp"]).strftime("%d/%m/%Y %H:%M:%S")
    sections = []
    if message["text"].strip():
        sections.append({"widgets": [{"textParagraph": {"text": message["text"]}}]})
    if message["imageUrl"]:
        sections.append({"widgets": [{"image": {"imageUrl": message["imageUrl"]}}]})
    if message["videoUrl"]:
        sections.append({"widgets": [{"textParagraph": {"text": f"📹 <a href='{message['videoUrl']}'>לחץ כאן לצפיה בסרטון</a>"}}]})

    if not sections:
        return

    card = {
        "cardsV2": [
            {
                "cardId": "telegramMessage",
                "card": {
                    "header": {
                        "title": channel_info["name"],
                        "subtitle": formatted_date,
                        "imageUrl": channel_info["imageUrl"],
                        "imageType": "CIRCLE"
                    },
                    "sections": sections
                }
            }
        ]
    }
    try:
        response = requests.post(GOOGLE_CHAT_WEBHOOK_URL, headers={'Content-Type': 'application/json'}, data=json.dumps(card))
        response.raise_for_status()
        print(f"הודעה נשלחה ל-Google Chat בהצלחה עבור הודעה {message['id']} מערוץ {channel_info['name']}")
    except requests.exceptions.RequestException as e:
        print(f"שגיאה בשליחת הודעה ל-Google Chat: {e}")

def check_for_new_messages():
    for channel in TELEGRAM_CHANNELS:
        channel_url = channel["url"]
        last_message_id = last_message_ids.get(channel_url, 0)
        html_content = fetch_url(channel_url)
        if html_content:
            channel_info = get_channel_info(html_content)
            messages = parse_messages_from_html(html_content)
            new_last_message_id = last_message_id
            for message in messages:
                if message["id"] > last_message_id:
                    if message["videoUrl"]:
                        message["videoUrl"] = upload_video_to_drive(message["videoUrl"])
                    send_card_to_google_chat(message, channel_info)
                    new_last_message_id = max(new_last_message_id, message["id"])
                    time.sleep(DELAY_BETWEEN_MESSAGES_MS)
            if new_last_message_id > last_message_id:
                last_message_ids[channel_url] = new_last_message_id

if __name__ == "__main__":
    # כאן הקוד ירוץ בלולאה או לפי תזמון שתגדירי
    while True:
        check_for_new_messages()
        time.sleep(1)  # בדוק כל דקה (ניתן לשנות)
