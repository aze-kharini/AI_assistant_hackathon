
DROP TABLE IF EXISTS varieties;

CREATE TABLE varieties
(
    var_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    rating DECIMAL,
    num_of_ratings INTEGER,
    description TEXT,
    sweetness DECIMAL,
    body DECIMAL,
    flavor DECIMAL
);

INSERT INTO varieties (name, rating, num_of_ratings, description, sweetness, body, flavor)
VALUES  ('Rubiaceae', NULL, NULL, 'Family of all coffee plants', NULL, NULL, NULL),
        ('Coffea Arabica', NULL, NULL, 'Main species of coffea, generally varieties of arabica are sweet, chocolaty and fruity.', 7, 5, 2),
        ('Coffea Canephora', NULL, NULL, 'Second largest species of coffee after arabica, also called robusta. More resistant but with strong bitterness. Used in blends to increae the body of coffee.', -8, 9, 8),
        ('Gesha', 5, 10, 'Excellent tasting coffee originating from Ethiopia. Exotic with notes of jasmine.', 9, 5, -10),
        ('Typica', 4, 10, 'Major varitey of arabica that is widely spread all over the world. Excellent taste and mouthfeel with fruity notes.', 7, 5, -2),
        ('Bourbon', 4, 10, 'Important variety evolved on the island of Bourbon. Famous for its sweetness and cup quality.', 9, 5, 5),
        ('Timor', 3, 10, 'Crossbreed between arabica and robusta. Higher resistence to disease, but unfortunately lower cup quality.',-4, 8, 6),
        ('Caturra', 3.5, 10, 'Sweetness inhereted from bourbon variety, with floral notes.', 8, 4, -6),
        ('Maragogipe', 4, 10, 'Pleasantyly acidic with distinct characteristics of the region. Popular becuse of it`s large berries.', 0, 4, -8),
        ('Mundo Nuovo', 3.5, 10, 'Crossbreed between Typica and Bourbon. Characteristic sweetness, low acidity and full body.', 9, 8, 2),
        ('Catuai', 3, 10, 'Very productive coffee popular in Brazil. Known for herbal taste with a bitter finnish.', -4, 5, -2),
        ('Catimor', 2.5, 10, 'Coffee resulting from Caturra and Timor variety with full-bodied and spicy notes.', -6, 9, 3),
        ('SL-28', 5, 10, 'The most famous variety from Scott`s Labs (SL prefix). Famous forrest berry flavors with great complexity and acidity.', 4, 5, -8);


DROP TABLE IF EXISTS schemas;

CREATE TABLE schemas
(
    schema_id TEXT PRIMARY KEY,
    schema_code TEXT
);

INSERT INTO schemas (schema_id, schema_code)
VALUES ('varieties', 'CREATE TABLE varieties (var_id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, rating DECIMAL, num_of_ratings INTEGER, description TEXT, sweetness DECIMAL, body DECIMAL, flavor DECIMAL);');