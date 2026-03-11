from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
import time 
import logging
import asyncio
from database import engine, Base,SessionLocal, Data
from dotenv import load_dotenv
import google.generativeai as genai
import os
import json
from fastapi.middleware.cors import CORSMiddleware

load_dotenv() 
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Smart Campus Assistant", description="A smart campus ai assistant ", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
#זה המנגנון rate limiting למניעת ספאם 
user_requests = {}
rate_limit_seconds = 3


class QuestionRequest(BaseModel):
    question: str = Field(..., min_length=1, max_length=300, description="The question of the student")



class AnswerResponse(BaseModel):
    answer: str 
    category: str
    confidence: float = 0.0


async def call_ai_service(question: str) -> dict:
    db = SessionLocal()
    try:
        Datas = db.query(Data).all()
        
        context_text = "מידע עדכני על מתקני הקמפוס ואנשי סגל (מרצים/מתרגלים):\n"
        for d in Datas:
            context_text += f"- {d.name} (קטגוריה: {d.category}): מיקום: {d.location}, שעות פעילות/קבלה: {d.operating_hours}, איש קשר: {d.contact_email}\n"
    finally:
        db.close() 
    
    prompt = f"""
    "אתה עוזר וירטואלי בקמפוס. עליך לענות אך ורק על בסיס הנתונים המסופקים. עליך להחזיר JSON תקין הכולל ציון ביטחון אלא אם כן צויין אחרת."
    
    ### המידע שברשותך (CONTEXT):
    {context_text}

    ### הנחיות קריטיות:
    1. כאשר מברכים אותך באיחולים כמו שלום, מה שלומך או נימוסים אחרים, הגדר את רמת ה-confidence כ-1.0 ואת הקטגוריה כ"מידע כללי".
    2. אם השאלה עוסקת באחד המתקנים, השירותים או אנשי הסגל המופיעים ב-CONTEXT, ענה בצורה שירותית לפי הנתונים והגדר confidence כ-1.0. אם שואלים על פגישה עם מרצה, ציין את שעות הקבלה והמיקום שלו.
    3. רק אם השאלה היא על נושא או אדם שבכלל לא מופיעים ב-CONTEXT (למשל: "איפה יש פיצה?", "מתי המבחן במתמטיקה?" או מרצה שלא קיים ברשימה), רק אז הגדר confidence נמוך מ-0.5.
    4. אם פונים אליך בשפה שהיא לא עברית תגיב - "אני לא למדתי בקמפוס, לכן אני מבין רק עברית".

    ### פורמט פלט:
    ענה אך ורק בפורמט JSON הבא:
    {{
        "answer": "התשובה שלך",
        "category": "הקטגוריה המתאימה (למשל: סגל אקדמי, מידע כללי, לוח זמנים)",
        "confidence": 0.90
    }}

    השאלה של הסטודנט: "{question}"
    """
    try:
        response = await model.generate_content_async(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
            )
        )
        ai_data = json.loads(response.text)
        return ai_data
        
    except Exception as e:
        logger.error(f"Gemini API Error: {str(e)}")
        return {"answer": "שגיאה", "category": "שגיאה", "confidence": 0.0}

@app.post("/ask", response_model=AnswerResponse)
async def ask_question(request: Request, body: QuestionRequest): 
    client_ip = request.client.host
    current_time = time.time() 

    if client_ip in user_requests:
        if  current_time - user_requests[client_ip]< rate_limit_seconds:
            raise HTTPException(status_code=429, detail="שלחת יותר מדי בקשות, אנא המתן מעט ונסה שוב.")
    user_requests[client_ip] = current_time 

    try:
        logger.info(f"Received question from {client_ip}: {body.question}")
        
        ai_response = await asyncio.wait_for(call_ai_service(body.question), timeout=30)

        if ai_response.get("confidence",1.0) < 0.60: 
            logger.warning(f"Low confidence answer from AI: ({ai_response.get('confidence')}).triggering fallback.") 
            return AnswerResponse(answer= "אופס! אני עדיין לא יודע את התשובה לשאלה הזאת, אני ממליץ לפנות אל מזכירות הקמפוס במספר 03-5555555", category="מידע כללי")
            
        return AnswerResponse(
            answer=ai_response["answer"],
            category=ai_response["category"],
            confidence=ai_response.get("confidence", 1.0)
        ) 

    except Exception as e:
        logger.error(f"Critical Error: {str(e)}") 
        return {"answer": f"Error: {str(e)}", "category": "שגיאה", "confidence": 0.0}

@app.get("/health")
async def health_check():
    return {"status": "ok", "message":"Smart ai campus is online!!"}
