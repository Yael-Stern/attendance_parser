def classify_report_type(raw_text: str) -> str:
    """
    מזהה את סוג הדו"ח באופן מדויק על סמך טקסט ה-OCR.
    """
    # אם טקסט ה-OCR ריק, מחזיר ברירת מחדל מסוג A
    if not raw_text:
        return "TYPE_A"

    # רשימת מילות מפתח לזיהוי דוח מסוג TYPE_B
    type_b_keywords = ["כרטיס עובד", "כרטסת עובד", "שעת כניסה", "שענת כניסה", "שעת יציאה", "יום בשבוע", "הערות"]
    # בדיקה האם קיימת לפחות מילת מפתח אחת של TYPE_B בטקסט
    if any(kw in raw_text for kw in type_b_keywords):
        return "TYPE_B"

    # רשימת מילות מפתח לזיהוי דוח מסוג TYPE_A
    type_a_keywords = ["125%", "150%", "שבת", "גליליון"]
    # בדיקה האם קיימת לפחות מילת מפתח אחת של TYPE_A בטקסט
    if any(kw in raw_text for kw in type_a_keywords):
        return "TYPE_A"

    # ברירת מחדל במקרה שלא נמצאה התאמה מובהקת לאף קבוצה
    return "TYPE_B"