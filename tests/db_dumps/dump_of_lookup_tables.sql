INSERT INTO booking.premium_level_varieties (id, key, name, "desc")
VALUES 
    (1, 'budget', 'Budget service', 'Minimum service for the level of the hotel to which the room belongs.'),
    (2, 'comfort', 'Comfort service', 'Average service for the level of the hotel to which the room belongs.'),
    (3, 'premium', 'Premium service', 'Premium service for the level of the hotel to which the room belongs.'),
    (4, 'presidential', 'Presidential service', 'Presidential service.');
INSERT INTO booking.service_varieties (id, key, name)
VALUES
    (1, 'wifi', 'Free Wi-Fi'),
    (2, 'pool', 'Swimming pool'),
    (3, 'spa', 'Availability of spa');