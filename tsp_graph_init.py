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


"""
Fichier de génération et gestion d'un graphe de lieux pour le problème du voyageur de commerce (TSP)
Groupe 5 Léa Léa Lou-Anne Lisa
"""

import numpy as np
import random
import csv
import tkinter as tk
from tkinter import Canvas, Text, Scrollbar

# ============================================================================
# CONSTANTES GLOBALES
# ============================================================================

LARGEUR = 800  # Largeur de la zone d'affichage
HAUTEUR = 600  # Hauteur de la zone d'affichage
NB_LIEUX = 10  # Nombre de lieux à générer/charger


# ============================================================================
# CLASSE LIEU
# ============================================================================

class Lieu:
    """
    Classe représentant un lieu avec ses coordonnées (x, y) et son nom.
    Permet de calculer la distance euclidienne entre deux lieux.
    """
    
    def __init__(self, x, y, nom):
        """
        Initialise un lieu avec ses coordonnées et son nom.
        
        Args:
            x (float): Coordonnée x du lieu
            y (float): Coordonnée y du lieu
            nom (str): Nom ou identifiant du lieu
        """
        self.x = x
        self.y = y
        self.nom = nom
    
    def distance(self, autre_lieu):
        """
        Calcule la distance euclidienne entre ce lieu et un autre lieu.
        Distance euclidienne: sqrt((x2-x1)² + (y2-y1)²)
        
        Args:
            autre_lieu (Lieu): L'autre lieu pour calculer la distance
            
        Returns:
            float: La distance euclidienne entre les deux lieux
        """
        # Calcul de la différence en x et y
        dx = self.x - autre_lieu.x
        dy = self.y - autre_lieu.y
        
        # Retourne la distance euclidienne
        return np.sqrt(dx**2 + dy**2)
    
    def __str__(self):
        """Représentation textuelle du lieu"""
        return f"Lieu {self.nom}: ({self.x:.2f}, {self.y:.2f})"


# ============================================================================
# CLASSE GRAPH
# ============================================================================

class Graph:
    """
    Classe représentant un graphe composé de plusieurs lieux.
    Gère la liste des lieux, la matrice des distances et les opérations associées.
    """
    
    def __init__(self):
        """
        Initialise un graphe vide.
        """
        self.liste_lieux = []  # Liste des objets Lieu
        self.matrice_od = None  # Matrice origine-destination (distances)
    
    def generer_lieux_aleatoires(self, nb_lieux=NB_LIEUX):
        """
        Génère aléatoirement des lieux dans l'espace défini par LARGEUR et HAUTEUR.
        Le premier lieu (lieu 0) est toujours le point de départ.
        
        Args:
            nb_lieux (int): Nombre de lieux à générer
        """
        self.liste_lieux = []
        
        # Génération de nb_lieux lieux avec coordonnées aléatoires
        for i in range(nb_lieux):
            # Coordonnées aléatoires dans l'espace défini
            # On laisse une marge de 50 pixels sur les bords pour l'affichage
            x = random.uniform(50, LARGEUR - 50)
            y = random.uniform(50, HAUTEUR - 50)
            
            # Création du lieu avec son numéro comme nom
            lieu = Lieu(x, y, str(i))
            self.liste_lieux.append(lieu)
        
        print(f"{nb_lieux} lieux générés aléatoirement.")
    
    def charger_graph(self, nom_fichier):
        """
        Charge la liste des lieux depuis un fichier CSV.
        Format attendu du CSV: nom,x,y (avec ou sans en-tête)
        
        Args:
            nom_fichier (str): Chemin vers le fichier CSV
        """
        self.liste_lieux = []
        
        try:
            with open(nom_fichier, 'r', encoding='utf-8') as fichier:
                lecteur = csv.reader(fichier)
                
                # Lecture de la première ligne pour détecter si c'est un en-tête
                premiere_ligne = next(lecteur)
                
                # Si la première ligne contient des nombres, c'est une donnée
                try:
                    x = float(premiere_ligne[1])
                    y = float(premiere_ligne[2])
                    nom = premiere_ligne[0]
                    lieu = Lieu(x, y, nom)
                    self.liste_lieux.append(lieu)
                except (ValueError, IndexError):
                    # C'est un en-tête, on l'ignore
                    pass
                
                # Lecture du reste des lignes
                for ligne in lecteur:
                    if len(ligne) >= 3:
                        nom = ligne[0]
                        x = float(ligne[1])
                        y = float(ligne[2])
                        lieu = Lieu(x, y, nom)
                        self.liste_lieux.append(lieu)
            
            print(f"{len(self.liste_lieux)} lieux chargés depuis {nom_fichier}.")
            
        except FileNotFoundError:
            print(f"Erreur: Le fichier {nom_fichier} n'existe pas.")
        except Exception as e:
            print(f"Erreur lors du chargement du fichier: {e}")
    
    def calcul_matrice_cout_od(self):
        """
        Calcule la matrice des distances (coûts) entre tous les lieux du graphe.
        Optimisation: On ne calcule qu'une fois chaque distance car distance(A,B) = distance(B,A).
        La matrice est symétrique avec des 0 sur la diagonale.
        
        Returns:
            numpy.ndarray: Matrice carrée des distances
        """
        n = len(self.liste_lieux)
        
        # Initialisation de la matrice avec des zéros
        self.matrice_od = np.zeros((n, n))
        
        # Remplissage de la matrice triangulaire supérieure
        # Optimisation: on ne calcule qu'une fois chaque distance
        for i in range(n):
            for j in range(i + 1, n):  # Commence à i+1 pour éviter la diagonale et les doublons
                # Calcul de la distance entre lieu i et lieu j
                dist = self.liste_lieux[i].distance(self.liste_lieux[j])
                
                # Stockage symétrique: distance(i,j) = distance(j,i)
                self.matrice_od[i][j] = dist
                self.matrice_od[j][i] = dist
        
        print("Matrice des distances calculée.")
        return self.matrice_od

def plus_proche_voisin(self, indice_lieu, lieux_non_visites):
        """
        Trouve le plus proche voisin d'un lieu donné parmi un ensemble de lieux non visités.
        Utilise la matrice de distances précalculée.
        Optimisation: ne parcourt que les lieux du set fourni au lieu de toute la liste.
        
        Args:
            indice_lieu (int): Indice du lieu de référence
            lieux_non_visites (set): Ensemble des indices des lieux non encore visités
            
        Returns:
            int: Indice du plus proche voisin, ou None si l'ensemble est vide
        """
        if not lieux_non_visites:
            return None
        
        # Distance minimale initialisée à l'infini
        distance_min = float('inf')
        indice_plus_proche = None
        
        # Parcours uniquement des lieux non visités (optimisation)
        for i in lieux_non_visites:
            # Récupération de la distance depuis la matrice précalculée
            dist = self.matrice_od[indice_lieu][i]
            
            # Mise à jour si on trouve un lieu plus proche
            if dist < distance_min:
                distance_min = dist
                indice_plus_proche = i
        
        return indice_plus_proche
    
# ============================================================================
# CLASSE ROUTE
# ============================================================================

class Route:
    """
    Classe représentant une route traversant tous les lieux d'un graphe.
    La route commence et se termine au lieu 0 (point de départ).
    """
    
    def __init__(self, graph):
        """
        Initialise une route pour un graphe donné.
        
        Args:
            graph (Graph): Le graphe contenant les lieux à visiter
        """
        self.graph = graph
        self.ordre = []  # Ordre de visite des lieux [0, 3, 8, 1, 2, 4, 6, 5, 9, 7, 0]
    
    def calcul_distance_route(self):
        """
        Calcule la distance totale de la route en utilisant l'ordre de visite.
        Parcourt tous les segments de la route et somme les distances.
        
        Returns:
            float: Distance totale de la route
        """
        distance_totale = 0.0
        
        # Parcours de la route et somme des distances entre lieux consécutifs
        for i in range(len(self.ordre) - 1):
            lieu_depart = self.ordre[i]
            lieu_arrivee = self.ordre[i + 1]
            distance_totale += self.graph.matrice_od[lieu_depart][lieu_arrivee]
        
        return distance_totale

# ============================================================================
# CLASSE AFFICHAGE
# ============================================================================

