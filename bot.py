import os
import asyncio
import datetime
import subprocess
import zipfile
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import environ
import pytz
import logging

# Logging sozlamalari
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# ENV o‘zgaruvchilarni yuklash
env = environ.Env()
environ.Env.read_env()

BOT_TOKEN = env("BOT_TOKEN")
OWNER_ID = int(env("OWNER_ID"))
DB_USER = env("DB_USER")
DB_NAME = env("DB_NAME")
DB_CONTAINER = env("DB_CONTAINER")

# Aiogram va APScheduler obyektlari
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

# Backup saqlanadigan papka
BACKUP_DIR = "./backups"
os.makedirs(BACKUP_DIR, exist_ok=True)

# Toshkent vaqti
TASHKENT_TZ = pytz.timezone("Asia/Tashkent")

# Backup vaqti (default 01:00)
backup_time = "01:00"


# FSM uchun holatlar
class BackupTimeState(StatesGroup):
    waiting_for_time = State()


def create_backup():
    """PostgreSQL bazasining backupini yaratish"""
    date_str = datetime.datetime.now(TASHKENT_TZ).strftime("%Y-%m-%d_%H-%M-%S")
    backup_filename = f"backup_{date_str}.sql"
    backup_path = os.path.join(BACKUP_DIR, backup_filename)

    try:
        # Docker exec orqali pg_dump buyrug'ini ishga tushirish
        with open(backup_path, "w") as backup_file:
            subprocess.run(
                ["docker", "exec", DB_CONTAINER, "pg_dump", "-U", DB_USER, DB_NAME],
                stdout=backup_file,
                check=True
            )
        logging.info(f"Backup muvaffaqiyatli yaratildi: {backup_path}")
        return backup_path
    except subprocess.CalledProcessError as e:
        logging.error(f"Backup yaratishda xatolik: {e}")
        return None
    except FileNotFoundError:
        logging.error("Docker topilmadi yoki boshqa xatolik!")
        return None


def zip_media_folder():
    """web/media papkasini zip qilish"""
    media_dir = "./web/media"  # Media papkasi joylashgan manzil
    if not os.path.exists(media_dir):
        logging.error("Media papkasi topilmadi!")
        return None

    date_str = datetime.datetime.now(TASHKENT_TZ).strftime("%Y-%m-%d_%H-%M-%S")
    zip_filename = f"media_backup_{date_str}.zip"
    zip_path = os.path.join(BACKUP_DIR, zip_filename)

    try:
        # Zip arxivini yaratish
        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(media_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, media_dir)
                    zipf.write(file_path, arcname)
        logging.info(f"Media papkasi muvaffaqiyatli arxivlandi: {zip_path}")
        return zip_path
    except Exception as e:
        logging.error(f"Media papkasini arxivlashda xatolik: {e}")
        return None


async def send_telegram_message(text):
    """Xabar yuborish"""
    await bot.send_message(OWNER_ID, text)


async def backup_and_send():
    """Backupni yaratish va yuborish (PostgreSQL + Media)"""
    await send_telegram_message("📌 PostgreSQL va Media backup jarayoni boshlandi...")

    # PostgreSQL backup
    pg_backup_file = create_backup()
    if pg_backup_file:
        await send_telegram_message("✅ PostgreSQL backup tayyor! Fayl jo‘natilmoqda...")
        document = FSInputFile(pg_backup_file)
        await bot.send_document(OWNER_ID, document=document)
        os.remove(pg_backup_file)  # Faylni yuborilgandan so'ng o'chirish
    else:
        await send_telegram_message("❌ PostgreSQL backup yaratishda xatolik yuz berdi!")

    # Media backup
    media_zip_file = zip_media_folder()
    if media_zip_file:
        await send_telegram_message("✅ Media backup tayyor! Fayl jo‘natilmoqda...")
        document = FSInputFile(media_zip_file)
        await bot.send_document(OWNER_ID, document=document)
        os.remove(media_zip_file)  # Faylni yuborilgandan so'ng o'chirish
    else:
        await send_telegram_message("❌ Media backup yaratishda xatolik yuz berdi!")


@dp.message(Command("backup"))
async def manual_backup(message: types.Message):
    """Darhol backup yaratish (PostgreSQL + Media)"""
    if message.from_user.id == OWNER_ID:
        await message.reply("📌 PostgreSQL va Media backup jarayoni boshlandi...")

        # PostgreSQL backup
        pg_backup_file = create_backup()
        if pg_backup_file:
            document = FSInputFile(pg_backup_file)
            await message.reply_document(document, caption="✅ PostgreSQL backup tayyor!")
            os.remove(pg_backup_file)  # Faylni yuborilgandan so'ng o'chirish
        else:
            await message.reply("❌ PostgreSQL backup yaratishda xatolik yuz berdi!")

        # Media backup
        media_zip_file = zip_media_folder()
        if media_zip_file:
            document = FSInputFile(media_zip_file)
            await message.reply_document(document, caption="✅ Media backup tayyor!")
            os.remove(media_zip_file)  # Faylni yuborilgandan so'ng o'chirish
        else:
            await message.reply("❌ Media backup yaratishda xatolik yuz berdi!")
    else:
        await message.reply("❌ Sizda bu buyruqni ishlatish huquqi yo‘q!")


@dp.message(Command("time"))
async def set_backup_time(message: types.Message, state: FSMContext):
    """Foydalanuvchidan backup vaqtini olish"""
    if message.from_user.id == OWNER_ID:
        await message.answer("⏰ Iltimos, backup vaqtini HH:MM formatida kiriting (masalan, 01:00 yoki 23:30):")
        await state.set_state(BackupTimeState.waiting_for_time)
    else:
        await message.answer("❌ Sizda bu buyruqni ishlatish huquqi yo‘q!")


@dp.message(BackupTimeState.waiting_for_time)
async def process_time_input(message: types.Message, state: FSMContext):
    """Foydalanuvchi tomonidan kiritilgan backup vaqtini qabul qilish"""
    global backup_time
    try:
        hours, minutes = map(int, message.text.split(":"))
        if 0 <= hours <= 23 and 0 <= minutes <= 59:
            backup_time = message.text

            # Oldingi backupni olib tashlash va yangisini qo‘shish
            scheduler.remove_all_jobs()

            scheduler.add_job(
                backup_and_send,
                trigger=CronTrigger(hour=hours, minute=minutes, timezone=TASHKENT_TZ),
                id="daily_backup"
            )

            await message.answer(f"✅ Backup har kuni {backup_time} (Toshkent vaqti) da amalga oshiriladi.")
            await state.clear()
        else:
            raise ValueError("Vaqtni to'g'ri kiriting!")
    except ValueError:
        await message.answer("❌ Noto‘g‘ri format! Iltimos, vaqtni HH:MM shaklida kiriting.")


async def main():
    """Botni ishga tushirish"""
    try:
        # Default 01:00 da backup qilish
        scheduler.add_job(
            backup_and_send,
            "cron",
            hour=1,
            minute=0,
            timezone=TASHKENT_TZ
        )
        scheduler.start()
        await send_telegram_message("✅ Bot ishga tushdi va backup tizimi faollashtirildi!")
    except Exception as e:
        await send_telegram_message(f"❌ Scheduler ishga tushirishda xatolik: {e}")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
