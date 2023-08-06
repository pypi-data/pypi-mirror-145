import re
from unidecode import unidecode

def separateId(s):
    prefix=s
    id=None
    if s is not None and ' ' in s:
        id = s.rsplit(' ',1)[1]
        patterns=['[0-9]+[\.\-]?[0-9]+','[0-9]+[\.\-]?[0-9]+[A-Za-z]','[A-Z]+\-?[0-9]+[\.\-]?[0-9]+']
        if re.match('|'.join(patterns),id):
            prefix = s.rsplit(' ',1)[0]
        else:
            id = None
    else:
        pattern='([A-Z]+)[\-\.]?([0-9]+.*)'
        m = re.match(pattern,s)
        if m:
            prefix=m.groups()[0]
            id=m.groups()[1]
    return (prefix,id)

def extractTypeHolders(s):
    typeholders = None
    if s is not None:
        typeholders = []
        prev_type_of_type = None
        prev_type_holder = None
        for type_holder_frag in s.split(';'):
            if type_holder_frag in ['null', '']:
                continue
            typeholder = dict()
            if not ' ' in type_holder_frag and prev_type_of_type is not None and prev_type_holder is not None:
                # This type is simply an object number, the type of type and holder must be read from the previous iteration
                typeholder['type_of_type'] = prev_type_of_type
                typeholder['type_holder'] = prev_type_holder
                typeholder['type_id'] = type_holder_frag
            else:
                typeholder['type_of_type'] = type_holder_frag.split(' ', 1)[0]
                typeholder['type_holder'] = type_holder_frag.split(' ', 1)[1]
                if re.search('[0-9]', typeholder['type_holder']):
                    prefix, id = separateId(typeholder['type_holder'])
                    typeholder['type_holder'] = prefix
                    typeholder['type_id'] = id
            typeholders.append(typeholder)
            prev_type_of_type = typeholder['type_of_type']
            prev_type_holder = typeholder['type_holder']
        pass
    return typeholders

def isPublishingAuthorCollector(publishingAuthors, collectorTeam, decode=True):
    author_is_collector = False
    if decode:
        publishingAuthors = unidecode(publishingAuthors)
        collectorTeam = unidecode(collectorTeam)
    if publishingAuthors is not None:
        for stdform in publishingAuthor2StandardForms(publishingAuthors):
            patts = standardForm2SubstantiveSurnamePattern(stdform)
            if re.search(patts, collectorTeam):
                author_is_collector = True
                break
    return author_is_collector

def publishingAuthor2StandardForms(s):
    standard_forms = None
    if s is not None:
        standard_forms = re.split('(?:\s&\s|,\s)', s)
        if ' ex ' in s:
            standard_forms = re.split('(?:\s&\s|,\s)', s.split(' ex ',1)[1])
    return standard_forms

def standardForm2SubstantiveSurnamePattern(s):
    substantivesurname_patt = None
    if s is not None:
        # Strip bis / f / ter: 
        s = re.sub(r'(?:\bf\.$|\bbis$|\bter$)','',s).strip()
        
        # Split on abbreviated initials and use last element
        elems = re.split(r'(?<=[A-Z])\.',s)
        substantivesurname = elems[-1].strip()

        # Construct set of alternative patterns
        patts = []
        if re.match('[^A-Za-z]', substantivesurname):
            patts.append(re.sub('[^A-Za-z]','.*?', substantivesurname))
        
        if re.search('[a-z][A-Z]',substantivesurname):
            patt_elems = re.split('([a-z][A-Z])',substantivesurname,1)
            patt = r'.*\b' + patt_elems[0] + patt_elems[1][0] + '.*?' + patt_elems[1][1] + patt_elems[2]
            if patt.endswith('.'):
                patt = patt + r'*?'    
            patt = patt + r'\b.*'
            patts.append(patt)

        # Split on non characters:
        elems = [elem.strip() for elem in re.split(r'[^A-Za-z]',substantivesurname)]
        for elem in elems:
            if len(elem) > 1 and elem != elem.lower():
                if elem + '.' in substantivesurname:
                    patts.append(r'\b' + elem + r'.*?\b')
                else:
                    patts.append(r'.*\b' + elem + r'\b.*')
        # Join alternative patterns to return a single pattern
        substantivesurname_patt = '(?:' + '|'.join(patts) + ')'
    return substantivesurname_patt

def main():
    s="holotype MICH;isotype AMES;isotype DAV 89230;105887;isotype F;isotype MA;isotype NY [2 sheets]"
    print(s)
    print(extractTypeHolders(s))

if __name__ == '__main__':
    main()
