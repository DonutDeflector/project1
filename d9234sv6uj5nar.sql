-- Adminer 4.6.3-dev PostgreSQL dump

\connect "d9234sv6uj5nar";

DROP TABLE IF EXISTS "check_ins";
DROP SEQUENCE IF EXISTS check_ins_id_seq;
CREATE SEQUENCE check_ins_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."check_ins" (
    "id" integer DEFAULT nextval('check_ins_id_seq') NOT NULL,
    "location_id" integer NOT NULL,
    "username" character varying NOT NULL,
    "comment" character varying NOT NULL,
    CONSTRAINT "check_ins_pkey" PRIMARY KEY ("id"),
    CONSTRAINT "check_ins_location_id_fkey" FOREIGN KEY (location_id) REFERENCES locations(id) NOT DEFERRABLE
) WITH (oids = false);


DROP TABLE IF EXISTS "locations";
DROP SEQUENCE IF EXISTS locations_id_seq;
CREATE SEQUENCE locations_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."locations" (
    "id" integer DEFAULT nextval('locations_id_seq') NOT NULL,
    "zipcode" character varying(5) NOT NULL,
    "city" character varying NOT NULL,
    "state" character varying NOT NULL,
    "lat" numeric NOT NULL,
    "long" numeric NOT NULL,
    "population" integer NOT NULL,
    CONSTRAINT "locations_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

CREATE INDEX "locations_city" ON "public"."locations" USING btree ("city");

CREATE INDEX "locations_zipcode" ON "public"."locations" USING btree ("zipcode");


DROP TABLE IF EXISTS "users";
DROP SEQUENCE IF EXISTS users_id_seq;
CREATE SEQUENCE users_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 START 1 CACHE 1;

CREATE TABLE "public"."users" (
    "id" integer DEFAULT nextval('users_id_seq') NOT NULL,
    "username" character varying NOT NULL,
    "password" character varying NOT NULL,
    CONSTRAINT "users_pkey" PRIMARY KEY ("id")
) WITH (oids = false);


-- 2018-07-11 02:59:55.281045+00
