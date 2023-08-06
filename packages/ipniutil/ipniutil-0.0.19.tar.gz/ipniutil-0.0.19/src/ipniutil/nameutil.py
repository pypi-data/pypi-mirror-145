import re

def extractDoi(remarks):
    doi = None
    if remarks is not None:
        patt='(?:doi[\.:]org[/:]?|doi[:;]?)(?P<doi>10.*?)(?:,.*|;.*| .*|\[.*| .*|$)'
        patt = re.compile(patt,flags=re.IGNORECASE)
        m = re.search(patt,remarks)
        if m:
            doi=m.groupdict()['doi']
    return doi

def isEpublished(remarks):
    flag = False
    if remarks is not None:
        flag = '[epublished]' in remarks.lower()
    return flag
