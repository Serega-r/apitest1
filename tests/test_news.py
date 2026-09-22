import allure
import pytest
from helpers.api_client import APIClient
from helpers.auth_helper import register_and_login
from models.schemas import NewsResponse, TagResponse, PaginatedNewsResponse

BASE_URL = "https://archiscope.ru"


@pytest.fixture
def client():
    return APIClient(BASE_URL)


@pytest.fixture
def auth_client(client):
    _, token = register_and_login(client)
    client.session.headers.update({"Authorization": f"Bearer {token}"})
    return client


@allure.epic("Новости")
@allure.feature("Создание новости")
class TestNewsCreate:

    @allure.story("Позитивный: создание новости без изображения")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.positive
    @pytest.mark.news
    def test_create_news_without_image(self, auth_client):
        news_data = {"title": "Тестовая новость", "text": "Текст тестовой новости для проверки", "subtitle": "Подзаголовок", "tags": "тест, автотест"}
        response = auth_client.post("/api/news/", data=news_data)

        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"

        data = response.json()
        parsed = NewsResponse(**data)
        assert parsed.title == news_data["title"]
        assert parsed.text == news_data["text"]


@allure.epic("Новости")
@allure.feature("Создание новости с изображением")
class TestNewsCreateWithImage:

    @allure.story("Позитивный: создание новости с изображением")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.positive
    @pytest.mark.news
    def test_create_news_with_image(self, auth_client, tmp_path):
        image_path = tmp_path / "test_image.png"
        image_path.write_bytes(b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82')

        with open(image_path, "rb") as f:
            files = {"image": ("test_image.png", f, "image/png")}
            data = {"title": "Новость с картинкой", "text": "Текст новости с изображением", "subtitle": "Подзаголовок", "tags": "тест"}
            response = auth_client.post("/api/news/", data=data, files=files)

        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"

        data = response.json()
        parsed = NewsResponse(**data)
        assert parsed.title == "Новость с картинкой"
        assert parsed.image_path is not None


@allure.epic("Новости")
@allure.feature("Фильтрация новостей")
class TestNewsFilters:

    @allure.story("Позитивный: пагинация")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.positive
    @pytest.mark.news
    def test_news_pagination(self, client):
        response = client.get("/api/news/", params={"page": 1, "per_page": 5})

        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"

        data = response.json()
        parsed = PaginatedNewsResponse(**data)
        assert parsed.page == 1
        assert parsed.per_page == 5

    @allure.story("Позитивный: поиск по тексту")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.positive
    @pytest.mark.news
    def test_news_search(self, client):
        response = client.get("/api/news/", params={"search": "тест"})

        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"

        data = response.json()
        parsed = PaginatedNewsResponse(**data)
        assert parsed.page == 1


@allure.epic("Новости")
@allure.feature("Детализация новости")
class TestNewsDetail:

    @allure.story("Позитивный: получение новости по ID")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.positive
    @pytest.mark.news
    def test_get_news_by_id(self, client):
        response_all = client.get("/api/news/", params={"per_page": 1})
        news_id = response_all.json()["items"][0]["id"]

        response = client.get(f"/api/news/{news_id}")

        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"

        data = response.json()
        parsed = NewsResponse(**data)
        assert parsed.id == news_id

    @allure.story("Негативный: несуществующий ID")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.negative
    @pytest.mark.news
    def test_get_news_invalid_id(self, client):
        response = client.get("/api/news/99999999")

        assert response.status_code == 404, f"Ожидался 404, получен {response.status_code}"


@allure.epic("Новости")
@allure.feature("Получение новостей")
class TestNewsGet:

    @allure.story("Позитивный: получение списка всех новостей")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.positive
    @pytest.mark.news
    def test_get_all_news(self, client):
        response = client.get("/api/news/")

        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"

        data = response.json()
        parsed = PaginatedNewsResponse(**data)
        assert parsed.page == 1
        assert parsed.per_page > 0
        assert parsed.total > 0
        assert len(parsed.items) > 0

    @allure.story("Позитивный: получение всех тегов")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.positive
    @pytest.mark.news
    def test_get_all_tags(self, client):
        response = client.get("/api/news/tags")

        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"

        data = response.json()
        assert isinstance(data, list)git remote add origin https://github.com/ТВОЙ_ЛОГИН/archiscope-api-tests.git