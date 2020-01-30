# NIRAHTECH-MAVEN-REPOSITORY
## I. PRESENTATION
Il s'agit d'un dépot publique pour les bibliothèques MAVEN.
Ces dépenses sont utilisées par des applications `Java`.

Ce dépot recense :
- des bibliothèques développées par NIRAH-TECHNOLOGY
- des bibliothèques externe développées par d'autre entreprises mais utilisées par NIRAH et qui sont donc jugés de confiance.

## II. UTILISATION - Publication de nouvelles versions
Pour publier une nouvelle version d'une bibliothèque, il faut éxécuter le script python `publish.py`.

Le script est compatible avec **n'importe quelle version** de `Python`.

### Executer la commande de publication
1. Télécharger le projet
> \> git pull https://github.com/Zaroastre/nirahtech-maven-repository.git
 
2. Se déplacer dans le projet.
> \> cd nirahtech-mavn-repository/
3. Exécuter le script en utilisant l'une des deux méthodes proposées  

> \> python publish.py

ou

> \> python publish.py /chemin/complet/au/fichier/nom-version.jar

En exécutant juste `python publish.py`, il faut penser à modifier la valeur de la variable `workspace_root_base` dnas le fichier `publish.py` afin qu'elle pointe sur le bon répertoire contenant les différents projets.

4. Valider l'ajout de la nouvelle bibliothèque et sa version publiée.
> \> git add . ; git commit -m "Ajout d'une nouvelle version." ; git push github repository ;

## III. UTILISATION - Utilisation d'une nouvelle version
Pour pouvoir utiliser l'une des bibliothèque publié sur le dépot, il faut, en étant dans un projet `Java` utilisant `Maven`, modifier le fichier `pom.xml` et y ajouter les sections `repositories` et `dependency` suvantes:


``` xml
<project>
    ...
    <repositories>
        <repository>
            <id>nirahtech-maven-repository</id>
            <name>Nirah-Technology Personnal Maven Repository</name>
            <url>https://maven.nirah-technology.fr/repository/</url>
        </repository>
    </repositories>
    ...
    <dependencies>
        ...
        <dependency>
            <groupId>io.nirahtech</groupId>
            <artifactId>project-name</artifactId>
            <version>0.1.2-VERSION</version>
        </dependency>
        ...
    </dependencies>
    ...
</project>
```