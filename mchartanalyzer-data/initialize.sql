/*
For re-initializing an empty database.
Also serves as a reference of database schema.
*/
CREATE TABLE "ARTISTS" (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT, `name` TEXT, `source_names` TEXT, `source_urls` TEXT, `update_time` TEXT
);
CREATE TABLE `ARTIST_CALCS` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT, `artist_id` INTEGER, `num_songs` INTEGER, `num_major_keys` INTEGER, `num_minor_keys` INTEGER, `update_time` TEXT, FOREIGN KEY(`artist_id`) REFERENCES ARTISTS(id)
);
CREATE TABLE "CHARTS" (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT, `song_id` INTEGER, `source_url` TEXT, `chords_specific` TEXT, `sections` TEXT, `is_new` INTEGER, `update_time` TEXT, FOREIGN KEY(`song_id`) REFERENCES `SONGS`(`id`)
);
CREATE TABLE "CHART_CALCS" (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT, `chart_id` INTEGER UNIQUE, `keys` TEXT, `keys_certainty` TEXT, `key_chords` TEXT, `update_time` TEXT, FOREIGN KEY(`chart_id`) REFERENCES `CHARTS`(`id`)
);
CREATE TABLE `SONGS` (
  `id` INTEGER PRIMARY KEY AUTOINCREMENT, `artist_id` INTEGER, `title` TEXT, `update_time` TEXT, FOREIGN KEY(`artist_id`) REFERENCES ARTISTS(id)
);
