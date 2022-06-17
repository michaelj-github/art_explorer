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
  share TEXT NOT NULL,
  collection INTEGER UNIQUE NOT NULL
);

CREATE TABLE artworks
(
  id INTEGER PRIMARY KEY,
  title TEXT NOT NULL,
  artist TEXT NOT NULL,
  department TEXT,
  creditLine TEXT,
  image_link TEXT NOT NULL,
  image_link_full TEXT
);

CREATE TABLE users_artworks
(
  id SERIAL PRIMARY KEY,
  username TEXT REFERENCES users (username) ON DELETE CASCADE,
  artwork_id INTEGER REFERENCES artworks (id) ON DELETE CASCADE,
  comment TEXT
);

INSERT INTO users
  (username, password, first_name, last_name, share, collection)
VALUES
('mellis', '$2b$12$RM3aeyACzaeAGOSDRpss0uTJ/pPWcFWMmt15bKH.OLW6.iOxPLh0u', 'Michael', 'Ellis', 'No', 101),
('mconner', '$2b$12$RM3aeyACzaeAGOSDRpss0uTJ/pPWcFWMmt15bKH.OLW6.iOxPLh0u', 'Matthew', 'Conner', 'No', 102),
('jalverez', '$2b$12$RM3aeyACzaeAGOSDRpss0uTJ/pPWcFWMmt15bKH.OLW6.iOxPLh0u', 'Jennifer', 'Alvarez', 'No', 103),
('jgarcia', '$2b$12$RM3aeyACzaeAGOSDRpss0uTJ/pPWcFWMmt15bKH.OLW6.iOxPLh0u', 'Joshua', 'Garcia', 'No', 104),
('dwilcox', '$2b$12$RM3aeyACzaeAGOSDRpss0uTJ/pPWcFWMmt15bKH.OLW6.iOxPLh0u', 'Daniel', 'Wilcox', 'No', 105),
('jlewis', '$2b$12$RM3aeyACzaeAGOSDRpss0uTJ/pPWcFWMmt15bKH.OLW6.iOxPLh0u', 'James', 'Lewis', 'No', 106),
('csantana', '$2b$12$RM3aeyACzaeAGOSDRpss0uTJ/pPWcFWMmt15bKH.OLW6.iOxPLh0u', 'Christopher', 'Santana', 'Yes', 107),
('alevy', '$2b$12$RM3aeyACzaeAGOSDRpss0uTJ/pPWcFWMmt15bKH.OLW6.iOxPLh0u', 'Ashley', 'Levy', 'Yes', 108),
('amathis', '$2b$12$RM3aeyACzaeAGOSDRpss0uTJ/pPWcFWMmt15bKH.OLW6.iOxPLh0u', 'Amanda', 'Mathis', 'Yes', 109),
('dbeltran', '$2b$12$RM3aeyACzaeAGOSDRpss0uTJ/pPWcFWMmt15bKH.OLW6.iOxPLh0u', 'David', 'Beltran', 'Yes', 110),
('jkramer', '$2b$12$RM3aeyACzaeAGOSDRpss0uTJ/pPWcFWMmt15bKH.OLW6.iOxPLh0u', 'Jessica', 'Kramer', 'Yes', 111);

INSERT INTO artworks
  (id, title, artist, department, creditline, image_link, image_link_full)
VALUES
('667895', 'The Virgin in prayer in an oval frame, after Reni', 'Anonymous', 'Drawings and Prints', 'The Elisha Whittelsey Collection, The Elisha Whittelsey Fund, 1951', 'https://images.metmuseum.org/CRDImages/dp/web-large/DP841763.jpg', 'https://images.metmuseum.org/CRDImages/dp/original/DP841763.jpg'),
('10159', 'Fur Traders Descending the Missouri', 'George Caleb Bingham', 'The American Wing', 'Morris K. Jesup Fund, 1933', 'https://images.metmuseum.org/CRDImages/ad/web-large/DT73.jpg', 'https://images.metmuseum.org/CRDImages/ad/original/DT73.jpg'),
('10786', 'The Beeches', 'Asher Brown Durand', 'The American Wing', 'Bequest of Maria DeWitt Jesup, from the collection of her husband, Morris K. Jesup, 1914', 'https://images.metmuseum.org/CRDImages/ad/web-large/DT75.jpg', 'https://images.metmuseum.org/CRDImages/ad/original/DT75.jpg'),
('10872', 'City and Sunset', 'Henry Farrer', 'The American Wing', 'Purchase, Gifts of Mrs. Louise Lamson and Mrs. Alfred N. Lawrence, Bequest of Antoinette D. T. Throckmorton, in memory of Jules and Ella Turcas, and Bequest of May Blackstone Huntington, by exchange; Mr. and Mrs. Harry L. Koenigsberg, Walter Knight Sturges and Vain and Harry Fish Foundation Gifts and Maria DeWitt Jesup Fund, 1985', 'https://images.metmuseum.org/CRDImages/ad/web-large/DT8072.jpg', 'https://images.metmuseum.org/CRDImages/ad/original/DT8072.jpg'),
('10945', 'Isola Bella in Lago Maggiore', 'Sanford Robinson Gifford', 'The American Wing', 'Gift of Colonel Charles A. Fowler, 1921', 'https://images.metmuseum.org/CRDImages/ad/web-large/DT1550.jpg', 'https://images.metmuseum.org/CRDImages/ad/original/DT1550.jpg'),
('11101', 'View of Yosemite Valley', 'Thomas Hill', 'The American Wing', 'Gift of Dr. and Mrs. Harold W. Lovell, 1971', 'https://images.metmuseum.org/CRDImages/ad/web-large/ap1971.245.jpg', 'https://images.metmuseum.org/CRDImages/ad/original/ap1971.245.jpg'),
('11235', 'Sunrise', 'George Inness', 'The American Wing', 'Anonymous Gift, in memory of Emil Thiele, 1954', 'https://images.metmuseum.org/CRDImages/ad/web-large/DP232470.jpg', 'https://images.metmuseum.org/CRDImages/ad/original/DP232470.jpg'),
('11324', 'Sunset', 'John Frederick Kensett', 'The American Wing', 'Gift of Thomas Kensett, 1874', 'https://images.metmuseum.org/CRDImages/ad/web-large/ap74.37.jpg', 'https://images.metmuseum.org/CRDImages/ad/original/ap74.37.jpg'),
('11325', 'Sunset on the Sea', 'John Frederick Kensett', 'The American Wing', 'Gift of Thomas Kensett, 1874', 'https://images.metmuseum.org/CRDImages/ad/web-large/DT226485.jpg', 'https://images.metmuseum.org/CRDImages/ad/original/DT226485.jpg'),
('11326', 'Sunset Sky', 'John Frederick Kensett', 'The American Wing', 'Gift of Thomas Kensett, 1874', 'https://images.metmuseum.org/CRDImages/ad/web-large/ap74.30.jpg', 'https://images.metmuseum.org/CRDImages/ad/original/ap74.30.jpg'),
('11329', 'Twilight on the Sound, Darien, Connecticut', 'John Frederick Kensett', 'The American Wing', 'Gift of Thomas Kensett, 1874', 'https://images.metmuseum.org/CRDImages/ad/web-large/ap74.24.jpg', 'https://images.metmuseum.org/CRDImages/ad/original/ap74.24.jpg'),
('11897', 'Lake Squam from Red Hill', 'William Trost Richards', 'The American Wing', 'Gift of The Reverend E. L. Magoon, D.D., 1880', 'https://images.metmuseum.org/CRDImages/ad/web-large/DT4564.jpg', 'https://images.metmuseum.org/CRDImages/ad/original/DT4564.jpg'),
('11910', 'Sunset on Mount Chocorua, New Hampshire', 'William Trost Richards', 'The American Wing', 'Gift of The Reverend E. L. Magoon, D.D., 1880', 'https://images.metmuseum.org/CRDImages/ad/web-large/ap80.1.10.jpg', 'https://images.metmuseum.org/CRDImages/ad/original/ap80.1.10.jpg'),
('12800', 'The Belated Party on Mansfield Mountain', 'Jerome B. Thompson', 'The American Wing', 'Rogers Fund, 1969', 'https://images.metmuseum.org/CRDImages/ad/web-large/DT2098.jpg', 'https://images.metmuseum.org/CRDImages/ad/original/DT2098.jpg'),
('18354', 'Lake George and the Village of Caldwell', 'Thomas Chambers', 'The American Wing', 'Gift of Edgar William and Bernice Chrysler Garbisch, 1966', 'https://images.metmuseum.org/CRDImages/ad/web-large/ap66.242.17.jpg', 'https://images.metmuseum.org/CRDImages/ad/original/ap66.242.17.jpg'),
('339864', 'The Jolly Flatboatmen', 'Thomas Doney', 'Drawings and Prints', 'Gertrude and Thomas Jefferson Mumford Collection, Gift of Dorothy Quick Mayer, 1942', 'https://images.metmuseum.org/CRDImages/dp/web-large/DT222840.jpg', 'https://images.metmuseum.org/CRDImages/dp/original/DT222840.jpg'),
('435526', 'The County Election', 'John Sartain', 'Drawings and Prints', 'The Elisha Whittelsey Collection, The Elisha Whittelsey Fund, 1952', 'https://images.metmuseum.org/CRDImages/dp/web-large/MM89468.jpg', 'https://images.metmuseum.org/CRDImages/dp/original/MM89468.jpg'),
('435773', 'The Weeders', 'Jules Breton', 'European Paintings', 'Bequest of Collis P. Huntington, 1900', 'https://images.metmuseum.org/CRDImages/ep/web-large/DT2155.jpg', 'https://images.metmuseum.org/CRDImages/ep/original/DT2155.jpg'),
('436061', 'Landscape with the Flight into Egypt', 'Aelbert Cuyp', 'European Paintings', 'Bequest of Josephine Bieber, in memory of her husband, Siegfried Bieber, 1970', 'https://images.metmuseum.org/CRDImages/ep/web-large/DP143208.jpg', 'https://images.metmuseum.org/CRDImages/ep/original/DP143208.jpg'),
('436062', 'Piping Shepherds', 'Aelbert Cuyp', 'European Paintings', 'Bequest of Collis P. Huntington, 1900', 'https://images.metmuseum.org/CRDImages/ep/web-large/DP143163.jpg', 'https://images.metmuseum.org/CRDImages/ep/original/DP143163.jpg'),
('436527', 'The Flowering Orchard', 'Vincent van Gogh', 'European Paintings', 'The Mr. and Mrs. Henry Ittleson Jr. Purchase Fund, 1956', 'https://images.metmuseum.org/CRDImages/ep/web-large/DP-14936-045.jpg', 'https://images.metmuseum.org/CRDImages/ep/original/DP-14936-045.jpg'),
('436558', 'View of Haarlem and the Haarlemmer Meer', 'Jan van Goyen', 'European Paintings', 'Purchase, 1871', 'https://images.metmuseum.org/CRDImages/ep/web-large/DP146495.jpg', 'https://images.metmuseum.org/CRDImages/ep/original/DP146495.jpg'),
('436827', 'Sunset on the Rhine', 'Barend Cornelis Koekkoek', 'European Paintings', 'Catharine Lorillard Wolfe Collection, Bequest of Catharine Lorillard Wolfe, 1887', 'https://images.metmuseum.org/CRDImages/ep/web-large/DP143198.jpg', 'https://images.metmuseum.org/CRDImages/ep/original/DP143198.jpg'),
('436833', 'Red Sunset on the Dnieper (Dnipro)', 'Arkhip Ivanovich Kuindzhi', 'European Paintings', 'Rogers Fund, 1974', 'https://images.metmuseum.org/CRDImages/ep/web-large/DT2557.jpg', 'https://images.metmuseum.org/CRDImages/ep/original/DT2557.jpg'),
('436947', 'Boating', 'Edouard Manet', 'European Paintings', 'H. O. Havemeyer Collection, Bequest of Mrs. H. O. Havemeyer, 1929', 'https://images.metmuseum.org/CRDImages/ep/web-large/DT45.jpg', 'https://images.metmuseum.org/CRDImages/ep/original/DT45.jpg'),
('437191', 'Landscape at Sunset', 'Aert van der Neer', 'European Paintings', 'Gift of J. Pierpont Morgan, 1917', 'https://images.metmuseum.org/CRDImages/ep/web-large/DP146446.jpg', 'https://images.metmuseum.org/CRDImages/ep/original/DP146446.jpg'),
('437304', 'Two Young Peasant Women', 'Camille Pissarro', 'European Paintings', 'Gift of Mr. and Mrs. Charles Wrightsman, 1973', 'https://images.metmuseum.org/CRDImages/ep/web-large/DT1860.jpg', 'https://images.metmuseum.org/CRDImages/ep/original/DT1860.jpg'),
('437310', 'The Boulevard Montmartre on a Winter Morning', 'Camille Pissarro', 'European Paintings', 'Gift of Katrin S. Vietor, in loving memory of Ernest G. Vietor, 1960', 'https://images.metmuseum.org/CRDImages/ep/web-large/DP-21959-001.jpg', 'https://images.metmuseum.org/CRDImages/ep/original/DP-21959-001.jpg'),
('437436', 'A Road in Louveciennes', 'Auguste Renoir', 'European Paintings', 'The Lesley and Emma Sheafer Collection, Bequest of Emma A. Sheafer, 1973', 'https://images.metmuseum.org/CRDImages/ep/web-large/DP265242.jpg', 'https://images.metmuseum.org/CRDImages/ep/original/DP265242.jpg'),
('437526', 'A Forest at Dawn with a Deer Hunt', 'Peter Paul Rubens', 'European Paintings', 'Purchase, The Annenberg Foundation, Mrs. Charles Wrightsman, Michel David-Weill, The Dillon Fund, Henry J. and Drue Heinz Foundation, Lola Kramarsky, Annette de la Renta, Mr. and Mrs. Arthur Ochs Sulzberger, The Vincent Astor Foundation, and Peter J. Sharp Gifts; special funds, gifts, and other gifts and bequests, by exchange, 1990', 'https://images.metmuseum.org/CRDImages/ep/web-large/DT4532.jpg', 'https://images.metmuseum.org/CRDImages/ep/original/DT4532.jpg'),
('437589', 'Ferry near Gorinchem', 'Salomon van Ruysdael', 'European Paintings', 'Bequest of Maria DeWitt Jesup, from the collection of her husband, Morris K. Jesup, 1914', 'https://images.metmuseum.org/CRDImages/ep/web-large/DP146477.jpg', 'https://images.metmuseum.org/CRDImages/ep/original/DP146477.jpg'),
('437860', 'Going Home', 'Fritz von Uhde', 'European Paintings', 'Mr. and Mrs. Isaac D. Fletcher Collection, Bequest of Isaac D. Fletcher, 1917', 'https://images.metmuseum.org/CRDImages/ep/web-large/DP-20645-001.jpg', 'https://images.metmuseum.org/CRDImages/ep/original/DP-20645-001.jpg'),
('437975', 'Sunset after a Storm on the Coast of Sicily', 'Andreas Achenbach', 'European Paintings', 'Catharine Lorillard Wolfe Collection, Bequest of Catharine Lorillard Wolfe, 1887', 'https://images.metmuseum.org/CRDImages/ep/web-large/DT12075.jpg', 'https://images.metmuseum.org/CRDImages/ep/original/DT12075.jpg'),
('437980', 'Cypresses', 'Vincent van Gogh', 'European Paintings', 'Rogers Fund, 1949', 'https://images.metmuseum.org/CRDImages/ep/web-large/DP130999.jpg', 'https://images.metmuseum.org/CRDImages/ep/original/DP130999.jpg'),
('437998', 'Olive Trees', 'Vincent van Gogh', 'European Paintings', 'The Walter H. and Leonore Annenberg Collection, Gift of Walter H. and Leonore Annenberg, 1998, Bequest of Walter H. Annenberg, 2002', 'https://images.metmuseum.org/CRDImages/ep/web-large/DT1946.jpg', 'https://images.metmuseum.org/CRDImages/ep/original/DT1946.jpg'),
('438025', 'The Holy Family with Saint John the Baptist', 'Nicolas Poussin', 'European Paintings', 'Bequest of Lore Heinemann, in memory of her husband, Dr. Rudolf J. Heinemann, 1996', 'https://images.metmuseum.org/CRDImages/ep/web-large/DP-20213-001.jpg', 'https://images.metmuseum.org/CRDImages/ep/original/DP-20213-001.jpg'),
('438643', 'Cloud Study (Distant Storm)', 'Simon Denis', 'European Paintings', 'The Whitney Collection, Gift of Wheelock Whitney III, and Purchase, Gift of Mr. and Mrs. Charles S. McVeigh, by exchange, 2003', 'https://images.metmuseum.org/CRDImages/ep/web-large/DP169448.jpg', 'https://images.metmuseum.org/CRDImages/ep/original/DP169448.jpg'),
('544214', 'Travelling Boat being Rowed', '', 'Egyptian Art', 'Rogers Fund and Edward S. Harkness Gift, 1920', 'https://images.metmuseum.org/CRDImages/eg/web-large/DP249000.jpg', 'https://images.metmuseum.org/CRDImages/eg/original/DP249000.jpg');

INSERT INTO users_artworks
  (username, artwork_id)
VALUES
('alevy', '339864'),
('alevy', '435526'),
('alevy', '437526'),
('alevy', '667895'),
('amathis', '10945'),
('amathis', '11101'),
('amathis', '11235'),
('amathis', '436558'),
('amathis', '437191'),
('amathis', '437589'),
('amathis', '438025'),
('csantana', '10159'),
('csantana', '10872'),
('csantana', '10945'),
('csantana', '435526'),
('csantana', '435773'),
('csantana', '437304'),
('csantana', '437526'),
('csantana', '667895'),
('dbeltran', '11324'),
('jkramer', '10786'),
('jkramer', '10872'),
('jkramer', '11324'),
('jkramer', '11325'),
('jkramer', '11326'),
('jkramer', '11329'),
('jkramer', '11897'),
('jkramer', '11910'),
('jkramer', '12800'),
('jkramer', '18354'),
('jkramer', '435773'),
('jkramer', '436061'),
('jkramer', '436062'),
('jkramer', '436527'),
('jkramer', '436558'),
('jkramer', '436827'),
('jkramer', '436833'),
('jkramer', '436947'),
('jkramer', '437191'),
('jkramer', '437304'),
('jkramer', '437310'),
('jkramer', '437436'),
('jkramer', '437526'),
('jkramer', '437860'),
('jkramer', '437975'),
('jkramer', '437980'),
('jkramer', '437998'),
('jkramer', '438643'),
('jkramer', '667895');
