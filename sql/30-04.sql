
-- get data

select * from  users; -- all columns

select user_id, name from users; -- columns

-- conditions
-- user id 1 data

select * from users where user_id = 1;


select * from users where user_id = 2;

select * from users where user_id > 10;

-- select * from conversations where conv_id = '2b7e8bec-79d5-466f-8bed-d9ba59f3bf5a';

-- multiple conditions -> login  email, password

select * from users where email='dilip@ss.co' and pword='14587452'  ; -- rows -> each row filter 

-- data insert

-- insert into users(`name`, `email`, `pword`) values ('Bhavitya', 'contact@bhavitya.ai', '12345678'  );

select * from users;

-- update data

select * from users where email='dd@ss.co' and pword='12154'; -- login

select  *  from users where email='dd@ss.co';

update users set pword = 'abcd1234', name='DDD' where email='dd@ss.coo';

-- delete

delete from users where email='dd@ss.co'; 










