# Part I : Init

Partie tranquilou avec au programme : **installation de Docker** sur votre poste, et vous faites **quelques lancements de conteneurs** depuis le terminal avec `docker run`.

Le but étant de prendre vos marques tranquillement avec l'utilisation de Docker sur votre poste si c'est pas déjà fait.

![No docker](./img/no_docker.png)

## Index

- [Part I : Init](#part-i--init)
  - [Index](#index)
- [I. Installation de Docker](#i-installation-de-docker)
  - [1. Install](#1-install)
  - [2. Vérifier que Docker est bien là](#2-vérifier-que-docker-est-bien-là)
  - [3. sudo c pa bo](#3-sudo-c-pa-bo)
- [II. Un premier conteneur en vif](#ii-un-premier-conteneur-en-vif)
  - [1. Simple run](#1-simple-run)
  - [2. Volumes](#2-volumes)
  - [3. Variable d'environnement](#3-variable-denvironnement)

# I. Installation de Docker

## 1. Install

Pour installer Docker, il faut **toujours** (comme d'hab en fait) se référer à la doc officielle.

**Je vous laisse donc suivre [les instructions de la doc officielle](https://docs.docker.com/engine/) pour installer Docker sur votre poste.**

> Je recommande l'install avec Hyper-V pour les Windowsiens (pas WSL).

## 2. Vérifier que Docker est bien là

Dans votre shell, les commandes suivantes doivent fonctionner :

```bash
docker info
docker ps
```

> Pour les Windowsiens, votre shell c'est Powershell (pas cmd bande de nazes).

## 3. sudo c pa bo

**Partie exclusive pour les Linuxiens s'il y en a.**

On va faire en sorte que vous puissiez taper des commandes `docker` sans avoir besoin des droits `root`, et donc de `sudo`.

Pour ça il suffit d'ajouter votre utilisateur au groupe `docker`.

> ***Pour que le changement de groupe prenne effet, il faut vous déconnecter/reconnecter de la session SSH** (pas besoin de reboot la machine, pitié).*

🌞 **Ajouter votre utilisateur au groupe `docker`**

- vérifier que vous pouvez taper des commandes `docker` comme `docker ps` sans avoir besoin des droits `root`

➜ Vous pouvez même faire un `alias` pour `docker`

Genre si tu trouves que taper `docker` c'est long, et tu préférerais taper `dk` tu peux faire : `alias dk='docker'`. Si tu écris cette commande dans ton fichier `~/.bashrc` alors ce sera effectif dans n'importe quel `bash` que tu ouvriras plutar.

# II. Un premier conteneur en vif

## 1. Simple run

> *Je rappelle qu'un "conteneur" c'est juste un mot fashion pour dire qu'on lance un processus un peu isolé sur la machine.*

Bon trève de blabla, on va lancer un truc qui juste marche.

On va lancer une petite API codée en Python par mes ptites mimines.

🌞 **Lancer un conteneur [`meow-api`](https://hub.docker.com/r/it4lik/meow-api)**

- avec la commande suivante :

```bash
docker run -p 8000:8000 it4lik/meow-api
```

✅ Résultat :

```
juliangabry@MacBook-Air-24 ~ % docker run -p 8000:8000 it4lik/meow-api::arm
Unable to find image 'it4lik/meow-api::arm' locally
latest: Pulling from it4lik/meow-api
8e328933b0c7: Pull complete 
039fc5a2754c: Pull complete 
ebb07cd170cc: Pull complete 
d6413c75b31d: Pull complete 
25244d620b74: Pull complete 
65a4d241c25b: Pull complete 
dad67da3f26b: Pull complete 
de5a3b3a918b: Pull complete 
Digest: sha256:1c319bdffb08d0508ac70204fad9fd83a8297c4794a63b2feee161450a7eff59
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8000
 * Running on http://172.17.0.2:8000
```


> Si tu mets pas le `-d` tu vas perdre la main dans ton terminal, et tu auras les logs du conteneur directement dans le terminal. `-d` comme *daemon* : pour lancer en tâche de fond. Essaie pour voir !

🌞 **Visitons**

- vérifier que le conteneur est actif avec une commande qui liste les conteneurs en cours de fonctionnement :

```
juliangabry@MacBook-Air-24 ~ % docker ps
CONTAINER ID   IMAGE             COMMAND           CREATED         STATUS         PORTS                    NAMES
9df4c1b3836a   it4lik/meow-api   "python app.py"   5 minutes ago   Up 5 minutes   0.0.0.0:8000->8000/tcp   ecstatic_curran
juliangabry@MacBook-Air-24 ~ % 
```

- afficher les logs du conteneur
  
```
juliangabry@MacBook-Air-24 ~ % docker logs 9df4c1b3836a
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8000
 * Running on http://172.17.0.2:8000
 ```

- afficher toutes les informations relatives au conteneur avec une commande `docker inspect`
```
juliangabry@MacBook-Air-24 ~ % docker inspect 9df4c1b3836a
[
    {
        "Id": "9df4c1b3836a27e20e51c4841e521ffb3f810a1619c1527eb480a95d2d1b28fa",
        "Created": "2025-06-23T08:22:39.202960637Z",
        "Path": "python",
        "Args": [
            "app.py"
        ],
        "State": {
            "Status": "running",
            "Running": true,
            "Paused": false,
            "Restarting": false,
            "OOMKilled": false,
            "Dead": false,
            "Pid": 916,
            "ExitCode": 0,
            "Error": "",
            "StartedAt": "2025-06-23T08:22:39.246535303Z",
            "FinishedAt": "0001-01-01T00:00:00Z"
        }
        ...
    }
]

```
- depuis le navigateur de votre PC, visiter la route `/` de l'API sur `http://votre_ip:8000`
```
curl http://localhost:8000
{
  "message": "Available routes",
  "routes": {
    "get_user_by_id": "http://localhost:8000/user/1",
    "list_all_users": "http://localhost:8000/users"
  }
}
```

---

🌞 **Lancer le conteneur en tâche de fond**

- ajoutez `-d` à la commande

> `-d` comme *daemon*. Un *daemon* c'est un programme qui s'exécute en fond.

```
juliangabry@MacBook-Air-24 ~ % docker run -d -p 8000:8000 it4lik/meow-api:arm
Unable to find image 'it4lik/meow-api:arm' locally
arm: Pulling from it4lik/meow-api
8fbf1dd6492c: Pull complete 
bf8a8047f2c7: Pull complete 
11ceb31c6e90: Pull complete 
c9e098cc9ddd: Pull complete 
14f5719d6358: Pull complete 
78f00d2fce16: Pull complete 
7a87bb464191: Pull complete 
d9e54ed038f8: Pull complete 
c5e137b9ec17: Pull complete 
c9871df95570: Pull complete 
ee3677d6f711: Pull complete 
Digest: sha256:aa62b5955aa84ac21143ef9294108b06701d36d3e90ad49896e811066542a107
Status: Downloaded newer image for it4lik/meow-api:arm
2fce568d06956c8d92e498738e554a953b499d9e6141011c60853de6b743263e
```

🌞 **Consultez les logs du conteneur**

- avec une commande `docker logs`
- il faudra préciser l'ID ou le nom du conteneur en argument à la commande

```
juliangabry@MacBook-Air-24 ~ % docker logs 2f             
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8000
 * Running on http://172.17.0.2:8000
Press CTRL+C to quit
```

## 2. Volumes

➜ On peut préciser genre mille options au lancement d'un conteneur, **go `docker run --help` pour voir !**

➜ Hop, on en profite pour voir un truc super utile avec Docker : le **partage de fichiers au moment où on `docker run`**

En effet, il est possible de partager un fichier ou un dossier avec un conteneur, au moment où on le lance. 

Typiquement quand tu codes, t'as la flemme de rebuild l'image à chaque fois, donc tu peux **monter ton code dans le conteneur au moment où tu run**.

Comme ça le code **dans le conteneur et le code sur ta machine** c'est **phyiquement le même**. Donc t'as même pas besoin de re-run quoi.

Ca se fait avec `-v` pour *volume* (on appelle ça "monter un volume")

🌞 **Remplacer le code `app.py`**

- vous devez écrire un ptit fichier de code Python 
  - écoute sur le port 8000 (comme mon API)
  - ptit service web (HTTP)
  - retourne un truc de votre choix quand on tape sur `/` (bonus pour les gifs de merde)
- faire un `docker run -v <votre_code>:/app/app.py it4lik/meow-api`
  - vous allez remplacer le fichier de code lancé au démarrage du conteneur
  
```
docker avancé % docker run -p 8000:8000 -v "$(pwd)/app.py:/app/app.py" it4lik meow-api:arm
Unable to find image 'it4lik/meow-api:arm' locally
arm: Pulling from it4lik/meow-api
78f00d2fce16: Pull complete 
8fbf1dd6492c: Pull complete 
11ceb31c6e90: Pull complete 
14f5719d6358: Pull complete 
ee3677d6f711: Pull complete 
c9e098cc9ddd: Pull complete 
c9871df95570: Pull complete 
d9e54ed038f8: Pull complete 
c5e137b9ec17: Pull complete 
bf8a8047f2c7: Pull complete 
7a87bb464191: Pull complete 
Digest: sha256:aa62b5955aa84ac21143ef9294108b06701d36d3e90ad49896e811066542a107
Status: Downloaded newer image for it4lik/meow-api:arm
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8000
 * Running on http://172.17.0.2:8000
```

🌞 **Prouvez que ça fonctionne avec une requête Web**

- je veux une commande `curl` dans le compte-rendu

```
juliangabry@MacBook-Air-24 ~ % curl localhost:8000

        <h1>🐱 Yo depuis mon app !</h1>
        <img src="https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif" alt="cat gif">                                              
```

## 3. Variable d'environnement

➜ Mon code lit la variable d'environnement `LISTEN_PORT` 

Si elle est définie, il écoute sur ce port là.

Si elle ne l'est pas, il écoute sur le port `8000` par défaut.

🌞 **Définir une variable d'environnement au lancement du conteneur**

- ajoutez une option sur le `docker run` pour lancer l'image `it4lik/meow-api` en définissant une variable d'environnement
- doit définir la variable d'environnement mentionnée plus haut
- écoutez sur le port `16789`


🌞 **Mettez à jour l'option `-p`**

- pour continuer d'accéder au conteneur

```
juliangabry@MacBook-Air-24 docker avancé % docker run -p 16789:16789 -e LISTEN_PORT=16789 -v "$(pwd)/app.py:/app/app_3.py" it4lik/meow-api:arm
 * Serving Flask app 'app'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:16789
 * Running on http://172.17.0.2:16789
```

🌞 **Prouvez que ça fonctionne avec une requête Web**

- je veux une commande `curl` dans le compte-rendu

```
juliangabry@MacBook-Air-24 docker avancé % curl localhost:16789

        <h1>🐱 Yo depuis mon app !</h1>
        <img src="https://media.giphy.com/media/JIX9t2j0ZTN9S/giphy.gif" alt="cat gif">
```