import json
from uuid import uuid4
from datetime import datetime

class PaymentSystem:
    def __init__(self, transactions="transaction.txt"):
        self.users = {}
        self.transactions = transactions

    def regist_user(self, name):
        user_id = str(uuid4())[:7]
        self.users[user_id] = {"name": name, "balance": 200.0}
        return user_id

    def send_money(self, from_who_id, to_who_id, amount):
        if from_who_id not in self.users or to_who_id not in self.users:
            print("❌ОШИБКА! Операция не прошла. Причина: данных нет в базе.")
            return False
        if self.users[from_who_id]["balance"] < float(amount):
            print("❌ОШИБКА! Операция не прошла. Причина: недостаточно средств.")
            return False

        self.users[from_who_id]["balance"] -= float(amount)
        self.users[to_who_id]["balance"] += float(amount)

        with open(self.transactions, "a") as file:
            file.write(f"От кого: {from_who_id}\nКому: {to_who_id}\nСумма: {amount}\nДата: {datetime.now()}")

        print("✔️Перевод успешно прошел! История сохранилась")

    def show_db(self):
        return self.users

if __name__ == '__main__':
    ps = PaymentSystem()
    while True:
        choice = input("Выберите действие:\n1)Зарегестрироваться\n2)Отправить деньги\n")
        if choice == "1":
            name_ch = input("Введите ваше имя:")
            user_id = ps.regist_user(name_ch)
            print(f"✔️Пользователь успешно создан. Ваш ID: {ps.regist_user(name_ch)}")
        elif choice == "2":
             sender = input("Напишите ваш ID:")
             recipient = input("Напишите ID получателя:")
             try:
                 amount = float(input("Введите сумму:"))
             except ValueError:
                 print("❌Ошибка! Сумма должна быть числом!")

             ps.send_money(sender, recipient, amount)

        elif choice == "база":
            print(ps.show_db())
        elif choice == "выйти":
            break
        else:
            print("❌Неверная команда")
