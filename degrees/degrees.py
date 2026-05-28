import csv
import sys

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    # The first node
    # source defined in line 65 - stores person id in state
    # First node has no action and no parent
    # origin = origin actor
    origin = Node(state=source, parent=None, action=None)

    # create a frontier and add first node

    # queue used for shortest path ( first in first out)
    frontier = QueueFrontier()
    frontier.add(origin)

    # creating an empty set called visited to
    # prevent infinite checking between visited nodes

    visited = set()

    # looping until shortest path found
    while True:

        # what if there is no solution
        # when there is nothing left in the frontier , then no solution

        if frontier.empty():
            return None

        # when not empty choose first node entered in frontier
        # remove node for checking
        node = frontier.remove()

        # once removed and checked add it to visited to prevent rechecking
        # state stores name(person_id) of node
        visited.add(node.state)

        # accessing movie_id and person_id from neighbors_for_person function
        # adding the neighbors to frontier

        for movie_id, person_id in neighbors_for_person(node.state):
            # only add neighbor node to frontier if not already added or visited
            if person_id not in visited and not (frontier.contains_state(person_id)):
                # define neighbor of node
                # parent was first node removed named node
                neighbor = Node(state=person_id, parent=node, action=movie_id)

                # There is a possibility of path 0 ( incase same name entered)
                # In such a case we check whether origin state == target
                if origin.state == target:
                    path_s = []
                    return path_s

                # checking if this neighbor is the target actor we are looking for
                # target defined in 68
                # if person_id of neihbor actor matches target person_id

                if neighbor.state == target:

                    # path followed in case of condition true
                    path_s = []

                    # tracing the path followed to reach target through parent when target matches
                    # and reversing the sequence of events to get the original path in the list

                    # if no parent then path has ended
                    while neighbor.parent is not None:
                        # if parent exists
                        # storing movie_id and person_id in a tuple and then adding to a list as prescribed
                        path_s.append((neighbor.action, neighbor.state))
                        # after appending neighbor we check neighbor.parent and so on as long as parent exists
                        neighbor = neighbor.parent

                    # when no parent found and path ended we reverse the path
                    # reversing is done to obtain original path
                    path_s.reverse()
                    return path_s

                # if frontier is not equal to target
                # continue the checking process
                frontier.add(neighbor)


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
