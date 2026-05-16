CREATE DATABASE travel_agency;
USE travel_agency;

-- ============================================================
--  TABLE: bookings
--  Saved when a user clicks "Book Now" and fills out the form.
-- ============================================================

CREATE TABLE bookings (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    package_name  VARCHAR(200) NOT NULL,   -- which package they want (selected from dropdown)
    name          VARCHAR(200) NOT NULL,   -- traveler's full name
    email         VARCHAR(200) NOT NULL,   -- traveler's email
    travel_date   DATE         NOT NULL,   -- when they want to travel
    num_travelers INT DEFAULT 1,           -- how many people
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
--  TABLE: comments
--  Saved when a user leaves a comment/review on a package.
--  We did this one in a previous homework.
-- ============================================================

CREATE TABLE comments (
    id           INT AUTO_INCREMENT PRIMARY KEY,
    package_name VARCHAR(200) NOT NULL,   -- which package the comment is about
    username     VARCHAR(100) NOT NULL,   -- display name the user typed
    message      TEXT         NOT NULL,   -- the comment text
    created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
--  TABLE: contacts
--  Saved when a user sends a message through the Contact page.
-- ============================================================

CREATE TABLE contacts (
    id         INT AUTO_INCREMENT PRIMARY KEY,
    name       VARCHAR(200) NOT NULL,
    email      VARCHAR(200) NOT NULL,
    subject    VARCHAR(300),
    message    TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



INSERT INTO comments (package_name, username, message) VALUES
('Lantern Festival Experience', 'Princesa',         'This looks amazing! Who else is going? Would love to meet fellow travelers!'),
('Lantern Festival Experience', 'Estrella',         'I went last year, the lantern release gave me chills. Highly recommend!'),
('Cherry Blossom Season',       'SakuraLover',      'Cherry blossom season in Japan is a dream. Kyoto is breathtaking!'),
('Seoul & Busan Adventure',     'KoreanCultureFan', 'Seoul is my favorite city. The street food alone is worth the trip!'),
('Carnival in Rio',             'Ysabel',           'Rio Carnival is on my bucket list! Anyone want to be travel buddies?')
;









