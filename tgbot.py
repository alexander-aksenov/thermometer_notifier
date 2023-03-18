import asyncio

from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, JobQueue, filters

class TgBot:
    def __init__(self, app, loop, data_storage):
        self.__app = app
        self.__async_loop = loop
        self.__ds = data_storage
        self.__context = None
        self.__chat_id = None
        self.__message = None

    @classmethod
    def create(cls, token, data_storage):
        # Create loop for the thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        app = Application.builder().token(token).build()
        res = cls(app, asyncio.new_event_loop(), data_storage)
        res.add_handlers()
        return res

    def run(self):
        self.__app.run_polling()

    def send_temperature(self):
        if self.__context is None:
            return
        if self.__message:
            return
        time = self.__ds.time
        temperature = "%.1f" % self.__ds.temperature
        write_str = "Temperature needs your attention: " + str(time) + " - " + str(temperature) + "°"
        self.__message = write_str
        self.__job_queue.run_once(self._send_message, 1, chat_id=self.__chat_id)

    def _remove_job_if_exists(name, context):
        jobs = context.get_jobs_by_name(name)
        for job in jobs:
            job.schedule_removal()

    async def _send_message(self, context):
        # TODO: fix races
        if self.__message:
            msg = self.__message
            self.__message = None
            await self.__context.bot.send_message(self.__chat_id, text=msg)

    async def _start(self, update, context):
        if self.__context:
            out_str = "Sorry, user already assigned for this session, you cannot use it"
        else:
            self.__context = context
            self.__chat_id = update.effective_message.chat_id
            self.__job_queue = context.job_queue
            out_str = "Welcome, you'll receive here news about temerature changes"

        user = update.effective_user

        await update.message.reply_html(
                rf"Hi {user.mention_html()}! " + out_str,
                reply_markup=ForceReply(selective=True),
        )

    async def _temperature(self, update, context):
        time = self.__ds.time
        temperature = "%.1f" % self.__ds.temperature
        humidity = "%.1f" % self.__ds.humidity
        write_str = str(time) + ": " + str(temperature) + "° " + str(humidity) + "%"
        await update.message.reply_text(write_str)

    async def _graphic(self, update, context):
        await update.message.reply_text("Sorry, not yet implemented")


    def add_handlers(self):
        self.__app.add_handler(CommandHandler('start', self._start))
        self.__app.add_handler(CommandHandler('temperature', self._temperature))
        self.__app.add_handler(CommandHandler('graph', self._graphic))
