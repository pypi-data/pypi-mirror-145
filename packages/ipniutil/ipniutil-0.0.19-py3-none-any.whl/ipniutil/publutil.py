import re
import numpy as np

def parseCollation(s):
    collation={'volume':None
            , 'issue':None
            , 'page':None}
    if re.match('^[0-9]+$', s):
        collation['page'] = s
    elif re.match('^[IVXLC]+$', s):
        collation['page'] = s
    elif re.match('[0-9]+ \(-[0-9]+\)$', s) or re.match('[0-9]+ \([0-9]+-[0-9]+\)$', s):
        collation['page'] = s.split(' ')[0]
    elif re.match('^[0-9]+, fig\. .*$', s):
        collation['page'] = s.split(',')[0]
    elif re.match(r'^(?P<volume>.*)\((?P<issue>.*?)\):\s*(?P<page>[0-9]+).*', s):
        m = re.match(r'^(?P<volume>.*)\((?P<issue>.*?)\):\s*(?P<page>[0-9]+).*', s)
        collation = m.groupdict()
    elif re.match(r'^(?P<volume>.*):\s*(?P<page>e?[0-9]+).*', s):
        m = re.match(r'^(?P<volume>.*):\s*(?P<page>e?[0-9]+).*', s)
        collation = m.groupdict()
        collation['issue'] = None
    return collation

def collation2volume(s):
    return parseCollation(s)['volume']

def collation2issue(s):
    return parseCollation(s)['issue']

def collation2page(s):
    return parseCollation(s)['page']

def isBook(publication):
    flag = False
    if 'isbn' in publication.keys() and publication['isbn'] is not None:
        flag = True
    if not flag: 
        if 'tl2Author' in publication.keys() and publication['tl2Author'] is not None \
                and 'date' in publication.keys() and publication['date'] is not None \
                and re.match('^(1[6-9][0-9][0-9]|20[0-2][0-9])$',publication['date']):
            flag = True
    return flag    

pissn_signifiers=['hard copy', 'p\-issn', 'paper', 'pissn', 'print']
eissn_signifiers=['digital', 'e\-issn', 'e\-pub', 'eissn', 'elec', 'epubl', 'issne', 'online']

def str2pissn(s):
    issn = None
    issns = extractIssn(s,categorise=True)
    if issns is not None and ('pissn' in issns.keys()):
        issn = hyphenateISSN(issns['pissn'])
    return issn

def str2eissn(s):
    issn = None
    issns = extractIssn(s,categorise=True)
    if issns is not None and ('eissn' in issns.keys()):
        issn = hyphenateISSN(issns['eissn'])
    return issn

def str2uncatissn(s):
    issn = None
    issns = extractIssn(s,categorise=True)
    if issns is not None and ('uncat' in issns.keys()):
        issn = issns['uncat']
    if type(issn) is list:
        issn = ','.join([hyphenateISSN(i) for i in issn])
    else:
        issn = hyphenateISSN(issn)
    return issn

def extractIssn(s, categorise=False):
    issns = None
    if s is not None:
        s = s.lower()
        issns = re.findall(r'([0-9]{4}\-[0-9]{3}[0-9x]|[0-9]{7}[0-9x])',s)
    if issns is not None:
        if categorise:
            if len(issns) == 1:
                if (re.match('.*('+'|'.join(pissn_signifiers) + ').*',s) 
                    and not re.match('.*('+'|'.join(eissn_signifiers) + ').*',s)):
                    issns = {'pissn':issns[0]}
                elif (re.match('.*('+'|'.join(eissn_signifiers) + ').*',s) 
                    and not re.match('.*('+'|'.join(pissn_signifiers) + ').*',s)):
                    issns = {'eissn':issns[0]}
                else:
                    issns = {'uncat':issns[0]}
            elif len(issns) == 2:
                if re.match('.*('+'|'.join(pissn_signifiers) + ').*('+'|'.join(eissn_signifiers) + ').*',s):
                    issns={'pissn':issns[0],'eissn':issns[1]}
                elif re.match('.*('+'|'.join(eissn_signifiers) + ').*('+'|'.join(pissn_signifiers) + ').*',s):
                    issns={'eissn':issns[0],'pissn':issns[1]}
                else:
                    issns = {'uncat':issns}
            else:
                issns = {'uncat':issns}    
        else:
            issns = {'uncat':issns} 
    return issns

def hyphenateISSN(s):
    hyphenateISSN=s
    if s is not None and s is not np.nan:
        if type(s) is str: 
            if '(' in s:
                s = s.split('(')[0].strip()
            if not '-' in s:
                hyphenateISSN = str(s)[0:4]+'-'+str(s)[4:]
        elif type(s) is int:
            hyphenateISSN = str(s)[0:4]+'-'+str(s)[4:]
        hyphenateISSN = hyphenateISSN.upper()
    return hyphenateISSN

def extractPlaceOfPublication(title):
    place = None
    if title is not None:
        if title.endswith('U.K.'):   
            place = 'GB'
        if title.endswith('W.A.'):   
            place = 'AU'
        if title.endswith('N.Z.'):
            place = 'NZ'
        if title.endswith('Mexico, D.F.') or title.endswith('México, D. F.'):
            place = 'MX'
        if place is None:
            elems = title.split('.')
            if len(elems) > 1:
                place = elems[-1]
                if place == '' and len(elems) > 2:
                    place = elems[-2]
    if place is not None:
        place = place.strip()
    return place

def remarks2BhlID(s):
    bhlid = None
    if s is not None and s is not np.nan:
        m = re.search('BHL_title_ID\:([0-9]+)', s, re.IGNORECASE)
        if m is not None:
            bhlid=m.group(1)
    return bhlid
    
def main():
    pass

if __name__ == '__main__':
    main()