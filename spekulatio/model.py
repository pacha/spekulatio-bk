from pydantic import BaseModel


class Model(BaseModel):
    class Config:
        use_enum_values = True
        underscore_attrs_are_private = True
        extra = "forbid"
