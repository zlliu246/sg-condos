CREATE DATABASE IF NOT EXISTS house_data;
USE house_data;

DROP TABLE IF EXISTS districts;
CREATE TABLE districts (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `district` INT,
    `postal_sectors` VARCHAR(255),
    `description` VARCHAR(255)
);

INSERT INTO districts (`district`, `postal_sectors`, `description`) VALUES
    (1, '01,02,03,04,05,06', "raffles place cecil marina people's park"),
    (2, '07,08', 'anson tanjong pagar'),
    (3, '14,15,16', 'queenstown tiong bahru'),
    (4, '09,10', 'telok blangah harbourfront'),
    (5, '11,12,13', 'pasir panjang hong leong garden clementi new town'),
    (6, '17', 'high street beach road (part)'),
    (7, '18,19', 'middle road golden mile'),
    (8, '20,21', 'little india'),
    (9, '22,23', 'orchard cairnhill river valley'),
    (10, '24,25,26,27', 'ardmore bukit timah holland road tanglin'),
    (11, '28,29,30', 'watten estate novena thomson'),
    (12, '31,32,33', 'balestier toa payoh serangoon'),
    (13, '34,35,36,37', 'macpherson braddell'),
    (14, '38,39,40,41', 'geylang eunos'),
    (15, '42,43,44,45', 'katong joo chiat amber road'),
    (16, '46,47,48', 'bedok upper east coast eastwood kew drive'),
    (17, '49,50,81', 'loyang changi'),
    (18, '51,52', 'tampines pasir ris'),
    (19, '53,54,55,82', 'serangoon garden hougang punggol'),
    (20, '56,57', 'bishan ang mo kio'),
    (21, '58,59', 'upper bukit timah clementi park ulu pandan'),
    (22, '60,61,62,63,64', 'jurong'),
    (23, '65,66,67,68', 'hillview dairy farm bukit panjang choa chu kang'),
    (24, '69,70,71', 'lim chu kang tengah'),
    (25, '72,73', 'kranji woodgrove'),
    (26, '77,78', 'upper thomson springleaf'),
    (27, '75,76', 'yishun sembawang'),
    (28, '79,80', 'seletar')
;