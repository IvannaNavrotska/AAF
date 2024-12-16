class RTreeNode:
    """Вузол R-дерева"""
    def __init__(self, is_leaf=True):
        self.is_leaf = is_leaf  # Чи є вузол листовим
        self.children = []      # Дочірні вузли або сегменти
        self.mbr = None         # Мінімальний охоплюючий прямокутник

    def compute_mbr(self):
        """Обчислює MBR для вузла"""
        if not self.children:
            self.mbr = None
            return
        if self.is_leaf:
            min_l = min(seg[0] for seg in self.children)
            max_h = max(seg[1] for seg in self.children)
        else:
            min_l = min(child.mbr[0] for child in self.children)
            max_h = max(child.mbr[1] for child in self.children)
        self.mbr = [min_l, max_h]


class RTree:
    """R-дерево для зберігання сегментів"""
    def __init__(self, max_leaf_size=3):
        self.root = RTreeNode()
        self.max_leaf_size = max_leaf_size

    def insert(self, segment):
        """Вставка сегмента у дерево"""
        self._insert_recursive(self.root, segment)
        if len(self.root.children) > self.max_leaf_size:
            self._split_root()

    def _insert_recursive(self, node, segment):
        """Рекурсивна вставка"""
        if node.is_leaf:
            # Перевірка на дублювання
            if segment not in node.children:
                node.children.append(segment)
                node.compute_mbr()
        else:
            # Обираємо найкращий дочірній вузол
            best_child = min(node.children, key=lambda c: self._mbr_enlargement(c.mbr, segment))
            self._insert_recursive(best_child, segment)
            node.compute_mbr()

        # Розбиття вузла при переповненні
        if len(node.children) > self.max_leaf_size:
            self._split_node(node)

    def _split_node(self, node):
        """Розбиває вузол на дві частини"""
        # Сортування елементів за лівим кінцем
        node.children.sort(key=lambda x: x[0] if node.is_leaf else x.mbr[0])
        mid = len(node.children) // 2

        # Створення нових дочірніх вузлів
        left_node = RTreeNode(is_leaf=node.is_leaf)
        right_node = RTreeNode(is_leaf=node.is_leaf)

        left_node.children = node.children[:mid]
        right_node.children = node.children[mid:]

        left_node.compute_mbr()
        right_node.compute_mbr()

        # Замінюємо поточний вузол дочірніми
        node.is_leaf = False
        node.children = [left_node, right_node]
        node.compute_mbr()

    def _split_root(self):
        """Розділення кореня"""
        left_child, right_child = self.root.children
        new_root = RTreeNode(is_leaf=False)
        new_root.children = [left_child, right_child]
        new_root.compute_mbr()
        self.root = new_root

    def _mbr_enlargement(self, mbr, segment):
        """Обчислює збільшення MBR при додаванні сегмента"""
        new_mbr = [min(mbr[0], segment[0]), max(mbr[1], segment[1])]
        return (new_mbr[1] - new_mbr[0]) - (mbr[1] - mbr[0])

    def print_tree(self, node=None, depth=0):
        """Рекурсивний вивід дерева"""
        if node is None:
            node = self.root
        print("  " * depth + f"MBR: {node.mbr}")
        if node.is_leaf:
            for seg in node.children:
                print("  " * (depth + 1) + f"Segment: {seg}")
        else:
            for child in node.children:
                self.print_tree(child, depth + 1)


# Тестування R-дерева
if __name__ == "__main__":
    rtree = RTree(max_leaf_size=3)

    # Додаємо сегменти
    segments = [[2, 10], [2, 7], [3, 4], [4, 6], [5, 8], [5, 10]]
    for segment in segments:
        rtree.insert(segment)

    # Вивід дерева
    print("R-дерево:")
    rtree.print_tree()
