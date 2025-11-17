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
        
        # Affichage de l'ordre de visite
        if afficher_ordre:
            for i, indice_lieu in enumerate(route.ordre[:-1]):  # Exclut le dernier (retour au 0)
                lieu = self.graph.liste_lieux[indice_lieu]
                self.canvas.create_text(lieu.x, lieu.y - 25, 
                                       text=f"{i}", 
                                       font=("Arial", 8), 
                                       fill="black")
    
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
# FONCTION PRINCIPALE (MAIN)
# ============================================================================

def main():
    """
    Fonction principale pour tester le système.
    Charge un graphe depuis un fichier CSV et affiche l'interface.
    """
    print("="*60)
    print("PROGRAMME TSP - Groupe 5")
    print("="*60)
    
    # Chargement du graphe depuis le fichier CSV
    nom_fichier = "graph_5.csv"
    graph = Graph(path=nom_fichier)
    
    # Vérification que le graphe est bien chargé
    if not graph.liste_lieux:
        print("Erreur: Impossible de charger le graphe. Arrêt du programme.")
        return
    
    print(f"\nGraphe chargé avec {len(graph.liste_lieux)} lieux.")
    print(f"Matrice de distances: {graph.matrice_od.shape}")
    
    # Exemple de création d'une route (algorithme du plus proche voisin simplifié)
    route_test = Route(graph)
    route_test.ordre = [0]  # Départ du lieu 0
    
    lieux_non_visites = set(range(1, len(graph.liste_lieux)))
    lieu_actuel = 0
    
    while lieux_non_visites:
        prochain_lieu = graph.plus_proche_voisin(lieu_actuel, lieux_non_visites)
        route_test.ordre.append(prochain_lieu)
        lieux_non_visites.remove(prochain_lieu)
        lieu_actuel = prochain_lieu
    
    route_test.ordre.append(0)  # Retour au point de départ
    
    distance_totale = route_test.calcul_distance_route()
    print(f"\nRoute calculée (plus proche voisin):")
    print(f"Ordre: {route_test.ordre}")
    print(f"Distance totale: {distance_totale:.2f}")
    
    # Création et lancement de l'interface graphique
    print("\nLancement de l'interface graphique...")
    affichage = Affichage(graph, titre="Groupe 5 - Léa Léa Lou-Anne Lisa")
    affichage.afficher_meilleure_route(route_test)
    affichage.ajouter_texte(f"Route calculée avec l'algorithme du plus proche voisin.\n")
    affichage.ajouter_texte(f"Distance totale: {distance_totale:.2f}\n")
    affichage.ajouter_texte(f"Ordre de visite: {route_test.ordre}\n")
    
    # Exemple de routes secondaires (pour démonstration)
    routes_demo = []
    for _ in range(5):
        route_random = Route(graph)
        route_random.ordre = [0] + random.sample(range(1, len(graph.liste_lieux)), 
                                                 len(graph.liste_lieux) - 1) + [0]
        routes_demo.append(route_random)
    
    affichage.afficher_routes_secondaires(routes_demo)
    
    affichage.lancer()
    
    print("\nProgramme terminé.")

# ============================================================================
# POINT D'ENTRÉE
# ============================================================================

if __name__ == "__main__":
    main()