####  pip install -r requirement.txt
```sh
mkvirtualenv -p ~/.pyenv/versions/3.6.0/bin/python django-message

https://docs.djangoproject.com/en/2.0/intro/tutorial01/
1.django-admin startproject mysite
2.
```

```sql
(django-message) ➜  mysite git:(master) ✗  python manage.py sqlmigrate msg 0001
BEGIN;
--
-- Create model Message
--
CREATE TABLE "msg_message" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "fromUserId" varchar(60) NOT NULL, "toUserId" varchar(60) NOT NULL, "status" integer NOT NULL, "title" varchar(100) NOT NULL, "Text" varchar(1000) NOT NULL, "isDelete" bool NOT NULL, "createAt" datetime NOT NULL, "updateAt" datetime NOT NULL);
COMMIT;
(django-message) ➜  mysite git:(master) ✗ python manage.py migrate

```


