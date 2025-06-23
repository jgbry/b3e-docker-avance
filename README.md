# Part II : Images

Dans cette deuxième partie, on va s'attarder sur le *build* d'image custom. **Faire en sorte de packager notre code dans une image toute fraîche.**

Y'a juste à avoir Docker installé, on run l'image, et ça tourne ! **No dépendances** (à part Docker).

![Docker build](./img/docker_build.png)

## Index

- [Part II : Images](#part-ii--images)
  - [Index](#index)
- [I. Images publiques](#i-images-publiques)
- [II. Construire une image](#ii-construire-une-image)
  - [A. Build la meow-api](#a-build-la-meow-api)
  - [B. Packagez vous-même une app](#b-packagez-vous-même-une-app)
  - [C. Ecrire votre propre Dockerfile](#c-ecrire-votre-propre-dockerfile)

# I. Images publiques

🌞 **Récupérez des images**

- avec la commande `docker pull`
- récupérez :
  - l'image `python` officielle en version 3.11 (`python:3.11` pour la dernière version)
  - l'image `mysql` officielle en version 8.0.42
  - l'image `wordpress` officielle en dernière version
    - c'est le tag `:latest` pour récupérer la dernière version
    - si aucun tag n'est précisé, `:latest` est automatiquement ajouté
  - l'image `linuxserver/wikijs` en dernière version
    - ce n'est pas une image officielle car elle est hébergée par l'utilisateur `linuxserver` contrairement aux 3 précédentes
    - on doit donc avoir un moins haut niveau de confiance en cette image
- listez les images que vous avez sur la machine avec une commande `docker`

> Quand on tape `docker pull python` par exemple, un certain nombre de choses est implicite dans la commande. Les images, sauf si on précise autre chose, sont téléchargées depuis [le Docker Hub](https://hub.docker.com/). Rendez-vous avec un navigateur sur le Docker Hub pour voir la liste des tags disponibles pour une image donnée. Sachez qu'il existe d'autres répertoires publics d'images comme le Docker Hub, et qu'on peut facilement héberger le nôtre. C'est souvent le cas en entreprise. **On appelle ça un "registre d'images"**.

```
juliangabry@MacBook-Air-24 docker avancé % docker pull python:3.11
3.11: Pulling from library/python
c016ca73232f: Pull complete 
7b9f5f869a6e: Pull complete 
828a2a41375b: Pull complete 
Digest: sha256:ce3b954c9285a7a145cba620bae03db836ab890b6b9e0d05a3ca522ea00dfbc9
Status: Downloaded newer image for python:3.11
docker.io/library/python:3.11

juliangabry@MacBook-Air-24 docker avancé % docker pull mysql:8.0.42
8.0.42: Pulling from library/mysql
9c7266afaf33: Pull complete 
12d652dc2508: Pull complete 
85065940bba5: Pull complete 
5ce44a171d06: Pull complete 
147b5c0a118e: Pull complete 
cffd736c905d: Pull complete 
1a9c3e4b007a: Pull complete 
1281dea9bbdc: Pull complete 
7dac163d5ad3: Pull complete 
65a492f1b8dd: Pull complete 
0984c0aea400: Pull complete 
Digest: sha256:98914997054781e301d675233d76f393168ea67002424c5291072e5593350e1b
Status: Downloaded newer image for mysql:8.0.42
docker.io/library/mysql:8.0.42

juliangabry@MacBook-Air-24 docker avancé % docker pull wordpress:latest
latest: Pulling from library/wordpress
34ef2a75627f: Pull complete 
b29695fa5193: Pull complete 
877a4d3e37c3: Pull complete 
68dcd2860c81: Pull complete 
211625f3b9f3: Pull complete 
a543208f4efc: Pull complete 
5ba2a3743b4b: Pull complete 
f79b6cf338f4: Pull complete 
cbda9f6cd672: Pull complete 
4f4fb700ef54: Pull complete 
02c79cd8699c: Pull complete 
0c3f64a2b782: Pull complete 
e5986a134440: Pull complete 
3630c4a6bfab: Pull complete 
afd2e054d8d1: Pull complete 
f8dd604a657c: Pull complete 
3fff45d01fc3: Pull complete 
39acdc354785: Pull complete 
c2a5deda81d7: Pull complete 
a25063be4912: Pull complete 
24fdd0d074fa: Pull complete 
3328044d89bc: Pull complete 
Digest: sha256:1931132b0b93230ee44d9628868e3ffe2076f49ba6569b36d281c0ccaa618ef4
Status: Downloaded newer image for wordpress:latest
docker.io/library/wordpress:latest

juliangabry@MacBook-Air-24 docker avancé % docker pull linuxserver/wikijs:latest
latest: Pulling from linuxserver/wikijs
b099656749ad: Pull complete 
1bfc3bc05ba0: Pull complete 
e1cde46db0e1: Pull complete 
8423e39ae289: Pull complete 
e7e33b357221: Pull complete 
bc92fab8947f: Pull complete 
8e2f36998bea: Pull complete 
0c12cf8e3fe6: Pull complete 
33fedb35122c: Pull complete 
Digest: sha256:f997a921b7695fc7528740ad2c36c10b0b9c23b2878a937487367ad98df15591
Status: Downloaded newer image for linuxserver/wikijs:latest
docker.io/linuxserver/wikijs:latest

juliangabry@MacBook-Air-24 docker avancé % docker images
REPOSITORY                                      TAG       IMAGE ID       CREATED        SIZE
it4lik/meow-api                                 arm       aa62b5955aa8   2 hours ago    1.62GB
linuxserver/wikijs                              latest    f997a921b769   9 days ago     788MB
python                                          3.11      ce3b954c9285   2 weeks ago    1.46GB
wordpress                                       latest    1931132b0b93   7 weeks ago    985MB
mysql                                           8.0.42    989149970547   2 months ago   1.05GB
docker.elastic.co/elasticsearch/elasticsearch   7.17.10   bc7ba1dc5067   2 years ago    1.01GB
docker.elastic.co/kibana/kibana                 7.17.10   4426892d5a87   2 years ago    1.42GB
docker.elastic.co/logstash/logstash             7.17.10   8fb88ff8789c   2 years ago    1.28GB
```


🌞 **Lancez un conteneur à partir de l'image Python**

- lancez un terminal `bash` ou `sh` à l'intérieur du conteneur
- vérifiez que la commande `python` est installée dans le conteneur, à la bonne version

> *Sympa d'installer Python dans une version spéficique en une commande non ? Peu importe que Python soit déjà installé sur le système ou pas. Puis on détruit le conteneur si on en a plus besoin.*

# II. Construire une image

Pour construire une image il faut :

- créer un fichier `Dockerfile`
- exécuter une commande `docker build` pour produire une image à partir du `Dockerfile`

## A. Build la meow-api

Dans ce repo git vous avez le [code](./app/app.py) et le fichier `Dockerfile` qui sert à *build* une image Docker.

🌞 **Récupérer le code et le `Dockerfile` sur votre machine**

- vrai tech le fait avec une commande et la met dans le compte-rendu
- créer un dossier et déplacer dedans le fichier de code et le `Dockerfile`

🌞 **Build une image `meow-api`**

- depuis un terminal, déplacez-vous dans le dossier qui contient le `Dockerfile`
- exécutez la commande :

```bash
# le caractère . fait référence au dossier actuel : le contexte de build
# -t permet de préciser un "tag" : le nom de l'image
docker build . -t meow-api
```

> Le build devrait être super rapide puisque vous avez déjà cette image. Docker ne stocke jamais deux fois la même chose.

🌞 **Afficher la liste des images dispos sur votre machine**

- dans la sortie de la commande, on devrait voir `meow-api` que vous venez de build

🌞 **Run cette image**

- faites un `docker run` qui lance l'image nouvellement build

## B. Packagez vous-même une app

Voilà un bout de code Python tout naze :

```python
import emoji

print(emoji.emojize("Cet exemple d'application est vraiment naze :thumbs_down:"))
```

🌞 **Ecrire un `Dockerfile` pour packager ce code**

- inspirez-vous de la structure de mon [`app/`](./app/) et du [`Dockerfile`](./app/Dockerfile) qu'il contient
- réservez encore un nouveau dossier sur votre machine pour stocker le code et son `Dockerfile`

🌞 **Build l'image**

- déplace-toi dans ton répertoire 
- `docker build . -t python_app:version_de_ouf`


🌞 **Proof !**

- une fois le build terminé, constater que l'image est dispo avec une commande `docker`

🌞 **Lancer l'image**

- lance l'image avec `docker run` :

```bash
docker run python_app:version_de_ouf
```

## C. Ecrire votre propre Dockerfile

![No master](./img/no_master.png)

➜ **Pour cette partie, récupérer un bout de code à vous**

- de préférence un service HTTP, un front web ou une API, peu importe
- t'as bien un truc qui traîne, un exo tout simple d'un autre cours ou quoi
- un truc standalone : qui a pas besoin de db ou quoi

🌞 **Ecrire un Dockerfile pour packager votre application**, il contient notamment :

- **`FROM`** : doit partir d'une image officielle
- **`COPY`** : ajoute le code dans l'image
- **`CMD`** : définit la commande à lancer quand le conteneur démarre

🌞 **Publiez votre image sur le Docker Hub**

- faut se créer un compte sur la WebUi du Docker Hub
- faut créer un *repository* depuis la WebUi, une fois connecté
- faut nommer correctement votre image, avec votre user dedans
  - genre moi c'était `it4lik/meow-api`
- et `docker push`
- dans le compte-rendu je veux :
  - toutes les commandes que vous avez tapées
  - l'URL de votre image sur la WebUI du Docker Hub
