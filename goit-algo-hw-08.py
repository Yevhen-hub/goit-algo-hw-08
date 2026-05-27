from collections import UserDict
import pickle


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError("Номер телефону повинен містити рівно 10 цифр.")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                self.phones.remove(p)
                return
        raise ValueError("Телефон не знайдено.")

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                p.value = Phone(new_phone).value
                return
        raise ValueError("Телефон не знайдено.")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def __str__(self):
        phones = "; ".join(phone.value for phone in self.phones)
        return f"Ім'я: {self.name.value}, телефони: {phones}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]


def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as file:
        pickle.dump(book, file)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as file:
            return pickle.load(file)
    except FileNotFoundError:
        return AddressBook()


def input_error(func):
    def inner(*args):
        try:
            return func(*args)
        except ValueError as error:
            return str(error)
        except IndexError:
            return "Будь ласка, введіть ім'я та номер телефону."
        except KeyError:
            return "Контакт не знайдено."

    return inner


@input_error
def add_contact(args, book):
    name, phone = args

    record = book.find(name)

    if record is None:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
        return "Контакт успішно додано."

    record.add_phone(phone)
    return "Телефон успішно додано."


@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args

    record = book.find(name)

    if record is None:
        raise KeyError

    record.edit_phone(old_phone, new_phone)

    return "Номер телефону успішно змінено."


@input_error
def show_phone(args, book):
    name = args[0]

    record = book.find(name)

    if record is None:
        raise KeyError

    return "; ".join(phone.value for phone in record.phones)


def show_all(book):
    if not book.data:
        return "Адресна книга порожня."

    return "\n".join(str(record) for record in book.data.values())


def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.lower().strip()
    return cmd, args


def main():
    book = load_data()

    print("Ласкаво просимо до бота-помічника!")

    while True:
        user_input = input("Введіть команду: ")

        if not user_input:
            continue

        command, args = parse_input(user_input)

        if command in ["close", "exit"]:
            save_data(book)
            print("До побачення!")
            break

        elif command == "hello":
            print("Чим можу допомогти?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        else:
            print("Невідома команда.")


if __name__ == "__main__":
    main()