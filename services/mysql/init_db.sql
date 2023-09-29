CREATE DATABASE IF NOT EXISTS site_vendas;
use site_vendas;

create table signup(
id_usuario int primary key auto_increment,
nome varchar(100) not null,
telefone varchar(100) not null,
email varchar (100) not null,
senha varchar (100) not null
)ENGINE=MyISAM DEFAULT CHARSET=latin1