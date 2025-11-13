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
    

    def plus_proche_voisin(self, indice_lieu, lieux_visites=None):
        """
        Trouve le plus proche voisin d'un lieu donné parmi les lieux non encore visités.
        Utilise la matrice de distances précalculée.
        
        Args:
            indice_lieu (int): Indice du lieu de référence
            lieux_visites (set): Ensemble des indices des lieux déjà visités
            
        Returns:
            int: Indice du plus proche voisin, ou None si tous les lieux sont visités
        """
        if self.matrice_od is None:
            print("Erreur: La matrice des distances n'est pas calculée.")
            return None
            
        if lieux_visites is None:
            lieux_visites = set()
        
        distance_min = float('inf')
        indice_plus_proche = None
        
        # Parcours de tous les lieux
        for i in range(len(self.liste_lieux)):
            # On ignore le lieu lui-même ET les lieux déjà visités
            if i != indice_lieu and i not in lieux_visites:
                dist = self.matrice_od[indice_lieu][i]
                
                if dist < distance_min:
                    distance_min = dist
                    indice_plus_proche = i
        
        return indice_plus_proche
    

    def calcul_distance_route(self, route):
        """
        Calcule la distance totale d'une route (succession de lieux).
        Utilise la matrice de distances précalculée.
        
        Args:
            route (Route): Objet Route contenant l'ordre de visite
            
        Returns:
            float: Distance totale de la route
        """
        if self.matrice_od is None:
            print("Erreur: La matrice des distances n'est pas calculée.")
            return 0.0

        distance_totale = 0.0
        ordre = route.ordre
        
        for i in range(len(ordre) - 1):
            lieu_depart = ordre[i]
            lieu_arrivee = ordre[i + 1]
            distance_totale += self.matrice_od[lieu_depart][lieu_arrivee]
        
        return distance_totale

# ============================================================================
# CLASSE ROUTE
# ============================================================================

class Route:
    """
    Classe représentant une route (un parcours) visitant tous les lieux d'un graphe.
    La route commence et se termine toujours au lieu 0 (dépôt).
    """
    
    def __init__(self, graph):
        """
        Initialise une route vide pour un graphe donné.
        
        Args:
            graph (Graph): Le graphe contenant les lieux à visiter
        """
        self.graph = graph
        self.ordre = []  # Liste ordonnée des indices des lieux visités
        self.distance = None  # Distance totale de la route (calculée à la demande)
    
    def generer_route_aleatoire(self):
        """
        Génère une route aléatoire visitant tous les lieux exactement une fois.
        La route commence et se termine au lieu 0.
        """
        nb_lieux = len(self.graph.liste_lieux)
        
        # Création d'une liste des lieux à visiter (sauf le lieu 0)
        lieux_a_visiter = list(range(1, nb_lieux))
        
        # Mélange aléatoire de l'ordre de visite
        random.shuffle(lieux_a_visiter)
        
        # Construction de la route: 0 -> lieux mélangés -> 0
        self.ordre = [0] + lieux_a_visiter + [0]
        
        # Recalcul de la distance
        self.distance = self.graph.calcul_distance_route(self)
    
    def generer_route_gloutonne(self):
        """
        Génère une route en utilisant l'heuristique du plus proche voisin.
        À chaque étape, on visite le lieu non visité le plus proche.
        """
        # Initialisation: on part du lieu 0
        self.ordre = [0]
        lieux_visites = {0}
        lieu_courant = 0
        
        # Tant qu'il reste des lieux à visiter
        while len(lieux_visites) < len(self.graph.liste_lieux):
            # Trouve le plus proche voisin non visité
            prochain_lieu = self.graph.plus_proche_voisin(lieu_courant, lieux_visites)
            
            if prochain_lieu is not None:
                # Ajout du lieu à la route
                self.ordre.append(prochain_lieu)
                lieux_visites.add(prochain_lieu)
                lieu_courant = prochain_lieu
        
        # Retour au lieu de départ
        self.ordre.append(0)
        
        # Calcul de la distance totale
        self.distance = self.graph.calcul_distance_route(self)
    
    def calculer_distance(self):
        """
        Calcule et met à jour la distance totale de la route.
        
        Returns:
            float: Distance totale de la route
        """
        self.distance = self.graph.calcul_distance_route(self)
        return self.distance
    
    def copier(self):
        """
        Crée une copie profonde de la route.
        
        Returns:
            Route: Nouvelle instance de Route avec le même ordre
        """
        nouvelle_route = Route(self.graph)
        nouvelle_route.ordre = self.ordre.copy()
        nouvelle_route.distance = self.distance
        return nouvelle_route
    
    def __str__(self):
        """Représentation textuelle de la route"""
        return f"Route: {self.ordre}, Distance: {self.distance:.2f}"


# ============================================================================
# CLASSE AFFICHAGE
# ============================================================================

class Affichage:
    """
    Classe gérant l'affichage graphique du graphe et des routes avec Tkinter.
    Permet de visualiser les lieux, la meilleure route, et des informations supplémentaires.
    """
    
    def __init__(self, graph, nom_groupe="Groupe 5 TSP"):
        """
        Initialise l'interface graphique Tkinter.
        
        Args:
            graph (Graph): Le graphe à afficher
            nom_groupe (str): Nom du groupe à afficher dans le titre
        """
        self.graph = graph
        self.meilleure_route = None
        self.population_routes = []  # Liste des N meilleures routes (pour affichage)
        self.afficher_population = False  # Flag pour afficher/masquer la population
        
        # Création de la fenêtre principale
        self.root = tk.Tk()
        self.root.title(f"Problème du Voyageur de Commerce - {nom_groupe}")
        
        # Frame principal pour organisation
        frame_principal = tk.Frame(self.root, bg='white')
        frame_principal.pack(fill=tk.BOTH, expand=True)
        
        # Canvas pour dessiner le graphe
        self.canvas = Canvas(frame_principal, width=LARGEUR, bg='white', highlightthickness=0)
        self.canvas.pack(padx=0, pady=0)
        
        # Zone de texte pour afficher les informations
        frame_texte = tk.Frame(self.root)
        frame_texte.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = Scrollbar(frame_texte)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.zone_texte = Text(frame_texte, height=8, yscrollcommand=scrollbar.set, 
                               font=('Arial', 9), wrap=tk.WORD, bg='white')
        self.zone_texte.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)        
        scrollbar.config(command=self.zone_texte.yview)
        
        
        # Liaison des touches clavier
        self.root.bind('<Escape>', self.quitter)
        self.root.bind('<space>', self.toggle_affichage_population)  # Touche espace pour afficher population
        self.root.protocol("WM_DELETE_WINDOW", self.quitter)

        
        # Affichage initial
        self.afficher_graph()
        self.ajouter_texte("Interface graphique initialisée.")
        self.ajouter_texte("Appuyez sur ESPACE pour afficher/masquer la population.")
        self.ajouter_texte("Appuyez sur ECHAP POUR QUITTER L'APPLICATION.")
    
    def afficher_graph(self):
        """
        Affiche tous les lieux du graphe sous forme de cercles numérotés.
        """
        rayon = 15  # Rayon des cercles représentant les lieux
        
        for i, lieu in enumerate(self.graph.liste_lieux):
            x, y = lieu.x, lieu.y
            
            # Couleur spéciale pour le lieu de départ (lieu 0)
            couleur = 'red' if i == 0 else 'lightblue'
            
            # Dessin du cercle
            self.canvas.create_oval(
                x - rayon, y - rayon, x + rayon, y + rayon,
                fill=couleur, outline='black', width=2
            )
            
            # Affichage du numéro du lieu au centre du cercle
            self.canvas.create_text(
                x, y, text=str(i), font=('Arial', 10, 'bold')
            )
    
    def afficher_route(self, route, couleur='blue', epaisseur=2, style=None, afficher_ordre=True):
        """
        Affiche une route sur le canvas avec une ligne reliant les lieux dans l'ordre.
        
        Args:
            route (Route): La route à afficher
            couleur (str): Couleur de la ligne
            epaisseur (int): Épaisseur de la ligne
            style (tuple): Style de ligne (ex: (5, 5) pour pointillés)
            afficher_ordre (bool): Si True, affiche l'ordre de visite au-dessus des lieux
        """
        if route is None or len(route.ordre) < 2:
            return
        
        # Dessin des segments de la route
        for i in range(len(route.ordre) - 1):
            lieu_depart = self.graph.liste_lieux[route.ordre[i]]
            lieu_arrivee = self.graph.liste_lieux[route.ordre[i + 1]]
            
            # Création de la ligne
            if style:
                self.canvas.create_line(
                    lieu_depart.x, lieu_depart.y,
                    lieu_arrivee.x, lieu_arrivee.y,
                    fill=couleur, width=epaisseur, dash=style
                )
            else:
                self.canvas.create_line(
                    lieu_depart.x, lieu_depart.y,
                    lieu_arrivee.x, lieu_arrivee.y,
                    fill=couleur, width=epaisseur
                )
        
        # Affichage de l'ordre de visite si demandé
        if afficher_ordre:
            for i, indice_lieu in enumerate(route.ordre[:-1]):  # Pas besoin du dernier (retour au 0)
                lieu = self.graph.liste_lieux[indice_lieu]
                self.canvas.create_text(
                    lieu.x, lieu.y - 25,
                    text=str(i + 1),
                    font=('Arial', 9),
                    fill='darkblue'
                )
    
    def actualiser_affichage(self, meilleure_route, population_routes=None, info_iteration=None):
        """
        Rafraîchit l'affichage complet: efface et redessine tout.
        
        Args:
            meilleure_route (Route): La meilleure route trouvée
            population_routes (list): Liste des N meilleures routes (optionnel)
            info_iteration (str): Informations sur l'itération courante (optionnel)
        """
        # Effacement du canvas
        self.canvas.delete('all')
        
        # Sauvegarde des données
        self.meilleure_route = meilleure_route
        if population_routes:
            self.population_routes = population_routes
        
        # Affichage de la population (routes grises) si activé
        if self.afficher_population and self.population_routes:
            for route in self.population_routes:
                if route != meilleure_route:  # On n'affiche pas la meilleure en gris
                    self.afficher_route(route, couleur='lightgray', epaisseur=1, afficher_ordre=False)
        
        # Affichage de la meilleure route (ligne bleue pointillée)
        if meilleure_route:
            self.afficher_route(meilleure_route, couleur='blue', epaisseur=2, style=(5, 5), afficher_ordre=True)
        
        # Affichage des lieux (par-dessus les routes)
        self.afficher_graph()
        
        # Mise à jour des informations textuelles
        if info_iteration:
            self.ajouter_texte(info_iteration)
        
        # Rafraîchissement de l'interface
        self.root.update()
    
    def toggle_affichage_population(self, event=None):
        """
        Active/désactive l'affichage de la population des routes.
        Appelé lors de l'appui sur la touche ESPACE.
        
        Args:
            event: Événement Tkinter (non utilisé mais requis pour le binding)
        """
        self.afficher_population = not self.afficher_population
        
        if self.afficher_population:
            self.ajouter_texte(f"Affichage de {len(self.population_routes)} routes de la population activé.")
        else:
            self.ajouter_texte("Affichage de la population désactivé.")
        
        # Rafraîchissement de l'affichage
        self.actualiser_affichage(self.meilleure_route, self.population_routes)
    
    def ajouter_texte(self, texte):
        """
        Ajoute une ligne de texte dans la zone d'information.
        
        Args:
            texte (str): Texte à ajouter
        """
        self.zone_texte.insert(tk.END, texte + '\n')
        self.zone_texte.see(tk.END)  # Auto-scroll vers la fin
    
    def quitter(self, event=None):
        """
        Ferme proprement l'application.
        Appelé lors de l'appui sur la touche ESC.
        
        Args:
            event: Événement Tkinter (non utilisé mais requis pour le binding)
        """
        self.ajouter_texte("Fermeture de l'application...")
        self.root.quit()
        self.root.destroy()
    
    def demarrer(self):
        """
        Lance la boucle principale de l'interface Tkinter.
        """
        self.root.mainloop()


# ============================================================================
# EXEMPLE D'UTILISATION
# ============================================================================

if __name__ == "__main__":
    # Création d'un graphe
    graph = Graph()
    
    # Option 1: Générer des lieux aléatoires
    graph.generer_lieux_aleatoires(NB_LIEUX)
    
    # Option 2: Charger depuis un fichier CSV 
    #graph = Graph(path="graph_5.csv")
    # ou avec un chemin complet:
    # graph = Graph(path="data/graph_20.csv")
    
    # Génération d'une route gloutonne (plus proche voisin)
    route_gloutonne = Route(graph)
    route_gloutonne.generer_route_gloutonne()
    print(f"Route gloutonne: {route_gloutonne}")
    
    # Génération de quelques routes aléatoires pour la population
    population = []
    for _ in range(5):
        route = Route(graph)
        route.generer_route_aleatoire()
        population.append(route)
    
    population.sort(key=lambda r: r.distance)

    # Création et lancement de l'interface graphique
    affichage = Affichage(graph, nom_groupe="Groupe 5 TSP")
    affichage.actualiser_affichage(
        meilleure_route=route_gloutonne,
        population_routes=population,
        info_iteration=f"Route initiale (gloutonne): Distance = {route_gloutonne.distance:.2f}"
    )
    
    # Démarrage de l'interface
    affichage.demarrer()

   