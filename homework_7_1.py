import re
from datetime import datetime, timedelta


class Field:
    def __init__(self, value):
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not re.match(r'^\d{10}$', value):
            raise ValueError("Phone number must consist of 10 digits")
        self.value = value


class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def add_birthday(self, birthday):
        if self.birthday is not None:
            raise ValueError("Birthday already set")
        self.birthday = Birthday(birthday)

    # Дата народження має бути у форматі DD.MM.YYYY.
    def show_birthday(self):
        if self.birthday:
            return self.birthday.value.strftime("%d.%m.%Y")
        return "Not set"

    def __str__(self):
        phones_str = ", ".join([p.value for p in self.phones])
        birthday_str = self.show_birthday()
        return f"Name: {self.name.value}, Phones: {phones_str}, Birthday: {birthday_str}"


class AddressBook:
    def __init__(self):
        self.contacts = {}

    def add_record(self, record):
        self.contacts[record.name.value] = record

    def get_record(self, name):
        return self.contacts.get(name)

    def find(self, name):
        return self.contacts.get(name)

    #
    # Додайте та адаптуйте до класу AddressBook нашу функцію з четвертого домашнього завдання, тиждень
    # 3, get_upcoming_birthdays, яка для контактів адресної книги повертає список користувачів, яких
    # потрібн привітати по днях на наступному тижні.

    def get_upcoming_birthdays(self):
        today = datetime.today()
        upcoming_birthdays = {}
        for name, record in self.contacts.items():
            if record.birthday:
                bday = record.birthday.value.replace(year=today.year)
                if today <= bday <= today + timedelta(days=7):
                    days_left = (bday - today).days
                    upcoming_birthdays.setdefault(days_left, []).append(name)
        return upcoming_birthdays


# Для перехоплення помилок вводу та виведення відповідного
# повідомлення про помилку використовуємо декоратор @input_error.

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            return str(e)

    return wrapper


#  функція add_contact має два призначення - додавання нового контакту або оновлення телефону для контакту,
# що вже існує в адресній книзі. Параметри функції це список аргументів args та сама адресна книга book.
@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


# Додати дату народження для вказаного контакту.
@input_error
def add_birthday(args, book: AddressBook):
    name, bday = args
    record = book.find(name)
    if record:
        record.add_birthday(bday)
        return f"Birthday {bday} added to contact {name}"
    return f"Contact {name} not found"


# Показати дату народження для вказаного контакту.
@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        return f"Birthday of {name} is {record.show_birthday()}"
    return f"Contact {name} not found"


# Показати дні народження, які відбудуться протягом наступного тижня.
@input_error
def birthdays(args, book: AddressBook):
    upcoming = book.get_upcoming_birthdays()
    result = []
    for days_left, names in sorted(upcoming.items()):
        for name in names:
            result.append(f"{name}: in {days_left} days")
    return "\n".join(result) if result else "No upcoming birthdays"


def parse_input(user_input):
    parts = user_input.strip().split()
    command = parts[0]
    args = parts[1:]
    return command, args


# Функція для зміни номеру телефону для вказаного контакту.
@input_error
def change_phone(args, book: AddressBook):
    name, new_phone = args
    record = book.find(name)
    if record:
        if len(record.phones) > 0:
            record.phones[0].edit_phone(new_phone)
            return f"Phone number for contact {name} changed to {new_phone}"
        else:
            record.add_phone(new_phone)
            return f"Phone number for contact {name} added as {new_phone}"
    return f"Contact {name} not found"

# окрема функція
@input_error
def phone(args, book: AddressBook):
    name = args[0]
    record = book.find(name)
    if record:
        phones = ", ".join(p.value for p in record.phones)
        return f"Phones for {name}: {phones}"
    return f"Contact {name} not found"

# окрема функція
@input_error
def all(book: AddressBook):
    records = [str(record) for record in book.contacts.values()]
    return "\n".join(records)


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command.lower() in ["close", "exit"]:
            print("Goodbye!")
            break

        elif command.lower() == "hello":
            print("How can I help you?")

        elif command.lower() == "add":
            print(add_contact(args, book))

        elif command.lower() == "change":
            print(change_phone(args, book))

        elif command.lower() == "phone":
            print(phone(args, book))

        elif command.lower() == "all":
            print(all(book))

        elif command.lower() == "add-birthday":
            # реалізація
            print(add_birthday(args, book))

        elif command.lower() == "show-birthday":
            # реалізація
            print(show_birthday(args, book))

        elif command.lower() == "birthdays":
            # реалізація
            print(birthdays(args, book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
