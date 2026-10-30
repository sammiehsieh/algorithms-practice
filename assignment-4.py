# discuss with GPT: https://chatgpt.com/share/6ae0a5b3-2ee0-83ea-910c-b087065718f2
#   - BFS has time complexity O(V + E), V means vertices, and E means edges
# Dijkstra's Algorithm: https://www.youtube.com/watch?v=HHvjmLKJaxM
#   - looked at it, but every highway is 1 step, so BFS is enough


from collections import deque


class City:
    def __init__(self, name, population):
        """
        task 1
        """
        self.name = name
        self.population = population
        self.neighbors = []

    def add_neighbor(self, other):
        """
        add a highway to another city
        skip it if the highway is already in the list
        """
        if other not in self.neighbors:
            self.neighbors.append(other)


def build_graph(population_file, road_file):
    """
    task 2: read the two files and build the graph of CITIES

    return a dict with city name -> city object
    """
    cities = {}

    # step 1. read the populations and create one city object per line (City A: 1000)
    with open(population_file, "r") as file1:
        for line in file1:
            line = line.strip()
            if line == "":
                continue  # stop here for this round
            parts = line.split(":")  # 冒號(:)：colon
            name = parts[0].strip()
            population = int(parts[1].strip())
            cities[name] = City(name, population)

    # step 2. read the highways and connect the cities (City A: City B)
    with open(road_file, "r") as file2:
        for line in file2:
            line = line.strip()
            if line == "":
                continue
            parts = line.split(":")
            name1 = parts[0].strip()
            name2 = parts[1].strip()
            # highways are bi-directional, so we add the road to both cities
            if name1 in cities and name2 in cities:
                cities[name1].add_neighbor(cities[name2])
                cities[name2].add_neighbor(cities[name1])

    return cities


# start with a city
def explore_island(start, visited):
    """
    this is a helper that uses BFS to visit every city on the same island as start
    mark the cities as visited and return them in a list

    BFS (take from front, add to back) so we use deque to quickly get/add
    deque(double-ended queue) append and popleft are both O(1)
    """
    island = []
    queue = deque()
    queue.append(start)  # let's go, start!
    visited.add(start)  # remember to put start into visited so it won't loop repeatedly

    while len(queue) > 0:
        current = queue.popleft()
        island.append(current)
        for neighbor in current.neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)

    return island


def count_islands(city_list):
    """
    task 3: count the ISLANDS, and explore them if haven't visited yet
    """
    visited = set()  # set(): things won't repeat, and there's no order
    count = 0

    for city in city_list:
        if city not in visited:
            explore_island(city, visited)
            count = count + 1

    return count


def island_populations(city_list):
    """
    task 4: return a list with the total population of each island (add up the population while exploring)
    """
    visited = set()  # set(): things won't repeat, and there's no order
    totals = []

    for city in city_list:
        if city not in visited:
            island = explore_island(city, visited)
            total = 0
            for c in island:
                total = total + c.population
            totals.append(total)

    return totals


def min_highways(start, end):
    """
    task 5: minimum number of highways to go from start to end

    uses BFS because every highway counts as 1 step

    returns -1 if the two cities are on different islands
    """
    if start == end:
        return 0

    distance = {}  # city -> how many highways from start
    distance[start] = 0
    queue = deque()  # cities we found but haven't checked their neighbors yet
    queue.append(start)

    # BFS's condition, keep going as long as there are cities waiting in the queue
    while len(queue) > 0:
        current = queue.popleft()
        # try this city's neighbors
        for neighbor in current.neighbors:
            # check with distance: is it our first time to meet?
            if neighbor not in distance:
                # yes first time, so add one step
                distance[neighbor] = distance[current] + 1
                if neighbor == end:
                    return distance[neighbor]
                # not the end yet, so line it up and check its neighbors later
                queue.append(neighbor)

    return -1


# build the graph from the two files and test all the tasks.
cities = build_graph("city_population.txt", "road_network.txt")
city_list = list(cities.values())

print("Number of cities:", len(city_list))
print("Number of islands:", count_islands(city_list))
print("Population of each island:", island_populations(city_list))

# Example for Task 5, change the names to cities in your file.
name1 = "Irvine"
name2 = "Fremont"
if name1 in cities and name2 in cities:
    print(
        f"Highways from {name1} to {name2}:", min_highways(cities[name1], cities[name2])
    )
