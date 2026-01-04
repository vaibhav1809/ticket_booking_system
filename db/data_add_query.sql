BEGIN;

-- ------------------------------------------------------------
-- 0) Reset (drop data only)
-- ------------------------------------------------------------
TRUNCATE TABLE
  tickets,
  payments,
  bookings,
  inventories,
  show_pricings,
  shows,
  venue_seats,
  venue_sections,
  events,
  venues,
  users
RESTART IDENTITY CASCADE;

-- ------------------------------------------------------------
-- 1) Users (few dummy accounts)
-- ------------------------------------------------------------
INSERT INTO users (email_id, phone, first_name, last_name, password_hash)
VALUES
  ('aarav.sharma@example.com',  '9000000001', 'Aarav',  'Sharma',  '\xDEADBEEF'::bytea),
  ('diya.iyer@example.com',     '9000000002', 'Diya',   'Iyer',    '\xDEADBEEF'::bytea),
  ('kabir.mehta@example.com',   '9000000003', 'Kabir',  'Mehta',   '\xDEADBEEF'::bytea),
  ('ananya.nair@example.com',   '9000000004', 'Ananya', 'Nair',    '\xDEADBEEF'::bytea),
  ('rohan.kulkarni@example.com','9000000005', 'Rohan',  'Kulkarni','\xDEADBEEF'::bytea);

-- ------------------------------------------------------------
-- 2) Venues (Bangalore + Mumbai only)
-- ------------------------------------------------------------
INSERT INTO venues (name, location, city, country, pincode, address)
VALUES
  ('PVR: Phoenix Marketcity', 'Whitefield',     'Bangalore', 'India', '560048', 'Phoenix Marketcity, Whitefield Main Rd'),
  ('INOX: Orion Mall',        'Rajajinagar',    'Bangalore', 'India', '560055', 'Orion Mall, Dr Rajkumar Rd'),
  ('PVR: Juhu',               'Juhu',           'Mumbai',    'India', '400049', 'Juhu Tara Rd, Juhu'),
  ('NCPA: Tata Theatre',      'Nariman Point',  'Mumbai',    'India', '400021', 'NCPA Marg, Nariman Point');

-- ------------------------------------------------------------
-- 3) Venue Sections (Silver/Gold/Platinum per venue)
-- ------------------------------------------------------------
INSERT INTO venue_sections (venue_id, name, "order")
SELECT v.venue_id, s.name, s.ord
FROM venues v
CROSS JOIN (VALUES
  ('Silver', 1),
  ('Gold', 2),
  ('Platinum', 3)
) AS s(name, ord);

-- ------------------------------------------------------------
-- 4) Venue Seats: 5 rows x 12 cols per venue (60 seats)
--    Section mapping by columns:
--      1-4   => Silver
--      5-8   => Gold
--      9-12  => Platinum
-- ------------------------------------------------------------
WITH section_map AS (
  SELECT
    vs.venue_id,
    MAX(CASE WHEN vs.name = 'Silver'   THEN vs.section_id END) AS silver_section_id,
    MAX(CASE WHEN vs.name = 'Gold'     THEN vs.section_id END) AS gold_section_id,
    MAX(CASE WHEN vs.name = 'Platinum' THEN vs.section_id END) AS platinum_section_id
  FROM venue_sections vs
  GROUP BY vs.venue_id
),
grid AS (
  SELECT
    v.venue_id,
    r AS row_nums,
    c AS col_nums
  FROM venues v
  CROSS JOIN generate_series(1, 5) AS r
  CROSS JOIN generate_series(1, 12) AS c
)
INSERT INTO venue_seats (section_id, row_nums, col_nums)
SELECT
  CASE
    WHEN g.col_nums BETWEEN 1 AND 4  THEN sm.silver_section_id
    WHEN g.col_nums BETWEEN 5 AND 8  THEN sm.gold_section_id
    ELSE sm.platinum_section_id
  END AS section_id,
  g.row_nums,
  g.col_nums
FROM grid g
JOIN section_map sm ON sm.venue_id = g.venue_id;

-- ------------------------------------------------------------
-- 5) Events (20: mix of MOVIE + CONCERT; India audience)
--    event_type enum: ('movie','concert','theatre','sport') in your schema
-- ------------------------------------------------------------
INSERT INTO events (event_type, duration_min, title, language, genre, created_on, created_by, last_updated_at)
VALUES
  -- Movies
  ('movie',   165, 'Pushpa 2: The Rule',            'Telugu',  'Action',     now(), 1, now()),
  ('movie',   155, 'Stree 2',                       'Hindi',   'Horror-Comedy', now(), 1, now()),
  ('movie',   170, 'Fighter',                       'Hindi',   'Action',     now(), 1, now()),
  ('movie',   160, 'Animal',                        'Hindi',   'Crime',      now(), 1, now()),
  ('movie',   175, 'Jawan',                         'Hindi',   'Action',     now(), 1, now()),
  ('movie',   150, '12th Fail',                     'Hindi',   'Drama',      now(), 1, now()),
  ('movie',   170, 'Salaar',                        'Kannada', 'Action',     now(), 1, now()),
  ('movie',   180, 'Kalki 2898 AD',                 'Telugu',  'Sci-Fi',     now(), 1, now()),
  ('movie',   145, 'Laapataa Ladies',               'Hindi',   'Comedy-Drama', now(), 1, now()),
  ('movie',   155, 'Sita Ramam (Re-release)',       'Telugu',  'Romance',    now(), 1, now()),
  ('movie',   160, 'Brahmastra (IMAX Special)',     'Hindi',   'Fantasy',    now(), 1, now()),
  ('movie',   150, 'Kantara (Re-release)',          'Kannada', 'Thriller',   now(), 1, now()),

  -- Concerts
  ('concert', 120, 'Arijit Singh Live',             'Hindi',   'Live Music', now(), 1, now()),
  ('concert', 120, 'Shreya Ghoshal Live',           'Hindi',   'Live Music', now(), 1, now()),
  ('concert', 120, 'Divine - Gully Tour',           'Hindi',   'Hip-Hop',    now(), 1, now()),
  ('concert', 120, 'Ritviz - Chill Vibes',          'Hindi',   'Electronic', now(), 1, now()),
  ('concert', 120, 'Prateek Kuhad Unplugged',       'Hindi',   'Indie',      now(), 1, now()),
  ('concert', 120, 'A.R. Rahman Tribute Night',     'Tamil',   'Orchestral', now(), 1, now()),
  ('concert', 120, 'Coke Studio Bharat Live',       'Hindi',   'Fusion',     now(), 1, now()),
  ('concert', 120, 'Sunburn Mini - City Edition',   'English', 'EDM',        now(), 1, now());

-- ------------------------------------------------------------
-- 6) Shows: 2 shows per event (one Bangalore, one Mumbai)
--    show status enum: ('draft','live','sold_out','cancelled')
-- ------------------------------------------------------------
WITH e AS (
  SELECT event_id, event_type
  FROM events
  ORDER BY event_id
),
blr_venues AS (
  SELECT venue_id FROM venues WHERE city = 'Bangalore' ORDER BY venue_id
),
mum_venues AS (
  SELECT venue_id FROM venues WHERE city = 'Mumbai' ORDER BY venue_id
),
chosen AS (
  SELECT
    e.event_id,
    -- alternate venues within the city by event_id
    (SELECT venue_id FROM blr_venues OFFSET ((e.event_id - 1) % 2) LIMIT 1) AS blr_venue_id,
    (SELECT venue_id FROM mum_venues OFFSET ((e.event_id - 1) % 2) LIMIT 1) AS mum_venue_id
  FROM e
)
INSERT INTO shows (event_id, venue_id, start_time, end_time, status)
SELECT
  c.event_id,
  c.blr_venue_id,
  -- Bangalore show: date shifts by event_id
  (timestamp with time zone '2026-01-10 18:30:00+05:30' + ((c.event_id - 1) * interval '1 day')) AS start_time,
  (timestamp with time zone '2026-01-10 21:00:00+05:30' + ((c.event_id - 1) * interval '1 day')) AS end_time,
  'live'::show_type AS status
FROM chosen c
UNION ALL
SELECT
  c.event_id,
  c.mum_venue_id,
  -- Mumbai show: same event next day, slightly later time
  (timestamp with time zone '2026-01-11 19:30:00+05:30' + ((c.event_id - 1) * interval '1 day')) AS start_time,
  (timestamp with time zone '2026-01-11 22:00:00+05:30' + ((c.event_id - 1) * interval '1 day')) AS end_time,
  'live'::show_type AS status
FROM chosen c;

-- ------------------------------------------------------------
-- 7) Show Pricings: 3 rows per show (Silver/Gold/Platinum)
--    Bangalore cheaper than Mumbai
-- ------------------------------------------------------------
INSERT INTO show_pricings (show_id, section_id, amount, currency)
SELECT
  s.show_id,
  vs.section_id,
  CASE
    WHEN v.city = 'Bangalore' AND vs.name = 'Silver'   THEN 250
    WHEN v.city = 'Bangalore' AND vs.name = 'Gold'     THEN 450
    WHEN v.city = 'Bangalore' AND vs.name = 'Platinum' THEN 700
    WHEN v.city = 'Mumbai'    AND vs.name = 'Silver'   THEN 300
    WHEN v.city = 'Mumbai'    AND vs.name = 'Gold'     THEN 550
    WHEN v.city = 'Mumbai'    AND vs.name = 'Platinum' THEN 900
    ELSE 400
  END AS amount,
  'INR' AS currency
FROM shows s
JOIN venues v ON v.venue_id = s.venue_id
JOIN venue_sections vs ON vs.venue_id = v.venue_id;

-- ------------------------------------------------------------
-- 8) Inventories: 1 row per (show_id, seat_id)
--    Includes price/currency copied from show_pricings per seat's section
-- ------------------------------------------------------------
INSERT INTO inventories (show_id, seat_id, status, booked_by, price, currency)
SELECT
  s.show_id,
  seat.seat_id,
  'available'::inventory_status AS status,
  NULL::int4 AS booked_by,
  sp.amount AS price,
  sp.currency
FROM shows s
JOIN venues v ON v.venue_id = s.venue_id
JOIN venue_sections vs ON vs.venue_id = v.venue_id
JOIN venue_seats seat ON seat.section_id = vs.section_id
JOIN show_pricings sp ON sp.show_id = s.show_id AND sp.section_id = vs.section_id;

COMMIT;

-- Quick sanity checks (optional)
-- SELECT count(*) AS venues      FROM venues;
-- SELECT count(*) AS sections    FROM venue_sections;
-- SELECT count(*) AS seats       FROM venue_seats;
-- SELECT count(*) AS events      FROM events;
-- SELECT count(*) AS shows       FROM shows;
-- SELECT count(*) AS show_prices FROM show_pricings;
-- SELECT count(*) AS inventory   FROM inventories;