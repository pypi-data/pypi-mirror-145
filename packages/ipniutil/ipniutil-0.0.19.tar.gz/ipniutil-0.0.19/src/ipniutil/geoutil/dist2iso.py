import re
from unidecode import unidecode

def splitDist(s, clean=True):
    dists = None
    if s is not None:
        if not re.match('\(;+\)', re.sub('[^\(\);]','',unidecode(s))):
            dists = s.split(';')
        else:
            dists = re.split('(?<=\));',s)
    if clean and dists is not None:
        dists = [cleanDist(dist) for dist in dists]
    return dists

def cleanDist(s, decode=True):
    cleaned = s
    if s is not None:
        if decode:
            cleaned = unidecode(cleaned)
        if cleaned.endswith('.;'):
            cleaned = re.sub('\.;$','',cleaned)
        if cleaned.endswith('.'):
            cleaned = re.sub('\.$','',cleaned)
        if cleaned.endswith(';'):
            cleaned = re.sub(';$','',cleaned)
        if cleaned.endswith('?'):
            cleaned = re.sub('\?$','',cleaned)
        if cleaned.count('(') == 1 and ',' in cleaned.split('(')[0]:
            cleaned = cleaned.split(' (')[0].rsplit(',',1)[1].strip() + ' (' + cleaned.split(' (')[1]
    return cleaned

def dist2joinlist(s, include_bracketed_text=False, clean=True):
    dist_l=None
    if s is not None:
        m = re.match('^(?P<pref>.*?) \((?P<br_content>[^\(\)]*?)\)$', s)
        if m is not None:
            pref = m.groupdict()['pref'].strip()
            br_content = m.groupdict()['br_content'].strip()
            if ',' in pref:
                pref = pref.rsplit(',',1)[1].strip()
            dist_l = [s, pref, pref + ', ' + br_content]
            if br_content.count(',') == 3:
                dist_l.append(br_content.split(',',1)[1].strip())
            if include_bracketed_text:
                dist_l.append(br_content)
        else:
            dist_l = [s]
        if dist_l is not None and clean:
            dist_l = [cleanDist(elem) for elem in dist_l]
    return dist_l

from ipniutil.geoutil import df_tdwg
def dist2iso(s):
    searchlist = dist2joinlist(unidecode(s), include_bracketed_text=True)    
    GEO_TXT_FIELD='as_text'
    iso_codes = list(df_tdwg[df_tdwg[GEO_TXT_FIELD].isin(searchlist)].iso.unique())
    if len(iso_codes) == 0:
        iso_codes = None
    return iso_codes