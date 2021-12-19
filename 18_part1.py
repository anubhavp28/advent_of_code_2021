from math import floor, ceil


class Node:
    def __init__(self, node_type: int, **args):
        self.type = node_type # 0 -> regular number, 1 -> pair
        self.parent = args.get('parent', None)
        self.value = args.get('value', None)
        self.left = args.get('left', None)
        self.right = args.get('right', None)
        self.height = args.get('height', 0)

    def __str__(self):
        if self.type == 0:
            return str(self.value)
        return '[' + str(self.left) + ',' + str(self.right) + ']'

    def __repr__(self):
        return self.__str__()


def to_tree(input, height = 0, parent = None):
    if isinstance(input, int):
        node = Node(0, value=input, height=height, parent=parent)
        return node

    node = Node(1, height=height, parent=parent)
    node.left = to_tree(input[0], height + 1, node)
    node.right = to_tree(input[1], height + 1, node)
    return node


def magnitude(tree):
    if tree.type == 1:
        return 3 * magnitude(tree.left) + 2 * magnitude(tree.right)
    return tree.value


def serialize(node, output):
    if node.type == 0:
        output.append(node)
    else:
        serialize(node.left, output)
        serialize(node.right, output)


def reduce(input):
    output = []
    serialize(input, output)

    # Explode
    for i in range(len(output) - 1):
        left, right, parent = output[i], output[i + 1], output[i].parent
        to_explode = left.parent is right.parent and parent.height == 4
        if to_explode:
            leftmost_pair = output[i].parent
            left = leftmost_pair.left.value
            right = leftmost_pair.right.value
            if i > 0:
                imm_left = output[i - 1]
                imm_left.value = imm_left.value + left
            if i + 2 < len(output):
                imm_right = output[i + 2]
                imm_right.value = imm_right.value + right
            leftmost_pair.type = 0
            leftmost_pair.value = 0
            leftmost_pair.left = leftmost_pair.right = None
            return True

    # Split
    for i in range(len(output)):
        if output[i].value >= 10:
            leftmost_num = output[i]
            leftmost_num.type = 1
            leftmost_num.left = Node(0,
                                     value=floor(leftmost_num.value / 2.0),
                                     height=leftmost_num.height + 1,
                                     parent=leftmost_num)
            leftmost_num.right = Node(0,
                                      value=ceil(leftmost_num.value / 2.0),
                                      height=leftmost_num.height + 1,
                                      parent=leftmost_num)
            return True

    return False


def add(tree1, tree2):
    root = Node(1)
    root.left = tree1
    root.right = tree2
    root.height = 0
    tree1.parent = root
    tree2.parent = root

    def increase_height(node):
        node.height = node.height + 1
        if node.type == 1:
            increase_height(node.left)
            increase_height(node.right)

    increase_height(tree1)
    increase_height(tree2)
    return root


with open('input.txt') as input_file:
    operands = [line.strip() for line in input_file]
    operands = [eval(op) for op in operands]

sum = operands[0]
sum = to_tree(sum)
for i in range(1, len(operands)):
    op = to_tree(operands[i])
    sum = add(sum, op)
    while reduce(sum):
        pass

print(sum)
print(magnitude(sum))
