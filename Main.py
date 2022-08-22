from operator import itemgetter


def diff(li1, li2):
    li_dif = [i for i in li1 + li2 if i not in li1 or i not in li2]
    return li_dif

def get_allowed_numbers(graph, node, numbers):
    not_allowed_numbers = [node[1] for node in graph[(node, False)] if node[1] != '']
    allowed_numbers = diff(numbers, not_allowed_numbers)
    return allowed_numbers

def node_degree(graph):
    index_neighbour_len = [(index, len(l[1])) for index, l in enumerate(graph.items()) if l[0][1] is False]
    max_neighbour = max(index_neighbour_len, key=itemgetter(1))[1]
    max_index_neighbour_len = [t[0] for t in index_neighbour_len if t[1] == max_neighbour]
    nodes = [list(graph)[index][0] for index in max_index_neighbour_len]
    return nodes

def minimum_remaining_choice(graph, numbers):
    nodes_without_number = [(node[0]) for node, numbered in graph.items() if node[1] is False]
    allowed_number_each_node = {}
    for node in nodes_without_number:
        allowed_number_each_node[node] = get_allowed_numbers(graph, node, numbers)

    min_available_number_len = min([len(allowed_numbers) for node, allowed_numbers in allowed_number_each_node.items()])
    nodes = [node for node, numbers in allowed_number_each_node.items() if len(numbers) is min_available_number_len]
    return nodes

def most_used_numbers_in_graph(graph, numbers):
    node_number = []
    number_n = {}

    for neighbours in graph.values():
        [node_number.append(c) for c in neighbours if c[1] != '']

    all_used_numbers = list(dict.fromkeys(node_number))

    if not all_used_numbers:
        return numbers

    for cc in all_used_numbers:
        if cc[1] not in number_n:
            number_n[cc[1]] = 1
        else:
            number_n[cc[1]] += 1

    number_of_max = max(number_n.items(), key=itemgetter(1))[1]
    numbers = [key for (key, value) in number_n.items() if value is number_of_max]

    return numbers

def numbering(graph, node, number):

    neighbours = graph[(node, False)]
    del graph[(node, False)]
    graph[(node, True)] = neighbours

    for nei_list in graph.values():

        for n in nei_list:
            if n[0] == node:
                l = list(n)
                l[1] = number
                t = tuple(l)
                nei_list.remove(n)
                nei_list.append(t)

def build_graph(n):
    graph = {}
    for i in range(n):
        for j in range(n):
            neighbours = []
            for k in range(n):
                for v in range(n):
                    if (k == i or v == j) and not (k == i and v == j):
                        neighbours.append((str(k*n + v + 1),''))
            graph[str(i*n + j + 1), False] = neighbours
    return graph

if __name__ == "__main__":

    n = int(input("Enter n\n"))

    domain = []
    for i in range(n):
        domain.append(str(i+1))

    graph = build_graph(n)

    for i in range(len(graph)):
        nodes_with_max_degree = node_degree(graph)
        nodes_with_minimum_remaining_choice = minimum_remaining_choice(graph, domain)
        most_used_numbers = most_used_numbers_in_graph(graph, domain)

        selected_node = set(nodes_with_max_degree).intersection(set(nodes_with_minimum_remaining_choice)).pop()
        numbers_for_selected_node = get_allowed_numbers(graph, selected_node, domain)
        common_number = set(most_used_numbers).intersection(set(numbers_for_selected_node))

        if common_number:
            number = common_number.pop()
        else:
            number = numbers_for_selected_node.pop()

        numbering(graph, selected_node, number)
 
    result = []
    for key,value in graph.items():
        for i in range(len(graph[key])):
            pair = (graph[key][i][0] , graph[key][i][1])
            if not pair in result:
                result.append(pair)

    result.sort(key=lambda tup: int(tup[0]))
    for i in range(n):
        for j in range(n):
            if j != n-1:
                print(result[i*n + j][1] + " ,", end='')
            else:
                print(result[i*n + j][1], end='')
        print('\n',end='')
