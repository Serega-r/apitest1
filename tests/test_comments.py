import allure
import pytest
from helpers.api_client import APIClient
from helpers.auth_helper import register_and_login
from models.schemas import CommentResponse

BASE_URL = "https://archiscope.ru"


@pytest.fixture
def client():
    return APIClient(BASE_URL)


@pytest.fixture
def auth_client(client):
    _, token = register_and_login(client)
    client.session.headers.update({"Authorization": f"Bearer {token}"})
    return client


@pytest.fixture
def news_id(auth_client):
    news_data = {"title": "Новость для коммента", "text": "Текст новости для комментария", "subtitle": "Подзаголовок", "tags": "тест"}
    response = auth_client.post("/api/news/", data=news_data)
    return response.json()["id"]


@allure.epic("Комментарии")
@allure.feature("Создание комментария")
class TestCommentCreate:

    @allure.story("Позитивный: создание комментария")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.positive
    @pytest.mark.comments
    def test_create_comment(self, auth_client, news_id):
        comment_data = {"text": "Это тестовый комментарий"}
        response = auth_client.post(f"/api/news/{news_id}/comments", json=comment_data)

        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"

        data = response.json()
        parsed = CommentResponse(**data)
        assert parsed.text == comment_data["text"]


@allure.epic("Комментарии")
@allure.feature("Получение комментариев")
class TestCommentGet:

    @allure.story("Позитивный: получение комментариев")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.positive
    @pytest.mark.comments
    def test_get_comments(self, client, news_id):
        response = client.get(f"/api/news/{news_id}/comments")

        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"

        data = response.json()
        assert isinstance(data, list)

    @allure.story("Негативный: несуществующая новость")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    @pytest.mark.comments
    def test_get_comments_invalid_news(self, client):
        response = client.get("/api/news/99999999/comments")
        assert response.status_code == 404, f"Ожидался 404, получен {response.status_code}"