from database import SessionLocal, Data, engine , Base

def seed_database():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    if db.query(Data).count() > 0:
        print("המסד כבר מכיל נתונים. אין צורך להזריק שוב.")
        db.close()
        return

    datas = [
        Data(
            name="מזכירות סטודנטים",
            category="לוח זמנים",
            location="בניין A, קומה 1, חדר 101",
            operating_hours="ימים א'-ה', 09:00-15:00",
            contact_email="office@smartcampus.tbc"
        ),
        Data(
            name="תמיכת מחשוב (IT) ואב הבית",
            category="מידע כללי",
            location="בניין C, חדר 20",
            operating_hours="ימים א'-ה', 08:00-18:00 (בחירום 050-1234567)",
            contact_email="it_support@smartcampus.tbc"
        ),
        Data(
            name="מעבדת מחשבים שנה א'",
            category="מידע כללי",
            location="בניין B, חדר 305",
            operating_hours="פתוח 24/7 (נדרש להעביר כרטיס סטודנט)",
            contact_email="labs@smartcampus.tbc"
        ),
        Data(
            name="כתובת הקמפוס",
            category="מידע כללי",
            location="דיוויד איילון 1,ירושלים",
            operating_hours= "הקמפוס פתוח 24/7",
            contact_email= "campus@smartcampus.tbc"
        ),
        Data(
            name="ד״ר עמית רומם - מרצה לפייתון ופיתוח צד שרת",
            category="סגל אקדמי",
            location="בניין B, חדר 401",
            operating_hours="שעות קבלה: יום ב', 10:00-12:00",
            contact_email="amit.r@smartcampus.tbc"
        ),
        Data(
            name="פרופ׳ יונית לוי - מרצה למדעי הנתונים",
            category="סגל אקדמי",
            location="בניין C, חדר 210",
            operating_hours="שעות קבלה: יום ד', 14:00-16:00",
            contact_email="yonit.l@smartcampus.tbc"
        ),
        Data(
            name="ד״ר דניאל ברשר - מרצה למסדי נתונים",
            category="סגל אקדמי",
            location="בניין A, חדר 105",
            operating_hours="שעות קבלה: יום א', 09:00-11:00",
            contact_email="daniel.a@smartcampus.tbc"
        ),
        Data(
            name="מר רון ספיר - מרצה להנדסת תוכנה וניהול גרסאות",
            category="סגל אקדמי",
            location="בניין B, חדר 302",
            operating_hours="שעות קבלה: יום ה', 12:00-14:00",
            contact_email="Ron.s@smartcampus.tbc"
        ),
        Data(
            name="ד״ר הראל אלון - מרצה לבינה מלאכותית ואוטומציה",
            category="סגל אקדמי",
            location="בניין C, חדר 405",
            operating_hours="שעות קבלה: יום ג', 16:00-18:00",
            contact_email="harel.b@smartcampus.tbc"
        )
    ]

    db.add_all(datas)
    db.commit()
    db.close()
    
    print("הנתונים הוזרקו בהצלחה למסד הנתונים! 🚀")

if __name__ == "__main__":
    seed_database()