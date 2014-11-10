create extension if not exists unaccent;

create text search configuration public.film_names (parser='default');
alter text search configuration film_names alter mapping for asciiword, asciihword, hword_asciipart, hword_numpart, word, hword, numword, hword_part with unaccent, simple;
