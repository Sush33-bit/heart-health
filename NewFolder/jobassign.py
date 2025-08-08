import heapq
import copy

class Node:
    def __init__(self, student, club, assigned, parent):
        self.studentID = student
        self.clubID = club
        self.assigned = copy.deepcopy(assigned)
        self.parent = parent
        self.pathCost = 0
        self.cost = 0
        if club != -1:
            self.assigned[club] = True

class CustomHeap:
    def __init__(self):
        self.heap = []

    def push(self, node):
        heapq.heappush(self.heap, (node.cost, node))

    def pop(self):
        if self.heap:
            return heapq.heappop(self.heap)[1]
        return None

def new_node(student, club, assigned, parent):
    return Node(student, club, assigned, parent)

def calculate_cost(cost_matrix, student, club, assigned):
    total_cost = 0
    N = len(cost_matrix)
    available_clubs = [True] * N
    for i in range(student + 1, N):
        min_cost = float('inf')
        min_club = -1
        for j in range(N):
            if not assigned[j] and available_clubs[j] and cost_matrix[i][j] < min_cost:
                min_cost = cost_matrix[i][j]
                min_club = j
        total_cost += min_cost
        available_clubs[min_club] = False
    return total_cost

def print_assignments(node):
    if node.parent is None:
        return
    print_assignments(node.parent)
    print(f"Assign Student {node.studentID + 1} to Club {node.clubID + 1}")

def find_min_cost(cost_matrix):
    N = len(cost_matrix)
    pq = CustomHeap()
    assigned = [False] * N
    root = new_node(-1, -1, assigned, None)
    root.cost = 0
    pq.push(root)

    while True:
        min_node = pq.pop()
        student = min_node.studentID + 1
        if student == N:
            print_assignments(min_node)
            return min_node.cost
        for club in range(N):
            if not min_node.assigned[club]:
                child = new_node(student, club, min_node.assigned, min_node)
                child.pathCost = min_node.pathCost + cost_matrix[student][club]
                child.cost = child.pathCost + calculate_cost(cost_matrix, student, club, child.assigned)
                pq.push(child)

if __name__ == "__main__":
    N = int(input("Enter the number of students and clubs: "))
    cost_matrix = []
    print(f"Enter the cost matrix (each row should have {N} space-separated values):")
    for i in range(N):
        row = list(map(int, input(f"Enter costs for Student {i + 1}: ").split()))
        cost_matrix.append(row)
    optimal_cost = find_min_cost(cost_matrix)
    print(f"\nOptimal Cost is {optimal_cost}")