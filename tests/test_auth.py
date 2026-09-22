import allure
import pytest
from helpers.api_client import APIClient
from helpers.data_generator import generate_user
from models.schemas import UserResponse, Token

BASE_URL = "https://archiscope.ru"


@pytest.fixture
def client():
    return APIClient(BASE_URL)


@allure.epic("Авторизация")
@allure.feature("Регистрация")
class TestRegister:

    @allure.story("Успешная регистрация нового пользователя")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.positive
    @pytest.mark.auth
    def test_register_success(self, client):
        user = generate_user()
        response = client.post("/api/auth/register", json=user)

        assert response.status_code == 200, f"Ожидал 200, получен {response.status_code}"

        data = response.json()
        parsed = UserResponse(**data)
        assert parsed.email == user["email"]
        assert parsed.first_name == user["first_name"]
        assert parsed.last_name == user["last_name"]

    @allure.story("Регистрация с уже существующим email")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    @pytest.mark.auth
    def test_register_existing_email(self, client):
        user = generate_user()
        client.post("/api/auth/register", json=user)
        response = client.post("/api/auth/register", json=user)
        assert response.status_code == 400, f"Ожидал 400, получен {response.status_code}"

    @allure.story("Регистрация с невалидными данными")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    @pytest.mark.auth
    def test_register_invalid_data(self, client):
        invalid_user = {"email": "not-an-email", "first_name": "Test", "last_name": "User", "password": "123"}
        response = client.post("/api/auth/register", json=invalid_user)
        assert response.status_code == 422, f"Ожидал 422, получен {response.status_code}"


@allure.epic("Авторизация")
@allure.feature("Вход в систему")
class TestLogin:

    @allure.story("Успешный вход")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.positive
    @pytest.mark.auth
    def test_login_success(self, client):
        user = generate_user()
        client.post("/api/auth/register", json=user)

        response = client.post("/api/auth/login", data={
            "username": user["email"],
            "password": user["password"],
            "grant_type": "password"
        })

        assert response.status_code == 200, f"Ожидал 200, получен {response.status_code}"

        data = response.json()
        token = Token(**data)
        assert token.access_token
        assert token.token_type == "bearer"

    @allure.story("Вход с неверными учётными данными")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    @pytest.mark.auth
    def test_login_invalid_credentials(self, client):
        response = client.post("/api/auth/login", data={
            "username": "wrong@example.com",
            "password": "wrongpassword",
            "grant_type": "password"
        })

        assert response.status_code == 401, f"Ожидал 401, получен {response.status_code}"