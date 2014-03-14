--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO pgadmin;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: pgadmin
--

CREATE SEQUENCE auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO pgadmin;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pgadmin
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO pgadmin;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: pgadmin
--

CREATE SEQUENCE auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO pgadmin;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pgadmin
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO pgadmin;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: pgadmin
--

CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO pgadmin;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pgadmin
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE TABLE auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone NOT NULL,
    is_superuser boolean NOT NULL,
    username character varying(30) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(75) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE public.auth_user OWNER TO pgadmin;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO pgadmin;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: pgadmin
--

CREATE SEQUENCE auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO pgadmin;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pgadmin
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: pgadmin
--

CREATE SEQUENCE auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO pgadmin;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pgadmin
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO pgadmin;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: pgadmin
--

CREATE SEQUENCE auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO pgadmin;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pgadmin
--

ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;


--
-- Name: countries; Type: TABLE; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE TABLE countries (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    name_orig character varying(255) NOT NULL,
    description text NOT NULL
);


ALTER TABLE public.countries OWNER TO pgadmin;

--
-- Name: countries_id_seq; Type: SEQUENCE; Schema: public; Owner: pgadmin
--

CREATE SEQUENCE countries_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.countries_id_seq OWNER TO pgadmin;

--
-- Name: countries_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pgadmin
--

ALTER SEQUENCE countries_id_seq OWNED BY countries.id;


--
-- Name: csvimport_csvimport; Type: TABLE; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE TABLE csvimport_csvimport (
    id integer NOT NULL,
    model_name character varying(255) NOT NULL,
    field_list character varying(255) NOT NULL,
    upload_file character varying(100) NOT NULL,
    file_name character varying(255) NOT NULL,
    encoding character varying(32) NOT NULL,
    upload_method character varying(50) NOT NULL,
    error_log text NOT NULL,
    import_date date NOT NULL,
    import_user character varying(255) NOT NULL
);


ALTER TABLE public.csvimport_csvimport OWNER TO pgadmin;

--
-- Name: csvimport_csvimport_id_seq; Type: SEQUENCE; Schema: public; Owner: pgadmin
--

CREATE SEQUENCE csvimport_csvimport_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.csvimport_csvimport_id_seq OWNER TO pgadmin;

--
-- Name: csvimport_csvimport_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pgadmin
--

ALTER SEQUENCE csvimport_csvimport_id_seq OWNED BY csvimport_csvimport.id;


--
-- Name: csvimport_importmodel; Type: TABLE; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE TABLE csvimport_importmodel (
    id integer NOT NULL,
    csvimport_id integer NOT NULL,
    numeric_id integer NOT NULL,
    natural_key character varying(100) NOT NULL,
    CONSTRAINT csvimport_importmodel_numeric_id_check CHECK ((numeric_id >= 0))
);


ALTER TABLE public.csvimport_importmodel OWNER TO pgadmin;

--
-- Name: csvimport_importmodel_id_seq; Type: SEQUENCE; Schema: public; Owner: pgadmin
--

CREATE SEQUENCE csvimport_importmodel_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.csvimport_importmodel_id_seq OWNER TO pgadmin;

--
-- Name: csvimport_importmodel_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pgadmin
--

ALTER SEQUENCE csvimport_importmodel_id_seq OWNED BY csvimport_importmodel.id;


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE TABLE django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    user_id integer NOT NULL,
    content_type_id integer,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE public.django_admin_log OWNER TO pgadmin;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: pgadmin
--

CREATE SEQUENCE django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_admin_log_id_seq OWNER TO pgadmin;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pgadmin
--

ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO pgadmin;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: pgadmin
--

CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.django_content_type_id_seq OWNER TO pgadmin;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pgadmin
--

ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO pgadmin;

--
-- Name: films; Type: TABLE; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE TABLE films (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    ftype character varying(255) NOT NULL,
    frelease_date date NOT NULL,
    fduration integer,
    fbudget integer,
    description text NOT NULL,
    rating_local double precision,
    rating_local_cnt smallint,
    rating_imdb double precision,
    rating_imdb_cnt integer,
    kinopoisk_id integer,
    age_limit smallint,
    kinopoisk_lastupdate timestamp with time zone,
    rating_kinopoisk double precision,
    rating_kinopoisk_cnt smallint,
    seasons_cnt smallint,
    name_orig character varying(255) NOT NULL,
    CONSTRAINT films_age_limit_check CHECK ((age_limit >= 0)),
    CONSTRAINT films_rating_kinopoisk_cnt_check CHECK ((rating_kinopoisk_cnt >= 0)),
    CONSTRAINT films_rating_local_cnt_check CHECK ((rating_local_cnt >= 0)),
    CONSTRAINT films_seasons_cnt_check CHECK ((seasons_cnt >= 0))
);


ALTER TABLE public.films OWNER TO pgadmin;

--
-- Name: films_countries; Type: TABLE; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE TABLE films_countries (
    id integer NOT NULL,
    films_id integer NOT NULL,
    countries_id integer NOT NULL
);


ALTER TABLE public.films_countries OWNER TO pgadmin;

--
-- Name: films_countries_id_seq; Type: SEQUENCE; Schema: public; Owner: pgadmin
--

CREATE SEQUENCE films_countries_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.films_countries_id_seq OWNER TO pgadmin;

--
-- Name: films_countries_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pgadmin
--

ALTER SEQUENCE films_countries_id_seq OWNED BY films_countries.id;


--
-- Name: films_extras; Type: TABLE; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE TABLE films_extras (
    id integer NOT NULL,
    film_id integer NOT NULL,
    etype character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    name_orig character varying(255) NOT NULL,
    description text NOT NULL,
    url character varying(255) NOT NULL
);


ALTER TABLE public.films_extras OWNER TO pgadmin;

--
-- Name: films_extras_id_seq; Type: SEQUENCE; Schema: public; Owner: pgadmin
--

CREATE SEQUENCE films_extras_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.films_extras_id_seq OWNER TO pgadmin;

--
-- Name: films_extras_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pgadmin
--

ALTER SEQUENCE films_extras_id_seq OWNED BY films_extras.id;


--
-- Name: films_genres; Type: TABLE; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE TABLE films_genres (
    id integer NOT NULL,
    films_id integer NOT NULL,
    genres_id integer NOT NULL
);


ALTER TABLE public.films_genres OWNER TO pgadmin;

--
-- Name: films_genres_id_seq; Type: SEQUENCE; Schema: public; Owner: pgadmin
--

CREATE SEQUENCE films_genres_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.films_genres_id_seq OWNER TO pgadmin;

--
-- Name: films_genres_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pgadmin
--

ALTER SEQUENCE films_genres_id_seq OWNED BY films_genres.id;


--
-- Name: films_id_seq; Type: SEQUENCE; Schema: public; Owner: pgadmin
--

CREATE SEQUENCE films_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.films_id_seq OWNER TO pgadmin;

--
-- Name: films_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pgadmin
--

ALTER SEQUENCE films_id_seq OWNED BY films.id;


--
-- Name: genres; Type: TABLE; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE TABLE genres (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    description text NOT NULL
);


ALTER TABLE public.genres OWNER TO pgadmin;

--
-- Name: genres_id_seq; Type: SEQUENCE; Schema: public; Owner: pgadmin
--

CREATE SEQUENCE genres_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.genres_id_seq OWNER TO pgadmin;

--
-- Name: genres_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pgadmin
--

ALTER SEQUENCE genres_id_seq OWNED BY genres.id;


--
-- Name: persons; Type: TABLE; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE TABLE persons (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    name_orig character varying(255) NOT NULL,
    bio text NOT NULL,
    photo character varying(100)
);


ALTER TABLE public.persons OWNER TO pgadmin;

--
-- Name: persons_extras; Type: TABLE; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE TABLE persons_extras (
    id integer NOT NULL,
    person_id integer NOT NULL,
    etype character varying(255) NOT NULL,
    name text NOT NULL,
    name_orig text NOT NULL,
    description text NOT NULL,
    url character varying(255) NOT NULL
);


ALTER TABLE public.persons_extras OWNER TO pgadmin;

--
-- Name: persons_extras_id_seq; Type: SEQUENCE; Schema: public; Owner: pgadmin
--

CREATE SEQUENCE persons_extras_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.persons_extras_id_seq OWNER TO pgadmin;

--
-- Name: persons_extras_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pgadmin
--

ALTER SEQUENCE persons_extras_id_seq OWNED BY persons_extras.id;


--
-- Name: persons_id_seq; Type: SEQUENCE; Schema: public; Owner: pgadmin
--

CREATE SEQUENCE persons_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.persons_id_seq OWNER TO pgadmin;

--
-- Name: persons_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pgadmin
--

ALTER SEQUENCE persons_id_seq OWNED BY persons.id;


--
-- Name: robots; Type: TABLE; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE TABLE robots (
    name character varying(255) NOT NULL,
    description text NOT NULL,
    last_start timestamp with time zone NOT NULL,
    next_start timestamp with time zone NOT NULL,
    rstatus integer NOT NULL
);


ALTER TABLE public.robots OWNER TO pgadmin;

--
-- Name: robots_log; Type: TABLE; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE TABLE robots_log (
    id integer NOT NULL,
    robot_name_id character varying(255) NOT NULL,
    created timestamp with time zone NOT NULL,
    value character varying(255) NOT NULL,
    itype integer NOT NULL
);


ALTER TABLE public.robots_log OWNER TO pgadmin;

--
-- Name: robots_log_id_seq; Type: SEQUENCE; Schema: public; Owner: pgadmin
--

CREATE SEQUENCE robots_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.robots_log_id_seq OWNER TO pgadmin;

--
-- Name: robots_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pgadmin
--

ALTER SEQUENCE robots_log_id_seq OWNED BY robots_log.id;


--
-- Name: seasons; Type: TABLE; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE TABLE seasons (
    id integer NOT NULL,
    film_id integer NOT NULL,
    release_date timestamp with time zone NOT NULL,
    series_cnt smallint NOT NULL,
    description text NOT NULL,
    number smallint NOT NULL,
    CONSTRAINT seasons_number_check CHECK ((number >= 0)),
    CONSTRAINT seasons_series_cnt_check CHECK ((series_cnt >= 0))
);


ALTER TABLE public.seasons OWNER TO pgadmin;

--
-- Name: seasons_id_seq; Type: SEQUENCE; Schema: public; Owner: pgadmin
--

CREATE SEQUENCE seasons_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.seasons_id_seq OWNER TO pgadmin;

--
-- Name: seasons_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pgadmin
--

ALTER SEQUENCE seasons_id_seq OWNED BY seasons.id;


--
-- Name: south_migrationhistory; Type: TABLE; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE TABLE south_migrationhistory (
    id integer NOT NULL,
    app_name character varying(255) NOT NULL,
    migration character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE public.south_migrationhistory OWNER TO pgadmin;

--
-- Name: south_migrationhistory_id_seq; Type: SEQUENCE; Schema: public; Owner: pgadmin
--

CREATE SEQUENCE south_migrationhistory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.south_migrationhistory_id_seq OWNER TO pgadmin;

--
-- Name: south_migrationhistory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pgadmin
--

ALTER SEQUENCE south_migrationhistory_id_seq OWNED BY south_migrationhistory.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE TABLE users (
    id integer NOT NULL,
    firstname character varying(255) NOT NULL,
    lastname character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    password character varying(255) NOT NULL,
    last_visited timestamp with time zone NOT NULL,
    created timestamp with time zone NOT NULL,
    ustatus smallint NOT NULL,
    userpic_type character varying(255),
    userpic_id integer,
    CONSTRAINT users_ustatus_check CHECK ((ustatus >= 0))
);


ALTER TABLE public.users OWNER TO pgadmin;

--
-- Name: users_films; Type: TABLE; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE TABLE users_films (
    id integer NOT NULL,
    user_id integer NOT NULL,
    film_id integer NOT NULL,
    ufstatus integer NOT NULL,
    ufrating integer NOT NULL,
    subscribed integer NOT NULL
);


ALTER TABLE public.users_films OWNER TO pgadmin;

--
-- Name: users_films_id_seq; Type: SEQUENCE; Schema: public; Owner: pgadmin
--

CREATE SEQUENCE users_films_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_films_id_seq OWNER TO pgadmin;

--
-- Name: users_films_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pgadmin
--

ALTER SEQUENCE users_films_id_seq OWNED BY users_films.id;


--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: pgadmin
--

CREATE SEQUENCE users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO pgadmin;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pgadmin
--

ALTER SEQUENCE users_id_seq OWNED BY users.id;


--
-- Name: users_logs; Type: TABLE; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE TABLE users_logs (
    id integer NOT NULL,
    user_id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    itype character varying(255) NOT NULL,
    iobject character varying(255) NOT NULL,
    itext character varying(255) NOT NULL
);


ALTER TABLE public.users_logs OWNER TO pgadmin;

--
-- Name: users_logs_id_seq; Type: SEQUENCE; Schema: public; Owner: pgadmin
--

CREATE SEQUENCE users_logs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_logs_id_seq OWNER TO pgadmin;

--
-- Name: users_logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pgadmin
--

ALTER SEQUENCE users_logs_id_seq OWNED BY users_logs.id;


--
-- Name: users_persons; Type: TABLE; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE TABLE users_persons (
    id integer NOT NULL,
    user_id integer NOT NULL,
    person_id integer NOT NULL,
    upstatus integer NOT NULL,
    subscribed integer NOT NULL
);


ALTER TABLE public.users_persons OWNER TO pgadmin;

--
-- Name: users_persons_id_seq; Type: SEQUENCE; Schema: public; Owner: pgadmin
--

CREATE SEQUENCE users_persons_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_persons_id_seq OWNER TO pgadmin;

--
-- Name: users_persons_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pgadmin
--

ALTER SEQUENCE users_persons_id_seq OWNED BY users_persons.id;


--
-- Name: users_pics; Type: TABLE; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE TABLE users_pics (
    id integer NOT NULL,
    user_id integer NOT NULL,
    url character varying(255) NOT NULL
);


ALTER TABLE public.users_pics OWNER TO pgadmin;

--
-- Name: users_pics_id_seq; Type: SEQUENCE; Schema: public; Owner: pgadmin
--

CREATE SEQUENCE users_pics_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_pics_id_seq OWNER TO pgadmin;

--
-- Name: users_pics_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pgadmin
--

ALTER SEQUENCE users_pics_id_seq OWNED BY users_pics.id;


--
-- Name: users_rels; Type: TABLE; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE TABLE users_rels (
    id integer NOT NULL,
    user_id integer NOT NULL,
    user_rel_id integer NOT NULL,
    rel_type character varying(255) NOT NULL,
    updated timestamp with time zone NOT NULL
);


ALTER TABLE public.users_rels OWNER TO pgadmin;

--
-- Name: users_rels_id_seq; Type: SEQUENCE; Schema: public; Owner: pgadmin
--

CREATE SEQUENCE users_rels_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_rels_id_seq OWNER TO pgadmin;

--
-- Name: users_rels_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pgadmin
--

ALTER SEQUENCE users_rels_id_seq OWNED BY users_rels.id;


--
-- Name: users_requests; Type: TABLE; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE TABLE users_requests (
    id integer NOT NULL,
    user_id integer NOT NULL,
    hash integer NOT NULL,
    created timestamp with time zone NOT NULL,
    rtype character varying(255) NOT NULL,
    value character varying(255) NOT NULL
);


ALTER TABLE public.users_requests OWNER TO pgadmin;

--
-- Name: users_requests_id_seq; Type: SEQUENCE; Schema: public; Owner: pgadmin
--

CREATE SEQUENCE users_requests_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_requests_id_seq OWNER TO pgadmin;

--
-- Name: users_requests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pgadmin
--

ALTER SEQUENCE users_requests_id_seq OWNED BY users_requests.id;


--
-- Name: users_socials; Type: TABLE; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE TABLE users_socials (
    id integer NOT NULL,
    user_id integer NOT NULL,
    stype character varying(255) NOT NULL,
    stoken character varying(255) NOT NULL,
    suserid integer NOT NULL,
    created timestamp with time zone NOT NULL,
    sphoto integer NOT NULL
);


ALTER TABLE public.users_socials OWNER TO pgadmin;

--
-- Name: users_socials_id_seq; Type: SEQUENCE; Schema: public; Owner: pgadmin
--

CREATE SEQUENCE users_socials_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_socials_id_seq OWNER TO pgadmin;

--
-- Name: users_socials_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: pgadmin
--

ALTER SEQUENCE users_socials_id_seq OWNED BY users_socials.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY countries ALTER COLUMN id SET DEFAULT nextval('countries_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY csvimport_csvimport ALTER COLUMN id SET DEFAULT nextval('csvimport_csvimport_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY csvimport_importmodel ALTER COLUMN id SET DEFAULT nextval('csvimport_importmodel_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY films ALTER COLUMN id SET DEFAULT nextval('films_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY films_countries ALTER COLUMN id SET DEFAULT nextval('films_countries_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY films_extras ALTER COLUMN id SET DEFAULT nextval('films_extras_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY films_genres ALTER COLUMN id SET DEFAULT nextval('films_genres_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY genres ALTER COLUMN id SET DEFAULT nextval('genres_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY persons ALTER COLUMN id SET DEFAULT nextval('persons_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY persons_extras ALTER COLUMN id SET DEFAULT nextval('persons_extras_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY robots_log ALTER COLUMN id SET DEFAULT nextval('robots_log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY seasons ALTER COLUMN id SET DEFAULT nextval('seasons_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY south_migrationhistory ALTER COLUMN id SET DEFAULT nextval('south_migrationhistory_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('users_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY users_films ALTER COLUMN id SET DEFAULT nextval('users_films_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY users_logs ALTER COLUMN id SET DEFAULT nextval('users_logs_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY users_persons ALTER COLUMN id SET DEFAULT nextval('users_persons_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY users_pics ALTER COLUMN id SET DEFAULT nextval('users_pics_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY users_rels ALTER COLUMN id SET DEFAULT nextval('users_rels_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY users_requests ALTER COLUMN id SET DEFAULT nextval('users_requests_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY users_socials ALTER COLUMN id SET DEFAULT nextval('users_socials_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: pgadmin
--

COPY auth_group (id, name) FROM stdin;
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pgadmin
--

SELECT pg_catalog.setval('auth_group_id_seq', 1, false);


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: pgadmin
--

COPY auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pgadmin
--

SELECT pg_catalog.setval('auth_group_permissions_id_seq', 1, false);


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: pgadmin
--

COPY auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can add permission	2	add_permission
5	Can change permission	2	change_permission
6	Can delete permission	2	delete_permission
7	Can add group	3	add_group
8	Can change group	3	change_group
9	Can delete group	3	delete_group
10	Can add user	4	add_user
11	Can change user	4	change_user
12	Can delete user	4	delete_user
13	Can add content type	5	add_contenttype
14	Can change content type	5	change_contenttype
15	Can delete content type	5	delete_contenttype
16	Can add session	6	add_session
17	Can change session	6	change_session
18	Can delete session	6	delete_session
19	Can add migration history	7	add_migrationhistory
20	Can change migration history	7	change_migrationhistory
21	Can delete migration history	7	delete_migrationhistory
22	Can add csv import	8	add_csvimport
23	Can change csv import	8	change_csvimport
24	Can delete csv import	8	delete_csvimport
25	Can add import model	9	add_importmodel
26	Can change import model	9	change_importmodel
27	Can delete import model	9	delete_importmodel
28	Can add Отношения пользователей	10	add_usersrels
29	Can change Отношения пользователей	10	change_usersrels
30	Can delete Отношения пользователей	10	delete_usersrels
31	Can add Пользователь	11	add_users
32	Can change Пользователь	11	change_users
33	Can delete Пользователь	11	delete_users
34	Can add Запросы пользователя	12	add_usersrequests
35	Can change Запросы пользователя	12	change_usersrequests
36	Can delete Запросы пользователя	12	delete_usersrequests
37	Can add Лог пользователя	13	add_userslog
38	Can change Лог пользователя	13	change_userslog
39	Can delete Лог пользователя	13	delete_userslog
40	Can add Картинки пользователя	14	add_userspics
41	Can change Картинки пользователя	14	change_userspics
42	Can delete Картинки пользователя	14	delete_userspics
43	Can add Социальность пользователя	15	add_userssocial
44	Can change Социальность пользователя	15	change_userssocial
45	Can delete Социальность пользователя	15	delete_userssocial
46	Can add Персона	16	add_persons
47	Can change Персона	16	change_persons
48	Can delete Персона	16	delete_persons
49	Can add Расширения персоны	17	add_personsextras
50	Can change Расширения персоны	17	change_personsextras
51	Can delete Расширения персоны	17	delete_personsextras
52	Can add Расширения персоны	18	add_userspersons
53	Can change Расширения персоны	18	change_userspersons
54	Can delete Расширения персоны	18	delete_userspersons
55	Can add Робот	19	add_robots
56	Can change Робот	19	change_robots
57	Can delete Робот	19	delete_robots
58	Can add Логирование робота	20	add_robotslog
59	Can change Логирование робота	20	change_robotslog
60	Can delete Логирование робота	20	delete_robotslog
61	Can add Страна	21	add_countries
62	Can change Страна	21	change_countries
63	Can delete Страна	21	delete_countries
64	Can add Жанр	22	add_genres
65	Can change Жанр	22	change_genres
66	Can delete Жанр	22	delete_genres
67	Can add Фильм	23	add_films
68	Can change Фильм	23	change_films
69	Can delete Фильм	23	delete_films
70	Can add Дополнительный материал	24	add_filmextras
71	Can change Дополнительный материал	24	change_filmextras
72	Can delete Дополнительный материал	24	delete_filmextras
73	Can add Связь Фильм-Пользователь	25	add_usersfilms
74	Can change Связь Фильм-Пользователь	25	change_usersfilms
75	Can delete Связь Фильм-Пользователь	25	delete_usersfilms
76	Can add Сезон	26	add_seasons
77	Can change Сезон	26	change_seasons
78	Can delete Сезон	26	delete_seasons
\.


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pgadmin
--

SELECT pg_catalog.setval('auth_permission_id_seq', 78, true);


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: pgadmin
--

COPY auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	pbkdf2_sha256$12000$aw3CTpsrmCws$nTr2BJ92eGBr4gRSDbaSvR/rlQxwhbPwPCFL2/KrTgE=	2014-03-14 16:51:21.302072+04	t	admin			tumani1@yandex.ru	t	t	2014-03-14 16:51:21.302072+04
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: pgadmin
--

COPY auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pgadmin
--

SELECT pg_catalog.setval('auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pgadmin
--

SELECT pg_catalog.setval('auth_user_id_seq', 1, true);


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: pgadmin
--

COPY auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pgadmin
--

SELECT pg_catalog.setval('auth_user_user_permissions_id_seq', 1, false);


--
-- Data for Name: countries; Type: TABLE DATA; Schema: public; Owner: pgadmin
--

COPY countries (id, name, name_orig, description) FROM stdin;
\.


--
-- Name: countries_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pgadmin
--

SELECT pg_catalog.setval('countries_id_seq', 1, false);


--
-- Data for Name: csvimport_csvimport; Type: TABLE DATA; Schema: public; Owner: pgadmin
--

COPY csvimport_csvimport (id, model_name, field_list, upload_file, file_name, encoding, upload_method, error_log, import_date, import_user) FROM stdin;
\.


--
-- Name: csvimport_csvimport_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pgadmin
--

SELECT pg_catalog.setval('csvimport_csvimport_id_seq', 1, false);


--
-- Data for Name: csvimport_importmodel; Type: TABLE DATA; Schema: public; Owner: pgadmin
--

COPY csvimport_importmodel (id, csvimport_id, numeric_id, natural_key) FROM stdin;
\.


--
-- Name: csvimport_importmodel_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pgadmin
--

SELECT pg_catalog.setval('csvimport_importmodel_id_seq', 1, false);


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: pgadmin
--

COPY django_admin_log (id, action_time, user_id, content_type_id, object_id, object_repr, action_flag, change_message) FROM stdin;
\.


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pgadmin
--

SELECT pg_catalog.setval('django_admin_log_id_seq', 1, false);


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: pgadmin
--

COPY django_content_type (id, name, app_label, model) FROM stdin;
1	log entry	admin	logentry
2	permission	auth	permission
3	group	auth	group
4	user	auth	user
5	content type	contenttypes	contenttype
6	session	sessions	session
7	migration history	south	migrationhistory
8	csv import	csvimport	csvimport
9	import model	csvimport	importmodel
10	Отношения пользователей	users	usersrels
11	Пользователь	users	users
12	Запросы пользователя	users	usersrequests
13	Лог пользователя	users	userslog
14	Картинки пользователя	users	userspics
15	Социальность пользователя	users	userssocial
16	Персона	users	persons
17	Расширения персоны	users	personsextras
18	Расширения персоны	users	userspersons
19	Робот	robots	robots
20	Логирование робота	robots	robotslog
21	Страна	films	countries
22	Жанр	films	genres
23	Фильм	films	films
24	Дополнительный материал	films	filmextras
25	Связь Фильм-Пользователь	films	usersfilms
26	Сезон	films	seasons
\.


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pgadmin
--

SELECT pg_catalog.setval('django_content_type_id_seq', 26, true);


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: pgadmin
--

COPY django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- Data for Name: films; Type: TABLE DATA; Schema: public; Owner: pgadmin
--

COPY films (id, name, ftype, frelease_date, fduration, fbudget, description, rating_local, rating_local_cnt, rating_imdb, rating_imdb_cnt, kinopoisk_id, age_limit, kinopoisk_lastupdate, rating_kinopoisk, rating_kinopoisk_cnt, seasons_cnt, name_orig) FROM stdin;
\.


--
-- Data for Name: films_countries; Type: TABLE DATA; Schema: public; Owner: pgadmin
--

COPY films_countries (id, films_id, countries_id) FROM stdin;
\.


--
-- Name: films_countries_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pgadmin
--

SELECT pg_catalog.setval('films_countries_id_seq', 1, false);


--
-- Data for Name: films_extras; Type: TABLE DATA; Schema: public; Owner: pgadmin
--

COPY films_extras (id, film_id, etype, name, name_orig, description, url) FROM stdin;
\.


--
-- Name: films_extras_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pgadmin
--

SELECT pg_catalog.setval('films_extras_id_seq', 1, false);


--
-- Data for Name: films_genres; Type: TABLE DATA; Schema: public; Owner: pgadmin
--

COPY films_genres (id, films_id, genres_id) FROM stdin;
\.


--
-- Name: films_genres_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pgadmin
--

SELECT pg_catalog.setval('films_genres_id_seq', 1, false);


--
-- Name: films_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pgadmin
--

SELECT pg_catalog.setval('films_id_seq', 1, false);


--
-- Data for Name: genres; Type: TABLE DATA; Schema: public; Owner: pgadmin
--

COPY genres (id, name, description) FROM stdin;
\.


--
-- Name: genres_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pgadmin
--

SELECT pg_catalog.setval('genres_id_seq', 1, false);


--
-- Data for Name: persons; Type: TABLE DATA; Schema: public; Owner: pgadmin
--

COPY persons (id, name, name_orig, bio, photo) FROM stdin;
\.


--
-- Data for Name: persons_extras; Type: TABLE DATA; Schema: public; Owner: pgadmin
--

COPY persons_extras (id, person_id, etype, name, name_orig, description, url) FROM stdin;
\.


--
-- Name: persons_extras_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pgadmin
--

SELECT pg_catalog.setval('persons_extras_id_seq', 1, false);


--
-- Name: persons_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pgadmin
--

SELECT pg_catalog.setval('persons_id_seq', 1, false);


--
-- Data for Name: robots; Type: TABLE DATA; Schema: public; Owner: pgadmin
--

COPY robots (name, description, last_start, next_start, rstatus) FROM stdin;
\.


--
-- Data for Name: robots_log; Type: TABLE DATA; Schema: public; Owner: pgadmin
--

COPY robots_log (id, robot_name_id, created, value, itype) FROM stdin;
\.


--
-- Name: robots_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pgadmin
--

SELECT pg_catalog.setval('robots_log_id_seq', 1, false);


--
-- Data for Name: seasons; Type: TABLE DATA; Schema: public; Owner: pgadmin
--

COPY seasons (id, film_id, release_date, series_cnt, description, number) FROM stdin;
\.


--
-- Name: seasons_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pgadmin
--

SELECT pg_catalog.setval('seasons_id_seq', 1, false);


--
-- Data for Name: south_migrationhistory; Type: TABLE DATA; Schema: public; Owner: pgadmin
--

COPY south_migrationhistory (id, app_name, migration, applied) FROM stdin;
1	django_extensions	0001_empty	2014-03-14 16:51:36.929829+04
2	users	0001_initial	2014-03-14 16:51:38.509475+04
3	robots	0001_initial	2014-03-14 16:51:39.274241+04
4	films	0001_initial	2014-03-14 16:51:40.988262+04
\.


--
-- Name: south_migrationhistory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pgadmin
--

SELECT pg_catalog.setval('south_migrationhistory_id_seq', 4, true);


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: pgadmin
--

COPY users (id, firstname, lastname, email, password, last_visited, created, ustatus, userpic_type, userpic_id) FROM stdin;
1	qwerty	qwerty	tumani1@yandex.ru	1234556	2014-03-13 13:53:40+04	2014-03-13 13:53:40+04	1	1	\N
\.


--
-- Data for Name: users_films; Type: TABLE DATA; Schema: public; Owner: pgadmin
--

COPY users_films (id, user_id, film_id, ufstatus, ufrating, subscribed) FROM stdin;
\.


--
-- Name: users_films_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pgadmin
--

SELECT pg_catalog.setval('users_films_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pgadmin
--

SELECT pg_catalog.setval('users_id_seq', 1, true);


--
-- Data for Name: users_logs; Type: TABLE DATA; Schema: public; Owner: pgadmin
--

COPY users_logs (id, user_id, created, itype, iobject, itext) FROM stdin;
\.


--
-- Name: users_logs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pgadmin
--

SELECT pg_catalog.setval('users_logs_id_seq', 1, false);


--
-- Data for Name: users_persons; Type: TABLE DATA; Schema: public; Owner: pgadmin
--

COPY users_persons (id, user_id, person_id, upstatus, subscribed) FROM stdin;
\.


--
-- Name: users_persons_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pgadmin
--

SELECT pg_catalog.setval('users_persons_id_seq', 1, false);


--
-- Data for Name: users_pics; Type: TABLE DATA; Schema: public; Owner: pgadmin
--

COPY users_pics (id, user_id, url) FROM stdin;
\.


--
-- Name: users_pics_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pgadmin
--

SELECT pg_catalog.setval('users_pics_id_seq', 1, false);


--
-- Data for Name: users_rels; Type: TABLE DATA; Schema: public; Owner: pgadmin
--

COPY users_rels (id, user_id, user_rel_id, rel_type, updated) FROM stdin;
\.


--
-- Name: users_rels_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pgadmin
--

SELECT pg_catalog.setval('users_rels_id_seq', 1, false);


--
-- Data for Name: users_requests; Type: TABLE DATA; Schema: public; Owner: pgadmin
--

COPY users_requests (id, user_id, hash, created, rtype, value) FROM stdin;
\.


--
-- Name: users_requests_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pgadmin
--

SELECT pg_catalog.setval('users_requests_id_seq', 1, false);


--
-- Data for Name: users_socials; Type: TABLE DATA; Schema: public; Owner: pgadmin
--

COPY users_socials (id, user_id, stype, stoken, suserid, created, sphoto) FROM stdin;
\.


--
-- Name: users_socials_id_seq; Type: SEQUENCE SET; Schema: public; Owner: pgadmin
--

SELECT pg_catalog.setval('users_socials_id_seq', 1, false);


--
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions_group_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_key UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission_content_type_id_codename_key; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_key UNIQUE (content_type_id, codename);


--
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_user_id_group_id_key; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_key UNIQUE (user_id, group_id);


--
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_user_id_permission_id_key; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_key UNIQUE (user_id, permission_id);


--
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: countries_pkey; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY countries
    ADD CONSTRAINT countries_pkey PRIMARY KEY (id);


--
-- Name: csvimport_csvimport_pkey; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY csvimport_csvimport
    ADD CONSTRAINT csvimport_csvimport_pkey PRIMARY KEY (id);


--
-- Name: csvimport_importmodel_pkey; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY csvimport_importmodel
    ADD CONSTRAINT csvimport_importmodel_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type_app_label_model_key; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_key UNIQUE (app_label, model);


--
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: films_countries_films_id_697f68618a81adc4_uniq; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY films_countries
    ADD CONSTRAINT films_countries_films_id_697f68618a81adc4_uniq UNIQUE (films_id, countries_id);


--
-- Name: films_countries_pkey; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY films_countries
    ADD CONSTRAINT films_countries_pkey PRIMARY KEY (id);


--
-- Name: films_extras_pkey; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY films_extras
    ADD CONSTRAINT films_extras_pkey PRIMARY KEY (id);


--
-- Name: films_genres_films_id_786da3a7ac3c7014_uniq; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY films_genres
    ADD CONSTRAINT films_genres_films_id_786da3a7ac3c7014_uniq UNIQUE (films_id, genres_id);


--
-- Name: films_genres_pkey; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY films_genres
    ADD CONSTRAINT films_genres_pkey PRIMARY KEY (id);


--
-- Name: films_pkey; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY films
    ADD CONSTRAINT films_pkey PRIMARY KEY (id);


--
-- Name: genres_pkey; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY genres
    ADD CONSTRAINT genres_pkey PRIMARY KEY (id);


--
-- Name: persons_extras_pkey; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY persons_extras
    ADD CONSTRAINT persons_extras_pkey PRIMARY KEY (id);


--
-- Name: persons_pkey; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY persons
    ADD CONSTRAINT persons_pkey PRIMARY KEY (id);


--
-- Name: robots_log_pkey; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY robots_log
    ADD CONSTRAINT robots_log_pkey PRIMARY KEY (id);


--
-- Name: robots_pkey; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY robots
    ADD CONSTRAINT robots_pkey PRIMARY KEY (name);


--
-- Name: seasons_film_id_d7c0afc8b6d3cb9_uniq; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY seasons
    ADD CONSTRAINT seasons_film_id_d7c0afc8b6d3cb9_uniq UNIQUE (film_id, number);


--
-- Name: seasons_pkey; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY seasons
    ADD CONSTRAINT seasons_pkey PRIMARY KEY (id);


--
-- Name: south_migrationhistory_pkey; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY south_migrationhistory
    ADD CONSTRAINT south_migrationhistory_pkey PRIMARY KEY (id);


--
-- Name: users_email_key; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users_films_pkey; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY users_films
    ADD CONSTRAINT users_films_pkey PRIMARY KEY (id);


--
-- Name: users_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY users_logs
    ADD CONSTRAINT users_logs_pkey PRIMARY KEY (id);


--
-- Name: users_persons_pkey; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY users_persons
    ADD CONSTRAINT users_persons_pkey PRIMARY KEY (id);


--
-- Name: users_pics_pkey; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY users_pics
    ADD CONSTRAINT users_pics_pkey PRIMARY KEY (id);


--
-- Name: users_pkey; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users_rels_pkey; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY users_rels
    ADD CONSTRAINT users_rels_pkey PRIMARY KEY (id);


--
-- Name: users_requests_pkey; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY users_requests
    ADD CONSTRAINT users_requests_pkey PRIMARY KEY (id);


--
-- Name: users_socials_pkey; Type: CONSTRAINT; Schema: public; Owner: pgadmin; Tablespace: 
--

ALTER TABLE ONLY users_socials
    ADD CONSTRAINT users_socials_pkey PRIMARY KEY (id);


--
-- Name: auth_group_name_like; Type: INDEX; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE INDEX auth_group_name_like ON auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id; Type: INDEX; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE INDEX auth_group_permissions_group_id ON auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id; Type: INDEX; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE INDEX auth_group_permissions_permission_id ON auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id; Type: INDEX; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE INDEX auth_permission_content_type_id ON auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id; Type: INDEX; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE INDEX auth_user_groups_group_id ON auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id; Type: INDEX; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE INDEX auth_user_groups_user_id ON auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id; Type: INDEX; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_permission_id ON auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id; Type: INDEX; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_user_id ON auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_like; Type: INDEX; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE INDEX auth_user_username_like ON auth_user USING btree (username varchar_pattern_ops);


--
-- Name: csvimport_importmodel_csvimport_id; Type: INDEX; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE INDEX csvimport_importmodel_csvimport_id ON csvimport_importmodel USING btree (csvimport_id);


--
-- Name: django_admin_log_content_type_id; Type: INDEX; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE INDEX django_admin_log_content_type_id ON django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id; Type: INDEX; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE INDEX django_admin_log_user_id ON django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date; Type: INDEX; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE INDEX django_session_expire_date ON django_session USING btree (expire_date);


--
-- Name: django_session_session_key_like; Type: INDEX; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE INDEX django_session_session_key_like ON django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: films_countries_countries_id; Type: INDEX; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE INDEX films_countries_countries_id ON films_countries USING btree (countries_id);


--
-- Name: films_countries_films_id; Type: INDEX; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE INDEX films_countries_films_id ON films_countries USING btree (films_id);


--
-- Name: films_extras_film_id; Type: INDEX; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE INDEX films_extras_film_id ON films_extras USING btree (film_id);


--
-- Name: films_genres_films_id; Type: INDEX; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE INDEX films_genres_films_id ON films_genres USING btree (films_id);


--
-- Name: films_genres_genres_id; Type: INDEX; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE INDEX films_genres_genres_id ON films_genres USING btree (genres_id);


--
-- Name: persons_extras_person_id; Type: INDEX; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE INDEX persons_extras_person_id ON persons_extras USING btree (person_id);


--
-- Name: robots_log_robot_name_id; Type: INDEX; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE INDEX robots_log_robot_name_id ON robots_log USING btree (robot_name_id);


--
-- Name: robots_log_robot_name_id_like; Type: INDEX; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE INDEX robots_log_robot_name_id_like ON robots_log USING btree (robot_name_id varchar_pattern_ops);


--
-- Name: robots_name_like; Type: INDEX; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE INDEX robots_name_like ON robots USING btree (name varchar_pattern_ops);


--
-- Name: seasons_film_id; Type: INDEX; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE INDEX seasons_film_id ON seasons USING btree (film_id);


--
-- Name: users_email_like; Type: INDEX; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE INDEX users_email_like ON users USING btree (email varchar_pattern_ops);


--
-- Name: users_films_film_id; Type: INDEX; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE INDEX users_films_film_id ON users_films USING btree (film_id);


--
-- Name: users_films_user_id; Type: INDEX; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE INDEX users_films_user_id ON users_films USING btree (user_id);


--
-- Name: users_logs_user_id; Type: INDEX; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE INDEX users_logs_user_id ON users_logs USING btree (user_id);


--
-- Name: users_persons_person_id; Type: INDEX; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE INDEX users_persons_person_id ON users_persons USING btree (person_id);


--
-- Name: users_persons_user_id; Type: INDEX; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE INDEX users_persons_user_id ON users_persons USING btree (user_id);


--
-- Name: users_pics_user_id; Type: INDEX; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE INDEX users_pics_user_id ON users_pics USING btree (user_id);


--
-- Name: users_rels_user_id; Type: INDEX; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE INDEX users_rels_user_id ON users_rels USING btree (user_id);


--
-- Name: users_rels_user_rel_id; Type: INDEX; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE INDEX users_rels_user_rel_id ON users_rels USING btree (user_rel_id);


--
-- Name: users_requests_user_id; Type: INDEX; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE INDEX users_requests_user_id ON users_requests USING btree (user_id);


--
-- Name: users_socials_user_id; Type: INDEX; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE INDEX users_socials_user_id ON users_socials USING btree (user_id);


--
-- Name: users_userpic_id; Type: INDEX; Schema: public; Owner: pgadmin; Tablespace: 
--

CREATE INDEX users_userpic_id ON users USING btree (userpic_id);


--
-- Name: auth_group_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_fkey FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: content_type_id_refs_id_93d2d1f8; Type: FK CONSTRAINT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT content_type_id_refs_id_93d2d1f8 FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: content_type_id_refs_id_d043b34a; Type: FK CONSTRAINT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT content_type_id_refs_id_d043b34a FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: countries_id_refs_id_bd771ca7; Type: FK CONSTRAINT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY films_countries
    ADD CONSTRAINT countries_id_refs_id_bd771ca7 FOREIGN KEY (countries_id) REFERENCES countries(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: csvimport_importmodel_csvimport_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY csvimport_importmodel
    ADD CONSTRAINT csvimport_importmodel_csvimport_id_fkey FOREIGN KEY (csvimport_id) REFERENCES csvimport_csvimport(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: film_id_refs_id_44e62927; Type: FK CONSTRAINT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY seasons
    ADD CONSTRAINT film_id_refs_id_44e62927 FOREIGN KEY (film_id) REFERENCES films(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: film_id_refs_id_b4e67790; Type: FK CONSTRAINT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY films_extras
    ADD CONSTRAINT film_id_refs_id_b4e67790 FOREIGN KEY (film_id) REFERENCES films(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: film_id_refs_id_f61d2690; Type: FK CONSTRAINT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY users_films
    ADD CONSTRAINT film_id_refs_id_f61d2690 FOREIGN KEY (film_id) REFERENCES films(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: films_id_refs_id_0a32f7f2; Type: FK CONSTRAINT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY films_genres
    ADD CONSTRAINT films_id_refs_id_0a32f7f2 FOREIGN KEY (films_id) REFERENCES films(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: films_id_refs_id_7c2aa0d5; Type: FK CONSTRAINT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY films_countries
    ADD CONSTRAINT films_id_refs_id_7c2aa0d5 FOREIGN KEY (films_id) REFERENCES films(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: genres_id_refs_id_a6661e9d; Type: FK CONSTRAINT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY films_genres
    ADD CONSTRAINT genres_id_refs_id_a6661e9d FOREIGN KEY (genres_id) REFERENCES genres(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: group_id_refs_id_f4b32aac; Type: FK CONSTRAINT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT group_id_refs_id_f4b32aac FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: person_id_refs_id_521b7954; Type: FK CONSTRAINT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY users_persons
    ADD CONSTRAINT person_id_refs_id_521b7954 FOREIGN KEY (person_id) REFERENCES persons(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: person_id_refs_id_5ebd47d7; Type: FK CONSTRAINT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY persons_extras
    ADD CONSTRAINT person_id_refs_id_5ebd47d7 FOREIGN KEY (person_id) REFERENCES persons(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: robot_name_id_refs_name_7743cc8e; Type: FK CONSTRAINT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY robots_log
    ADD CONSTRAINT robot_name_id_refs_name_7743cc8e FOREIGN KEY (robot_name_id) REFERENCES robots(name) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_1375fe71; Type: FK CONSTRAINT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY users_logs
    ADD CONSTRAINT user_id_refs_id_1375fe71 FOREIGN KEY (user_id) REFERENCES users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_16d1a555; Type: FK CONSTRAINT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY users_pics
    ADD CONSTRAINT user_id_refs_id_16d1a555 FOREIGN KEY (user_id) REFERENCES users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_40c41112; Type: FK CONSTRAINT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT user_id_refs_id_40c41112 FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_4dc23c39; Type: FK CONSTRAINT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT user_id_refs_id_4dc23c39 FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_533186e8; Type: FK CONSTRAINT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY users_persons
    ADD CONSTRAINT user_id_refs_id_533186e8 FOREIGN KEY (user_id) REFERENCES users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_571187ab; Type: FK CONSTRAINT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY users_requests
    ADD CONSTRAINT user_id_refs_id_571187ab FOREIGN KEY (user_id) REFERENCES users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_bd11dfad; Type: FK CONSTRAINT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY users_films
    ADD CONSTRAINT user_id_refs_id_bd11dfad FOREIGN KEY (user_id) REFERENCES users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_c0d12874; Type: FK CONSTRAINT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT user_id_refs_id_c0d12874 FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_c83f9f4b; Type: FK CONSTRAINT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY users_socials
    ADD CONSTRAINT user_id_refs_id_c83f9f4b FOREIGN KEY (user_id) REFERENCES users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_e1908a29; Type: FK CONSTRAINT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY users_rels
    ADD CONSTRAINT user_id_refs_id_e1908a29 FOREIGN KEY (user_id) REFERENCES users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_rel_id_refs_id_e1908a29; Type: FK CONSTRAINT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY users_rels
    ADD CONSTRAINT user_rel_id_refs_id_e1908a29 FOREIGN KEY (user_rel_id) REFERENCES users(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: userpic_id_refs_id_52f925e4; Type: FK CONSTRAINT; Schema: public; Owner: pgadmin
--

ALTER TABLE ONLY users
    ADD CONSTRAINT userpic_id_refs_id_52f925e4 FOREIGN KEY (userpic_id) REFERENCES users_pics(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

