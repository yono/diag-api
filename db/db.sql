-- CREATE DATABASE diagapi_development;
CREATE TABLE diag (
  id SERIAL,
  src text,
  note text,
  imgpath text,
  diagtype_id integer
);

CREATE TABLE diagtype (
  id SERIAL,
  name text
);
