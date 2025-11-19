# app/my_project/dao/base.py

from typing import Any, Type
from ..utils.db import db


class BaseDAO:
    """
    Базовий DAO-клас для CRUD-операцій з будь-якою ORM-моделлю.
    Використовується як батьківський клас для DAO сутностей.
    """

    def __init__(self, model: Type[Any]):
        """
        model — це клас SQLAlchemy-моделі (наприклад Airline, Flight і т.д.)
        """
        self.model = model

    # --- READ ---
    def get_all(self):
        return self.model.query.all()

    def get(self, obj_id: Any):
        return self.model.query.get(obj_id)

    # --- CREATE ---
    def create(self, **kwargs):
        obj = self.model(**kwargs)
        db.session.add(obj)
        db.session.commit()
        return obj

    # --- UPDATE ---
    def update(self, obj, **kwargs):
        for key, value in kwargs.items():
            setattr(obj, key, value)
        db.session.commit()
        return obj

    # --- DELETE ---
    def delete(self, obj):
        db.session.delete(obj)
        db.session.commit()
