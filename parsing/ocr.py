import asyncio
import pymupdf
from winsdk.windows.media.ocr import OcrEngine
from winsdk.windows.globalization import Language
from winsdk.windows.storage.streams import InMemoryRandomAccessStream, DataWriter
from winsdk.windows.graphics.imaging import BitmapDecoder


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extracts text from scanned or digital PDFs using PyMuPDF and Windows native OCR (winsdk)
    completely within Python/Windows, without external dependencies like Tesseract or Poppler.
    """

    async def _extract():
        try:
            raw_text = ""

            # אתחול מנוע ה-OCR של ווינדוס לשפה העברית
            try:
                lang = Language("he-IL")
                ocr_engine = OcrEngine.try_create_from_language(lang)
            except Exception:
                ocr_engine = None

            if not ocr_engine:
                ocr_engine = OcrEngine.try_create_from_user_profile_languages()

            if not ocr_engine:
                print("Error: Windows OCR engine could not be initialized.")
                return ""

            # פתיחת קובץ ה-PDF באמצעות ספריית PyMuPDF
            doc = pymupdf.open(pdf_path)

            for page_num in range(len(doc)):
                page = doc[page_num]

                # המרת עמוד ה-PDF לתמונה ברזולוציה גבוהה (DPI 150)
                pix = page.get_pixmap(dpi=150)
                img_bytes = pix.tobytes("png")

                # טעינת סיביות התמונה לזרם זיכרון (Stream) עבור מנוע ה-OCR של ווינדוס
                stream = InMemoryRandomAccessStream()
                writer = DataWriter(stream)
                writer.write_bytes(img_bytes)
                await writer.store_async()
                await writer.flush_async()
                stream.seek(0)

                decoder = await BitmapDecoder.create_async(stream)
                software_bitmap = await decoder.get_software_bitmap_async()

                # ביצוע פענוח טקסט (OCR) מובנה על התמונה
                result = await ocr_engine.recognize_async(software_bitmap)

                if result and result.lines:
                    page_text = "\n".join([line.text for line in result.lines])
                    raw_text += page_text + "\n"

            doc.close()

            # ניקוי שגיאות זיהוי נפוצות של OCR (המרת האות O האנגלית לאפס)
            cleaned_text = raw_text.replace("O", "0")
            return cleaned_text

        except Exception as e:
            print(f"OCR Error processing {pdf_path}: {e}")
            return ""

    # הפעלה סינכרונית של פונקציית ה-Async לחילוץ הטקסט
    return asyncio.run(_extract())