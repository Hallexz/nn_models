from fastapi import FastAPI
from routers import users, posts

app = FastAPI()

app.include_router(users.router)
app.include_router(posts.router)

'''
1. Регистрация нового пользователя:
   - Метод: POST
   - Путь: /users/
   - Описание: Позволяет зарегистрировать нового пользователя в системе.
   - Параметры запроса: Объект User с полями username, email и password.
   - Возвращаемый результат: Созданный объект пользователя без пароля.

2. Получение пользователя по ID:
   - Метод: GET
   - Путь: /users/{user_id}
   - Описание: Позволяет получить информацию о пользователе по его ID.
   - Параметры запроса: user_id - ID пользователя.
   - Возвращаемый результат: Объект пользователя без пароля.

3. Создание нового поста:
   - Метод: POST
   - Путь: /posts/
   - Описание: Позволяет создать новый пост.
   - Параметры запроса: Объект Post с полями user_id, text и необязательными полями media, likes, comments и reposts.
   - Возвращаемый результат: Созданный объект поста.

4. Получение списка всех постов:
   - Метод: GET
   - Путь: /posts/
   - Описание: Позволяет получить список всех постов.
   - Возвращаемый результат: Список объектов постов.

5. Получение поста по ID:
   - Метод: GET
   - Путь: /posts/{post_id}
   - Описание: Позволяет получить информацию о посте по его ID.
   - Параметры запроса: post_id - ID поста.
   - Возвращаемый результат: Объект поста.

6. Обновление поста:
   - Метод: PUT
   - Путь: /posts/{post_id}
   - Описание: Позволяет обновить информацию о посте.
   - Параметры запроса: post_id - ID поста, объект Post с обновленными полями.
   - Возвращаемый результат: Обновленный объект поста.

7. Удаление поста:
   - Метод: DELETE
   - Путь: /posts/{post_id}
   - Описание: Позволяет удалить пост по его ID.
   - Параметры запроса: post_id - ID поста.
   - Возвращаемый результат: Сообщение об успешном удалении поста.

8. Лайк поста:
   - Метод: POST
   - Путь: /posts/{post_id}/like/{user_id}
   - Описание: Позволяет пользователю поставить лайк на пост или убрать лайк, если он уже поставлен.
   - Параметры запроса: post_id - ID поста, user_id - ID пользователя.
   - Возвращаемый результат: Обновленный объект поста.

9. Добавление комментария к посту:
   - Метод: POST
   - Путь: /posts/{post_id}/comment
   - Описание: Позволяет добавить комментарий к посту.
   - Параметры запроса: post_id - ID поста, объект Comment с полями user_id и text.
   - Возвращаемый результат: Обновленный объект поста.

10. Репост поста:
    - Метод: POST
    - Путь: /posts/{post_id}/repost/{user_id}
    - Описание: Позволяет сделать репост поста.
    - Параметры запроса: post_id - ID поста, user_id - ID пользователя, который делает репост.
    - Возвращаемый результат: Обновленный объект исходного поста.

11. Загрузка медиафайла:
    - Метод: POST
    - Путь: /posts/{post_id}/media
    - Описание: Позволяет загрузить медиафайл (изображение, видео) и прикрепить его к посту.
    - Параметры запроса: post_id - ID поста, file - загружаемый файл.
    - Возвращаемый результат: Обновленный объект поста с добавленным путем к медиафайлу.

12. Получение списка постов пользователя:
    - Метод: GET
    - Путь: /users/{user_id}/posts
    - Описание: Позволяет получить список всех постов конкретного пользователя.
    - Параметры запроса: user_id - ID пользователя.
    - Возвращаемый результат: Список объектов постов пользователя.

13. Подписка на пользователя:
    - Метод: POST
    - Путь: /users/{user_id}/follow/{follower_id}
    - Описание: Позволяет одному пользователю подписаться на другого пользователя.
    - Параметры запроса: user_id - ID пользователя, на которого подписываются, follower_id - ID пользователя, который подписывается.
    - Возвращаемый результат: Обновленный объект пользователя, на которого подписались.

14. Отписка от пользователя:
    - Метод: POST
    - Путь: /users/{user_id}/unfollow/{follower_id}
    - Описание: Позволяет одному пользователю отписаться от другого пользователя.
    - Параметры запроса: user_id - ID пользователя, от которого отписываются, follower_id - ID пользователя, который отписывается.
    - Возвращаемый результат: Обновленный объект пользователя, от которого отписались.
'''