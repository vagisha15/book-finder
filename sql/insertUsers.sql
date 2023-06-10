CREATE TABLE if not exists user_data (
    username TEXT PRIMARY KEY,
    email TEXT UNIQUE,
    password TEXT,
    status TEXT CHECK (status IN ('active', 'inactive', 'disabled')),
    role TEXT CHECK(role IN ('admin','user')),
    register_time TEXT
);

DELETE FROM user_data;

INSERT INTO user_data VALUES('user_free','test@gmail.com','$2b$12$E2h35wKPuFb3Vr8uC6Du8uzukmu0f2wM44uzm.UthGjKzKHEiMZNK','active','user','2023-04-27 19:34:57.473330-04:00');

INSERT INTO user_data VALUES('damg7245','damg@gmail.com','$2b$12$yJ/iddK8UQjzx0oC3M/WteYutgmtGgub8uukDPZHj4gkk69hN97Jy','active','admin','2023-04-27 19:34:57.473330-04:00');


select * from users;

INSERT INTO users (username, password,email,fname,lname) VALUES ("thejasbh","admin123","thejas@gmail.com","Thejas","Bharadwaj")

