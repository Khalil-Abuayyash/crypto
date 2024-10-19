# crypto

#creating Tables:

CREATE TABLE coin ( 
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE prediction (
    id INT AUTO_INCREMENT PRIMARY KEY,
    coin_id INT NOT NULL,
    type ENUM('long', 'short') NOT NULL,
    predicted_at BIGINT NOT NULL,
    verified_at BIGINT,
    is_succeeded TINYINT(1) DEFAULT 0,
    FOREIGN KEY (coin_id) REFERENCES coin(id), 
    CHECK (verified_at >= predicted_at)
);
