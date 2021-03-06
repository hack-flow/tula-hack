import sqlite3


class DataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def add_user(self, name, hash_password):
        try:
            self.__cur.execute(
                f"SELECT COUNT() as `count` FROM users WHERE username LIKE '{name}'"
            )
            res = self.__cur.fetchone()
            if res["count"]:
                print("Пользователь с таким username уже существует")
                return False

            self.__cur.execute(
                "INSERT INTO users VALUES(NULL, ?, ?)", (name, hash_password)
            )
            self.__db.commit()
        except sqlite3.Error as e:
            print("Error server :( " + str(e))
            return False
        return True

    def get_user(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1")
            res = self.__cur.fetchone()
            if not res:
                print("Пользователь не найден")
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))
        return False

    def get_user_by_name(self, name):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE username = '{name}' LIMIT 1")
            res = self.__cur.fetchone()
            print(res)
            if not res:
                print("Пользователь не найден")
                return False
            return res
        except sqlite3.Error as e:
            print("Ошибка получения данных из БД " + str(e))

        return False

    def get_portfolio(self, username: str) -> dict:
        try:
            self.__cur.execute(f"SELECT * FROM portfolio WHERE username={username}")
            general_info = self.__cur.fetchone()

            self.__cur.execute(f"SELECT * FROM contacts WHERE username={username}")
            contacts = self.__cur.fetchone()

            self.__cur.execute(f"SELECT * FROM works WHERE username={username}")
            works = self.__cur.fetchall()

            self.__cur.execute(f"SELECT * FROM awards WHERE username={username}")
            awards = self.__cur.fetchall()

            self.__cur.execute(f"SELECT * FROM projects WHERE username={username}")
            projects = self.__cur.fetchall()

            self.__cur.execute(f"SELECT * FROM main_skills WHERE username={username}")
            main_skills = self.__cur.fetchall()

            self.__cur.execute(f"SELECT * FROM extra_skills WHERE username={username}")
            extra_skills = self.__cur.fetchall()

            self.__cur.execute(f"SELECT * FROM education WHERE username={username}")
            education = self.__cur.fetchone()
        except sqlite3.Error:
            return {}

        return {
            **general_info,
            **contacts,
            **works,
            **awards,
            **projects,
            **main_skills,
            **extra_skills,
            **education,
        }
