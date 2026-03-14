# Telegram Socks Scraper

این پروژه یک **اسکریپت Python** است که از کانال‌های تلگرام ساکس جمع‌آوری می‌کند و خروجی آن را در GitHub آپدیت می‌کند.  
هر بار اسکریپت اجرا شود، فایل `socks5.txt` و `telegram_socks.txt` بروزرسانی می‌شوند.

---

## ویژگی‌ها

- استخراج **SOCKS5** از پیام‌های تلگرام
- پشتیبانی از **User/Password** و بدون آن
- استخراج چند ساکس در یک پیام
- حذف لینک‌های تکراری
- ذخیره جداگانه: `telegram_socks.txt` و `socks5.txt`
- **GitHub آپدیت اتوماتیک** پس از هر اجرا
- امن برای **Rate Limit تلگرام** (با محدودیت پیام و sleep)

---

## پیش‌نیازها

- Python 3.11+
- Telethon:
```bash
pip install telethon
