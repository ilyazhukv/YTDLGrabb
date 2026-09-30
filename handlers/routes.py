import os

import imageio_ffmpeg
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile, KeyboardButton, Message, ReplyKeyboardMarkup
from yt_dlp import YoutubeDL

from forms.url import UrlForm

router = Router()

ydl_opts = {
    "ffmpeg_location": imageio_ffmpeg.get_ffmpeg_exe(),
    "outtmpl": "outtmpl/%(id)s.%(ext)s",
    "format": "bestvideo+bestaudio/best",
    "merge_output_format": "mp4"
}

def get_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Download Video")]],
        resize_keyboard=True
    )
    return keyboard

@router.message(Command("start"))
@router.message(F.text == "Download Video")
async def download_v(message: Message, state: FSMContext):
    await message.answer("Write the url video:", reply_markup=get_reply_keyboard())
    await state.set_state(UrlForm.url)

@router.message(UrlForm.url, F.text)
async def proccess_download(message: Message, state: FSMContext):
    await state.update_data(url=message.text)
    data = await state.get_data()
    url = data["url"]

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url=url, download=True)
        video_id = f"{info.get("id")}.{info.get("ext")}"

    file_path = f"outtmpl/{video_id}"
    file_size = os.path.getsize(file_path)

    if file_size > 48 * 1024 * 1024:
        await message.answer("Sorry, the Telegram bot cannot send files larger than 50 MB.")
        os.remove(file_path)
    else:
        video_file = FSInputFile(file_path)
        await message.answer_video(video=video_file)
        os.remove(file_path)
