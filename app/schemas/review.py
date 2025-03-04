#######################################
#
#   Схема данных для сущности Review
#
#######################################

from pydantic import BaseModel


class CreateReview(BaseModel):
    grage: int
    comment: str
    product_id: int
