create database playMusica;

use playmusica;

create table musica(
	id_musica int primary key auto_increment not null,
    nome_musica varchar(50) not null,
    cantor_banda varchar(50) not null,
    genero_musica varchar(50) not null );

insert into musica (nome_musica, cantor_banda, genero_musica)
values('Paparazzi', 'Lady Gaga', 'POP');

insert into musica (nome_musica, cantor_banda, genero_musica)
values('Just Dance', 'Lady Gaga', 'POP');

insert into musica (nome_musica, cantor_banda, genero_musica)
values('Moon', 'Guerrer', 'Pop'),
('Nice', 'Guess', 'Rock'),
('leozin', 'MC leo do creu', 'Funk'),
('Where', 'Guess', 'Rock'),
('The trap', 'MC leo do creu', 'Trap'),
('Where 2', 'Dj Rob', 'Trap'),
('The trap 2', 'MC leo do creu', 'Trap'),
('The Music', 'Lady Gaga', 'Rock');

select * from musica;

select * from musica where cantor_banda = 'Lady Gaga';

select * from musica where cantor_banda like '%l%';

select * from musica where genero_musica <> 'Pop';

select * from musica where id_musica < 5;

update musica set genero_musica = 'Pop' where id_musica = 2;

delete from musica where id_musica >= 11;

/*	Comandos do Usuario  */

create table usuario(
	id_usuario int primary key auto_increment not null,
    nome_usuario varchar(50) not null,
    login_usuario varchar(20) not null,
    senha_usuario varchar(15) not null );
    
select * from usuario;

insert into usuario(nome_usuario, login_usuario, senha_usuario)
values('Igor Silva', 'igorv.gama2', 'admin');

truncate table usuario;

alter table usuario
add unique(login_usuario);

insert into usuario(nome_usuario, login_usuario, senha_usuario)
values('Igor Silva', 'igorv.gama', 'admin'),
('Geraldo Augusto', 'geraldo.aug', '123'),
('Igor Gama', 'ig.gama', 'admin'),
('Robet', 'robet_shc', '147812588aA'),
('Fernando', 'fef.fefes', 'admin');

delete from usuario where id_usuario = 11;