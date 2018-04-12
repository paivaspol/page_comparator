def GetDOMTree(dom_tree_filename, for_hdp):
    '''
    Parses the dom tree file and returns the DOM tree representation.
    '''
    import json
    from DOMTree import DOMTree
    with open(dom_tree_filename, 'r') as input_file:
        dom_json = json.loads(input_file.read())
        return DOMTree(dom_json['result']['root'], for_hdp)
