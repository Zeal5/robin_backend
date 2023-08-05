BEGIN;

CREATE SEQUENCE IF NOT EXISTS keys_id_seq;
CREATE SEQUENCE IF NOT EXISTS users_id_seq;

CREATE TABLE IF NOT EXISTS public.keys
(
    id integer NOT NULL DEFAULT nextval('keys_id_seq'::regclass),
    user_id bigint,
    key_name character varying COLLATE pg_catalog."default",
    key_value character varying COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT keys_pkey PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.users
(
    id integer NOT NULL DEFAULT nextval('users_id_seq'::regclass),
    tg_id bigint NOT NULL,
    subscribed boolean,
    tester boolean,
    CONSTRAINT users_pkey PRIMARY KEY (id),
    CONSTRAINT users_tg_id_key UNIQUE (tg_id)
);

ALTER TABLE IF EXISTS public.keys
    ADD CONSTRAINT keys_user_id_fkey FOREIGN KEY (user_id)
    REFERENCES public.users (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE NO ACTION;

END;

