### Баги / ошибки:
 * В личном кабинете загружается отсутствующий ресурс findMeError.js
   ```
   test_app_1  | 172.25.0.6 - - [10/Jun/2021 14:00:14] "GET /static/scripts/findMeError.js HTTP/1.10m" 404 -
   ```
 * При регистрации с двумя и более некорректными параметрами ответ от сервера не обрабатывается и пользователь видит что-то подобное 
   ```    
    {'username': ['Incorrect username length'], 'email': ['Incorrect email length', 'Invalid email address']}
    {'email': ['Invalid email address'], 'password': ['Passwords must match']}
   ```
 * При создании пользователя с одинаковым email возникает ошибка `Internal error` `test_create_user_with_existing_email`:
   ```
    test_app_1  | 01.06.2021 12:06:25.749 - app - ERROR - /reg err: 'bool' object has no attribute 'is_active'
    test_app_1  | 172.18.0.1 - - [01/Jun/2021 12:06:25] "POST /reg HTTP/1.1" 500 -
   ```
   docker logs
   ```
   test_app_1  | 08.06.2021 08:19:40.323 - app - ERROR - Can not create user: admin1, err: (pymysql.err.IntegrityError) (1062, "Duplicate entry '123@gmail.com' for key 'email'")
   test_app_1  | [SQL: INSERT INTO test_users (username, password, email, access, active, start_active_time) VALUES (%(username)s, %(password)s, %(email)s, %(access)s, %(active)s, %(start_active_time)s)]
   test_app_1  | [parameters: {'username': 'admin1', 'password': '123', 'email': '123@gmail.com', 'access': '1', 'active': '0', 'start_active_time': None}]
   test_app_1  | (Background on this error at: http://sqlalche.me/e/gkpj)
   test_app_1  | 08.06.2021 08:19:40.323 - app - ERROR - /reg err: 'bool' object has no attribute 'is_active'
   test_app_1  | 172.20.0.1 - - [08/Jun/2021 08:19:40] "POST /reg HTTP/1.1" 500 -
   ```
 * При создании пользователя с повторяющимся логином HTTP код ответа - 409 `test_create_user_with_existing_name`
   ```
    test_app_1  | 172.18.0.1 - - [01/Jun/2021 15:37:38] "POST /reg HTTP/1.1" 409 -
   ```
 * При создании пользователя с паролем, длиной больше чем 255, возникает ошибка `Internal error` `test_input_data_len_negative[password_long]`:
   ```
    test_app_1  | 01.06.2021 16:28:37.155 - app - ERROR - Can not create user: BCMOozz, err: (pymysql.err.DataError) (1406, "Data too long for column 'password' at row 1")
    test_app_1  | [SQL: INSERT INTO test_users (username, password, email, access, active, start_active_time) VALUES (%(username)s, %(password)s, %(email)s, %(access)s, %(active)s, %(start_active_time)s)]
    test_app_1  | [parameters: {'username': 'BCMOozz', 'password': 'ETH*NDdef0II$+0c5q*HdkxKJMuVh6jEX)^h!getBd+R%tfDNhmF&)wq90$$U4E7I3528x5RgCjDYR@^7R)4WnX24i_k$Ao%H6KDt7_yA7KhgA(hcUk_nJzOqC0fFxJ+y@swWmY5AnqwZSBG4Pu9EXocwa_2Yc1Lh*8TA#nf$&^V@B@V$hFIxgk4P_rw6&C8iq!Ch4y^uQ&tCBgxNj4V)BbgJ&ceh3x%N!F9N#2Zgc3189J4tcM_RgzADFvgH(B+', 'email': 'pnicholson@beck.com', 'access': '1', 'active': '0', 'start_active_time': None}]
    test_app_1  | (Background on this error at: http://sqlalche.me/e/9h9h)
    test_app_1  | 01.06.2021 16:28:37.155 - app - ERROR - /reg err: 'bool' object has no attribute 'is_active'
    test_app_1  | 172.18.0.1 - - [01/Jun/2021 16:28:37] "POST /reg HTTP/1.1" 500 -
   ```
 * UI ошибка — после появления ошибки форма не меняет свой размер обратно
 * При создании пользователя через UI с корректными данными флаг `active != 1` `test_create_user_correct`
 * При логгировании время в образе приложения фиксировано UTF+0, если на локальной машине запускать в docker-compose получаем рассинхронизацию (может быть неудобно для отладки)
 * `POST /api/add_user` возвращает `210 UNKNOWN`, ожидается `201 Created`; пользователь в бд создаётся при корректных данных. `test_add_user` 
 * `POST /api/add_user` при некорректных данных ошибка `210 UNKNOWN`, хотя должна быть `401` `test_invalid_data`
 * `POST /api/add_user` при добавлении пользователя с email, длиной <= 5, пользователь добавляется в базу данных `test_invalid_data[email_short]`. ?(В UI форме пользователь не добавляется и появляется ошибка `Incorrect email length`)
 * `POST /api/add_user` при добавлении пользователя с повторяющимся email ожидается ответ `304`, а не `210`. `test_duplicate_email`
 * `POST /api/add_user` при запросе методом `OPTIONS` возвращается статус код `200` вместо `405`. `test_invalid_method[OPTIONS]`
 * `POST /api/add_user` при запросе с невалидными `headers` возвращается статус код `210` вместо `400`. `test_invalid_headers`
 * `POST /api/block_user` разрешены методы кроме `GET`, ответ `200` вместо `405`. `test_invalid_methods`
 * `POST /api/accept_user` разрешены методы кроме `GET`, ответ `200` вместо `405`. `test_invalid_methods`
 * `POST /api/delete_user` разрешены методы кроме `GET`, ответ `200` вместо `405`. `test_invalid_methods`
