import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup
from make_card import writer_func
import os
from config import token

# Set up logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Set up reply keyboard
language = ReplyKeyboardMarkup(resize_keyboard=True)
language.add('Russian', 'English')


class UserState(StatesGroup):
    language = State()
    fullname = State()
    company = State()
    phone = State()
    email = State()
    site = State()
    address = State()
    job = State()


# Start command handler
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await UserState.language.set()
    await message.answer('Выберите язык: ', reply_markup=language)


@dp.errors_handler()
async def my_error_handler(update, exception):
    logging.exception("An error occurred: %s", exception)
    return True


@dp.message_handler(state=UserState.language)
async def choose_language(message: types.Message, state: FSMContext):
    if message.text not in ['Russian', 'English']:
        await message.answer('Пожалуйста, выберите язык!')
        return

    async with state.proxy() as data:
        data['language'] = message.text

    await UserState.next()
    welcome_msg = "Добро пожаловать в нашего бота! Введите изображение вашего логотипа: " if data['language'] == 'Russian' else "Welcome to our bot! Enter your fullname: "
    await message.answer(welcome_msg)


@dp.message_handler(state=UserState.fullname)
async def get_fullname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['fullname'] = message.text

    await UserState.next()
    await message.answer(
        'Введите название вашей компании: ' if data['language'] == 'Russian' else 'Enter your company name: ')


@dp.message_handler(state=UserState.company)
async def get_company(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['company'] = message.text

    await UserState.next()
    await message.answer('Введите ваш номер телефона: ' if data['language'] == 'Russian' else 'Enter your phone number: ')


@dp.message_handler(state=UserState.phone)
async def get_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone'] = message.text

    await UserState.next()
    await message.answer('Введите вашу email: ' if data['language'] == 'Russian' else 'Enter your email: ')

@dp.message_handler(state=UserState.email)
async def get_phone(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['email'] = message.text

    await UserState.next()
    await message.answer('Введите вашу site: ' if data['language'] == 'Russian' else 'Enter your site: ')


@dp.message_handler(state=UserState.site)
async def get_email(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['site'] = message.text
    await UserState.next()
    await message.answer('Введите вашу address: ' if data['language'] == 'Russian' else 'Enter your address: ')

@dp.message_handler(state=UserState.address)
async def get_email(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = message.text
    await UserState.next()
    await message.answer('Введите вашу job: ' if data['language'] == 'Russian' else 'Enter your job: ')

@dp.message_handler(state=UserState.job)
async def get_job(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['job'] = message.text


        # (fullname, job, phone, email, site, address, company):

        writer_func(data['fullname'], data['job'], data['phone'], data['email'], data['site'], data['address'], data['company'])

        with open(f'media/{data["fullname"]}1.png', 'rb') as img_file1:
            await message.answer_photo(img_file1)

        with open(f'media/{data["fullname"]}2.png', 'rb') as img_file2:
            await message.answer_photo(img_file2)

        thank_you_msg = 'Спасибо за информацию!' if data['language'] == 'Russian' else 'Thank you for your information!'
        await message.answer(thank_you_msg)
        # os.system(f"rm -r {data['fullname']}1.png")
        # os.system(f"rm -r {data['fullname']}2.png")
    await state.finish()




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
