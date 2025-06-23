# Part III. Compose

Pour la fin de ce TP on va manipuler un peu `docker compose`.

C'est vitre **très très chiant** de lancer plein de conteneurs manuellement (avec `docker run` ou une UI) dès qu'on a des conteneurs qui dépendent d'autres.

Genre une app et sa db comme ma `meow-api`. **Pour éviter ça, on peut utiliser `docker compose` qui permet de lancer plusieurs conteneurs en même temps.**

![Not enough](./img/not_enough.jpg)

## Index

- [Part III. Compose](#part-iii-compose)
  - [Index](#index)
- [I. Getting started](#i-getting-started)
  - [1. Run it](#1-run-it)
  - [2. What about networking](#2-what-about-networking)
- [II. A working meow-api](#ii-a-working-meow-api)
  - [1. Rédigez la structure du docker-compose.yml](#1-rédigez-la-structure-du-docker-composeyml)
  - [2. L'image MySQL officielle](#2-limage-mysql-officielle)
  - [3. Seed](#3-seed)
  - [4. Build automatisé](#4-build-automatisé)
  - [5. Variables d'environnement](#5-variables-denvironnement)
  - [6. Rendu attendu](#6-rendu-attendu)

# I. Getting started

## 1. Run it

🌞 **Créez un fichier `docker-compose.yml`**

- dans un nouveau dossier dédié
- le contenu est le suivant :

```yml
version: "3"

services:
  conteneur_nul:
    image: debian
    entrypoint: sleep 9999
  conteneur_flopesque:
    image: debian
    entrypoint: sleep 9999
```

Ce fichier est ~~presque~~ parfaitement équivalent à l'enchaînement de commandes suivantes (*ne les faites pas hein*, c'est juste pour expliquer) :

```bash
$ docker network create compose_test
$ docker run --name conteneur_nul --network compose_test debian sleep 9999
$ docker run --name conteneur_flopesque --network compose_test debian sleep 9999
```

```
juliangabry@MacBook-Air-24 part3 % nano docker-compose.yml

juliangabry@MacBook-Air-24 b3e-docker-avance % docker network create compose_test
e138fd89f14c240aa28efbfe3f85a67da473d126fc23c04a628300040147f78f
```

> Très chiant à taper ces commandes, et encore, c'est des `docker run` simples.

🌞 **Lancez les deux conteneurs** avec `docker compose`

- déplacez-vous dans le dossier `compose_test` qui contient le fichier `docker-compose.yml`
- go exécuter `docker compose up -d`

> Si tu mets pas le `-d` tu vas perdre la main dans ton terminal, et tu auras les logs des deux conteneurs. `-d` comme *daemon* : pour lancer en tâche de fond.

```
mkdir compose_test
cd compose_test

juliangabry@MacBook-Air-24 compose_test % docker compose up -d
WARN[0000] /Users/juliangabry/Desktop/Efrei/docker avancé/part3/b3e-docker-avance/docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion 
[+] Running 3/3
 ✔ Network b3e-docker-avance_default                  Created                                                                       0.0s 
 ✔ Container b3e-docker-avance-conteneur_flopesque-1  Started                                                                       0.3s 
 ✔ Container b3e-docker-avance-conteneur_nul-1        Started  
```

🌞 **Vérifier que les deux conteneurs tournent**

- toujours avec une commande `docker`
- tu peux aussi use des trucs comme `docker compose ps` ou `docker compose top` qui sont cools dukoo
  - `docker compose --help` pour voir les bails

```
juliangabry@MacBook-Air-24 compose_test % docker ps
CONTAINER ID   IMAGE     COMMAND        CREATED              STATUS              PORTS     NAMES
83ed53ed2691   debian    "sleep 9999"   22 seconds ago       Up 22 seconds                 b3e-docker-avance-conteneur_flopesque-1
15a78671e415   debian    "sleep 9999"   22 seconds ago       Up 22 seconds                 b3e-docker-avance-conteneur_nul-1
db3f9337d7c8   debian    "sleep 9999"   About a minute ago   Up About a minute             conteneur_flopesque
54c79f3c5148   debian    "sleep 9999"   3 minutes ago        Up 3 minutes                  conteneur_nul

juliangabry@MacBook-Air-24 compose_test % docker compose ps
WARN[0000] /Users/juliangabry/Desktop/Efrei/docker avancé/part3/b3e-docker-avance/docker-compose.yml: the attribute `version` is obsolete, it will be ignored, please remove it to avoid potential confusion 
NAME                                      IMAGE     COMMAND        SERVICE               CREATED          STATUS          PORTS
b3e-docker-avance-conteneur_flopesque-1   debian    "sleep 9999"   conteneur_flopesque   29 seconds ago   Up 29 seconds   
b3e-docker-avance-conteneur_nul-1         debian    "sleep 9999"   conteneur_nul         29 seconds ago   Up 29 seconds   
juliangabry@MacBook-Air-24 compose_test  
```

## 2. What about networking

🌞 **Pop un shell dans le conteneur `conteneur_nul`**

- référez-vous au mémo Docker
- effectuez un `ping conteneur_flopesque` (ouais ouais, avec ce nom là)
  - un conteneur est aussi léger que possible, aucun programme/fichier superflu : t'auras pas la commande `ping` !
  - il faudra installer un paquet qui fournit la commande `ping` pour pouvoir tester
  - juste pour te faire remarquer que les conteneurs ont pas besoin de connaître leurs IP : les noms fonctionnent
  
```
root@54c79f3c5148:/# apt update && apt install -y iputils-ping
Get:1 http://deb.debian.org/debian bookworm InRelease [151 kB]
Get:2 http://deb.debian.org/debian bookworm-updates InRelease [55.4 kB]
Get:3 http://deb.debian.org/debian-security bookworm-security InRelease [48.0 kB]
Get:4 http://deb.debian.org/debian bookworm/main arm64 Packages [8693 kB]
Get:5 http://deb.debian.org/debian bookworm-updates/main arm64 Packages [756 B]
Get:6 http://deb.debian.org/debian-security bookworm-security/main arm64 Packages [264 kB]
Fetched 9213 kB in 2s (4921 kB/s)                        
Reading package lists... Done
...

root@54c79f3c5148:/# ping conteneur_flopesque
PING conteneur_flopesque (172.18.0.3) 56(84) bytes of data.
64 bytes from conteneur_flopesque.compose_test (172.18.0.3): icmp_seq=1 ttl=64 time=1.83 ms
64 bytes from conteneur_flopesque.compose_test (172.18.0.3): icmp_seq=2 ttl=64 time=0.202 ms
64 bytes from conteneur_flopesque.compose_test (172.18.0.3): icmp_seq=3 ttl=64 time=0.059 ms
...
```

# II. A working meow-api

Bon, la `meow-api` elle throw des belles erreurs SQL quand on va sur une de ses (seules) routes comme `/users`.

Elle a besoin d'une database pour fonctionner.

Dans cette partie vous allez :

- écrire un `docker-compose.yml` pour lancer :
  - `meow-api`
  - et l'image `mysql` officielle pour lui fournir une db
- lire le code [`app.py`](./app/app.py) pour apprendre :
  - l'IP (ou le nom) à laquelle le code essaie de se co pour sa db
  - le nom de la db utilisée
  - le nom du user utilisé pour se connecter à la db
  - le password utilisé
- faire ce qu'il faut pour que ça fonctionne !

Je vous guide comme j'aurais fait, mais le seul rendu attendu est le fichier `docker-compose.yml`.

## 1. Rédigez la structure du docker-compose.yml

➜ Rédigez la structure de base du `docker-compose.yml`.

**Je vous conseille de déjà lancer la `meow-api` seule**, comme avec un `docker run`. Avoir le même résultat qu'avec le `docker run` quoi, mais avec `docker compose`.

➜ Ensuite vous ajoutez un deuxième conteneur au `docker-compose.yml` qui se base sur l'image `mysql` officielle.

**Le nom du conteneur de base de données déclaré dans le `docker-compose.yml` doit être justement choisi** : c'est le nom auquel le code se connecte. 

## 2. L'image MySQL officielle

➜ Quand on lance l'image MySQL officielle, on peut définir plusieurs variables d'environnement pour :

- créer une database
- créer un utilisateur qui sera admin sur cette database
- d'autres trucs

➜ **Allez lire le [README de l'image officielle](https://hub.docker.com/_/mysql) pour voir comment faire ça.**

**Mettez à jour le `docker-compose.yml`** pour que la bonne database soit créée (celle à laquelle la `meow-api` se connecte), avec le bon user et le bon password.

➜ Je vous conseille de tester à ce moment là : quand vous faites un `docker compose up` l'API devrait fonctionner correctement, juste y'a pas de users existants.

## 3. Seed

Avec l'image MySQL officielle, il est possible de lancer automatiquement des scripts `.sql` quand le conteneur démarre. Idéal pour seed notre db avec des données de test.

➜ **Allez lire de nouveau le [README de l'image officielle](https://hub.docker.com/_/mysql) pour voir comment faire ça.**

Ajoutez un script `seed.sql` à côté du `docker-compose.yml`, il doit être utilisé pour créer 5 users de test dans la base de données.

## 4. Build automatisé

➜ Il est possible d'automatiquement déclencher le `build` des images appelées dans le `docker-compose.yml` au moment où on `docker compose up` (on peut le forcer avec `docker compose up --build`).

Vraiment pratique pour filer juste un dépôt git avec un `docker-compose.yml` qui fait tout !

➜ Ajoutez le `Dockerfile` de la `meow-api` dans le dossier. Oui vous avez peut-être déjà le `Dockerfile` stocké dans votre dépôt, l'idée ici c'est d'avoir une structure un peu standard avec un dossier qui est autonome et contient tout le nécessaire.

L'image `meow-api` doit être automatiquement build quand on allume le bazar.

## 5. Variables d'environnement

➜ On peut indiquer un fichier qui contient des variables d'environnement pour chaque conteneur

Ces variables seront chargées dans l'environnement du conteneur et seront donc accessibles dans le code.

➜ **Ajoutez un fichier `.env` qui sert à définir la variable `LISTEN_PORT` pour la `meow-api`.**

Ajoutez l'option nécessaire dans le `docker-compose.yml` pour que ce fichier `.env` soit lu par le conteneur qui lance la `meow-api`.

## 6. Rendu attendu

🌞 **Un dossier `meow_compose/` dans votre dépôt git, qui contient :**

- le `docker-compose.yml`
- le fichier de seed SQL `seed.sql`
- le fichier d'environnement `.env`
- le `Dockerfile` pour build `meow-api`

🌞 **Dans votre README de rendu**

- un `docker compose up` qui fonctionne
- un `curl` sur l'API, sur la route `/users`
- un `curl` sur l'API, sur la route `/user/3`


```
mkdir meow_compose
cd meow_compose

docker compose up --build

juliangabry@MacBook-Air-24 docker avancé % curl http://localhost:13010/users
[{"favorite_insult":"mergeur fou","id":1,"name":"Alice"},{"favorite_insult":"cowboy du CSS","id":2,"name":"Bob"},{"favorite_insult":"copieur StackOverflow","id":3,"name":"Charlie"},{"favorite_insult":"oubliateur de tests","id":4,"name":"Diana"},{"favorite_insult":"push master sur main","id":5,"name":"Eve"}]
juliangabry@MacBook-Air-24 docker avancé % curl http://localhost:13010/user/3
{"favorite_insult":"copieur StackOverflow","id":3,"name":"Charlie"}
juliangabry@MacBook-Air-24 docker avancé % 
```