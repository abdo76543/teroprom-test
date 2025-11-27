from abc import ABC, abstractmethod
import requests
import time


class APIClientError(Exception):
    pass


class APIServerError(Exception):
    pass


class APIClientTimeoutError(Exception):
    pass


class APIClientRateLimitError(Exception):
    pass


class APIClientUndefinedError(Exception):
    pass


class IAPIClient(ABC):
    @abstractmethod
    def get_timeout(self) -> dict:
        """
        URL = "https://www.fruityvice.com/api/fruit/apple"
        Соединения свыше 5 секунд должны быть прерваны и вызвать исключение APIClientTimeoutError.
        """

    @abstractmethod
    def get_rate_limit(self) -> dict:
        """
        URL = "https://api.dictionaryapi.dev/api/v2/entries/en/hello"
        Ограничение: 30 запросов за 10 секунд.
        При превышении возвращает ошибку 429. Повторять до 5 раз.
        """

    @abstractmethod
    def get_client_error(self) -> dict:
        """
        URL = "https://httpbin.org/status/400"
        При ошибке 400 вызвать APIClientError.
        """

    @abstractmethod
    def get_server_error(self) -> dict:
        """
        URL = "https://httpbin.org/status/500"
        При ошибке 500 вызвать APIServerError.
        """


class APIClient(IAPIClient):
    def get_timeout(self) -> dict:
        url = "https://www.fruityvice.com/api/fruit/apple"
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.Timeout:
            raise APIClientTimeoutError("Запрос превысил 5 секунд")
        except requests.RequestException as e:
            raise APIClientUndefinedError(f"Неопределенная ошибка: {e}")

    def get_rate_limit(self) -> dict:
        url = "https://api.dictionaryapi.dev/api/v2/entries/en/hello"
        retries = 5
        for attempt in range(retries):
            try:
                response = requests.get(url)
                if response.status_code == 429:
                    time.sleep(0.5)  # ждём перед повтором
                    continue
                response.raise_for_status()
                return response.json()
            except requests.RequestException as e:
                if attempt == retries - 1:
                    raise APIClientUndefinedError(f"Неопределенная ошибка: {e}")
                time.sleep(0.5)

    def get_client_error(self) -> dict:
        url = "https://httpbin.org/status/400"
        try:
            response = requests.get(url)
            if response.status_code == 400:
                raise APIClientError("Ошибка клиента 400")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise APIClientUndefinedError(f"Неопределенная ошибка: {e}")

    def get_server_error(self) -> dict:
        url = "https://httpbin.org/status/500"
        try:
            response = requests.get(url)
            if response.status_code == 500:
                raise APIServerError("Ошибка сервера 500")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise APIClientUndefinedError(f"Неопределенная ошибка: {e}")
