def isset(object,key,secondary=None):
    if (secondary):
        try:
            return object[key][secondary]
        except KeyError:
            return ""
    else:
        
        try:
            return object[key]
        except KeyError:
            return ""
                
