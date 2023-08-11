import pygame
import random
import math
import heapq
from collections import defaultdict

def group_routes_by_index(routes, start, end):
    grouped_routes = []
    for route in routes:
        if len(grouped_routes):
            for grp_routes in grouped_routes:
                if not route in grp_routes:
                    can_add = True
                    for i, value in enumerate(route):
                        if value == end or value == start:
                            continue
                        filtred_list = [tableau for tableau in grp_routes if len(tableau) > i and tableau[i] == value]
                        if len(filtred_list):
                            can_add = False
                            break;

                    if can_add:
                        grp_routes.append(route)
                    else:
                        grouped_routes.append([route])
        else:
            grouped_routes.append([route])
    # reverse
    for route in routes:
        if len(grouped_routes):
            for grp_routes in grouped_routes:
                if not route in grp_routes:
                    can_add = True
                    for i, value in enumerate(route):
                        if value == end:
                            break
                        if not i == 0:
                            filtred_list = [tableau for tableau in grp_routes if len(tableau) > i and tableau[i] == value]
                            if len(filtred_list):
                                can_add = False
                                break;

                    if can_add:
                        grp_routes.append(route)


    return sorted(grouped_routes, key=lambda x: len(x))

def filter_current_game(routes, current_game, start, end):
    return_list = []
    for route in routes:
        is_correct = True
        for i, value in enumerate(route):
            filtred_list = [tableau for tableau in current_game if len(tableau) > i and tableau[i] == value]
            if len(filtred_list) and not value == end and not value == start:
                is_correct = False
                break
        if is_correct:
            return_list.append(route)
    return return_list

def find_all_paths(graph, start, end):
    paths = []  # Liste pour stocker tous les chemins possibles
    queue = [(0, [start])]  # File de priorité pour les chemins à explorer

    while queue:
        (cost, path) = heapq.heappop(queue)

        current = path[-1]

        if current == end:
            paths.append(path)
        else:
            for neighbor, weight in graph[current].items():
                if neighbor not in path:
                    heapq.heappush(queue, (cost + weight, path + [neighbor]))
    return sorted(paths, key=lambda x: len(x))

def generat_info(max_fourmis, max_ville):
    nbr_fourmis = random.randint(6, max_fourmis)
    nbr_ville = random.randint(4, max_ville)
    # nbr_ville = 3

    # Créer des villes et initialiser les routes
    villes = [f"Ville {i}" for i in range(1, nbr_ville + 1)]
    routes = set({})

    # Créer des routes vers les villes plus éloignées
    for i in range(nbr_ville):
        if not i == nbr_ville - 1:
            max_routes = random.randint(1, nbr_ville - i)
            for n in range(max_routes):
                selected_ville = random.randint(i + 1, nbr_ville - 1)
                new_route = (i, selected_ville)
                if not new_route in routes:
                    routes.add(new_route)

    start = random.randint(0, nbr_ville - 1)
    end = None
    while not end:
        new_end = random.randint(0, nbr_ville - 1)
        if not new_end == start:
            end = new_end

    # villes = ["Ville 1", "Ville 2", "Ville 3", "Ville 4", "Ville 5", "Ville 6"]
    # routes = [(0, 1), (0, 2), (0, 4), (1, 2), (2, 3), (3, 4), (3, 5)]
    # start = 0
    # end = 5

    # Retourner les informations
    return nbr_fourmis, villes, routes, start, end


input_fourmis = int(input("Définissez un nombre de fourmis maximum"))
input_ville = int(input("Définissez un nombre de ville maximum"))

# Données reçues
nombre_fourmis, villes, routes, start, end = generat_info(input_fourmis, input_ville)

# Initialisation de Pygame
pygame.init()
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Schéma de la carte")

# Couleurs
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
circle_radius = 20

# dictionnaire pour stocker les coordonnées des villes
ville_coords = {}

# dictionnaire pour stocker les routes sous forme de listes de points (x, y)
routes_coords = {}

# Calcul des coordonnées des villes
for i, ville in enumerate(villes):
    angle = (2 * math.pi * i) / len(villes)
    x = int(screen_width / 2 + 200 * math.cos(angle))
    y = int(screen_height / 2 + 200 * math.sin(angle))
    ville_coords[ville] = (x, y)

# Calcul des coordonnées des routes
for route in routes:
    ville_source, ville_dest = route
    x1, y1 = ville_coords[villes[ville_source]]
    x2, y2 = ville_coords[villes[ville_dest]]
    if ville_source not in routes_coords:
        routes_coords[ville_source] = []
    routes_coords[ville_source].append((x1, y1))
    routes_coords[ville_source].append((x2, y2))


graph = defaultdict(dict)
# Calcul des routes possible jusqu'a l'arrivé
for route in routes:
    ville_source, ville_dest = route
    distance = 1
    graph[villes[ville_source]][villes[ville_dest]] = distance
    graph[villes[ville_dest]][villes[ville_source]] = distance

routes = find_all_paths(graph, villes[start], villes[end])

list_fourmis = []
class Personnage:
    def __init__(self, name):
        self.name = name
        self.where = ville_coords[villes[start]]
        self.go = None
        self.x = self.where[0]
        self.y = self.where[1]
        self.is_gonne = False
        self.route_index = 0
        self.visted = [villes[start]]
        self.direction_list = []
        self.on_turn= False
        list_fourmis.append(self)

    def set_direction(self, direction):
        self.direction_list = direction
        self.on_turn = True

    def get_current_ville(self):
        for ville, coords in ville_coords.items():
            if math.dist((self.x, self.y), coords) < circle_radius:
                return ville
        return None

    def choise_ville(self):
        if self.where is ville_coords[villes[end]] and self.is_gonne == False:
            print("Une fourmis est arrivé!")
            self.is_gonne = True
            self.on_turn = False
        elif not len(self.direction_list) == 0:
            self.move_to_ville(self.direction_list[0])

    def move_to_ville(self, ville):
        wher_go = ville_coords[ville]
        self.visted.append(ville)
        self.go = wher_go
        self.route_index = 0
        self.on_turn = True
        if not len(self.direction_list) == 0:
            self.direction_list.pop(0)

    def update(self):
        if not self.is_gonne and self.on_turn and not self.go is None:
            dest_x, dest_y = self.go
            angle = math.atan2(dest_y - self.y, dest_x - self.x)
            self.x += math.cos(angle) * 2
            self.y += math.sin(angle) * 2
            if math.dist((self.x, self.y), (dest_x, dest_y)) < 5:
                self.where = self.go
                self.go = None
                self.on_turn = False



    def get_chemin(self):
        return f"{self.where} - {self.go}"

def fourmis_on_turn():
    for element in list_fourmis:
        if element.on_turn and not element.is_gonne:
            return True
    return False

def fourmis_end():
    for element in list_fourmis:
        if not element.is_gonne:
            return False
    return True

for i in range(nombre_fourmis):
    Personnage(i)


possible_route = routes
current = []

turn = 0
score = 0

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(white)

    # Affiche les routes
    for ville_source, coords in routes_coords.items():
        for i in range(0, len(coords), 2):
            pygame.draw.line(screen, black, coords[i], coords[i + 1], 2)

    # Affiche les villes
    for index, (ville, (x, y)) in enumerate(ville_coords.items()):
        color = black
        if index == start:
            color = red
        elif index == end:
            color = blue
        pygame.draw.circle(screen, color, (x, y), circle_radius)
        font = pygame.font.Font(None, 24)
        text = font.render(ville, True, black)
        screen.blit(text, (x - circle_radius, y - circle_radius - 20))
    fourm = fourmis_on_turn()
    if not fourm:
        possible_route = filter_current_game(routes, current, villes[start], villes[end])
        list_choise = group_routes_by_index(possible_route, villes[start], villes[end])
        if len(list_choise):
            # Ajouter
            fourmis_dormeuse = [fourmis for fourmis in list_fourmis if len(list_fourmis) > i and not fourmis.is_gonne and len(fourmis.direction_list) == 0]
            if len(list_choise[0]) > len(fourmis_dormeuse):
                for i,perso in enumerate(fourmis_dormeuse):
                    perso.set_direction(list_choise[0][i][:])
                    current.append(list_choise[0][i][:])
            else:
                for i,direction in enumerate(list_choise[0]):
                    fourmis_dormeuse[i].set_direction(direction[:])
                    current.append(direction[:])
        for fourmis in list_fourmis:
            fourmis.choise_ville()
        for traject in current:
            if not len(traject) == 0:
                traject.pop(0)
            if len(traject) == 0:
                current.pop(current.index(traject))
                score += 1
        if fourmis_end():
            break
        turn += 1



    for personnage in list_fourmis:
        # Met à jour le personnage
        personnage.update()
        # Affiche le personnage
        pygame.draw.circle(screen, green, (int(personnage.x), int(personnage.y)), circle_radius / 3)



    pygame.display.flip()



input(f"Le score de l'algo est de: {score} tours. pour quitter appuyer sur une touche")
pygame.quit()
