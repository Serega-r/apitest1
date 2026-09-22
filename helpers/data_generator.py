from faker import Faker

fake = Faker()


def generate_user():
    return {
        "email": fake.email(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "phone": fake.phone_number(),
        "password": fake.password(length=12)
    }