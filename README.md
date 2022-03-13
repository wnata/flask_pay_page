# flask_pay_page
                                                        Тестовое задание python dev API.

Необходимо разработать и реализовать ﬂask сервис. Сервис состоит из одной страницы со следующими элементами:
Сумма оплаты (поле ввода суммы);
Валюта оплаты (выпадающий список со значениями EUR, USD, RUB);
Описание товара (многострочное поле ввода информации);
Оплатить (кнопка);
При нажатии на кнопку “Оплатить”, происходит следующее:
если валюта в выпадающем списке указана “EUR”, то пользователь направляется на страницу оплаты без выбора направления (по протоколу Pay, стр. 3)
если валюта указана “USD”, то осуществляется запрос на выставление счета на оплату по API (метод Bill, стр. 4) в валюте Piastrix. Если получен корректный ответ, пользователь должен перенаправляться на страницу оплаты платёжной системы Piastrix (на url из ответа).
если валюта указана “RUB”, то осуществляется запрос на выставление счета на оплату по API (метод Invoice, стр. 6) с указанием обязательного параметра payway= perfectmoney_usd. Если получен корректный ответ, пользователь должен перенаправляться на страницу оплаты платёжной системы Perfectmoney.

Во всех случаях необходимо предусмотреть логирование работы сервиса и хранение следующей информации: валюта, сумма, время отправки, описание, идентификатор платежа в БД или файл.

Готовое задание выложить на github (или подобный сервис), а приложение задеплоить на heroku или любой другой хостинг.


Параметры для выполнения запросов: 
shop_id = 5 
secretKey = SecretKey01
payway = perfectmoney_usd (для invoice)

Правила формирования подписи (sign)
Строка формируется следующим образом: все обязательные параметры запроса упорядочиваются в алфавитном порядке ключей, значения конкатенируются через знак двоеточие (“:”), в конце добавляется секретный ключ (без знака ":"), от полученной строки генерируется sha256 хеш и его HEX-представление передается в параметре запроса sign.

Для каждого метода свой набор обязательных параметров, также могут передаваться дополнительные параметры, но в формировании подписи они не участвуют.

Пример формирования подписи для запроса invoice.

request = {
	"currency": "643",
	"sign": "07a596eb1dbcb83d5a7b2f1c9572d455af7e71b9ea5c32e3c3892f099ae67ac2",
	"payway": "perfectmoney_usd",
	"amount": "12.34",
	"shop_id": "5",
	"shop_order_id": 4126,
	"description": "Test invoice"
}

Секретный ключ магазина (из настроек магазина):

secret = “SecretKey01”

Список обязательных параметров для запроса invoice:
keys_required = ("shop_id", "payway", "amount", "currency", "shop_order_id")	

Упорядоченные ключи:
keys_sorted = ['amount', 'currency', 'payway', 'shop_id', 'shop_order_id']	

Строка для генерации sha256 хеша имеет вид:
12.34:643:perfectmoney_usd:5:4126SecretKey01	 

HEX-представление хеша:
 07a596eb1dbcb83d5a7b2f1c9572d455af7e71b9ea5c32e3c3892f099ae67ac2 

Для онлайн проверки можно использовать онлайн сервис

http://www.xorbin.com/tools/sha256-hash-calculator

Выставление счета для оплаты через PAY
Для перенаправления плательщика на страницу оплаты, необходимо сформировать и подтвердить HTML-форму.

URL: https://pay.piastrix.com/ru/pay или https://pay.piastrix.com/en/pay
 Метод: POST, GET

Обязательные параметры: amount, currency, shop_id, shop_order_id 

Пример формирования подписи для запроса:
keys_sorted = ['amount', 'currency', 'shop_id', 'shop_order_id']

Строка для генерации sha256 хеша имеет вид: 
10.00:643:5:101SecretKey01

HEX-представление хеша:
 e4580435a252d61ef91b71cb23ed7bee4d77de94ced36411526d2ce3b66ada8f

Пример HTML-формы:

<form name="Pay" method="post" action="https://pay.piastrix.com/ru/pay" accept-charset="UTF-8"> <input type="hidden" name="amount" value="10.00"/> <input type="hidden" name="currency" value="643"/> <input type="hidden" name="shop_id" value="1"/> <input type="hidden" name="sign" value="2a966c9942652c115640f584b101f4124a8c44e9f119b449195beacf539e98b9"/> <input type="hidden" name="shop_order_id" value="101"/>
<input type="submit"/> <input type="hidden" name="description" value="Test invoice"/> </form>



Где,
Параметр
Описание
Формат
shop_id
идентификатор магазина в системе Piastrix
5
amount
сумма выставленного счета
"1.00"
currency
валюта выставленного счета
840 - Доллар США, 643 - Российский рублю, 978 - Евро
description
описание к выставленному счету


shop_order_id
номер счета на стороне магазина
строка до 255 символов. В зависимости от настроек магазина, может проверяться на уникальность
sign
подпись, см. п. Правила формирования подписи (sign)






Выставление счетов для оплаты - в валюте Piastix - bill

URL: https://core.piastrix.com/bill/create
Метод: POST
Content-Type: application/json
Обязательные параметры: shop_amount, shop_currency, shop_id, shop_order_id, payer_currency 


Пример запроса:	
{
	"description": "Test Bill",
	"payer_currency": 643,
	"shop_amount": "23.15",
	"shop_currency": 643,
	"shop_id": "112",
	"shop_order_id": 4239,
	"sign": "ad7fbe8df102bc70e28deddba8b45bb3f4e6cafdaa69ad1ecc0e8b1d4e770575"
}
Где,

Параметр
Описание
Формат
shop_id
идентификатор магазина в системе Piastrix
5
shop_amount
сумма выставленного счета
"1.00"
shop_currency
валюта выставленного счета (зачисления на магазин)
643 - Российский рубль, 840 - Доллар США, 978 - Евро, 980 - Украинская гривна
payer_currency
валюта оплаты плетельщиком (валюта списания с плательщика в системе Piastrix, может отличаться от валюты магазина)
643 - Российский рубль, 840 - Доллар США, 978 - Евро, 980 - Украинская гривна
sign
подпись
a7f5bcbb774cea9d9886cbb3ce2f8731359e356a7d759437b4e9e31da1152109
shop_order_id
номер счета на стороне магазина, формат
строка до 255 символов
description
описание выставленного счета (не обязательный параметр)


payer_account
email или номер счета плательщика на стороне платежной системы Piastrix (не обязательный параметр),
support@piastrix.com или 201494711279



 Пример ответа:
{
	"data": {
		"created": "Wed, 06 Dec 2017 14:30:44 GMT",
		"id": 25,
		"lifetime": 43200,
		"payer_account": null,
		"payer_currency": 643,
		"payer_price": 23.15,
		"shop_amount": 23.15,
		"shop_currency": 643,
		"shop_id": 3,
		"shop_order_id": 4239,
		"shop_refund": 23.15,
		"url": "https://wallet.piastrix.com/ru/bill/pay/WtvoXPzcphd"
	},
	"error_code": 0,
	"message": "Ok",
	"result": true
}
Где,

data – информация по созданному счеты для оплаты
id – уникальный идентификатор счета в системе Piastrix
lifetime – время действия счета для оплаты, в минутах, по умолчанию: 43200 минут
payer_account – аккаунт плательщика, которому выставлен счет для оплаты (если передавался в запросе)
payer_currency – валюта, в которой должен оплатить счет плательщик
payer_price – сумма, которую должен оплатить плательщик для погашения счета
shop_currency – валюта счета, зачисления на магазина
shop_amount – сумма счета, переданная магазином
shop_id – идентификатор магазина
shop_order_id – номер счета на стороне магазина
url – URL на который можно перенаправить пользователя для оплаты счета.



Пример ошибки при выставлении счета:
{
	"data": null,
	"message": "invalid sign",
	"error_code": 1,
	"result": false
}
message – описание ошибки; 
error_code – код ошибки


Выставление счета для других валют - invoice

URL: https://core.piastrix.com/invoice/create
Метод: POST, Content-Type = application/json
Обязательные параметры: amount, currency, payway, shop_id, shop_order_id, sign
 
 
data - source для отправки методом method параметров из data. 
method – метод оправки data на source, формат: POST, GET 
url – URL на который необходимо отправить data методом method 
id – уникальный идентификатор счета в системе Piastrix


Для перенаправления клиента для оплаты выставленного счета, необходимо данную информацию использовать для генерации и подтверждения HTML-формы, например:

<form method="GET" action="https://payeer.com/api/merchant/process.php">
    <input name="lang" value="ru" />
    <input name="m_curorderid" value="68685634"/>
    <input name="m_historyid" value="558274963"/>
    <input name="m_historytm" value="1525080667"/>
    <input name="referer" value=" https://payeer.com/merchant/?m_historyid=558274963&m_historytm=1525080667&m_curorderid=68685634 &lang=ru"/>
    <input type="submit"/>
</form>

Т.е. из ответа invoice необходимо сформировать форму, где method = method, action=url, input = параметры из data

 Пример ошибки при выставлении инвойса:
{
	"data": null,
	"error_code": 4,
	"message": "Payer price amount is too small, min: 1.0",
	"result": false
}


message – описание ошибки; 
error_code – код
