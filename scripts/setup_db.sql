create user bitespeed_user with password 'bitespeed1234';
drop database IF EXISTS fluxkart_customer_db;
drop database IF EXISTS fluxkart_customer_test_db;
create database fluxkart_customer_db owner bitespeed_user;
create database fluxkart_customer_test_db owner bitespeed_user;