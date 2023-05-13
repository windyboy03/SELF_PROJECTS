
def gini_index(groups, classes):
    """"
        # Calc the proportion in each group
        proportion = count(class_value)/ count(rows)

        # Calc each child node with gini index

        gini_index = 1 - sum(proportion*proportion)
        gini_index = gini_index * (group_size / total)
    """
    # Count spit point
    n_split = sum(len(group) for group in groups)
    n_split = float(n_split)
    # Sum all Gini index each class
    gini_index = 0.0
    for group in groups:
        size = len(group)
        size = float(size)
        if size == 0:
            continue
        score = 0.0
        for class_ in classes:
            p = [row[-1] for row in group]
            p = p.count(class_)/size
            score += p*p
        # Add weighting to gini-index
        gini_index += (1-score)*(size/n_split)
    return gini_index

def split_data(index, value, dataset):
    left, right = [],[]
    for row in dataset:
        if row[index] < value:
            left.append(row)
        else:
            right.append(row)
    return left, right


def get_split(dataset):
    class_val = set(row[-1] for row in dataset)
    class_val = list(class_val)
    a_index, a_value, a_score, a_groups = 999, 999, 999, 999
    for index in range(len(dataset[0])-1):
        for row in dataset:
            groups = split_data(index, row[index], dataset)
            gini = gini_index(groups, class_val)
            if gini < a_score:
                a_index, a_value, a_score,a_groups = index, row[index], gini, groups
    return {'index': a_index, 'value': a_value, 'groups': a_groups}



def most_common(group):
    outcomes = [row[-1] for row in group]
    return max(set(outcomes), key=outcomes.count)
# Create child split
def split(node, max_depth=3, min_size=5, depth=3):
    left, right = node['groups']
    #del(node['groups'])
    # Check no split
    if not left or not right:
        node['left'] = node['right'] = most_common(left + right )
        return
    # Check depth max
    if depth >= max_depth:
        node['left'] = most_common(left)
        node['right'] = most_common(right)
        return
    # Check min size and Recursive split
    if len(right) <= min_size:
        node['right'] = most_common(right)
    else:
        node['right'] = get_split(right)
        split((node['right'], max_depth, min_size, depth+1))
    # Like right node
    if len(left) <= min_size:
        node['left'] = most_common(right)
    else:
        node['left'] = get_split(right)
        split((node['left'], max_depth, min_size, depth+1))

def build_tree(train, max_depth=3, min_size=5):
    root = get_split(train)
    split(root, max_depth, min_size, 1)
    return root

def predict(node, row):
    if row[node['index']] < node['value']:
        if isinstance(node['left'], dict):
            return predict(node['left'], row)
        else:
            return node['left']
    else:
        if isinstance(node['right'], dict):
            return predict(node['right'], row)
        else:
            return node['right']
      
