class DOMNode(object):
    '''
    Represents a DOM Node. It holds the node's ID, type, value, and attributes.
    '''
    def __init__(self, node_id, node_type, value, attributes):
        '''
        Initializes the DOM node.
        Params:
            node_id: (int) The node ID of this DOM node.
            node_type: (string) The string representation of the node.
            value: (string) The value of the node. If this node contains a #text node, it will be populated in the value property.
            attributes: (map<string,string>) Attributes of this node.
        '''
        self.id = node_id
        self.type = node_type.lower()
        self.value = value
        self.attributes = attributes

    
    def CompareStructure(self, other):
        '''
        Returns whether the tag matches. This is to just compare the structure of the page.
        '''
        return self.type == other.type


    def __eq__(self, other):
        '''
        Returns whether the two DOMNodes are equal.
        
        Two nodes are considered equal when they have the same type, value, and attributes.
        '''
        return (self.type == other.type and self.value == other.value and self.attributes == other.attributes)


    def __ne__(self, other):
        return not self.__eq__(other)


    def __str__(self):
        '''
        Returns the string representation of this DOMNode
        '''
        return '''
        Node: <{0}>
            id: {1}
            value: {2}
            attrs: {3}
        '''.format(self.type, self.id, self.value.encode('utf-8'), self.attributes).strip() + '\n'


def ConstructDOMNodeObj(dom_json):
    attrs = SerializeAttributes(dom_json['attributes']) if 'attributes' in dom_json else {}
    value = ''
    if 'children' in dom_json and len(dom_json['children']) == 1 and dom_json['children'][0]['nodeName'].lower() == '#text':
        value = dom_json['children'][0]['nodeValue']
        
        # Remove the children nodes, since we already embed this info in the parent node.
        del dom_json['children']

    return DOMNode(dom_json['nodeId'], dom_json['nodeName'], value, attrs)


def SerializeAttributes(attributes):
    '''
    Returns a map of attributes from the array representation: [ key_1, val_1, key_2, val_2, ..., key_n, val_n ]
    '''
    attrs = {}
    for i in range(0, len(attributes), 2):
        key = attributes[i]
        val = attributes[i + 1]
        attrs[key] = val
    return attrs
