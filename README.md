# Part III : Base image

Dans cette partie on s'attarder un peu sur **le choix de l'image de base.**

➜ **Déjà : la sécu.** On veut s'assurer que notre image est pas **toute pourrie** (pas remplie de vulns critiques). Pour ce qui est de **la provenance**, dans l'idéal on veut une image conçue par les dévs du truc (notion de confiance).

> Genre si on utilise une image `debian` on aimerait qu'elles soient fournies par les gars de chez Debian. Idem pour n'importe quelle autre image, comme une image `ubuntu` ou `symfony`.

➜ Pour **une bonne maîtrise de l'environnement**, on va souvent préférer prendre une image contenant juste un OS basique, et ajouter nous-mêmes notre langage/framework/libs/autres dépendances. Ca permet aussi de choisir parfois des configs exotiques, mais nécessaires.

> C'pas rare que les entreprises éditent elles-mêmes des images internes. Attention quand ça provient de l'extérieur en tout cas !

➜ Parmi les images officielles les plus utilisées comme base, on trouve notamment `debian` et `alpine`.

> L'image officielle `ubuntu` est pas mal utilisée aussi. Et d'autres. Mais y'a un peu la question de `alpine` versus the world.

➜ **Dans cette partie, on va donc se concentrer sur les premières lignes du `Dockerfile`, en particulier le `FROM`.**

## 1. Provenance

Vous pourrez trouver ces infos en partant de [la WebUI du Docker Hub](https://hub.docker.com/).

🌞 **Donnez le lien vers les `Dockerfile`s opensource qui permettent de produire**

- l'image `debian:latest`
- l'image `alpine:latest`
- l'image que vous aviez utilisé comme `FROM` jusqu'à maintenant

```
1. Docker Hub : https://hub.docker.com/_/debian
2. Docker Hub : https://hub.docker.com/_/alpine
3. Docker Hub : https://hub.docker.com/_/debian
```

> Z'avez vu ce `FROM scratch` dans les `Dockerfile` de `alpine` ou `debian` ? Clin d'oeil clin d'oeil. 

## 2. Vulnérabilités connues

Vous pensez que l'image `debian:latest` officielle (par exemple) contient combien de vulnérabilités connues ?

Ptite partie pour répondre à cette question, j'vous donne juste le tool, et vous lancez juste pour avoir la réponse !

Le tool que je vous recommande c'est [`trivy`](https://github.com/aquasecurity/trivy), outil efficace et plutôt mature.

> Il existe plein de tools pour ça, certains avec des WebUI sexy. J'aime toujours beaucoup les outils en CLI parce que ça s'intègre à tout et n'importe quoi, des hooks git, des pipelines de CI/CD, ou n'importe quoi d'autres : c'est trop facile à wrapper dans autre chose.

🌞 **Déterminer le nombre et la criticité des vulns connues dans les images**

- `debian:latest`
- `alpine:latest`
- l'image que vous aviez utilisé comme `FROM` jusqu'à maintenant

```
debian:latest : 
┌──────────────────────────────┬────────┬─────────────────┬─────────┐
│            Target            │  Type  │ Vulnerabilities │ Secrets │
├──────────────────────────────┼────────┼─────────────────┼─────────┤
│ debian:latest (debian 12.11) │ debian │       78        │    -    │
└──────────────────────────────┴────────┴─────────────────┴─────────┘
Total: 78 (UNKNOWN: 0, LOW: 58, MEDIUM: 12, HIGH: 7, CRITICAL: 1)

alpine:latest : 

┌───────────────────────────────┬────────┬─────────────────┬─────────┐
│            Target             │  Type  │ Vulnerabilities │ Secrets │
├───────────────────────────────┼────────┼─────────────────┼─────────┤
│ alpine:latest (alpine 3.22.0) │ alpine │        0        │    -    │
└───────────────────────────────┴────────┴─────────────────┴─────────┘
Total: 0

```

> Note : la criticité c'est genre "low" "medium" "high" "critical" par exemple. [Des termes définis de façon plus ou moins standard](https://nvd.nist.gov/vuln-metrics).

## 3. Dockerfile writing

➜ **Ecrire un `Dockerfile-alpine`**

- en partant du `Dockerfile` de la partie précédente (il faut donc modifier le début)
- commence par un `FROM alpine:xxx`
  - vous remplacez la `xxx` par la dernière version explicitement ([***version pinning***](https://jonathan.bergknoff.com/journal/always-pin-your-versions/))
  - pas de `latest`
- s'en suit sûrement un ou plusieurs `RUN` pour installer :
  - votre langage
  - votre tooling (genre un gestionnaire de paquet pour télécharger des dépendances)
  - d'autres dépendances si besoin
- la fin du `Dockerfile-alpine` devraient être identique à `Dockerfile`
- pas besoin qu'il soit dans le dépôt de rendu ce fichier

➜ **Ecrire un `Dockerfile-debian`**

- pareil mais avec l'image `debian` officielle
- pas besoin qu'il soit dans le dépôt de rendu ce fichier

## 4. Measure !

🌞 **Build time**

- deux commandes `docker build` chronométrée dans le rendu, utilisées pour build ces deux `Dockerfile`s
- au moment du build, elles doivent être nommées décemment ces deux images svp
- utilisez un truc pour chronométrer le temps du `build` en terminal :

```bash
# Linux et MacOS : y'a la commande time
time docker build ...

# Windows : ça s'fait avec Measure-Command
Measure-Command { docker build ... }
```

```
docker build -f Dockerfile-debian -t jellyfin-debian:latest .  0.18s user 0.24s system 7% cpu 5.847 total
docker build -f Dockerfile-alpine -t jellyfin-alpine:latest .  0.16s user 0.20s system 8% cpu 4.091 total
```

🌞 **Comparaison post-build**

- comparez la taille des deux images
  - avec une simple commande `docker`
- comparez la perf des deux images
  - ça va très largement dépendre de votre app ça
  - ça serait bien de timer combien de temps prend l'app à démarrer, à fonctionner, à traiter une requête un peu lourde, ce genre de truc
  - le but est de mettre en évidence (ou pas) la lenteur de `alpine`

```
juliangabry@MacBook-Air-24 b3e-docker-avance % docker images | grep jellyfin
jellyfin-alpine   latest    9e985ec73689   11 minutes ago   555MB
jellyfin-debian   latest    bf01cfbe9c27   2 hours ago      880MB


Debian :

juliangabry@MacBook-Air-24 b3e-docker-avance % time seq 1 1000 | xargs -n1 -P1000 -I{} curl -s -o /dev/null http://localhost:8096/
seq 1 1000  0.00s user 0.00s system 42% cpu 0.007 total
xargs -n1 -P1000 -I{} curl -s -o /dev/null http://localhost:8096/  4.12s user 5.81s system 360% cpu 2.755 total

juliangabry@MacBook-Air-24 b3e-docker-avance % ab -n 1000 -c 100 http://localhost:8096/
This is ApacheBench, Version 2.3 <$Revision: 1903618 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking localhost (be patient)
Completed 100 requests
Completed 200 requests
Completed 300 requests
Completed 400 requests
Completed 500 requests
Completed 600 requests
Completed 700 requests
Completed 800 requests
Completed 900 requests
Completed 1000 requests
Finished 1000 requests


Server Software:        Kestrel
Server Hostname:        localhost
Server Port:            8096

Document Path:          /
Document Length:        0 bytes

Concurrency Level:      100
Time taken for tests:   0.191 seconds
Complete requests:      1000
Failed requests:        0
Non-2xx responses:      1000
Total transferred:      130000 bytes
HTML transferred:       0 bytes
Requests per second:    5235.27 [#/sec] (mean)
Time per request:       19.101 [ms] (mean)
Time per request:       0.191 [ms] (mean, across all concurrent requests)
Transfer rate:          664.63 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    2   1.6      1       6
Processing:     6   16   7.0     14      40
Waiting:        5   16   7.0     14      40
Total:          9   18   6.7     16      42

Percentage of the requests served within a certain time (ms)
  50%     16
  66%     18
  75%     20
  80%     21
  90%     29
  95%     34
  98%     39
  99%     39
 100%     42 (longest request)

Alpine :

juliangabry@MacBook-Air-24 b3e-docker-avance % time seq 1 1000 | xargs -n1 -P1000 -I{} curl -s -o /dev/null http://localhost:8096/
seq 1 1000  0.00s user 0.00s system 71% cpu 0.006 total
xargs -n1 -P1000 -I{} curl -s -o /dev/null http://localhost:8096/  4.34s user 6.23s system 389% cpu 2.714 total

juliangabry@MacBook-Air-24 b3e-docker-avance % ab -n 1000 -c 100 http://localhost:8096/
This is ApacheBench, Version 2.3 <$Revision: 1903618 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking localhost (be patient)
Completed 100 requests
Completed 200 requests
Completed 300 requests
Completed 400 requests
Completed 500 requests
Completed 600 requests
Completed 700 requests
Completed 800 requests
Completed 900 requests
Completed 1000 requests
Finished 1000 requests


Server Software:        Kestrel
Server Hostname:        localhost
Server Port:            8096

Document Path:          /
Document Length:        0 bytes

Concurrency Level:      100
Time taken for tests:   0.316 seconds
Complete requests:      1000
Failed requests:        0
Non-2xx responses:      1000
Total transferred:      130000 bytes
HTML transferred:       0 bytes
Requests per second:    3163.25 [#/sec] (mean)
Time per request:       31.613 [ms] (mean)
Time per request:       0.316 [ms] (mean, across all concurrent requests)
Transfer rate:          401.58 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    2   1.9      2       7
Processing:     6   19   9.1     17     100
Waiting:        6   19   9.1     17      96
Total:          7   21   8.8     19     101

Percentage of the requests served within a certain time (ms)
  50%     19
  66%     23
  75%     26
  80%     28
  90%     33
  95%     38
  98%     42
  99%     44
 100%    101 (longest request)
```

![Perfs](./img/high_perf.jpg)

## 3. Choose yourself !

➜ **Choisissez ce que vous préférez pour continuer le TP**

- l'un de ces deux `Dockerfile`s devient votre `Dockerfile` pour la suite du TP, j'veux pas entendre parler de l'autre !

> Si on avait pas utilisé de multi-stage build, il aurait fallu éditer deux `Dockerfile` là. Relou. Ou oublier de le faire. Encore plus relou.

---

➜ [**Dernière partie avec quelques tips en vrac**](./part4.md)
