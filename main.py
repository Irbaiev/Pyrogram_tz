import asyncio
from sqlalchemy import create_engine, Column, Integer, String, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from pyrogram import Client, filters, types
from loguru import logger
from configparser import ConfigParser

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(Integer, unique=True)
    registered_at = Column(DateTime, default=datetime.utcnow)
    message_history = Column(String, default="")


engine = create_engine("sqlite:///userbot.db")
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

config = ConfigParser()
config.read("config.ini")

api_id = config.get("pyrogram", "api_id")
api_hash = config.get("pyrogram", "api_hash")

app = Client("my_account", api_id, api_hash)


async def send_message(chat_id, text):
    try:
        sent_message = await app.send_message(chat_id=chat_id, text=text)
        logger.info(f"Sent message: {sent_message.message_id}, Text: {text}")
    except Exception as e:
        logger.error(f"Error sending message: {e}")


async def check_user(user_id):
    session = Session()
    user = session.query(User).filter_by(telegram_id=user_id).first()
    if not user:
        new_user = User(telegram_id=user_id)
        session.add(new_user)
        session.commit()


async def start_funnel(chat_id):
    await asyncio.sleep(5)
    sent_message = await app.send_message(chat_id, "Добрый день!")

    logger.info(f"Отправлено сообщение {chat_id}: Добрый день!")

    await asyncio.sleep(10)
    sent_message = await app.send_message(chat_id, "Подготовил для вас материал")

    logger.info(f"Отправлено сообщение {chat_id}: Подготовил для вас материал")

    sent_message = await app.send_photo(
        chat_id,
        "https://wl-adme.cf.tsp.li/resize/728x/webp/b08/221/c63ec85c10a9b1c2ff00ccb952.jpg.webp",
    )

    logger.info(f"Отправлено фото {chat_id}")

    await asyncio.sleep(10)

    session = Session()
    user = session.query(User).filter_by(telegram_id=chat_id).first()
    if not user or "Хорошего дня" not in user.message_history:
        sent_message = await app.send_message(
            chat_id, "Скоро вернусь с новым материалом!"
        )

        logger.info(
            f"Отправлено сообщение {chat_id}: Скоро вернусь с новым материалом!"
        )


@app.on_message(filters=filters.private & filters.command("users_today"))
async def users_today_command(_, message):
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    session = Session()
    today_users_count = (
        session.query(func.count(User.id))
        .filter(User.registered_at >= today_start)
        .scalar()
    )

    sent_message = await app.send_message(
        message.chat.id,
        f"Зарегистрированных пользователей сегодня: {today_users_count}",
    )

    logger.info(
        f"Отправлено сообщение: {sent_message.message_id if hasattr(sent_message, 'message_id') else 'N/A'}, "
        f"Text: Зарегистрированных пользователей сегодня: {today_users_count}"
    )


@app.on_message(filters=filters.private)
async def handle_messages(_, message):
    user_id = message.from_user.id
    text = message.text

    logger.info(f"Получено сообщение от пользователя {user_id}: {text}")

    await check_user(user_id)

    session = Session()
    user = session.query(User).filter_by(telegram_id=user_id).first()
    if user:
        new_history = user.message_history + f" {text}"
        user.message_history = new_history
        session.commit()

        if "Хорошего дня" not in new_history:
            await start_funnel(message.chat.id)

    logger.info(f"Сообщение обработано: {text}")


app.run()
