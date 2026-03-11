from fastapi.testclient import TestClient
from main import app 

client = TestClient(app)

def test_ask_endpoint_success():
   
    payload = {"question": "מתי המזכירות פתוחה?"}
    
    response = client.post("/ask", json=payload)
    
    assert response.status_code == 200

    data = response.json()
    
    assert "answer" in data, "The response must contain an 'answer' field"
    assert "category" in data, "The response must contain a 'category' field"
    
    assert len(data["answer"]) > 0

    #באמצעות בדיקה זאת , בדקנו כמה דברים, ראשית אם הסרבר מחזיר לנו סטטוס 200- כלומר השרת לא קורס ומחזיר תשובה תקינה, שנית אם השרת מחזיר json תקין שעומד בציפיות שלנו  ובנוסף אם הai מחזיר תשובה עם תוכן ולא ריקה 
    #קיבלנו בפלט את השורה test_main.py::test_ask_endpoint_success PASSED [100%] שאומרת שהבדיקה עברה בהצלחה והסרבר מדבר עם הבוט בצורה חלקה
    #ניתן לראות שישנה אזהרה בטסט שמתריאה שהsdk שבשימוש כבר לא יקבל תמיכה ויש גרסה חדשה יותר.
    