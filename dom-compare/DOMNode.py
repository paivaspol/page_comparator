# JSON Key Constants
NODE_ID = 'nodeId'
NODE_NAME = 'nodeName'
NODE_VALUE = 'nodeValue'
NODE_CHILDREN = 'children'
NODE_ATTRIBUTES = 'attributes'
NODE_PARENT_ID = 'parentId'

class DOMNode(object):
    '''
    Represents a DOM Node. It holds the node's ID, type, value, and attributes.
    '''
    def __init__(self, node_id, node_type, value, attributes, parent_id, signature):
        '''
        Initializes the DOM node.
        Params:
            node_id: (int) The node ID of this DOM node.
            node_type: (string) The string representation of the node.
            value: (string) The value of the node. If this node contains a #text node, it will be populated in the value property.
            attributes: (map<string,string>) Attributes of this node.
            parent_id: (int) The ID of the parent of this node.
            signature: (string) the signature of this node.
        '''
        self.id = node_id
        self.type = node_type.lower()
        self.value = value
        self.attributes = attributes
        self.parent_id = parent_id
        self.signature = signature


    def IsVisible(self):
        '''
        Returns whether the DOMNode is visible or not by determining the style in the attribute.
        If there is no associated style with the node, the node is assumed to be visible.
        '''

        # These tags are always considered "visible"
        exemptions = [ '#document', 'html', 'head', 'body' ]
        for e in exemptions:
            if self.type == e:
                return True

        if 'style' not in self.attributes:
            return True

        style = self.attributes['style'].replace(' ', '')
        return not ('display:none' in style or 'visibility:hidden' in style or ('height:0px' in style and 'width:0px' in style))

    
    def CompareStructure(self, other):
        '''
        Returns whether the tag matches. This is to just compare the structure of the page.
        '''
        return self.type == other.type and self.CompareAttrs(other, structure_only=True)


    def ComputeStructureHash(self):
        '''
        Returns the hash value of the node only considering the type and the attributes.
        '''
        attrs_hash = sum([ hash(key) + hash(val) for key, val in self.attributes.iteritems() ])
        return hash(self.type) + attrs_hash


    def CompareAttrs(self, other, structure_only=False):
        '''
        Returns whether self.attributes == other.attributes.

        The special case is the class attribute where the values can be reordered.
        '''
        structure_only_keys = { 'class', 'id' }
        if len(self.attributes) != len(other.attributes):
            return False
        
        # The keys do not match
        self_attr_keys = { x for x in self.attributes.keys() if (not structure_only) or (structure_only and x in structure_only_keys) }
        other_attr_keys = { x for x in other.attributes.keys() if (not structure_only) or (structure_only and x in structure_only_keys) }

        if self_attr_keys != other_attr_keys:
            return False

        for k in self_attr_keys:
            if k == 'class':
                # Skip checking for class attribute.
                continue
            
            # The two attribute values are not the same.
            if self.attributes[k] != other.attributes[k]:
                return False

        # Check the class attribute
        if 'class' in self.attributes and 'class' in other.attributes:
            # We want to do a comparison that does not take the order of the
            # value into account.
            splitted_self_class = self.attributes['class'].split()
            splitted_other_class = other.attributes['class'].split()
            self_class_set = { x for x in splitted_self_class }
            other_class_set = { x for x in splitted_other_class }

            # The classes are equal when the number of classes applied
            # match and the elements in the two sets match.
            if not (len(splitted_self_class) == len(splitted_other_class) and \
                    self_class_set == other_class_set):
                return False

        return True


    def Serialize(self):
        '''
        Returns a map representation of this DOM node object with
        children as empty.
        '''
        result = {}
        result[NODE_ID] = self.id
        result[NODE_NAME] = self.type
        result[NODE_VALUE] = self.value
        result[NODE_PARENT_ID] = self.parent_id
        result[NODE_ATTRIBUTES] = []
        for k, v in self.attributes.iteritems():
            result[NODE_ATTRIBUTES].append(k)
            result[NODE_ATTRIBUTES].append(v)
        result[NODE_CHILDREN] = []
        return result


    def __hash__(self):
        '''
        Returns the hash value for this node object.

        The hash is computed from the type and the value of the object.
        '''
        return self.ComputeStructureHash() + hash(self.value)


    def __eq__(self, other):
        '''
        Returns whether the two DOMNodes are equal.
        
        Two nodes are considered equal when they have the same type, value, and attributes.
        '''
        # print 'SELF:'
        # print self
        # print 'OTHER:'
        # print other
        # print '==================================================='
        return (self is None and other is None) or \
                (self is not None and other is not None and self.type == other.type \
                and self.value == other.value and self.CompareAttrs(other))


    def __ne__(self, other):
        return not self.__eq__(other)


    def __str__(self):
        '''
        Returns the string representation of this DOMNode
        '''
        return '''
        Node: <{0}>
            id: {1}
            parent_id: {2}
            value: {3}
            attrs: {4}
            signature: {5}
        '''.format(self.type, self.id, self.parent_id, self.value.encode('utf-8'), self.attributes, self.signature).strip() + '\n'


def ConstructDOMNodeObj(dom_json, node_signature, for_hdp=False):
    attrs = SerializeAttributes(dom_json[NODE_ATTRIBUTES], for_hdp) if NODE_ATTRIBUTES in dom_json else {}
    value = ''
    if NODE_CHILDREN in dom_json and len(dom_json[NODE_CHILDREN]) == 1 and dom_json[NODE_CHILDREN][0][NODE_NAME].lower() == '#text':
        # TODO(vaspol) can this contain multiple adjacent text nodes?
        value = dom_json[NODE_CHILDREN][0][NODE_VALUE]
        
        # Remove the children nodes, since we already embed this info in the parent node.
        del dom_json[NODE_CHILDREN]
    parent_id = -1 if NODE_PARENT_ID not in dom_json else dom_json[NODE_PARENT_ID]
    return DOMNode(dom_json[NODE_ID], dom_json[NODE_NAME], value, attrs, parent_id, node_signature)


def ConstructSignature(node_json):
    '''
    Returns a string that represents the signature of this node.

    The signature of a node is defined is <[type]>\[attributes\].
    '''
    return '<{0}>{1}'.format(node_json[NODE_NAME], str(node_json[NODE_ATTRIBUTES] if NODE_ATTRIBUTES in node_json else []))


def SerializeAttributes(attributes, for_hdp):
    '''
    Returns a map of attributes from the array representation: [ key_1, val_1, key_2, val_2, ..., key_n, val_n ]
    '''
    attrs_interested = [ 'id', 'class', 'src', 'href' ]
    attrs = {}
    for i in range(0, len(attributes), 2):
        key = attributes[i]
        val = attributes[i + 1]
        if for_hdp and key not in attrs_interested:
            continue
        attrs[key] = val
    return attrs
