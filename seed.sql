-- DROP DATABASE IF EXISTS  art_explorer_db;
-- CREATE DATABASE art_explorer_db;
-- \c art_explorer_db
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS artworks;
DROP TABLE IF EXISTS users_artworks;
CREATE TABLE users
(
  username TEXT PRIMARY KEY,
  password TEXT NOT NULL,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  share TEXT NOT NULL
);

CREATE TABLE artworks
(
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  artist TEXT NOT NULL,
  image_link TEXT NOT NULL
);

CREATE TABLE users_artworks
(
  id SERIAL PRIMARY KEY,
  username TEXT REFERENCES users (username) ON DELETE CASCADE,
  artwork_id INTEGER REFERENCES artworks (id) ON DELETE CASCADE,
  comment TEXT
);

INSERT INTO users
  (username, password, first_name, last_name, share)
VALUES
('mellis', '$2b$12$RM3aeyACzaeAGOSDRpss0uTJ/pPWcFWMmt15bKH.OLW6.iOxPLh0u', 'Michael', 'Ellis', 'Yes'),
('csantana', '$2b$12$RM3aeyACzaeAGOSDRpss0uTJ/pPWcFWMmt15bKH.OLW6.iOxPLh0u', 'Christopher', 'Santana', 'Yes'),
('jkramer', '$2b$12$RM3aeyACzaeAGOSDRpss0uTJ/pPWcFWMmt15bKH.OLW6.iOxPLh0u', 'Jessica', 'Kramer', 'Yes'),
('mconner', '$2b$12$RM3aeyACzaeAGOSDRpss0uTJ/pPWcFWMmt15bKH.OLW6.iOxPLh0u', 'Matthew', 'Conner', 'Yes'),
('alevy', '$2b$12$RM3aeyACzaeAGOSDRpss0uTJ/pPWcFWMmt15bKH.OLW6.iOxPLh0u', 'Ashley', 'Levy', 'Yes'),
('jalverez', '$2b$12$RM3aeyACzaeAGOSDRpss0uTJ/pPWcFWMmt15bKH.OLW6.iOxPLh0u', 'Jennifer', 'Alvarez', 'Yes'),
('jgarcia', '$2b$12$RM3aeyACzaeAGOSDRpss0uTJ/pPWcFWMmt15bKH.OLW6.iOxPLh0u', 'Joshua', 'Garcia', 'Yes'),
('amathis', '$2b$12$RM3aeyACzaeAGOSDRpss0uTJ/pPWcFWMmt15bKH.OLW6.iOxPLh0u', 'Amanda', 'Mathis', 'No'),
('dwilcox', '$2b$12$RM3aeyACzaeAGOSDRpss0uTJ/pPWcFWMmt15bKH.OLW6.iOxPLh0u', 'Daniel', 'Wilcox', 'No'),
('dbeltran', '$2b$12$RM3aeyACzaeAGOSDRpss0uTJ/pPWcFWMmt15bKH.OLW6.iOxPLh0u', 'David', 'Beltran', 'No'),
('jlewis', '$2b$12$RM3aeyACzaeAGOSDRpss0uTJ/pPWcFWMmt15bKH.OLW6.iOxPLh0u', 'James', 'Lewis', 'No');

INSERT INTO artworks
  (id, title, artist, image_link)
VALUES
('11207', 'The Flower Girl', 'Charles Cromwell Ingham', 'https://images.metmuseum.org/CRDImages/ad/web-large/DT2784.jpg'),
('11325', 'Sunset on the Sea', 'John Frederick Kensett', 'https://images.metmuseum.org/CRDImages/ad/web-large/DT226485.jpg'),
('10159', 'Fur Traders Descending the Missouri', 'George Caleb Bingham', 'https://images.metmuseum.org/CRDImages/ad/web-large/DT73.jpg'),
('436947', 'Boating', 'Edouard Manet', 'https://images.metmuseum.org/CRDImages/ep/web-large/DT45.jpg'),
('437549', 'Wheat Fields', 'Jacob van Ruisdael', 'https://images.metmuseum.org/CRDImages/ep/web-large/DP145911.jpg'),
('437097', 'Haystacks: Autumn', 'Jean-François Millet', 'https://images.metmuseum.org/CRDImages/ep/web-large/DP124093.jpg'),
('435809', 'The Harvesters', 'Pieter Bruegel the Elder', 'https://images.metmuseum.org/CRDImages/ep/web-large/DP119115.jpg'),
('282040', '[Landscape with Clouds]', 'Roger Fenton', 'https://images.metmuseum.org/CRDImages/ph/web-large/DP107953.jpg'),
('11053', 'Newburyport Meadows', 'Martin Johnson Heade', 'https://images.metmuseum.org/CRDImages/ad/web-large/DT2050.jpg'),
('435773', 'The Weeders', 'Jules Breton', 'https://images.metmuseum.org/CRDImages/ep/web-large/DT2155.jpg'),
('380480', 'The Champions of the Mississippi – "A Race for the Buckhorns"', 'Frances Flora Bond Palmer', 'https://images.metmuseum.org/CRDImages/dp/web-large/DT9290.jpg'),
('10872', 'City and Sunset', 'Henry Farrer', 'https://images.metmuseum.org/CRDImages/ad/web-large/DT8072.jpg'),
('437526', 'A Forest at Dawn with a Deer Hunt', 'Peter Paul Rubens', 'https://images.metmuseum.org/CRDImages/ep/web-large/DT4532.jpg'),
('16202', 'Clouds over Water (Long Island Sound?) (from Sketchbook)', 'Henry Ward Ranger', 'https://images.metmuseum.org/CRDImages/ad/web-large/263380.jpg'),
('682964', 'Autumnal Sunset', 'David Lucas', 'https://images.metmuseum.org/CRDImages/dp/web-large/DP875031.jpg'),
('338925', 'Bullbaiting in a Venetian Piazza', 'Francesco Guardi', 'https://images.metmuseum.org/CRDImages/dp/web-large/DP810102.jpg'),
('438817', 'The Dance Class', 'Edgar Degas', 'https://images.metmuseum.org/CRDImages/ep/web-large/DP-20101-001.jpg'),
('437586', 'A Country Road', 'Salomon van Ruysdael', 'https://images.metmuseum.org/CRDImages/ep/web-large/DP143152.jpg'),
('193623', 'Diana and the Stag', 'Joachim Friess', 'https://images.metmuseum.org/CRDImages/es/web-large/DT2525.jpg'),
('438738', 'Haystacks, Morning, Éragny', 'Camille Pissarro', 'https://images.metmuseum.org/CRDImages/ep/web-large/DP-20613-001.jpg'),
('436290', 'Flowers by a Stone Vase', 'Peter Faes', 'https://images.metmuseum.org/CRDImages/ep/web-large/ep48.187.737.R.jpg'),
('436061', 'Landscape with the Flight into Egypt', 'Aelbert Cuyp', 'https://images.metmuseum.org/CRDImages/ep/web-large/DP143208.jpg'),
('342234', 'Equestrian Statue of Constantine the Great', 'Francesco Faraone Aquila', 'https://images.metmuseum.org/CRDImages/dp/web-large/DP273762.jpg'),
('5998', 'Plate', '', 'https://images.metmuseum.org/CRDImages/ad/web-large/DP207700.jpg'),
('323766', 'Fragment of a vessel with wheat stalks and a procession of bulls in relief', '', 'https://images.metmuseum.org/CRDImages/an/web-large/DP271923.jpg'),
('421651', 'William Evelyn of St Clere, Kent, Holding a Spaniel', 'Hugh Douglas Hamilton', 'https://images.metmuseum.org/CRDImages/dp/web-large/DP829473.jpg'),
('436199', 'Christ Healing the Sick', 'Christian Wilhelm Ernst Dietrich', 'https://images.metmuseum.org/CRDImages/ep/web-large/DP-22532-001.jpg'),
('437536', 'Wolf and Fox Hunt', 'Peter Paul Rubens', 'https://images.metmuseum.org/CRDImages/ep/web-large/DT5526.jpg'),
('647338', 'Saint Francis in Ecstasy', 'Giovanni Benedetto Castiglione (Il Grechetto)', 'https://images.metmuseum.org/CRDImages/ep/web-large/DP328663.jpg'),
('266672', 'French Machinery', 'Charles Thurston Thompson', 'https://images.metmuseum.org/CRDImages/ph/web-large/DP200354.jpg'),
('437346', 'Inter artes et naturam (Between Art and Nature)', 'Pierre Puvis de Chavannes', 'https://images.metmuseum.org/CRDImages/ep/web-large/DP-14201-039.jpg'),
('50694', 'Meiping (Plum) Vase with Bamboo and Rocks', '', 'https://images.metmuseum.org/CRDImages/as/web-large/205575.jpg'),
('438820', 'Young Ladies of the Village', 'Gustave Courbet', 'https://images.metmuseum.org/CRDImages/ep/web-large/DT1967.jpg'),
('438128', 'The Flight into Egypt', 'Giovanni Battista Tiepolo', 'https://images.metmuseum.org/CRDImages/ep/web-large/CT_41570.jpg'),
('435986', 'View of Lormes', 'Camille Corot', 'https://images.metmuseum.org/CRDImages/ep/web-large/DT9008.jpg'),
('437652', 'The Virgin Adoring the Child with the Infant Saint John the Baptist', 'Jacopo di Arcangelo (called Jacopo del Sellaio)', 'https://images.metmuseum.org/CRDImages/ep/web-large/ep41.100.10.bw.R.jpg'),
('415297', 'Road into a Village, plate 19 from Regiunculae et Villae Aliquot Ducatus Brabantiae', 'Claes Jansz. Visscher', 'https://images.metmuseum.org/CRDImages/dp/web-large/DP825684.jpg'),
('365456', 'Figures on a Beach, Northern France', 'Thomas Shotter Boys', 'https://images.metmuseum.org/CRDImages/dp/web-large/DP800802.jpg'),
('435526', 'The County Election', 'John Sartain', 'https://images.metmuseum.org/CRDImages/dp/web-large/MM89468.jpg'),
('339864', 'The Jolly Flatboatmen', 'Thomas Doney', 'https://images.metmuseum.org/CRDImages/dp/web-large/DT222840.jpg'),
('437052', '1807, Friedland', 'Ernest Meissonier', 'https://images.metmuseum.org/CRDImages/ep/web-large/DT2144.jpg'),
('435962', 'Hagar in the Wilderness', 'Camille Corot', 'https://images.metmuseum.org/CRDImages/ep/web-large/DT2013.jpg'),
('838850', 'The Temptation of St. Anthony', 'Hieronymus Bosch', 'https://images.metmuseum.org/CRDImages/dp/web-large/DP-19966-001.jpg'),
('220023', 'Sample', '', 'https://images.metmuseum.org/CRDImages/es/web-large/DP2539.jpg'),
('45326', 'Magpie on Viburnum Branch', 'Genga', 'https://images.metmuseum.org/CRDImages/as/web-large/DP279663.jpg'),
('436946', 'The Brioche', 'Edouard Manet', 'https://images.metmuseum.org/CRDImages/ep/web-large/DP-13655-001.jpg');

INSERT INTO users_artworks
  (username, artwork_id)
VALUES
('mellis', '193623'),
('mellis', '338925'),
('mellis', '435809'),
('mellis', '437586'),
('mellis', '438817'),
('mellis', '682964'),
('csantana', '10159'),
('csantana', '45326'),
('csantana', '50694'),
('csantana', '266672'),
('csantana', '365456'),
('csantana', '415297'),
('csantana', '435526'),
('csantana', '435962'),
('csantana', '435986'),
('csantana', '436946'),
('csantana', '437052'),
('csantana', '437346'),
('csantana', '437536'),
('csantana', '437652'),
('csantana', '438128'),
('csantana', '438817'),
('csantana', '438820'),
('csantana', '647338'),
('csantana', '838850'),
('jkramer', '5998'),
('jkramer', '10159'),
('jkramer', '45326'),
('jkramer', '339864'),
('jkramer', '435986'),
('jkramer', '436946'),
('jkramer', '438128'),
('mconner', '10872'),
('mconner', '11053'),
('mconner', '11207'),
('mconner', '282040'),
('mconner', '342234'),
('mconner', '380480'),
('mconner', '435773'),
('mconner', '435809'),
('mconner', '436061'),
('mconner', '436947'),
('mconner', '437097'),
('mconner', '437549'),
('alevy', '5998'),
('alevy', '323766'),
('alevy', '421651'),
('alevy', '436199'),
('jalverez', '16202'),
('jalverez', '437526'),
('jgarcia', '436290'),
('jgarcia', '438738');
