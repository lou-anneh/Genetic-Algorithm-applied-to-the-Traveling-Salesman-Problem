#create classes 

#classe Lieu
#Cette classe sert à mémoriser les coordonnées x et y du lieu à visiter et son nom
#La classe disposera d'une fonction de calcul de distance entre 2 lieux.
#La distance utilisée est la distance euclidienne.


#classe Graphe
#Cette classe est utilisée pour mémoriser une liste de lieux (variable liste_lieux).
#La liste des lieux devra être récupérée du TP précédent ou générée de manière aléatoire avec des coordonnées qui devront être adaptées pour tenir dans un espace défini grâce à deux constantes LARGEUR=800 et HAUTEUR=600. 
#Le nombre de lieux sera défini dans une constante nommée NB_LIEUX.
#Une fonction nommée calcul_matrice_cout_od sera définie pour calculer ou importer une matrice de distances entre chaque lieu du graphe et stocker ce résultat dans une variable de classe matrice_od.
#Le graph disposera également d'une fonction nommée plus_proche_voisin permettant de renvoyer le plus proche voisin d'un lieu en utilisant la matrice de distances.
#Cette classe disposera d'une méthode de lecture dans un fichier CSV de la liste des coordonnées des lieux (charger_graph).
#Des fichiers CSV contenant des exemples de liste de lieux sont fournis sur moodle. Les fichiers CSV utilisés pour l'évaluation auront exactement la même structure.


# #classe Route
# Cette classe sert à générer une route traversant tous les lieux d'un graph. La classe route disposera d'une variable ordre représentant la succession des lieux visités. Une contrainte particulière impose que le premier et dernier élément visité soit le lieu de départ du graphe correspondant au lieu numéroté 0 dans la variable liste_lieux du graph.
# Exemple de contenu de la variable ordre d'une route : [0,3,8,1,2,4,6,5,9,7,0] 
# Une fonction de calcul de la distance totale de la route nommée calcul_distance_route devra être créée dans la classe Graph.
# La distance utilisée est la distance euclidienne.

# •	classe Affichage:
# La classe Affichage servira à afficher les Lieux du graphe sous forme de cercles avec le numéro du Lieu inscrit au milieu du cercle.
# Vous indiquerez le nom de votre groupe dans le titre de la fenêtre Tkinter
# Les éléments graphiques seront dessinés dans un espace de type Canvas d'une taille définie par les constantes LARGEUR et HAUTEUR.
# Une zone de texte positionnée en dessous de la zone graphique servira à afficher l'évolution des étapes des différents algorithmes (nombre d'itérations, meilleure distance trouvée, etc...)
# Cette classe affichera une ligne bleue pointillée représentant la meilleure route trouvée.
# L'ordre de visite des lieux de la route sera indiqué au-dessus de chaque Lieu visité.
# L'appui sur une touche de votre choix devra permettre d'afficher en fonction de votre algorithme:
# - les N meilleures routes trouvées en gris clair (population pour l'algorithme génétique) par exemple 5.
# - une matrice de coûts de déplacements entre les Lieux (phéromones pour l'algorithme des colonies de fourmis)
# L'appui sur la touche ESC servira à quitter complètement le programme et fermer l'interface graphique.

