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
import random
import time

# ============================================================================
# CONSTANTES GLOBALES
# ============================================================================

LARGEUR = 800  # Largeur de la zone d'affichage
HAUTEUR = 600  # Hauteur de la zone d'affichage
NB_LIEUX = 30  # Nombre de lieux à générer/charger depuis un fichier csv

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
    def __init__(self, x, y, nom):
    
        """
        Initialise un lieu avec ses coordonnées et son nom.
        
        Args:
            x (float): Coordonnée x du lieu
            y (float): Coordonnée y du lieu
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
    
    def __repr__(self):
        return f"Lieu {self.nom}: ({self.x:.2f}, {self.y:.2f})"

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
                
                for num_ligne, ligne in enumerate(lecteur):
                    if len(ligne) <2 :
                        continue
                    
                    print(f"Ligne {num_ligne}: {ligne}")
                    
                # Lecture de la première ligne pour détecter si c'est un en-tête
                # premiere_ligne = next(lecteur)
                # print(f"Première ligne du fichier: {premiere_ligne}")
                
                # On vérifie si la première ligne est une donnée (x, y)
                    try:
                    # On vérifie les colonnes 1 et 2 pour les nombres
                        x = float(ligne[0])
                        y = float(ligne[1])
                    
                        nom=str(len(self.liste_lieux))
                        lieu = Lieu(x, y, nom)
                        self.liste_lieux.append(lieu)
                
                    except (ValueError, IndexError): 
                        pass
                    # C'est un en-tête (ex: "nom", "x", "y") ou format invalide, on l'ignore 
                    
                
                # Lecture du reste des lignes
                for ligne in lecteur:
                    if len(ligne) >= 3: # S'assurer qu'on a au moins 3 colonnes
                        try:
                            x = float(ligne[0])
                            y = float(ligne[1])
                            
                            nom=str(len(self.liste_lieux))
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

class Affichage:
    """
    Classe pour l'affichage graphique du graphe et des routes avec Tkinter.
    Affiche les lieux, la meilleure route, et des informations textuelles.
    """
    
    def __init__(self, graph, titre="Groupe 5"):
        """
        Initialise l'interface graphique.
        
        Args:
            graph (Graph): Le graphe à afficher
            titre (str): Titre de la fenêtre
        """
        self.graph = graph
        self.meilleure_route = None
        self.routes_population = []  # Pour stocker les N meilleures routes
        self.afficher_population = False  # Flag pour afficher/masquer les routes
        
        # Création de la fenêtre principale
        self.root = tk.Tk()
        self.root.title(titre)
        
        # Canvas pour le dessin
        self.canvas = Canvas(self.root, width=LARGEUR, height=HAUTEUR, bg="white")
        self.canvas.pack()
        
        # Frame pour la zone de texte avec scrollbar
        text_frame = tk.Frame(self.root)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Zone de texte pour les informations
        self.text_info = Text(text_frame, height=10, width=100, 
                             yscrollcommand=scrollbar.set)
        self.text_info.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.text_info.yview)
        
        # Gestion des événements clavier
        self.root.bind('<Escape>', self.quitter)
        self.root.bind('<space>', self.toggle_population)  # Touche espace pour afficher/masquer
        
        # Affichage initial
        self.afficher_lieux()
        self.ajouter_texte("Interface initialisée.\n")
        self.ajouter_texte("Appuyez sur ESPACE pour afficher/masquer les routes secondaires.\n")
        self.ajouter_texte("Appuyez sur ESC pour quitter.\n")
    
    def afficher_lieux(self):
        """
        Affiche tous les lieux du graphe sous forme de cercles avec leur numéro.
        """
        rayon = 15
        
        for i, lieu in enumerate(self.graph.liste_lieux):
            x, y = lieu.x, lieu.y

            # Couleur spécifique pour le point 0
            couleur = "red" if i == 0 else "lightgray"
            
            # Dessin du cercle
            self.canvas.create_oval(x - rayon, y - rayon, 
                                   x + rayon, y + rayon,
                                   fill=couleur, outline="black", width=2)
            
            # Numéro du lieu au centre
            self.canvas.create_text(x, y, text=str(i), 
                                   font=("Arial", 10, "bold"))
    
    def afficher_route(self, route, couleur="blue", style="", largeur=2, afficher_ordre=True):
        """
        Affiche une route sur le canvas.
        
        Args:
            route (Route): La route à afficher
            couleur (str): Couleur de la ligne
            style (str): Style de ligne ("" pour continu, "dash" pour pointillé)
            largeur (int): Épaisseur de la ligne
            afficher_ordre (bool): Si True, affiche l'ordre de visite au-dessus des lieux
        """
        if not route or not route.ordre:
            return
        
        # Configuration du style de ligne
        dash_config = (5, 5) if style == "dash" else ()
        
        # Traçage de la route
        for i in range(len(route.ordre) - 1):
            lieu_depart = self.graph.liste_lieux[route.ordre[i]]
            lieu_arrivee = self.graph.liste_lieux[route.ordre[i + 1]]
            
            self.canvas.create_line(lieu_depart.x, lieu_depart.y,
                                   lieu_arrivee.x, lieu_arrivee.y,
                                   fill=couleur, width=largeur, dash=dash_config)
    
    def afficher_meilleure_route(self, route):
        """
        Affiche la meilleure route trouvée en bleu pointillé.
        
        Args:
            route (Route): La meilleure route à afficher
        """
        self.meilleure_route = route
        self.rafraichir_affichage()
    
    def afficher_routes_secondaires(self, routes):
        """
        Stocke les N meilleures routes pour affichage optionnel.
        
        Args:
            routes (list): Liste de Route à afficher en gris clair
        """
        self.routes_population = routes
        if self.afficher_population:
            self.rafraichir_affichage()
    
    def toggle_population(self, event=None):
        """
        Active/désactive l'affichage des routes secondaires.
        """
        self.afficher_population = not self.afficher_population
        self.rafraichir_affichage()
        
        if self.afficher_population:
            self.ajouter_texte(f"Affichage de {len(self.routes_population)} routes secondaires activé.\n")
        else:
            self.ajouter_texte("Affichage des routes secondaires désactivé.\n")
    
    def rafraichir_affichage(self):
        """
        Efface et redessine tous les éléments graphiques.
        """
        self.canvas.delete("all")
        
        # Affichage des routes secondaires si activé
        if self.afficher_population:
            for route in self.routes_population:
                self.afficher_route(route, couleur="lightgray", largeur=1, afficher_ordre=False)
        
        # Affichage de la meilleure route
        if self.meilleure_route:
            self.afficher_route(self.meilleure_route, couleur="blue", 
                              style="dash", largeur=2, afficher_ordre=True)
        
        # Réaffichage des lieux (par-dessus les routes)
        self.afficher_lieux()
    
    def ajouter_texte(self, texte):
        """
        Ajoute du texte dans la zone d'information.
        
        Args:
            texte (str): Texte à ajouter
        """
        self.text_info.insert(tk.END, texte)
        self.text_info.see(tk.END)  # Scroll automatique vers le bas
    
    def quitter(self, event=None):
        """
        Ferme l'application proprement.
        """
        self.ajouter_texte("\nFermeture de l'application...\n")
        self.root.quit()
        self.root.destroy()
    
    def lancer(self):
        """
        Lance la boucle principale de l'interface graphique.
        """
        self.root.mainloop()

# ============================================================================
# CLASSE TSP_GA
# ============================================================================

"""
TSP_GA avec affichage dans UNE SEULE fenêtre
L'affichage se met à jour pendant l'exécution
"""

import threading

class TSP_GA_Interactive:
    """
    Algorithme génétique avec affichage interactif.
    Mise à jour de l'affichage pendant l'exécution.
    """
    
    def __init__(self, graph, affichage):
        """
        Args:
            graph (Graph): Le graphe
            affichage (Affichage): L'interface graphique
        """
        self.graph = graph
        self.affichage = affichage
        self.nb_lieux = len(graph.liste_lieux)
        
        # Configuration
        self._configurer_parametres()
        
        # Variables
        self.population = []
        self.meilleure_route = None
        self.meilleure_distance = float('inf')
        self.iteration_meilleure = 0
        self.iteration_courante = 0
        self.en_cours = False
    
    def _configurer_parametres(self):
        """Configure les paramètres selon le nombre de lieux."""
        n = self.nb_lieux
        
        if n <= 10:
            self.taille_population = 20
            self.nb_elite = 2
            self.taux_mutation = 0.1
            self.taux_crossover = 0.7
            self.nb_iterations_max = 50
            self.frequence_affichage = 5 
        elif n <= 20:
            self.taille_population = 30
            self.nb_elite = 3
            self.taux_mutation = 0.08
            self.taux_crossover = 0.75
            self.nb_iterations_max = 100
            self.frequence_affichage = 10
        elif n <= 50:
            self.taille_population = 30
            self.nb_elite = 3
            self.taux_mutation = 0.05
            self.taux_crossover = 0.75
            self.nb_iterations_max = 150
            self.frequence_affichage = 15
        elif n <= 100:
            self.taille_population = 25
            self.nb_elite = 3
            self.taux_mutation = 0.05
            self.taux_crossover = 0.7
            self.nb_iterations_max = 100
            self.frequence_affichage = 10
        elif n <= 200:
            self.taille_population = 20
            self.nb_elite = 2
            self.taux_mutation = 0.08
            self.taux_crossover = 0.65
            self.nb_iterations_max = 75
            self.frequence_affichage = 10
        elif n <= 500:
            self.taille_population = 15
            self.nb_elite = 2
            self.taux_mutation = 0.1
            self.taux_crossover = 0.6
            self.nb_iterations_max = 50
            self.frequence_affichage = 5
        elif n <= 1000:
            self.taille_population = 12
            self.nb_elite = 2
            self.taux_mutation = 0.12
            self.taux_crossover = 0.55
            self.nb_iterations_max = 40
            self.frequence_affichage = 5
        else:
            self.taille_population = max(8, 10000 // n)
            self.nb_elite = 1
            self.taux_mutation = 0.15
            self.taux_crossover = 0.5
            self.nb_iterations_max = max(20, 20000 // n)
            self.frequence_affichage = 5
    
    def initialiser_avec_heuristique(self):
        """
        Initialise avec l'heuristique du plus proche voisin.
        AFFICHE la route heuristique dans l'interface.
        """
        from __main__ import Route
        
        # Heuristique = plus proche voisin
        route_heuristique = Route(self.graph)
        ordre = [0]
        lieux_non_visites = set(range(1, self.nb_lieux))
        lieu_actuel = 0
        
        while lieux_non_visites:
            prochain = self.graph.plus_proche_voisin(lieu_actuel, lieux_non_visites)
            if prochain is None:
                break
            ordre.append(prochain)
            lieux_non_visites.remove(prochain)
            lieu_actuel = prochain
        
        ordre.append(0)
        route_heuristique.ordre = ordre
        route_heuristique._distance_cache = route_heuristique.calcul_distance_route()
        
        print(f"Route heuristique: {route_heuristique._distance_cache:.2f}")
        
        # AFFICHAGE de la route heuristique
        self.affichage.afficher_meilleure_route(route_heuristique)
        self.affichage.ajouter_texte(f"Route heuristique (plus proche voisin): {route_heuristique._distance_cache:.2f}\n")
        self.affichage.ajouter_texte(f"   Ordre: {route_heuristique.ordre}\n\n")
        
        # Initialisation de la population
        self.population = [route_heuristique]  # Commence avec l'heuristique
        
        for _ in range(self.taille_population - 1):
            route = Route(self.graph)
            lieux = list(range(1, self.nb_lieux))
            random.shuffle(lieux)
            route.ordre = [0] + lieux + [0]
            route._distance_cache = route.calcul_distance_route()
            self.population.append(route)
        
        # Tri
        self.population.sort(key=lambda r: r._distance_cache)
        self.meilleure_route = self.population[0]
        self.meilleure_distance = self.meilleure_route._distance_cache
    
    def _actualiser_affichage_safe(self):
        """Met à jour l'affichage de manière thread-safe."""
        try:
            def update():
                # Top 10 routes uniques
                routes_uniques = []
                distances_vues = set()
                for route in self.population[:20]:
                    if route._distance_cache not in distances_vues:
                        distances_vues.add(route._distance_cache)
                        routes_uniques.append(route)
                    if len(routes_uniques) >= 10:
                        break
                
                # Affichage
                if len(routes_uniques) > 1:
                    self.affichage.afficher_routes_secondaires(routes_uniques[1:])
                self.affichage.afficher_meilleure_route(self.meilleure_route)
            
            self.affichage.root.after(0, update)
        except:
            pass
    
    def selection_tournoi(self, taille_tournoi=3):
        """Sélection par tournoi."""
        taille_tournoi = min(taille_tournoi, len(self.population) // 2)
        candidats = random.sample(self.population, taille_tournoi)
        return min(candidats, key=lambda r: r._distance_cache)
    
    def crossover_ox(self, parent1, parent2):
        """Crossover OX."""
        from __main__ import Route
        
        ordre1 = parent1.ordre[1:-1]
        ordre2 = parent2.ordre[1:-1]
        taille = len(ordre1)
        
        if taille < 2:
            enfant = Route(self.graph)
            enfant.ordre = parent1.ordre.copy()
            enfant._distance_cache = parent1._distance_cache
            return enfant
        
        point1 = random.randint(0, taille - 1)
        point2 = random.randint(point1 + 1, taille)
        
        enfant_ordre = [None] * taille
        enfant_ordre[point1:point2] = ordre1[point1:point2]
        
        villes_utilisees = set(enfant_ordre[point1:point2])
        position = point2
        
        for ville in ordre2[point2:] + ordre2[:point2]:
            if ville not in villes_utilisees:
                enfant_ordre[position % taille] = ville
                villes_utilisees.add(ville)
                position += 1
        
        enfant = Route(self.graph)
        enfant.ordre = [0] + enfant_ordre + [0]
        enfant._distance_cache = enfant.calcul_distance_route()
        return enfant
    
    def mutation_swap(self, route):
        """Mutation swap."""
        if random.random() < self.taux_mutation:
            ordre = route.ordre[1:-1]
            if len(ordre) > 1:
                i, j = random.sample(range(len(ordre)), 2)
                ordre[i], ordre[j] = ordre[j], ordre[i]
                route.ordre = [0] + ordre + [0]
                route._distance_cache = None
    
    def mutation_2opt(self, route):
        """Mutation 2-opt."""
        if random.random() < self.taux_mutation * 0.5:
            ordre = route.ordre[1:-1]
            if len(ordre) > 3:
                i = random.randint(0, len(ordre) - 3)
                j = random.randint(i + 2, len(ordre))
                ordre[i:j] = reversed(ordre[i:j])
                route.ordre = [0] + ordre + [0]
                route._distance_cache = None
    
    def nouvelle_generation(self):
        """Nouvelle génération avec élitisme."""
        from __main__ import Route
        
        nouvelle_population = []
        
        # Élitisme
        for i in range(self.nb_elite):
            nouvelle_population.append(self.population[i])
        
        # Génération
        compteur = 0
        while len(nouvelle_population) < self.taille_population and compteur < self.taille_population * 5:
            compteur += 1
            
            try:
                parent1 = self.selection_tournoi()
                parent2 = self.selection_tournoi()
                
                if random.random() < self.taux_crossover:
                    enfant = self.crossover_ox(parent1, parent2)
                else:
                    enfant = Route(self.graph)
                    enfant.ordre = parent1.ordre.copy()
                    enfant._distance_cache = parent1._distance_cache
                
                self.mutation_swap(enfant)
                if self.nb_lieux <= 100:
                    self.mutation_2opt(enfant)
                
                if enfant._distance_cache is None:
                    enfant._distance_cache = enfant.calcul_distance_route()
                
                # Pas de doublons
                est_doublon = any(r.ordre == enfant.ordre for r in nouvelle_population)
                if not est_doublon:
                    nouvelle_population.append(enfant)
            except:
                pass
        
        # Compléter si besoin
        while len(nouvelle_population) < self.taille_population:
            route = Route(self.graph)
            lieux = list(range(1, self.nb_lieux))
            random.shuffle(lieux)
            route.ordre = [0] + lieux + [0]
            route._distance_cache = route.calcul_distance_route()
            nouvelle_population.append(route)
        
        self.population = nouvelle_population
        self.population.sort(key=lambda r: r._distance_cache)
        
        # Mise à jour meilleure
        distance_actuelle = self.population[0]._distance_cache
        if distance_actuelle < self.meilleure_distance:
            self.meilleure_route = self.population[0]
            self.meilleure_distance = distance_actuelle
            self.iteration_meilleure = self.iteration_courante
            return True  # Amélioration trouvée
        return False
    
    def executer_thread(self):
        """Exécute l'algo dans un thread."""
        import time
        
        temps_debut = time.time()
        self.affichage.ajouter_texte(f"Algorithme génétique: {self.nb_iterations_max} itérations\n\n")
        
        for iteration in range(1, self.nb_iterations_max + 1):
            if not self.en_cours:
                break
            
            self.iteration_courante = iteration
            amelioration = self.nouvelle_generation()
            
            # Affichage périodique OU si amélioration
            if iteration % self.frequence_affichage == 0 or amelioration or iteration == self.nb_iterations_max:
                self._actualiser_affichage_safe()
                
                temps_ecoule = time.time() - temps_debut
                vitesse = iteration / temps_ecoule if temps_ecoule > 0 else 0

                info = (f"Iter {iteration:3d}/{self.nb_iterations_max} | "
                       f"Best: {self.meilleure_distance:7.2f} | "
                       f"Found: iter {self.iteration_meilleure:3d}")

                if amelioration:
                    self.affichage.root.after(0, lambda i=info: self.affichage.ajouter_texte(i + "\n"))
        
        # Final
        temps_total = time.time() - temps_debut
        
        def affichage_final():
            self.affichage.ajouter_texte(f"Meilleure distance: {self.meilleure_distance:.2f}\n")
            self.affichage.ajouter_texte(f"Trouvée: itération {self.iteration_meilleure}\n")
            self.affichage.ajouter_texte(f"Temps: {temps_total:.2f}s\n")
        
        self.affichage.root.after(0, affichage_final)
        self.en_cours = False
    
    def lancer(self):
        """Lance l'algorithme dans un thread."""
        self.en_cours = True
        thread = threading.Thread(target=self.executer_thread, daemon=False)
        thread.start()


# ============================================================================
# FONCTION PRINCIPALE
# ============================================================================

def main_interactive(nom_fichier=None):

    from __main__ import Graph, Affichage, NB_LIEUX
    
    # Chargement
    if nom_fichier:
        graph = Graph(path=nom_fichier)
    else:
        graph = Graph(path=None, nb_lieux_defaut=NB_LIEUX)
    
    if not graph.liste_lieux:
        print("Erreur")
        return
    
    # Interface
    affichage = Affichage(graph, titre=f"TSP - {len(graph.liste_lieux)} lieux")
    
    # Algorithme
    tsp_ga = TSP_GA_Interactive(graph, affichage)
    tsp_ga.initialiser_avec_heuristique()
    
    # Lancement dans un thread
    affichage.root.after(1000, tsp_ga.lancer)
    
    # Interface (bloquant)
    affichage.lancer()


if __name__ == "__main__":
    
    # === OPTION 1 : FICHIER CSV ===================================
    # Décommente pour utiliser un fichier fourni
    utiliser_fichier = False  # <<<<<<<< mettre False pour tester avec génération aléatoire

    if utiliser_fichier:
        nom_fichier = "graph_20.csv" 
        graph = Graph(path=nom_fichier)

    # === OPTION 2 : GÉNÉRATION ALÉATOIRE ===========================
    else:
        NB_LIEUX = 50  # <<<<<<<< tu mets la valeur que tu veux ici
        graph = Graph(path=None, nb_lieux_defaut=NB_LIEUX)

    # Vérification
    if not graph.liste_lieux:
        print("Erreur: graphe vide.")
    else:
        # Lancement du programme interactif complet
        main_interactive(nom_fichier=None)
