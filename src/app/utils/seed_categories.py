from src.app.repositories.category_repository import CategoryRepository

def seed_default_categories():
    repo = CategoryRepository()
    
    # Verificar se já existem categorias padrão (user_id=None)
    existing_categories = repo.get_all_categories(user_id=None)
    if existing_categories:
        print("Categorias padrão já existem. Pulando seed.")
        return

    default_categories = [
        "Alimentação",
        "Transporte",
        "Moradia",
        "Saúde",
        "Lazer",
        "Educação",
        "Salário",
        "Investimentos",
        "Outros"
    ]

    print("Criando categorias padrão...")
    for category_name in default_categories:
        data = {
            "name": category_name,
            "user_id": None  # Categoria global
        }
        repo.create_category(data)
        print(f"Categoria '{category_name}' criada.")

if __name__ == "__main__":
    seed_default_categories()
