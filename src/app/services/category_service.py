from src.app.repositories.category_repository import CategoryRepository

class CategoryService:
    def __init__(self):
        self.repo = CategoryRepository()

    def create_category(self, data):
        return self.repo.create_category(data)

    def get_all_categories(self):
        return self.repo.get_all_categories()

    def get_category_by_id(self, category_id):
        return self.repo.get_category_by_id(category_id)

    def update_category(self, category_id, data):
        return self.repo.update_category(category_id, data)

    def delete_category(self, category_id):
        return self.repo.delete_category(category_id)
