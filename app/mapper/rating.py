####################################################
#
#           Маппер для сущности Rating
#
####################################################

from app.schemas.review import CreateReview
from app.models.rating import Rating


def data_to_model(
        data: CreateReview,
        user: dict,
    ) -> Rating:
    """
    Функция для преобразования данных схемы в данные модели
    """
    return Rating(
        grade=data.grage,
        product_id=data.product_id,
        user_id=user.get("id"),
    )
