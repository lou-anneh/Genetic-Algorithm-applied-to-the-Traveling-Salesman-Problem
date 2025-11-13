"""
Fichier de génération et gestion d'un graphe de lieux pour le problème du voyageur de commerce (TSP)
Groupe 5
#test
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

NB_LIEUX = 5  # Nombre de lieux à générer/charger depuis un fichier csv

# ============================================================================
# CLASSE LIEU
#Cette classe sert à mémoriser les coordonnées x et y du lieu à visiter et son nom
#La classe disposera d'une fonction de calcul de distance entre 2 lieux.
#La distance utilisée est la distance euclidienne.
# ============================================================================

class Lieu:   
    """
    Classe représentant un lieu avec ses coordonnées (x, y) et son nom.
    Permet de calculer la distance euclidienne entre deux lieux.
    """
    def __init__(self, x, y):
    
        """
        Initialise un lieu avec ses coordonnées et son nom.
        
        Args:
            x (float): Coordonnée x du lieu
            y (float): Coordonnée y du lieu
        """
        self.x = x
        self.y = y
    
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
    
    def __repr__(self):
        return "("+ str(self.x)+", "+str(self.y)+")"


# ============================================================================
# CLASSE GRAPH
#Cette classe est utilisée pour mémoriser une liste de lieux (variable liste_lieux).
#La liste des lieux devra être récupérée du TP précédent ou générée de manière aléatoire avec des coordonnées qui devront être adaptées pour tenir dans un espace défini grâce à deux constantes LARGEUR=800 et HAUTEUR=600. 
#Le nombre de lieux sera défini dans une constante nommée NB_LIEUX.
#Une fonction nommée calcul_matrice_cout_od sera définie pour calculer ou importer une matrice de distances entre chaque lieu du graphe et stocker ce résultat dans une variable de classe matrice_od.
#Le graph disposera également d'une fonction nommée plus_proche_voisin permettant de renvoyer le plus proche voisin d'un lieu en utilisant la matrice de distances.
#Cette classe disposera d'une méthode de lecture dans un fichier CSV de la liste des coordonnées des lieux (charger_graph).
#Des fichiers CSV contenant des exemples de liste de lieux sont fournis sur moodle. Les fichiers CSV utilisés pour l'évaluation auront exactement la même structure.

# ============================================================================

import numpy as np
import random
import csv
# Assure-toi que Lieu est défini au-dessus de ce code
# Assure-toi que les constantes (LARGEUR, HAUTEUR, NB_LIEUX) sont définies

class Graph:
    """
    Classe représentant un graphe composé de plusieurs lieux.
    Gère la liste des lieux, la matrice des distances et les opérations associées.
    """
    
    def __init__(self, path=None, nb_lieux_defaut=NB_LIEUX):
        """
        Initialise un graphe.
        Si path est None, génère des lieux aléatoires (Cas 1).
        Si path est fourni, charge les lieux depuis le fichier (Cas 2).
        
        Args:
            path (str, optional): Chemin vers le fichier CSV.
            nb_lieux_defaut (int, optional): Nombre de lieux à générer si path est None.
        """
        self.liste_lieux = []
        self.matrice_od = None
        
        if path is None:
            # CAS 1: Génération aléatoire si aucun fichier n'est fourni
            print("Mode: Génération aléatoire de lieux.")
            self.generer_lieux_aleatoires(nb_lieux_defaut)
        else:
            # CAS 2: Chargement depuis un fichier
            print(f"Mode: Chargement depuis le fichier {path}.")
            self.charger_graph(path)
            
        # Après la génération OU le chargement, on calcule la matrice
        if self.liste_lieux:
            self.calcul_matrice_cout_od()
        else:
            print("Erreur: Aucun lieu n'a été chargé ou généré.")

    
    def generer_lieux_aleatoires(self, nb_lieux=NB_LIEUX):
        """
        CAS 1: Génère aléatoirement des lieux dans l'espace défini par LARGEUR et HAUTEUR.
        
        Args:
            nb_lieux (int): Nombre de lieux à générer
        """
        self.liste_lieux = []
        
        for i in range(nb_lieux):
            x = random.uniform(50, LARGEUR - 50)
            y = random.uniform(50, HAUTEUR - 50)
            lieu = Lieu(x, y, str(i))
            self.liste_lieux.append(lieu)
        
        print(f"{nb_lieux} lieux générés aléatoirement.")
    
    
    def charger_graph(self, nom_fichier):
        """
        CAS 2 : Charge la liste des lieux depuis un fichier CSV.
        Format attendu du CSV: nom,x,y (avec ou sans en-tête)
        Met également à jour la variable globale NB_LIEUX.
        
        Args:
            nom_fichier (str): Chemin vers le fichier CSV (ex: "graph_5.csv")
        """
        self.liste_lieux = []
        global NB_LIEUX # Indique qu'on veut modifier la variable GLOBALE

        try:
            # Extraction de NB_LIEUX depuis le nom du fichier
            # Ex: "data/graph_5.csv" -> "graph_5.csv"
            nom_base = nom_fichier.split('/')[-1]
            # "graph_5.csv" -> ["graph", "5.csv"] -> "5.csv"
            partie_num = nom_base.split('_')[1]
            # "5.csv" -> ["5", "csv"] -> "5"
            nb_str = partie_num.split('.')[0]
            
            NB_LIEUX = int(nb_str)
            print(f"Variable globale NB_LIEUX mise à jour à {NB_LIEUX} (via le nom du fichier).")

        except (IndexError, ValueError, TypeError):
            print(f"Avertissement: Impossible d'extraire NB_LIEUX depuis le nom '{nom_fichier}'.")
            print("Le format attendu est 'prefix_NOMBRE.csv'.")
        
        try:
            with open(nom_fichier, 'r', encoding='utf-8') as fichier:
                lecteur = csv.reader(fichier)
                
                # Lecture de la première ligne pour détecter si c'est un en-tête
                premiere_ligne = next(lecteur)
                
                # On vérifie si la première ligne est une donnée (nom, x, y)
                try:
                    # On vérifie les colonnes 1 et 2 pour les nombres
                    x = float(premiere_ligne[1])
                    y = float(premiere_ligne[2])
                    nom = premiere_ligne[0]
                    lieu = Lieu(x, y, nom)
                    self.liste_lieux.append(lieu)
                
                except (ValueError, IndexError):
                    # C'est un en-tête (ex: "nom", "x", "y") ou format invalide, on l'ignore
                    pass
                
                # Lecture du reste des lignes
                for ligne in lecteur:
                    if len(ligne) >= 3: # S'assurer qu'on a au moins 3 colonnes
                        try:
                            nom = ligne[0]
                            x = float(ligne[1])
                            y = float(ligne[2])
                            lieu = Lieu(x, y, nom)
                            self.liste_lieux.append(lieu)
                        except ValueError:
                            # Ignorer les lignes mal formatées (ex: du texte dans x ou y)
                            print(f"Ligne ignorée (format non numérique): {ligne}")
                
            print(f"{len(self.liste_lieux)} lieux chargés depuis {nom_fichier}.")
            
            # Vérification de cohérence
            if len(self.liste_lieux) != NB_LIEUX:
                 print(f"Avertissement: Le fichier contient {len(self.liste_lieux)} lieux, "
                       f"mais le nom du fichier indiquait {NB_LIEUX}.")
                 # On met à jour NB_LIEUX pour refléter la réalité du fichier
                 NB_LIEUX = len(self.liste_lieux)
                 print(f"NB_LIEUX ajusté à {NB_LIEUX}.")

        except FileNotFoundError:
            print(f"Erreur: Le fichier {nom_fichier} n'existe pas.")
        except StopIteration:
            # Gère le cas où le fichier est complètement vide
            print(f"Erreur: Le fichier {nom_fichier} est vide.")
        except Exception as e:
            print(f"Erreur lors du chargement du fichier: {e}")

    
    def calcul_matrice_cout_od(self):
        """
        Calcule la matrice des distances (coûts) entre tous les lieux du graphe.
        """
        n = len(self.liste_lieux)
        if n == 0:
            print("Impossible de calculer la matrice: liste_lieux est vide.")
            return None
            
        self.matrice_od = np.zeros((n, n))
        
        for i in range(n):
            for j in range(i + 1, n): 
                dist = self.liste_lieux[i].distance(self.liste_lieux[j])
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
