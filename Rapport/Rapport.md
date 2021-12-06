# **SD701 - Rapport de projet** : Qualite de l'air dans le metro parisien

## **1) Presentation du jeu de données principale**

### **Origine du jeu de données et features**

Le jeu de données étudié dans le cadre de ce projet est issu de l'API RATP.  
Il contient les mesures moyennes heure par heure des indicateurs suivants :
- Paramètres climatiques usuels : température en °C et taux d'humidité en %
- Indicateur du renouvellement de l'air : CO2 en ppm
- Indicateurs de la qualité de l'air : NO, NO2 et PM10 en µg/m3

Ces mesures représentent 50 000 valeurs par an environ pour chaque station de métro équipée d'une station de mesure. Au total, 3 stations sont équipées de ce dispositif :
- Auber : quai du RER A
- Chatelet : quai du métro 4
- Franklin Roosevelt : quai du métro 1

La collecte de ces mesures a commencée en 2013. Au total, le jeu de données contient donc quelques 1 350 000 valeurs (450 000 par station).


### **Qualité du jeu de données**

Avant d'amorcer l'exploitation du jeu de données à proprement parler, il est nécessaire d'estimer sa qualité, à savoir principalement le nombre de valeurs exploitables par station.

<p float="left">
  <img src="Pictures/Partie_1/null_param.png" width="300" />
  <img src="Pictures/Partie_1/null_station.png" width="300" /> 
  <img src="Pictures/Partie_1/null_year.png" width="300" />
</p>

<p float="center">
  <img src="Pictures/Partie_1/null_station_param.png" width="450" />
  <img src="Pictures/Partie_1/null_station_year.png" width="450" />
</p>

- 40% des valeurs à disposition pour la station Auber sont des valeurs nulles : il semblerait qu'à partir de 2018, les capteurs de cette station aient cessé de fonctionner.
- Plus de 90% des mesures de la station Châtelet sur l'année 2018 sont inexploitables. Sur les autres années, cette station ne présente pas plus de 20% de valeurs nulles.
- Il n'y a pas de dissymétrie au niveau du nombre de valeurs nulles par paramètre : autrement dit, on dispose d'un nombre globalement identique de valeurs exploitables pour chaque paramètre.

### **Comparaison des qualités de l'air moyennes dans les 3 stations**

Valeurs moyennes des paramètres sur l'ensemble du jeu de données :
<p float="left">
	<img src="Pictures/Partie_1/moy_par_param.png" width="450" />
	<img src="Pictures/Partie_1/moy_par_param_par_station.png" width="450" />
</p>

- La station Châtelet semble moins exposée au NO et au NO2 que les stations Auber et Franklin Roosevelt.
- La station Franklin Roosevelt est moins exposée au PM10 que Auber et Chatelet.
- Les paramètres de température, d'humidité ainsi que la concentration en CO2 sont très proches sur les 3 stations.

### **Patterns d'évolution temporelle des indicateurs de qualité de l'air**

Courbes d'évolution moyennées sur l'ensemble des valeurs pour les 3 stations sur différentes échelles de temps.
Dans l'ordre : 
- Heure par heure jours ouvrés
- Heure par heure weekends
- Jour de la semaine
- Mois de l'année
- Années depuis 2013

L'objectif ici étant d'afficher l'évolution des paramètres indépendemment de leur valeur intrinsèque, les valeurs sont divisées par la moyenne, ce qui donne des courbes sans unité oscillant autour de 1.

<p float="left">
	<img src="Pictures/Partie_1/weekday_par_param.png" width="450" />
	<img src="Pictures/Partie_1/weekend_par_param.png" width="450" />
	<img src="Pictures/Partie_1/week_par_param.png" width="450" />
</p>
<p float="left">
	<img src="Pictures/Partie_1/year_par_param.png" width="450" />
	<img src="Pictures/Partie_1/years_par_param.png" width="450" />
	<img src="Pictures/Partie_1/legend_param.png" width="70" />
</p>

**Variations à court terme : au cours d'une même journée et au cours de la semaine**
- TEMP et HUMI : pas ou peu de variations
- CO2 et NO2 : variations non négligeables  (de l'ordre de 10-20%)
- NO et PM10 : variations significatives (de l'ordre de 40-50%)

**Variations à moyen terme : au cours de l'année**
- CO2, NO2 HUMI et PM10 : pas ou peu de variations
- TEMP : variations saisonnières non négligeables (de l'ordre de 20%)
- NO : variations saisonnières significatives (de l'ordre de 40%)

**Variations à long terme : au fil des ans**
- TEMP, HUMO, CO2 : pas ou peu de variations
- PM10, NO et NO2 : tendance baissière au fil des ans

Les courbes ci-dessus laissent appraître, en moyenne sur les 3 stations, des cycles d'évolution des paramètres de qualité de l'air sur différentes échelles de temps.  
Il peut être intéressant de vérifier si chacune des stations individuellement suivent les mêmes patterns d'évolution. Les graphes ci-dessous représentent la comparaison des évolutions du paramètre NO sur les 3 stations (même échelles de temps que les graphes ci-dessus).

<p float="left">
	<img src="Pictures/Partie_1/weekday_par_station.png" width="450" />
	<img src="Pictures/Partie_1/weekend_par_station.png" width="450" />
	<img src="Pictures/Partie_1/week_par_station.png" width="450" />
</p>
<p float="left">
	<img src="Pictures/Partie_1/year_par_station.png" width="450" />
	<img src="Pictures/Partie_1/years_par_station.png" width="450" />
	<img src="Pictures/Partie_1/legend_station.png" width="70" />
</p>

En dehors des variations années après annnées qui présentent certaines incohérences, on remarque que toutes les variations listées dans la partie précédente sont bien communes aux 3 stations et relèvent donc de phénomènes à priori généralisables.

## **2) Premiers algorithmes**

### **Clustering et classification :** détermination du type de jour (ouvré ou weekend) à partir des relevés de qualité de l'air

**Choix des paramètres :**

Les algorithmes de classification que nous connaissons (kmeans, k-voisins) sont tous deux soumis à la malédiction de la dimension car basés sur des calculs de distance. Or, si l'on voulait rassembler l'ensemble des valeurs dont on dispose pour chaque journée dans un vecteur, le vecteur obtenu aurait une taille de 24 heures * 6 paramètres = 144 variables. Il est donc fort probable que les algorithmes soient inefficaces.  
Pour éviter ce problème, on tente de simplifier le modèle et de se ramener à des vecteurs de taille plus raisonnable. Pour cela, plusieurs approches ont été testées :
- Vecteurs journaliers contenant pour chaque paramètre sa valeur et sa variance, en moyennant ou non au préalable toutes les données sur les 3 stations.
- Vecteurs journaliers divisés par la concentration moyenne journalière, dont on extrait la variance ainsi que l'horaire du pic de concentration de chaque variable. C'est cette approche qui s'est avérée être la plus efficace. Voici ci-dessous un extrait des 3 premiers vecteurs du jeu de données transformé.

<img src="Pictures/Partie_2/vecteur_classification.png" width="800" />

C'est ce jeu de donnée retravaillé que l'on va utiliser dans les deux parties suivantes.

**Approche non supervisée : k-means**

En effectuant un k-means sur des vecteurs tels qu'introduits précédemment, et en règlant le nombre de clusters sur 2, on obtient les résultats suivants :
- Le cluster contenant le plus faible nombre de points (à priori assimilables aux jours du weekend) contient 39,4% des points (le % de réels de jours du weekend dans le dataset est de 27.7%).
- La clusterisation correspond à la qualité jour ouvré / weekend dans 57.9% des cas.
- On obtient la matrice de confusion suivane :

<img src="Pictures/Partie_2/confusion_k_means.png" width="300" />

La capacité du kmeans à déterminé si des mesurs viennent d'un jour ouvré ou d'un jour du weekend est donc assez limitée. On pourrait tenter d'améliorer notre capacité de classification en adoptant un modèle supervisé.

**Approche supervisée : k-voisins**

On peut profiter de la connaissance de la date de chacun des relevés pour mettre en oeuvre un modèle d'apprentissage supervisé. On utilise le modèle des k-voisins.

On génère un jeu d'entrainement et un jeu de test contenant 33% des valeurs.  
On commence par déterminer le nombre de voisins optimal par validation croisée : on obtient la valeur 12.  
On entraîne ensuite le modèle sur l'ensemble des données d'entraînement avec ce paramètre k=12 optimal, puis on mesure les performances de prédictions du modèle sur le jeu de test. Les performances obtenues sont les suivantes :

- % de prédictions correctes : 84%
- f1-score : 68%
- matrice de confusion :

<img src="Pictures/Partie_2/confusion_k_voisins.png" width="300" />

Lors des tests effectués, on a remarqué que les performances étaient meilleures si on standardisait le jeu de données au préalable. Les résultats ci-dessus ont donc été obtenus avec des variables explicatives standardisées. Les performances du modèles sont globalement correctes.  

Bien qu'il soit intéressant de remarquer que la qualité de l'air dans le métro a une "signature" en fonction du type de jour (semaine ou weekend), cette approche n'a que peu d'intérêt en pratique car on connait toujours la date du jour : une prédiction de ce type n'est donc pas vraiment utile en pratique.


### **Prédiction de la qualité de l'air de la station Franklin Roosevelt**

Au vu de la qualité du jeu de données (voir partie dédiée ci-dessus), ainsi que pour diminuer le travail de collecte de données complémentaires par la suite, on choisit de se limiter aux prédictions de qualité de l'air sur la station Franklin Roosevelt.

Le modèle développé ici se fixe pour objectif de prédire la valeur d'un paramètre de qualité de l'air en se basant uniquement sur l'année, le mois, le numéro du jour dans la semaine et l'heure.

**Construction du modèle**

On se focalise sur un unique paramètre à la fois, mais la démarche est reproductible quel que soit le paramètre. Les éléments qui suivent se basent sur le paramètre N02.

Format du jeu de données injecté dans le modèle :

<img src="Pictures/Partie_2/vecteur_prediction.png" width="250" />

Les analyses préliminaires ont montré que l'évolution de la valeur des paramètres en fonction de l'heure du jour était strictement non linéaire. Nos connaissances en terme d'algorithme de régression non linéaire étant limitées, on utilise ici également l'algorithme des k-voisins, mais dans sa version régression et non classification.

Après division du jeu de donnés en un set d'entrainement et un set de test (33% des données), on détermine le k optimal à partir d'une cross validation sur le jeu d'entraînement. Le paramètre k optimal est 16.

Courbe d'erreur de cross-validation en fonction du paramètre k :

<img src="Pictures/Partie_2/cross_val_predicteur.png" width="450" />

**Performances du modèle**

En prédiction sur le jeu de test, le modèle donne un coefficient de détermination R2 de 0.55. Les performances du modèle sont donc limitées.

Comparons les valeurs moyennes prédites par le modèle sur les différentes échelles de temps par rapport aux valeurs vraies :

<img src="Pictures/Partie_2/comparaison_NO_pred_true_moyens.png" width="1350" />

On constate qu'en moyenne, le modèle semble plutôt bon. En revanche, si il présente un coefficient de détermination aussi faible, c'est qu'il n'est pas performant pour décrire les écarts de qualité de l'air d'un jour à l'autre, ce qui est normal car on n'a pas encore introduit de paramètres permettant par exemple de différencier deux lundis ou deux mardis.


## **3) Enrichissement du jeu de données par des sources complémentaires en vue d'améliorer les prédictions**

Jusqu'à présent, toutes les courbes de qualité de l'air présentées étaient des courbes moyennes obtenues à partir d'un grand nombre de valeur. Essayons maintenant de comparer l'évolution de la qualité de l'air au sein de la station Franklin Roosevelt sans moyenner les valeurs sur plusieurs jours. Par exemple, les courbes ci-dessous comparent les lundis 9 et 16 juin 2014.

<img src="Pictures/Partie_3/comparaison_NO_9_16_juin_2014.png" width="450" />

On constate des écarts de qualité de l'air significatifs sur certaines plages horaires : par exemple autour de 4h du matin le 9 juin 2014, la concentration en NO est de plus de 45 µg/m3, alors qu'elle est de moins de 15 µg/m3 le 16 juin à la même heure. On constate un écart également significatif en fin de journée (35 µg/m3 VS 20 µg/m3).

Or, dans le modèle introduit précédemment, rien ne permet justement de différencier ces deux jours : c'est donc pour cela que le modèle est limité en terme de performances. Cette analyse préliminaire met donc en évidence la nécessité d'introduire de nouvelles variables explicatives dans notre modèle, si l'on veut espérer effectuer des prédictions plus fines. On pourra également essayer d'autre modèles que les k-voisins.


### **Collecte de données complémentaires**

A vous de jouer mes petits poulets !!


### **Nouveaux modèles prédictifs**

Idem et envoyez moi du bois sur les scores de prédiction :)



