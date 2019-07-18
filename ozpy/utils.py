__author__ = 'Imam Omar Mochtar (iomarmochtar@gmail.com)'


class OZUtils:

    @classmethod
    def get_attrs(self, attrs, look_for=[]):
        result = {}
        # mark for what has been found
        _found_lfor = []
        convert_vals = {'TRUE': True, 'FALSE': False} 
        for attr in attrs:
            k = attr['n']
            if look_for and k not in look_for:
                continue
            v = attr['_content']
            # convert value
            if v in convert_vals:
                v = convert_vals[v]

            result[k] = v
           
            # just stop if all that we want search has been found
            if k in look_for:
                _found_lfor.append(k)

            if look_for and len(look_for) == len(_found_lfor):
                break
        return result

    @classmethod
    def get_attr(self, attrs, search, default_val=None):
        return self.get_attrs(attrs, [search]).get(search, default_val)

