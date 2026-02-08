# src/app/externals/db/test_connection.py

import os
import sys

# Adiciona o diretório raiz (financePlus) ao path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../"))
)

from src.app.externals.db.connection import SessionLocal
from src.app.externals.models.user import User

session = SessionLocal()

user = User(name="Tharles", email_address="teste@example.com", password="123456")
session.add(user)
session.commit()

print("Usuário criado com sucesso:", user.as_dict)
