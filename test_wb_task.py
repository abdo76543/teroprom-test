import sys
import time
import logging
from pathlib import Path

ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))
from tasks.wb_task import IWBScraper
from tasks.wb_task import WBScraperUndefinedError
from tasks.wb_task import WBScraperProductNotFoundError
from tasks.wb_task import WBProduct
from logger import log


class WBScraperTestError(Exception):
    pass


class WBScraperTestBackend:
    def __init__(
        self,
        scraper: IWBScraper,
        log: logging.Logger,
    ) -> None:
        self.scraper = scraper
        self.log = log

    def test_get_product(self) -> None:
        articles = [74439191, 386285843, 280011745, 340143517, 362400110]
        for article in articles:
            try:
                self.log.debug(f"Запрашиваю товар с артикулом: {article}")
                product = self.scraper.get_product(article)
                self.log.debug(f"Получен товар: {product}")

                if not isinstance(product, WBProduct):
                    self.log.error(f"Получен некорректный объект: {product}")
                    raise WBScraperTestError(f"Получен некорректный объект: {product}")

                if product.article != article:
                    self.log.error(
                        f"Артикул товара не совпадает: {product.article} != {article}"
                    )
                    raise WBScraperTestError(
                        f"Артикул товара не совпадает: {product.article} != {article}"
                    )

                if not product.name:
                    self.log.error("Название товара не найдено.")
                    raise WBScraperTestError("Название товара не найдено.")
                if not product.brand:
                    self.log.error("Бренд товара не найден.")
                    raise WBScraperTestError("Бренд товара не найден.")
                if product.old_price is None or product.cur_price is None:
                    self.log.error("Цены товара не найдены.")
                    raise WBScraperTestError("Цены товара не найдены.")

            except WBScraperProductNotFoundError as ex:
                self.log.error(f"Товар с артикулом {article} не найден: {ex}")
            except WBScraperUndefinedError as ex:
                self.log.error(
                    f"Неопределенная ошибка при получении товара {article}: {ex}"
                )


def main(scraper: IWBScraper) -> None:
    tests = WBScraperTestBackend(scraper, log)
    tests.test_get_product()
