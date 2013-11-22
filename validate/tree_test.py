#!/usr/bin/python2
def parse_data(fname):
    def to_list(x):
        return map(bool2f, x)

    def head(xs):
        return xs[0]

    def tail(xs):
        return xs[1:]

    def bool2f(x):
        if x == 'True':
            return 1.0
        if x == 'False':
            return 0.0
        return x
    from scipy.io import arff
    (data, meta,) = arff.loadarff(open(fname, 'r'))
    data_ll = map(to_list, data)
    labels = map(head, data_ll)
    attrs = map(tail, data_ll)
    return (labels, attrs)

def train_cart_tree(data_tuple):
    (labels, attrs,) = data_tuple
    from sklearn import tree
    clf = tree.DecisionTreeClassifier(min_samples_leaf=5)
    clf = clf.fit(attrs, labels)
    return clf

def draw_tree(clf):
    import pydot
    import StringIO
    output = StringIO.StringIO()
    tree.export_graphviz(clf, out_file=output)
    graph = pydot.graph_from_dot_data(output.getvalue())
    graph.write_pdf('tree.pdf')

def test_test():
    import operator
    clf = train_cart_tree(parse_data('training_trimmed.arff'))
    (test_labels, test_attrs,) = parse_data('test_trimmed.arff')
    res_labels = clf.predict(test_attrs)
    right_num = map(operator.eq, res_labels.tolist(), test_labels).count(True)
    print 'Right number {0} in total test number {1}'.format(right_num, len(res_labels))
if __name__ == "__main__":
    test_test()


