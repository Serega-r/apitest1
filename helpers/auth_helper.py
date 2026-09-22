from helpers.data_generator import generate_user


def register_and_login(client):
    user = generate_user()
    client.post("/api/auth/register", json=user)

    response = client.post("/api/auth/login", data={
        "username": user["email"],
        "password": user["password"],
        "grant_type": "password"
    })
    token = response.json()["access_token"]
    return user, token