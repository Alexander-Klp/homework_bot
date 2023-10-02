<h1>python telegram bot</h1>
<img src="https://pictures.s3.yandex.net/resources/Untitled_1668986958.png">
<p>python telegram bot - это бот телеграмм,  который обращается к API сервиса Практикум.Домашка и узнает статус вашей домашней работы: взята ли ваша домашка в ревью, проверена ли она, а если проверена — то принял её ревьюер или вернул на доработку.
</p>

<h2>Как бот работает</h2>
<ul>
  <li><p>раз в 10 минут опрашивает API сервиса Практикум.Домашка и проверяет статус отправленной на ревью домашней работы.</p>
  </lo>
  <li><p>при обновлении статуса анализирует ответ API и отправляет вам соответствующее уведомление в Telegram.</p>
  </li>
  <li><p>логирует свою работу и сообщать вам о важных проблемах сообщением в Telegram.</p>
 
</ul>
<h2>Установка и настройка</h2>
  <p>Чтобы развернуть проект локально, cклонируйте проект:</p>
  <blockquote>git clone git@github.com:Alexander-Klp/homework_bot.git
  </blockquote>
  <p>Установите зависимости из файла requirements.txt:</p>
  <blockquote>pip install -r requirements.txt </blockquote>
  <p>Создайте файл .env в корневой папке проекта и добавьте в него следующие переменные окружения:</p>
  <blockquote>TELEGRAM_TOKEN=ваш_токен_телеграм
              PRACTICUM_TOKEN=ваш_токен_практикума
              TELEGRAM_CHAT_ID=ваш_ID_чата_телеграм 
              </blockquote>
  <p><ul>
        <li>TELEGRAM_TOKEN - токен вашего бота в Telegram.</li>
        <li>PRACTICUM_TOKEN - токен API Practicum.</li>
        <li>TELEGRAM_CHAT_ID - ID чата в Telegram, куда будут отправляться уведомления.</li>
      </ul>
   </p>
  <p>Запустите бота</p>
  <blockquote>python homework.py </blockquote>

<h2>Использования</h2>
<p>При первом запуске бот выдаст статус последней домашней работы и раз в 10 минут будет мониторить изменение статуса. Если статус изменится, вы получите уведомление в Telegram.</p>


<h2>Автор</h2>
<p>Проект "Блогикум" был разработан <a href="https://github.com/Alexander-Klp">студентом</a> школы <a href="https://practicum.yandex.ru/">Яндекс.Практикум</a>
</p>
<p>Проверен Михой Душнилой =)</p>
