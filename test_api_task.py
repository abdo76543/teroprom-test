import sys
import time
import logging
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))
from tasks.api_task import IAPIClient
from tasks.api_task import APIClientError
from tasks.api_task import APIServerError
from tasks.api_task import APIClientTimeoutError
from tasks.api_task import APIClientUndefinedError
from logger import log


class APIClientTestError(Exception):
    pass


class APIClientTestBackend:
    def __init__(
        self,
        api: IAPIClient,
        log: logging.Logger,
    ) -> None:
        self.api = api
        self.log = log

    def test_get_timeout(self) -> None:
        self.log.debug("Начало теста: test_get_timeout")
        for i in range(100):
            try:
                self.log.debug(f"[{i+1}/100] Отправка запроса get_timeout")
                start = time.time()
                data = self.api.get_timeout()
                end = time.time()
                self.log.debug(f"[{i+1}/100] Время выполнения: {end - start:.2f} сек")
                if end - start > 5:
                    self.log.error(
                        f"[{i+1}/100] Запрос выполняется слишком долго: {end - start:.2f} сек"
                    )
                    raise APIClientTestError(
                        "Запрос выполняется слишком долго. Ожидаемое время выполнения: 5 секунд."
                    )

                if data.get("name") != "Apple":
                    self.log.error(f"[{i+1}/100] Некорректные данные: {data}")
                    raise APIClientTestError(
                        "Некорректные данные. Ожидалось значение: Apple."
                    )

            except APIClientTimeoutError as ex:
                self.log.warning(f"[{i+1}/100] Ошибка таймаута: {ex}")

            except APIClientUndefinedError as ex:
                self.log.warning(f"[{i+1}/100] Неопределенная ошибка: {ex}")

            except Exception as ex:
                raise APIClientTestError("Возникла непредусмотренная ошибка") from ex

    def test_get_rate_limit(self) -> None:
        self.log.debug("Начало теста: test_get_rate_limit")
        for i in range(100):
            try:
                self.log.debug(f"[{i+1}/100] Отправка запроса get_rate_limit")
                data = self.api.get_rate_limit()
                if "hello" not in data[0].get("word"):
                    self.log.error(f"[{i+1}/100] Некорректные данные")
                    raise APIClientTestError(
                        "Некорректные данные. Ожидалось значение: hello."
                    )

            except APIClientUndefinedError as ex:
                self.log.warning(f"[{i+1}/100] Неопределенная ошибка: {ex}")

            except Exception as ex:
                raise APIClientTestError("Возникла непредусмотренная ошибка") from ex

    def test_get_client_error(self) -> None:
        self.log.debug("Начало теста: test_get_client_error")
        for i in range(10):
            try:
                self.log.debug(f"[{i+1}/10] Отправка запроса get_client_error")
                self.api.get_client_error()

            except APIClientError as ex:
                self.log.warning(f"[{i+1}/10] Ошибка клиента: {ex}")

            except APIClientUndefinedError as ex:
                self.log.warning(f"[{i+1}/10] Неопределенная ошибка: {ex}")

            except Exception as ex:
                raise APIClientTestError("Возникла непредусмотренная ошибка") from ex

    def test_get_server_error(self) -> None:
        self.log.debug("Начало теста: test_get_server_error")
        for i in range(10):
            try:
                self.log.debug(f"[{i+1}/10] Отправка запроса get_server_error")
                self.api.get_server_error()

            except APIServerError as ex:
                self.log.warning(f"[{i+1}/10] Ошибка сервера: {ex}")

            except APIClientUndefinedError as ex:
                self.log.warning(f"[{i+1}/10] Неопределенная ошибка: {ex}")

            except Exception as ex:
                raise APIClientTestError("Возникла непредусмотренная ошибка") from ex


def main(api: IAPIClient) -> None:
    tests = APIClientTestBackend(api, log)
    tests.test_get_timeout()
    tests.test_get_rate_limit()
    tests.test_get_client_error()
    tests.test_get_server_error()
