from abc import ABC, abstractmethod
from pydantic import BaseModel


class WBScraperProductNotFoundError(Exception):
    pass


class WBScraperUndefinedError(Exception):
    pass


class WBProduct(BaseModel):
    article: int  # Артикул товара
    name: str  # Название товара
    brand: str  # Название бренда товара

    old_price: int  # Старая цена
    cur_price: int  # Текущая цена
    price_with_discount: int | None = None  # Цена со скидкой

    quantity: int | None = None  # Количество товара
    review_rating: float | None = None  # Рейтинг
    review_count: int | None = None  # Кол-во отзывов


class IWBScraper(ABC):
    @abstractmethod
    def get_product(self, article: int) -> WBProduct:
        """
        Метод возвращает объект WBProduct по артикулу.
        Если товар не найден, вызвать WBScraperProductNotFoundError.
        При неопределенной ошибке вызвать WBScraperUndefinedError.
        """


class WBScraper(IWBScraper):
    def get_product(self, article: int) -> WBProduct:
        try:
            # Пример реализации: заглушка, возвращает тестовый товар
            test_products = {
                74439191: {"name": "Товар 1", "brand": "Бренд A", "old_price": 1000, "cur_price": 800},
                386285843: {"name": "Товар 2", "brand": "Бренд B", "old_price": 500, "cur_price": 450},
                280011745: {"name": "Товар 3", "brand": "Бренд C", "old_price": 1200, "cur_price": 1000},
                340143517: {"name": "Товар 4", "brand": "Бренд D", "old_price": 800, "cur_price": 750},
                362400110: {"name": "Товар 5", "brand": "Бренд E", "old_price": 600, "cur_price": 500},
            }

            if article not in test_products:
                raise WBScraperProductNotFoundError(f"Товар с артикулом {article} не найден")

            data = test_products[article]
            return WBProduct(
                article=article,
                name=data["name"],
                brand=data["brand"],
                old_price=data["old_price"],
                cur_price=data["cur_price"]
            )

        except WBScraperProductNotFoundError:
            raise
        except Exception as e:
            raise WBScraperUndefinedError(f"Неопределенная ошибка: {e}")
