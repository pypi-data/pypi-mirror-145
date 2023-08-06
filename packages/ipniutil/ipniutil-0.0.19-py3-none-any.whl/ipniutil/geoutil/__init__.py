import pandas as pd
import numpy as np
import pkg_resources

ISO_ALPHA2_FIELD='alpha-2'
ISO_ALPHA3_FIELD='alpha-3'
ISO_NAME_FIELD='name'
ISO_REGION_FIELD='region'
ISO_SUBREGION_FIELD='sub-region'

IPNI_DIST_ISO_FIELD='iso_dist'
IPNI_DIST_ISO3_FIELD='iso3_dist'
IPNI_DIST_REGION_FIELD='iso_region_dist'
IPNI_DIST_SUBREGION_FIELD='iso_subregion_dist'

iso_file='data/iso_std.csv'
stream = pkg_resources.resource_stream(__name__, iso_file)

iso_cols=[ISO_ALPHA2_FIELD,ISO_ALPHA3_FIELD,ISO_REGION_FIELD,ISO_SUBREGION_FIELD]
df_iso= pd.read_csv(stream,sep=',',encoding='utf8',usecols=iso_cols,nrows=None,keep_default_na=False,na_values=['',None])
df_iso.columns=[IPNI_DIST_ISO_FIELD,IPNI_DIST_ISO3_FIELD,IPNI_DIST_REGION_FIELD,IPNI_DIST_SUBREGION_FIELD]

tdwg_l1_file='data/tdwg_l1.txt'
stream = pkg_resources.resource_stream(__name__, tdwg_l1_file)
df_l1 = pd.read_csv(stream,sep='*',decimal=",",encoding='utf8',keep_default_na=False,na_values=['',None])

tdwg_l2_file='data/tdwg_l2.txt'
stream = pkg_resources.resource_stream(__name__, tdwg_l2_file)
df_l2 = pd.read_csv(stream,sep='*',decimal=",",encoding='utf8',keep_default_na=False,na_values=['',None])

tdwg_l3_file='data/tdwg_l3.txt'
stream = pkg_resources.resource_stream(__name__, tdwg_l3_file)
df_l3 = pd.read_csv(stream,sep='*',decimal=",",encoding='ISO-8859-1',keep_default_na=False,na_values=['',None])

tdwg_l4_file='data/tdwg_l4.txt'
stream = pkg_resources.resource_stream(__name__, tdwg_l4_file)
df_l4 = pd.read_csv(stream,sep='*',decimal=",",encoding='ISO-8859-1',keep_default_na=False,na_values=['',None])

# l1 - no parent, so just some renames
df_l1_flat = df_l1
df_l1_flat['level']=[1]*len(df_l1_flat)
df_l1_flat['code']=df_l1_flat['L1 code']
df_l1_flat['parent']=[None]*len(df_l1_flat)
df_l1_flat['as_text']=df_l1_flat['L1 continent']

# l2 to l1
df_l2_flat = pd.merge(left=df_l2
        , right=df_l1
        , left_on='L1 code'
        , right_on='L1 code'
        , how='left')
df_l2_flat['level']=[2]*len(df_l2_flat)
df_l2_flat['code']=df_l2_flat['L2 code']
df_l2_flat['parent']=df_l2_flat['L1 code']
df_l2_flat['as_text']=df_l2_flat.apply(lambda row: '{} ({})'.format(row['L2 region'],row['L1 continent']),axis=1)

# l3 to l2
df_l3_flat = pd.merge(left=df_l3
        , right=df_l2_flat
        , left_on='L2 code'
        , right_on='L2 code'
        , how='left')
df_l3_flat['level']=[3]*len(df_l3_flat)
df_l3_flat['code']=df_l3_flat['L3 code']
df_l3_flat['parent']=df_l3_flat['L2 code']
df_l3_flat['as_text']=df_l3_flat.apply(lambda row: '{} ({}, {})'.format(row['L3 area'], row['L2 region'],row['L1 continent']),axis=1)

# l4 to l3
df_l4_flat = pd.merge(left=df_l4
        , right=df_l3_flat
        , left_on='L3 code'
        , right_on='L3 code'
        , how='left')
df_l4_flat['level']=[4]*len(df_l4_flat)
df_l4_flat['code']=df_l4_flat['L4 code']
df_l4_flat['parent']=df_l4_flat['L3 code']
df_l4_flat['as_text']=df_l4_flat.apply(lambda row: '{} ({}, {}, {})'.format(row['L4 country'], row['L3 area'], row['L2 region'],row['L1 continent']),axis=1)

cols=['level','code','as_text','parent']
df_tdwg=pd.concat([df_l1_flat[cols]
                    , df_l2_flat[cols+['L2 ISOcode']]
                    , df_l3_flat[cols+['L2 ISOcode','L3 ISOcode']]
                    , df_l4_flat[cols+['L2 ISOcode','L3 ISOcode','L4 ISOcode']]]
                    , sort=False)
mask=(df_tdwg['L2 ISOcode'].notnull()|df_tdwg['L3 ISOcode'].notnull()|df_tdwg['L4 ISOcode'].notnull())
df_tdwg.loc[mask,'iso']=df_tdwg[mask].apply(lambda row: list(set([iso for iso in [row['L4 ISOcode'],row['L3 ISOcode'],row['L4 ISOcode']] if iso not in [None,np.nan]]))[0],axis=1)
df_tdwg.drop(columns=['L2 ISOcode','L3 ISOcode','L4 ISOcode'],inplace=True)

# Assign ISO at L2 if children all share same code
g = df_tdwg[df_tdwg.level==3].groupby('parent').agg({'iso':'unique'})
g['iso_c']=g.iso.apply(len)
g = g[g.iso_c==1]
g['iso_v']=g.iso.apply(lambda x: x[0])
iso_mapper=g[g.iso_v.notnull()].iso_v.to_dict()
mask=(df_tdwg.iso.isnull() & (df_tdwg.level==2))
df_tdwg.loc[mask,'iso']=df_tdwg[mask].code.map(iso_mapper)    

# # Todo - use corrections
tdwg_corrections_file='resources/tdwg-hierarchy-corrections.txt'
stream = pkg_resources.resource_stream(__name__, tdwg_corrections_file)

df = pd.read_csv(stream, sep=',')    
for i, row in df.iterrows():
    mask = (df_tdwg['level']==row['level'])&(df_tdwg['code']==row['code'])
    df_tdwg.loc[mask,'iso']=row['iso']

from ipniutil.geoutil import dist2iso
df_tdwg['as_text_expl']=df_tdwg.as_text.apply(lambda x: dist2iso.dist2joinlist(x, include_bracketed_text=True))
df_tdwg=df_tdwg[['as_text_expl','iso']].explode('as_text_expl')
df_tdwg.columns=['as_text','iso']