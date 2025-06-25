# Part II : Des environnements différents

**On utilise généralement pas tout à fait nos *images* de la même façon en dév ou en prod.**

➜ **En dév**, on veut pouvoir `docker run` notre code, et facilement le modifier sans avoir à rebuild à chaque fois.

Pour du dév, vous me contredirez peut-être, mais moi je veux : un environnement que je peux facilement custom/changer, tester rapidement mon code quand je rajoute juste un point-virgule, 

On va donc utiliser un *volume* au moment du `docker run` pour poser notre code.

> Pour rappel, l'utilisation d'un *volume* (le `-v` de `docker run`) ne fait aucune copie : il rend directement accessible dans le conteneur un fichier ou dossier qui se trouve en réalité sur la machine hôte. C'est idéal dans notre cas : on monte notre code, et si on le modifie sur notre PC, ça sera donc aussi modifié dans le conteneur ! Donc on dév toujours dans notre IDE, mais le code est en permanence lancé dans un conteneur !

➜ **En revanche, en prod**, c'est l'exact inverse : on veut que le code soit harcodé dans l'image

Pour la prod on veut de la sécu, de la stabilité, des trucs qui juste fonctionnent, **faciles à maintenir**, ce genre de trucs.

Les images sont **strictement immuables** : il est **impossible** de modifier une *image* existante. Si tu veux la modifier, **il faut rebuild** une nouvelle *image*.

**Donc avoir le code hardcodé dans l'image, c'est une mesure très forte de sécurité.**

De plus, l'image est alors ***standalone*** : elle fonctionne juste quand on la `docker run`, pas besoin d'avoir d'autres fichiers (pas besoin d'avoir le code sur la machine qui `docker run` pour le monter avec un *volume*).

## Index

- [Part II : Des environnements différents](#part-ii--des-environnements-différents)
  - [Index](#index)
  - [1. Prod](#1-prod)
  - [2. Dév](#2-dév)
  - [3. Multi-stage build](#3-multi-stage-build)
    - [A. Intro](#a-intro)
    - [B. Do it](#b-do-it)

## 1. Prod

➜ **Ecrire un `Dockerfile-prod`**

- le code et ses dépendances sont contenus dans l'image (comme le `Dockerfile` de la partie précédente ui je sais)
- une variable d'environnement `ENVIRONMENT` est définie à la valeur `prod`
- ne doit pas utiliser `CMD` mais uniquement `ENTRYPOINT`
  - on hardcode un max pour rentre l'image complètement prévisible et prédictible.

> Avec cette variable `ENVIRONMENT` on simule des différences spécifiques entre les deux environnements. Même si j'ai déjà vu ça IRL (et le code vérifiait en checkant cette variable dans quel environnement il tournait pour faire des trucs différents).

➜ **Ecrire un `docker-compose-prod.yml`**

- votre app est lancée à partir de `Dockerfile-prod`
- un build automatique avec `build` pour l'image de votre application
  - il faudra préciser explicitement le nom du `Dockerfile` vu que ce n'est plus le nom standard

➜ **Structure du repo attendue** à ce stade

```bash
❯ tree -a -L2
.
├── docker-compose-prod.yml
├── docker-compose.yml
├── Dockerfile
├── Dockerfile-prod
├── .env.sample
├── .gitignore
├── README.md
├── requirements.txt
└── src
    └── main.py
```

🌞 **Test !**

- un `docker compose up` dans le compte-rendu
  - il faudra explicitement préciser le nom du fichier vu qu'il n'est plus standard non plus !
- suivi d'un `curl` qui prouve que le service fonctionne

## 2. Dév

➜ **Ecrire un `Dockerfile-dev`**

- le code n'est PAS contenu dans l'image
- les dépendances sont bien contenues dans l'image
- une variable d'environnement `ENVIRONMENT` est définie à la valeur `dev`

➜ **Ecrire un `docker-compose-dev.yml`**

- votre app est lancée à partir de `Dockerfile-dev`
- un build automatique avec `build` pour l'image de votre application
  - il faudra préciser explicitement le nom du `Dockerfile` vu que ce n'est plus le nom standard
- monte le dossier `src/` (ou son contenu) dans le conteneur de votre application
  - on parle du dossier `src/` qui se situe sur votre PC
  - doit être monté au bon endroit dans `/app` pour que l'image se lance correctement

➜ **Structure du repo attendue** à ce stade

```bash
❯ tree -a -L2
.
├── docker-compose-dev.yml
├── docker-compose-prod.yml
├── docker-compose.yml
├── Dockerfile
├── Dockerfile-dev
├── Dockerfile-prod
├── .env.sample
├── .gitignore
├── README.md
├── requirements.txt
└── src
    └── main.py
```

🌞 **Test !**

- un `docker compose up` dans le compte-rendu
  - il faudra explicitement préciser le nom du fichier vu qu'il n'est plus standard non plus !
- suivi d'un `curl` qui prouve que le service fonctionne

> **A PARTIR DE NOW** c'est censé être tout aussi pratique de use ton environnement Docker qu'un env installé sur ta machine, pendant que tu dév. Grâce au volume monté au moment du `run` en particulier, on dév dans notre IDE, et les changements sont accessibles dans l'environnement conteneurisé. Plus besoin d'installer quoi que ce soit sur nos machines, on fait passer le code ez, etc ! FAIS TOI DU BIEN et utilise Docker.

## 3. Multi-stage build

### A. Intro

➜ Ptite feature très cool pour build des images, qu'on rencontre absolument partout aujourd'hui : [**le multi-stage build**](https://docs.docker.com/build/building/multi-stage/).

Ca permet de partager explicitement certaines instructions `Dockerfile` entre plusieurs images.

➜ Dit concrètement avec un exemple : dans notre cas, les deux `Dockerfile` (`Dockerfile-dev` et `Dockerfile-prod`) partagent beaucoup de choses, comme leur image de base et les dépendances de votre code (et d'autres trucs).

Plutôt que d'avoir deux `Dockerfile`s similaires à genre 75%, on va **explicitement mutualiser ces instructions communes** dans un seul `Dockerfile`.

Toujours dans le même (ou pas) on pourra indiquer la suite des étapes pour `prod` et une autre suite d'étapes pour `dev`. Et ainsi complètement éviter la redondance de nos `Dockerfile`.

> De plus on couple encore plus fortement les deux environnements. On limite les différences potentielles entre `dev` et `prod` en l'occurrence, pour garder l'aspect prédictible et prévisible au maximum !

---

### B. Do it

➜ **Remplacez les deux `Dockerfile`s par un seul**

- utilise la mécanique de multi-stage
  - on évite ~~quasiment~~ complètement le code redondant
- un ptit exemple :

```Dockerfile
## D'abord tout ce qui est commun dans le premier "stage"
# Image de base commune
FROM debian

# Workdir commun
WORKDIR /app

# Install des dépendances communes
RUN apt-get update -y && apt-get install -y python

# On peut même partager le ENTRYPOINT
ENTRYPOINT ["python", "main.py"]

## ENSUITE on va définir deux stages : un dev et un prod

# dev d'abord because why not
FROM base AS dev

# instructions spécifiques à l'image de dév
RUN echo dev

# puis la prod
FROM base AS prod

# instructions spécifiques à l'image de prod
RUN echo prod
```

➜ **Structure du repo attendue** à ce stade

```bash
❯ tree -a -L2
.
├── docker-compose-dev.yml
├── docker-compose-prod.yml
├── docker-compose.yml
├── Dockerfile     # de nouveau un seul Dockerfile
├── .env.sample
├── .gitignore
├── README.md
├── requirements.txt
└── src
    └── main.py
```

🌞 **Test !**

- j'veux les deux commandes `docker build` dans le compte-rendu
- il faut ajouter `--target` pour préciser quel environnement on veut build

---

➜ [**Lien vers la partie 3 consacrée à une ptite étude des images de base**](./part3.md)
