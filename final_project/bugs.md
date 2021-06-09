### Баги / ошибки:
 * В личном кабинете загружается отсутствующий ресурс findMeError.js
 * При регистрации с двумя и более некорректными параметрами ответ от сервера не обрабатывается и пользователь видит что-то подобное 
   ```    
    {'username': ['Incorrect username length'], 'email': ['Incorrect email length', 'Invalid email address']}
    {'email': ['Invalid email address'], 'password': ['Passwords must match']}
   ```
 * При создании пользователя с одинаковым email возникает ошибка `Internal error`:
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
 * При создании пользователя с повторяющимся логином HTTP код ответа - 409
   ```
    test_app_1  | 172.18.0.1 - - [01/Jun/2021 15:37:38] "POST /reg HTTP/1.1" 409 -
   ```
 * При создании пользователя с паролем, длиной больше чем 255, возникает ошибка `Internal error`:
   ```
    test_app_1  | 01.06.2021 16:28:37.155 - app - ERROR - Can not create user: BCMOozz, err: (pymysql.err.DataError) (1406, "Data too long for column 'password' at row 1")
    test_app_1  | [SQL: INSERT INTO test_users (username, password, email, access, active, start_active_time) VALUES (%(username)s, %(password)s, %(email)s, %(access)s, %(active)s, %(start_active_time)s)]
    test_app_1  | [parameters: {'username': 'BCMOozz', 'password': 'ETH*NDdef0II$+0c5q*HdkxKJMuVh6jEX)^h!getBd+R%tfDNhmF&)wq90$$U4E7I3528x5RgCjDYR@^7R)4WnX24i_k$Ao%H6KDt7_yA7KhgA(hcUk_nJzOqC0fFxJ+y@swWmY5AnqwZSBG4Pu9EXocwa_2Yc1Lh*8TA#nf$&^V@B@V$hFIxgk4P_rw6&C8iq!Ch4y^uQ&tCBgxNj4V)BbgJ&ceh3x%N!F9N#2Zgc3189J4tcM_RgzADFvgH(B+', 'email': 'pnicholson@beck.com', 'access': '1', 'active': '0', 'start_active_time': None}]
    test_app_1  | (Background on this error at: http://sqlalche.me/e/9h9h)
    test_app_1  | 01.06.2021 16:28:37.155 - app - ERROR - /reg err: 'bool' object has no attribute 'is_active'
    test_app_1  | 172.18.0.1 - - [01/Jun/2021 16:28:37] "POST /reg HTTP/1.1" 500 -
   ```
 * Время в приложении для UI = UTF+0, API = UTF+3
 * `POST /api/add_user` возвращает `210 UNKNOWN`, ожидается `201 Created`; пользователь в бд создаётся при корректных данных. При некорректных данных ошибка `210`, хотя должна быть `401`
 * UI ошибка — после появления ошибки форма не меняет свой размер обратно
 * При добавлении пользователя с email, длиной <= 5, через API `POST /api/add_user` пользователь добавляется в базу данных ?(В UI форме пользователь не добавляется и появляется ошибка `Incorrect email length`)
 * При блокировании пользователя с использованием остальных HTTP методов — ответ `200` и пользователь блокируется. Ожидается `405` и пользователь не блокируется 