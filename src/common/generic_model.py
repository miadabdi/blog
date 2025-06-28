from datetime import datetime

from sqlmodel import Field, SQLModel, func


class GenericModel(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(sa_column_kwargs={"server_default": func.now()})
    updated_at: datetime = Field(
        sa_column_kwargs={"server_default": func.now(), "onupdate": func.now()}
    )
    # def __init_subclass__(cls, **kwargs):
    #     super().__init_subclass__(**kwargs)
    #     # Register event listener for each subclass that becomes a table
    #     if kwargs.get("table", False):  # Only if table=True is passed

    #         @event.listens_for(cls, "before_update")
    #         def update_timestamp(mapper, connection, target: GenericModel):
    #             target.updated_at = datetime.now()
