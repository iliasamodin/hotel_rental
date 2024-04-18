INSERT INTO booking.hotels (id, name, location, stars) 
VALUES 
    (1, 'Cosmos Collection Altay Resort', 'Altai Republic, Maiminsky district, Urlu-Aspak village, Leshoznaya street, 20', 3),
    (2, 'Skala', 'Altai Republic, Maiminsky district, Barangol village, Chuyskaya street 40a', 4),
    (3, 'Aru-Kol', 'Altai Republic, Turochaksky district, Artybash village, Teletskaya street, 44a', 2),
    (4, 'Hotel Syktyvkar', 'Komi Republic, Syktyvkar, Kommunisticheskaya street, 67', 4),
    (5, 'Palace', 'Komi Republic, Syktyvkar, Pervomaiskaya street, 62', 4),
    (6, 'Bridge Resort', 'Urban village Sirius, Figurnaya street, 45', 3);
INSERT INTO booking.premium_level_varieties (id, key, name, "desc")
VALUES 
    (1, 'budget', 'Budget service', 'Minimum service for the level of the hotel to which the room belongs.'),
    (2, 'comfort', 'Comfort service', 'Average service for the level of the hotel to which the room belongs.'),
    (3, 'premium', 'Premium service', 'Premium service for the level of the hotel to which the room belongs.'),
    (4, 'presidential', 'Presidential service', 'Presidential service.');
INSERT INTO booking.rooms (id, hotel_id, premium_level_id, ordinal_number, maximum_persons, price)
VALUES
    (1, 1, 1, 1, 1, 24500),
    (2, 1, 2, 2, 2, 22450),
    (3, 2, 3, 1, 3, 4570),
    (4, 2, 2, 2, 2, 4350),
    (5, 3, 2, 1, 2, 7080),
    (6, 3, 3, 2, 3, 9815),
    (7, 4, 1, 1, 1, 4300),
    (8, 4, 3, 2, 2, 4700),
    (9, 5, 2, 1, 2, 5000),
    (10, 5, 4, 2, 4, 8000),
    (11, 6, 1, 1, 1, 8125);
INSERT INTO booking.service_varieties (id, key, name)
VALUES
    (1, 'wifi', 'Free Wi-Fi'),
    (2, 'pool', 'Swimming pool'),
    (3, 'spa', 'Availability of spa');
INSERT INTO booking.hotels_services (hotel_id, service_variety_id)
VALUES
    (1, 1),
    (2, 1),
    (2, 2),
    (3, 1),
    (3, 2),
    (4, 1),
    (4, 2),
    (5, 1),
    (5, 2),
    (5, 3);
INSERT INTO booking.rooms_services (room_id, service_variety_id)
VALUES
    (2, 1),
    (3, 1),
    (4, 1),
    (5, 1),
    (6, 1),
    (8, 1),
    (9, 1),
    (10, 1),
    (10, 2);
INSERT INTO booking.users (id, email, phone, password, first_name, last_name) 
VALUES 
    (1, 'fedor@moloko.ru', '557(535)619-59-26', 'hashed_password_1', 'Fedor', 'Smallman'),
    (2, 'sharik@moloko.ru', '67(21)225-90-27', 'hashed_password_2', 'Sharik', 'Alfdog');
INSERT INTO booking.bookings (id, user_id, room_id, number_of_persons, check_in_dt, check_out_dt, total_cost) 
VALUES
    (1, 1, 1, 1, '2023-06-15 14:00:00+05:00', '2023-06-30 12:00:00+05:00', 24500),
    (2, 2, 7, 1, '2023-06-25 14:00:00+05:00', '2023-07-10 12:00:00+05:00', 4300);