-- database schema for library project
--
---------------------------------------------------
create table categories(
	id integer primary key autoincrement not null,
	title text not null,
	href text not null
);

-- books table
create table books(
    id integer primary key autoincrement not null,
    title text not null,
    author text,
    publisher text,
    year text,
    category integer not null references categories(id)
);
