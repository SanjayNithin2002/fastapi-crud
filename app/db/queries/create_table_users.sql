create table users (
    id UUID primary key default gen_random_uuid(), 
    first_name varchar(50) not null check(char_length(first_name) >= 1),
    last_name varchar(50) not null check(char_length(last_name) >= 1),
    age integer not null check(age >= 0 and age <= 120),
    email varchar(255) not null unique, 
    pfp_external_link TEXT null, 
    password TEXT not null,
    created_at timestamptz not null default now()
)
