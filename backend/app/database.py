import sqlite3
import os
from collections.abc import Generator
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / 'data' / 'webshop.db'
PRODUCT_CATEGORIES = (
    'Lyxiga',
    'Traditionella',
    'Fjäderpenna',
    'För astronauter',
    'Limited Edition',
)


def get_connection() -> sqlite3.Connection:
    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    return connection


def get_database() -> Generator[sqlite3.Connection, None, None]:
    connection = get_connection()
    try:
        yield connection
    finally:
        connection.close()


def initialize_database() -> None:
    with get_connection() as connection:
        connection.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                slug TEXT UNIQUE,
                summary TEXT,
                description TEXT,
                price_ore INTEGER NOT NULL CHECK (price_ore >= 0),
                compare_at_price_ore INTEGER,
                currency TEXT NOT NULL DEFAULT 'SEK',
                image_url TEXT,
                is_available INTEGER NOT NULL DEFAULT 1,
                is_outlet INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        _migrate_products_table(connection)
        connection.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                slug TEXT NOT NULL UNIQUE,
                description TEXT
            )
        ''')
        connection.execute('''
            CREATE TABLE IF NOT EXISTS product_categories (
                product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
                category_id INTEGER NOT NULL REFERENCES categories(id) ON DELETE CASCADE,
                PRIMARY KEY (product_id, category_id)
            )
        ''')
        _replace_product_categories(connection)
        connection.execute('''
            CREATE TABLE IF NOT EXISTS product_images (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
                file_name TEXT NOT NULL,
                alt_text TEXT,
                sort_order INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        connection.execute('''
            CREATE TABLE IF NOT EXISTS product_reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL REFERENCES products(id) ON DELETE CASCADE,
                user_id INTEGER,
                rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
                comment TEXT NOT NULL,
                author_name TEXT NOT NULL DEFAULT 'Anonym kund',
                review_title TEXT NOT NULL DEFAULT 'Recension',
                status TEXT NOT NULL DEFAULT 'PENDING',
                verified_purchase INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        _migrate_product_reviews(connection)
        _migrate_review_templates(connection)
        connection.execute('''
            CREATE TABLE IF NOT EXISTS review_templates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                rating INTEGER NOT NULL CHECK (rating BETWEEN 1 AND 5),
                comment TEXT NOT NULL,
                active INTEGER NOT NULL DEFAULT 1
            )
        ''')
        _seed_review_templates(connection)
        connection.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, username TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL, role TEXT NOT NULL CHECK (role IN ('USER', 'ADMIN')),
            active INTEGER NOT NULL DEFAULT 1
        )''')
        _migrate_users_table(connection)
        connection.execute('''CREATE TABLE IF NOT EXISTS user_sessions (
            token_hash TEXT PRIMARY KEY, user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )''')
        connection.execute('''CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL REFERENCES users(id),
            status TEXT NOT NULL DEFAULT 'PENDING', created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )''')
        connection.execute('''CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
            product_id INTEGER NOT NULL,
            product_name TEXT NOT NULL,
            price_ore INTEGER NOT NULL CHECK (price_ore >= 0),
            quantity INTEGER NOT NULL CHECK (quantity > 0),
            condition TEXT NOT NULL CHECK (condition IN ('NEW', 'USED', 'WORN'))
        )''')
        _seed_admin_user(connection)
        connection.execute('''CREATE TABLE IF NOT EXISTS cart_items (
            user_id INTEGER NOT NULL REFERENCES users(id), product_id INTEGER NOT NULL REFERENCES products(id),
            quantity INTEGER NOT NULL DEFAULT 1 CHECK (quantity > 0), PRIMARY KEY (user_id, product_id)
        )''')
        connection.execute('''CREATE TABLE IF NOT EXISTS carts (
            id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL UNIQUE REFERENCES users(id),
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        )''')
        connection.execute('''CREATE TABLE IF NOT EXISTS cart_line_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT, cart_id INTEGER NOT NULL REFERENCES carts(id) ON DELETE CASCADE,
            product_id INTEGER NOT NULL REFERENCES products(id), quantity INTEGER NOT NULL DEFAULT 1,
            condition TEXT NOT NULL CHECK (condition IN ('NEW', 'USED', 'WORN')), UNIQUE(cart_id, product_id, condition)
        )''')
        _migrate_cart_line_items(connection)


def _migrate_products_table(connection: sqlite3.Connection) -> None:
    """Gör en äldre lokal databas kompatibel utan att radera data."""
    existing_columns = {
        row['name'] for row in connection.execute('PRAGMA table_info(products)')
    }
    migrations = {
        'slug': 'ALTER TABLE products ADD COLUMN slug TEXT',
        'summary': 'ALTER TABLE products ADD COLUMN summary TEXT',
        'compare_at_price_ore': 'ALTER TABLE products ADD COLUMN compare_at_price_ore INTEGER',
        'currency': "ALTER TABLE products ADD COLUMN currency TEXT NOT NULL DEFAULT 'SEK'",
        'image_url': 'ALTER TABLE products ADD COLUMN image_url TEXT',
        'is_available': 'ALTER TABLE products ADD COLUMN is_available INTEGER NOT NULL DEFAULT 1',
        'is_outlet': 'ALTER TABLE products ADD COLUMN is_outlet INTEGER NOT NULL DEFAULT 0',
        'created_at': 'ALTER TABLE products ADD COLUMN created_at TEXT',
        'short_description': 'ALTER TABLE products ADD COLUMN short_description TEXT',
        "product_type": "ALTER TABLE products ADD COLUMN product_type TEXT NOT NULL DEFAULT 'STANDARD'",
        "availability": "ALTER TABLE products ADD COLUMN availability TEXT NOT NULL DEFAULT 'IN_STOCK'",
        'active': 'ALTER TABLE products ADD COLUMN active INTEGER NOT NULL DEFAULT 1',
        'updated_at': 'ALTER TABLE products ADD COLUMN updated_at TEXT',
        "condition": "ALTER TABLE products ADD COLUMN condition TEXT NOT NULL DEFAULT 'NEW'",
        'featured': 'ALTER TABLE products ADD COLUMN featured INTEGER NOT NULL DEFAULT 0',
        'stock_quantity': 'ALTER TABLE products ADD COLUMN stock_quantity INTEGER NOT NULL DEFAULT 0',
    }
    for column, statement in migrations.items():
        if column not in existing_columns:
            connection.execute(statement)


def _migrate_users_table(connection: sqlite3.Connection) -> None:
    existing_columns = {
        row['name'] for row in connection.execute('PRAGMA table_info(users)')
    }
    migrations = {
        "email": "ALTER TABLE users ADD COLUMN email TEXT NOT NULL DEFAULT ''",
        "address": "ALTER TABLE users ADD COLUMN address TEXT NOT NULL DEFAULT ''",
        "postal_code": "ALTER TABLE users ADD COLUMN postal_code TEXT NOT NULL DEFAULT ''",
        "city": "ALTER TABLE users ADD COLUMN city TEXT NOT NULL DEFAULT ''",
    }
    for column, statement in migrations.items():
        if column not in existing_columns:
            connection.execute(statement)


def _migrate_product_reviews(connection: sqlite3.Connection) -> None:
    existing_columns = {
        row['name'] for row in connection.execute('PRAGMA table_info(product_reviews)')
    }
    migrations = {
        "author_name": "ALTER TABLE product_reviews ADD COLUMN author_name TEXT NOT NULL DEFAULT 'Anonym kund'",
        "review_title": "ALTER TABLE product_reviews ADD COLUMN review_title TEXT NOT NULL DEFAULT 'Recension'",
    }
    for column, statement in migrations.items():
        if column not in existing_columns:
            connection.execute(statement)


def _replace_product_categories(connection: sqlite3.Connection) -> None:
    """Behåll endast webbshopens fasta produktkategorier."""
    placeholders = ', '.join('?' for _ in PRODUCT_CATEGORIES)
    connection.execute(
        f'''DELETE FROM product_categories
            WHERE category_id IN (
                SELECT id FROM categories WHERE name NOT IN ({placeholders})
            )''',
        PRODUCT_CATEGORIES,
    )
    connection.execute(
        f'DELETE FROM categories WHERE name NOT IN ({placeholders})',
        PRODUCT_CATEGORIES,
    )
    for name in PRODUCT_CATEGORIES:
        slug = name.lower().replace(' ', '-')
        connection.execute(
            'INSERT OR IGNORE INTO categories (name, slug) VALUES (?, ?)',
            (name, slug),
        )

    default_category = connection.execute(
        'SELECT id FROM categories WHERE name = ?',
        ('Lyxiga',),
    ).fetchone()
    if default_category:
        connection.execute(
            '''INSERT OR IGNORE INTO product_categories (product_id, category_id)
               SELECT products.id, ? FROM products
               WHERE NOT EXISTS (
                   SELECT 1 FROM product_categories
                   WHERE product_categories.product_id = products.id
               )''',
            (default_category['id'],),
        )


def _migrate_cart_line_items(connection: sqlite3.Connection) -> None:
    """Tillåt samma produkt i kundvagnen med olika skick."""
    table = connection.execute(
        "SELECT sql FROM sqlite_master WHERE type = 'table' AND name = 'cart_line_items'"
    ).fetchone()
    if not table or 'UNIQUE(cart_id, product_id, condition)' in table['sql']:
        return
    connection.execute('''CREATE TABLE cart_line_items_new (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cart_id INTEGER NOT NULL REFERENCES carts(id) ON DELETE CASCADE,
        product_id INTEGER NOT NULL REFERENCES products(id),
        quantity INTEGER NOT NULL DEFAULT 1,
        condition TEXT NOT NULL CHECK (condition IN ('NEW', 'USED', 'WORN')),
        UNIQUE(cart_id, product_id, condition)
    )''')
    connection.execute('''INSERT INTO cart_line_items_new (id, cart_id, product_id, quantity, condition)
        SELECT id, cart_id, product_id, quantity, condition FROM cart_line_items''')
    connection.execute('DROP TABLE cart_line_items')
    connection.execute('ALTER TABLE cart_line_items_new RENAME TO cart_line_items')


def _migrate_review_templates(connection: sqlite3.Connection) -> None:
    old_table = connection.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'demo_review_templates'"
    ).fetchone()
    new_table = connection.execute(
        "SELECT 1 FROM sqlite_master WHERE type = 'table' AND name = 'review_templates'"
    ).fetchone()
    if old_table and not new_table:
        connection.execute('ALTER TABLE demo_review_templates RENAME TO review_templates')


def _seed_review_templates(connection: sqlite3.Connection) -> None:
    """Förifyllda recensioner för skolprojektets produktpreview."""
    reviews = [
        ('Jag skulle kunna skriva en roman om den här pennan.', 'Astrid', 34, 'Jag köpte en penna. Sedan köpte jag tre till. Jag vet inte riktigt vad som hände, men jag ångrar ingenting. De skriver så fint att jag börjat skriva ner saker jag egentligen inte behöver skriva ner. 10/10.'),
        ('Min gamla penna är numera arbetslös.', 'Johan', 42, 'Jag trodde ärligt talat att en penna var en penna. Jag hade fel. Den här skriver så mjukt att jag nästan började skriva under mina mejl med "Med vänliga hälsningar" igen.'),
        ('Äntligen en penna som överlever mitt kaos.', 'Maja', 27, 'Jag tappar pennor. Ofta. Väldigt ofta. Den här har överlevt både handväskan, soffan, bilen och tre veckor i botten av en flyttkartong. Jag är imponerad. Pennan är tydligen gjord av starkare material än jag själv.'),
        ('Jag skulle bara köpa EN.', 'Fredrik', 38, 'Gick in på sidan för att köpa en penna. Kom ut med fem. Min sambo har frågor. Jag har inga svar. Men jag har väldigt bra pennor.'),
        ('Min handstil har inte blivit bättre. Men den ser bättre ut.', 'Linnea', 31, 'Viktig skillnad. Jag skriver fortfarande som en stressad läkare med dålig tid. Men med den här pennan känns det åtminstone professionellt.'),
        ('Pennan gjorde mötet 17 % mindre tråkigt.', 'Oskar', 45, 'Kan inte lova att pennan förbättrade mötet. Men jag skrev väldigt mycket anteckningar och såg extremt fokuserad ut. Ingen märkte att jag egentligen ritade små dinosaurier i marginalen.'),
        ('Jag har hittat MIN penna.', 'Elin', 29, 'Ni vet när man provar en massa och plötsligt bara klickar det? Så var det här. Perfekt vikt, perfekt känsla och ett bläck som bara flyter. Jag och min penna har nu ett exklusivt förhållande.'),
        ('Min son tog min penna. Det här är ett problem.', 'Henrik', 51, 'Jag köpte pennan till mig själv. Min son lånade den. Han vägrar lämna tillbaka den. Jag överväger att beställa en ny och gömma den. Tack för ett oväntat familjedrama.'),
        ('Snabb leverans och alldeles för trevlig penna.', 'Sofia', 36, 'Paketet kom snabbt, pennan var snygg och den skriver fantastiskt. Jag har egentligen inget negativt att säga. Det känns nästan misstänkt. Kommer definitivt handla här igen.'),
        ('Jag visste inte att jag var en pennperson.', 'Viktor', 40, 'Tydligen är jag det. Jag trodde att folk som hade åsikter om pennor var lite speciella. Nu har jag själv åsikter om pennor. Jag har till och med en favorit. Vad har ni gjort med mig?'),
    ]
    for title, name, age, comment in reviews:
        connection.execute(
            '''INSERT INTO review_templates (title, name, age, rating, comment)
               SELECT ?, ?, ?, 5, ?
               WHERE NOT EXISTS (SELECT 1 FROM review_templates WHERE title = ?)''',
            (title, name, age, comment, title),
        )


def _seed_admin_user(connection: sqlite3.Connection) -> None:
    from app.core.security import hash_password
    username = os.getenv('SEED_ADMIN_USERNAME')
    password = os.getenv('SEED_ADMIN_PASSWORD')
    if not username or not password:
        return
    row = connection.execute('SELECT id FROM users WHERE username = ?', (username,)).fetchone()
    if row is None:
        connection.execute('INSERT INTO users (name, username, password_hash, role) VALUES (?, ?, ?, ?)', (os.getenv('SEED_ADMIN_NAME', 'Admin'), username, hash_password(password), 'ADMIN'))
    else:
        connection.execute('UPDATE users SET password_hash = ?, role = ? WHERE id = ?', (hash_password(password), 'ADMIN', row['id']))
