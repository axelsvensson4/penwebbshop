import sqlite3


class ProductRepository:
    def __init__(self, database: sqlite3.Connection):
        self.database = database

    def slug_exists(self, slug: str) -> bool:
        return self.database.execute('SELECT 1 FROM products WHERE slug = ?', (slug,)).fetchone() is not None

    def create(self, values: dict[str, object]) -> sqlite3.Row:
        cursor = self.database.execute(
            '''INSERT INTO products (
                name, slug, summary, short_description, description, price_ore, currency,
                is_available, is_outlet, product_type, availability, active, condition, featured, stock_quantity
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (
                values['name'], values['slug'], values['short_description'], values['short_description'],
                values['description'], values['price_ore'], values['currency'],
                values['is_available'], values['is_outlet'], values['product_type'],
                values['availability'], values['active'], values['condition'], values['featured'], values['stock_quantity'],
            ),
        )
        self.database.commit()
        return self.get_by_id(cursor.lastrowid)

    def get_by_id(self, product_id: int) -> sqlite3.Row:
        row = self.database.execute(
            '''SELECT products.id, products.name, products.slug, products.short_description,
                      products.description, products.price_ore, products.currency,
                      categories.name AS category, products.product_type, products.availability,
                      products.active, products.image_url, products.condition, products.featured, products.stock_quantity
               FROM products
               LEFT JOIN product_categories ON product_categories.product_id = products.id
               LEFT JOIN categories ON categories.id = product_categories.category_id
               WHERE products.id = ?''',
            (product_id,),
        ).fetchone()
        if row is None:
            raise LookupError('Produkt hittades inte.')
        return row

    def find_or_create_category(self, name: str) -> int:
        slug = name.strip().lower().replace(' ', '-')
        row = self.database.execute('SELECT id FROM categories WHERE slug = ?', (slug,)).fetchone()
        if row:
            return int(row['id'])
        cursor = self.database.execute('INSERT INTO categories (name, slug) VALUES (?, ?)', (name.strip(), slug))
        return int(cursor.lastrowid)

    def assign_category(self, product_id: int, category_id: int) -> None:
        self.database.execute('INSERT INTO product_categories (product_id, category_id) VALUES (?, ?)', (product_id, category_id))
        self.database.commit()

    def update(self, product_id: int, values: dict[str, object]) -> None:
        self.database.execute(
            '''UPDATE products SET name = ?, summary = ?, short_description = ?, description = ?,
               price_ore = ?, currency = ?, is_available = ?, is_outlet = ?, product_type = ?,
               availability = ?, active = ?, condition = ?, featured = ?, stock_quantity = ?, updated_at = CURRENT_TIMESTAMP
               WHERE id = ?''',
            (
                values['name'], values['short_description'], values['short_description'], values['description'],
                values['price_ore'], values['currency'], values['is_available'], values['is_outlet'],
                values['product_type'], values['availability'], values['active'], values['condition'],
                values['featured'], values['stock_quantity'], product_id,
            ),
        )
        self.database.execute('DELETE FROM product_categories WHERE product_id = ?', (product_id,))

    def commit(self) -> None:
        self.database.commit()

    def add_image(self, product_id: int, file_name: str, alt_text: str | None) -> None:
        self.database.execute(
            'INSERT INTO product_images (product_id, file_name, alt_text) VALUES (?, ?, ?)',
            (product_id, file_name, alt_text),
        )
        self.database.execute('UPDATE products SET image_url = ? WHERE id = ?', (f'/uploads/products/{file_name}', product_id))
        self.database.commit()
