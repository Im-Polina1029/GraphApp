import unittest
from app import bfs_tree  

class TestBFS(unittest.TestCase):
    
    def setUp(self):
        # 1. ÷епочка 1-2-3-4
        self.chain_matrix = [
            [0,1,0,0],
            [1,0,1,0],
            [0,1,0,1],
            [0,0,1,0]
        ]
        # 2. «везда (центр 2)
        self.star_matrix = [
            [0,1,0,0],
            [1,0,1,1],
            [0,1,0,0],
            [0,1,0,0]
        ]
        # 3. “реугольник + вершина 4, соединЄнна€ с 3
        self.triangle_matrix = [
            [0,1,1,0],
            [1,0,1,0],
            [1,1,0,1],
            [0,0,1,0]
        ]
        # 4. Ќесв€зный: две компоненты
        self.disconnected_matrix = [
            [0,1,0,0],
            [1,0,0,0],
            [0,0,0,1],
            [0,0,1,0]
        ]
        # 5. ќдна вершина
        self.single_matrix = [[0]]
        # 6. — петлЄй
        self.loop_matrix = [
            [1,1],
            [1,0]
        ]
        # 7. ѕолный граф K3
        self.k3_matrix = [
            [0,1,1],
            [1,0,1],
            [1,1,0]
        ]
    #order должен быть равен списку [1, 2, 3, 4].
    def test_1_order_chain_start1(self):
        order, _ = bfs_tree(self.chain_matrix, 1)
        self.assertEqual(order, [1,2,3,4])
    #ѕервый элемент order Ч 3. ¬торой и третий Ч это множество {2, 4}. „етвертый Ч 1.
    def test_2_order_chain_start3(self):
        order, _ = bfs_tree(self.chain_matrix, 3)
        self.assertEqual(order[0], 3)
        self.assertEqual(set(order[1:3]), {2,4})
        self.assertEqual(order[3], 1)
#ƒлина списка edges должна быть равна 3 (дл€ всех трех провер€емых графов с 4 вершинами).
    def test_3_edges_count(self):
        _, edges = bfs_tree(self.chain_matrix, 1)
        self.assertEqual(len(edges), 3)
        _, edges = bfs_tree(self.star_matrix, 2)
        self.assertEqual(len(edges), 3)
        _, edges = bfs_tree(self.triangle_matrix, 1)
        self.assertEqual(len(edges), 3)
#ѕри движении от любой вершины к корню по родител€м, мы не должны встретить вершину дважды.
    def test_4_no_cycles(self):
        _, edges = bfs_tree(self.triangle_matrix, 1)
        parent = {c: p for p, c in edges}
        for node in [2,3,4]:
            seen = set()
            cur = node
            while cur in parent and cur not in seen:
                seen.add(cur)
                cur = parent[cur]
            self.assertNotIn(cur, seen)
#ћножество вершин в order должно быть {1, 2}.  оличество ребер Ч 1.
    def test_5_disconnected(self):
        order, edges = bfs_tree(self.disconnected_matrix, 1)
        self.assertEqual(set(order), {1,2})
        self.assertEqual(len(edges), 1)
        self.assertTrue((1,2) in edges or (2,1) in edges)
#order должен быть [1], а edges Ч пустой список [].
    def test_6_single_vertex(self):
        order, edges = bfs_tree(self.single_matrix, 1)
        self.assertEqual(order, [1])
        self.assertEqual(edges, [])
#ѕервый элемент order Ч 2. ќстальные элементы Ч это множество {1, 3, 4}.
    def test_7_star_order(self):
        order, _ = bfs_tree(self.star_matrix, 2)
        self.assertEqual(order[0], 2)
        self.assertEqual(set(order[1:]), {1,3,4})
#¬ order должны быть обе вершины {1, 2}. ¬ edges должно быть одно ребро.
    def test_8_loop(self):
        order, edges = bfs_tree(self.loop_matrix, 1)
        self.assertEqual(set(order), {1,2})
        self.assertEqual(len(edges), 1)
#–ассто€ни€: до 2 Ч 1, до 3 Ч 2, до 4 Ч 3.
    def test_9_shortest_path(self):
        order, edges = bfs_tree(self.chain_matrix, 1)
        dist = {1:0}
        for v in order[1:]:
            for p,c in edges:
                if c == v:
                    dist[v] = dist[p] + 1
                    break
        self.assertEqual(dist[2], 1)
        self.assertEqual(dist[3], 2)
        self.assertEqual(dist[4], 3)
#ѕервый элемент order Ч 1. ќстальные Ч это множество {2, 3}. ” обоих ребер родитель Ч 1.
    def test_10_full_graph(self):
        order, edges = bfs_tree(self.k3_matrix, 1)
        self.assertEqual(order[0], 1)
        self.assertEqual(set(order[1:]), {2,3})
        self.assertEqual(len(edges), 2)
        parents = {p for p,_ in edges}
        self.assertEqual(parents, {1})

if __name__ == '__main__':
    unittest.main()