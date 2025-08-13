import json
import os.path
from uuid import uuid4
from datetime import datetime

db = "db.json"

def save_data_to_db(data):
    with open(db, "w") as file:
        json.dump(data, file, indent=4)

def load_data_from_db():
    if os.path.exists(db):
        with open(db, "r") as file:
            return json.load(file)
    return {"users": {}}

class PaymentSystem:
    def __init__(self, transactions="transaction.txt"):
        self.db = "db.json"
        self.transactions = transactions
        self.entered = False
        self.current_user = None

    def regist_user(self, name):
        user_id = str(uuid4())[:7]
        data = load_data_from_db()
        data["users"][user_id] = {"name": name, "balance": 200.0}
        save_data_to_db(data)
        return user_id

    def enter_user(self, id):
        data = load_data_from_db()
        if id not in data["users"]:
            print(f"❌ОШИБКА! Пользователя с ID {id} нету в базе. Попробуйте создать аккаунт")
            return False

        print(f"✔️Вы успешно вошли в аккаунт {id}, {data[id]['name']}")
        self.current_user = id
        self.entered = True

    def send_money(self, from_who_id, to_who_id, amount):
        if float(amount) <= 0:
            print("❌ОШИБКА! Сумма перевода должна быть больше нуля")
            return False

        data = load_data_from_db()

        if from_who_id not in data["users"] or to_who_id not in data["users"]:
            print("❌ОШИБКА! Операция не прошла. Причина: данных нет в базе.")
            return False
        if data[from_who_id][id]["balance"] < float(amount):
            print("❌ОШИБКА! Операция не прошла. Причина: недостаточно средств.")
            return False

        data[from_who_id]["balance"] -= float(amount)
        data[to_who_id]["balance"] += float(amount)
        save_data_to_db(data)

        with open(self.transactions, "a") as file:
            file.write(f"[{datetime.now()}] От кого: {from_who_id}\nКому: {to_who_id}\nСумма: {amount}\n")
        print("✔️Перевод успешно прошел! История сохранилась")

    def show_db(self):
        data = load_data_from_db()
        return data

if __name__ == '__main__':
    ps = PaymentSystem()
    while True:
        choice = input("Выберите действие:\n1)Зарегестрироваться\n2)Войти в аккаунт\n3)Отправить деньги\n")
        if choice == "1":
            name_ch = input("Введите ваше имя:")
            user_id = ps.regist_user(name_ch)
            print(f"✔️Пользователь успешно создан. Ваш ID: {ps.regist_user(name_ch)}")
        elif choice == "3":
             sender = input("Напишите ваш ID:")
             recipient = input("Напишите ID получателя:")
             try:
                 amount = float(input("Введите сумму:"))
             except ValueError:
                 print("❌Ошибка! Сумма должна быть числом!")

             ps.send_money(sender, recipient, amount)
        elif choice == "2":
            id = input("Введите ваше ID: ")
            ps.enter_user(id)
            choise1 = input("Выберите действие: 1)Отправить деньги")
            if choise1 == "1":
                sender1 = input("Напишите ваш ID:")
                recipient1 = input("Напишите ID получателя:")
                try:
                    amount1 = float(input("Введите сумму:"))
                except ValueError:
                    print("❌Ошибка! Сумма должна быть числом!")

                ps.send_money(sender1, recipient1, amount1)
        elif choice == "база":
            print(ps.show_db())
        elif choice == "выйти":
            break
        else:
            print("❌Неверная команда")

# 13-08-25
