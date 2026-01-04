DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO public;

CREATE TABLE "venues" (
  "venue_id" SERIAL,
  "name" varchar(50),
  "location" varchar(20),
  "city" varchar(20),
  "country" varchar(20),
  "pincode" varchar(6),
  "address" varchar(100),
  PRIMARY KEY ("venue_id")
);

CREATE TABLE "venue_sections" (
  "section_id" SERIAL,
  "venue_id" int4,
  "name" varchar(20),
  "order" int2,
  PRIMARY KEY ("section_id"),
  CONSTRAINT "FK_venue_sections_venue_id"
    FOREIGN KEY ("venue_id")
      REFERENCES "venues"("venue_id")
);

CREATE TABLE "users" (
  "user_id" SERIAL,
  "email_id" varchar(20) unique,
  "phone" varchar(20) unique,
  "first_name" varchar(50),
  "last_name" varchar(50),
  "password_hash" bytea,
  PRIMARY KEY ("user_id")
);

CREATE TYPE event_type AS ENUM ('movie', 'concert', 'theatre', 'sport');
CREATE TABLE "events" (
  "event_id" SERIAL,
  "event_type" event_type,
  "duration_min" int4,
  "title" varchar(100),
  "language" varchar(20),
  "genre" varchar(20),
  "created_on" timestamptz,
  "created_by" int4,
  "last_updated_at" timestamptz,
  PRIMARY KEY ("event_id"),
  CONSTRAINT "FK_events_created_by"
    FOREIGN KEY ("created_by")
      REFERENCES "users"("user_id")
);

CREATE TYPE show_type AS ENUM ('draft', 'live', 'sold_out', 'cancelled');
CREATE TABLE "shows" (
  "show_id" SERIAL,
  "event_id" int4,
  "venue_id" int4,
  "start_time" timestamptz,
  "end_time" timestamptz,
  "status" show_type,
  PRIMARY KEY ("show_id"),
  CONSTRAINT "FK_shows_event_id"
    FOREIGN KEY ("event_id")
      REFERENCES "events"("event_id"),
  CONSTRAINT "FK_shows_venue_id"
    FOREIGN KEY ("venue_id")
      REFERENCES "venues"("venue_id")
);

CREATE TABLE "venue_seats" (
  "seat_id" SERIAL,
  "section_id" int4,
  "row_nums" int4,
  "col_nums" int4,
  PRIMARY KEY ("seat_id"),
  CONSTRAINT "FK_venue_seats_section_id"
    FOREIGN KEY ("section_id")
      REFERENCES "venue_sections"("section_id")
);

CREATE TYPE payment_provider AS ENUM ('upi', 'credit-card', 'debit-card');
CREATE TYPE payment_status AS ENUM ('pending', 'success', 'failed');
CREATE TABLE "payments" (
  "payment_id" SERIAL,
  "booking_id" int4,
  "provider" payment_provider,
  "status" payment_status,
  "amount" int4,
  "currency" varchar(3),
  "created_at" timestamptz,
  PRIMARY KEY ("payment_id")
);

CREATE TABLE "show_pricings" (
  "show_id" SERIAL,
  "section_id" int4,
  "amount" int4,
  "currency" varchar(3),
  CONSTRAINT "FK_show_pricings_section_id"
    FOREIGN KEY ("section_id")
      REFERENCES "venue_sections"("section_id")
);

CREATE TYPE inventory_status AS ENUM ('available', 'booked', 'not_available');
CREATE TABLE "inventories" (
  "show_id" int4,
  "seat_id" int4,
  "status" inventory_status,
  "booked_by" int4,
  "price" int4,
  "currency" varchar(3),
  CONSTRAINT "FK_inventories_seat_id"
    FOREIGN KEY ("seat_id")
      REFERENCES "venue_seats"("seat_id"),
  CONSTRAINT "FK_inventories_booked_by"
    FOREIGN KEY ("booked_by")
      REFERENCES "users"("user_id"),
  CONSTRAINT "FK_inventories_show_id"
    FOREIGN KEY ("show_id")
      REFERENCES "shows"("show_id")
);

CREATE TYPE booking_status AS ENUM ('initiated', 'confirmed', 'cancelled', 'expired');
CREATE TABLE "bookings" (
  "booking_id" SERIAL,
  "user_id" int4,
  "show_id" int4,
  "status" booking_status,
  "confirnmed_at" timestamptz,
  PRIMARY KEY ("booking_id"),
  CONSTRAINT "FK_bookings_user_id"
    FOREIGN KEY ("user_id")
      REFERENCES "users"("user_id")
);

CREATE TYPE ticket_status AS ENUM ('active', 'cancelled', 'used');
CREATE TABLE "tickets" (
  "ticket_id" SERIAL,
  "booking_id" int4,
  "seat_id" int4,
  "ticket_code" varchar(20) unique,
  "qr_payload" text,
  "issued_at" timestamptz,
  "status" ticket_status,
  "used_at" timestamptz,
  PRIMARY KEY ("ticket_id"),
  CONSTRAINT "FK_tickets_seat_id"
    FOREIGN KEY ("seat_id")
      REFERENCES "venue_seats"("seat_id"),
  CONSTRAINT "FK_tickets_booking_id"
    FOREIGN KEY ("booking_id")
      REFERENCES "bookings"("booking_id")
);