create table tournaments(
    id serial primary key,
    ema_id int not null,
    name text not null,
    place text not null,
    country text not null,
    date date not null,
    players int not null,
    mers_weight numeric(2,1) not null,
    mukrs_days int not null,
    excluded_from_ingestion boolean not null default false,
    ingested_on timestamp with time zone not null default now(),
    is_latest boolean not null default true
);

create table players(
    id serial primary key,
    ema_number text unique,
    first_name text not null,
    last_name text not null,
    country text not null
);

create table tournament_results(
    tournament_id int not null,
    player_id int not null,
    base_rank int not null,
    primary key (tournament_id, player_id),
    foreign key (tournament_id) references tournaments(id) on delete cascade,
    foreign key (player_id) references players(id) on delete cascade
);