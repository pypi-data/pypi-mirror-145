import pandas as pd
import geopandas as gpd
import os
from math import radians, cos, sin, asin, sqrt, atan2
import numpy as np
from shapely.geometry import Polygon, MultiPoint, Point
from shapely.ops import nearest_points
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans

def distance(lat1, lat2, lon1, lon2, measure=None):
     
    # The math module contains a function named
    # radians which converts from degrees to radians.
    lon1 = radians(lon1)
    lon2 = radians(lon2)
    lat1 = radians(lat1)
    lat2 = radians(lat2)
      
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
 
    c = 2 * asin(sqrt(a))
    
    if measure.upper() == 'KM':
        r = 6371 # Radius of earth in kilometers
    else:
        r = 3956 # Radius of earth in Miles
    # calculate the result 
    return(c * r)


### POPULATION CENTER ###
## DATA FROM POLTICAL GEOGRAPHY FROM PL94 'GEOID20','INTPTLAT20','INTPTLON20','geometry'
## GEOGRAPHIC DATA FROM Block Assignment Files 'DistrictName', 'blk_GEOID20', 'geometry'

def weighted_centroind(df, District_ID, GEOID='GEOID20', Population='POP100', Lat='INTPTLAT20', Lon='INTPTLON20', dist_geo='geometry'):
    dfList = list(set(df[District_ID].tolist()))
    cdObj = {i: {'wx': None, 'wy':None, 'cx':None , 'cy':None} for i in  dfList}
    for cd in dfList:
        df_cd = df[df[District_ID] == cd]
        m = df_cd[Population].sum()
        df['vy'] = df_cd[Population]*df_cd[Lat].astype('float')
        df['vx'] = df_cd[Population]*df_cd[Lon].astype('float')
        vy = df['vy'].sum()
        vx = df['vx'].sum()
        cdObj[cd]['wy'] = vy/m
        cdObj[cd]['wx'] = vx/m

        cdObj[cd]['cy'] =  df.iloc[0][dist_geo].centroid.y
        cdObj[cd]['cx'] =  df.iloc[0][dist_geo].centroid.x
    df_centernoids = pd.DataFrame.from_dict(cdObj, orient='index')
    df_centernoids = df_centernoids.dropna(how='any')
    dfList = list(df_centernoids.index)
    df_centernoids.to_csv('basic_points.csv')
    df_wp = df_centernoids[['wy','wx']]
    df_wp = gpd.GeoDataFrame(df_wp, geometry = gpd.points_from_xy(df_wp.wx,df_wp.wy))
    df_cp = df_centernoids[['cy','cx']]
    df_cp = gpd.GeoDataFrame(df_cp, geometry = gpd.points_from_xy(df_cp.cx,df_cp.cy))
    df_cp = df_cp.set_crs('epsg:4269')
    df_wp = df_wp.set_crs('epsg:4269')
    district_profile = {i: {'pop_center':None,'pop_boundry':None} for i in  dfList}
    for dis in dfList:
        df_c = df_cp[df_cp.index==dis]
        df_w = df_wp[df_wp.index==dis]
        district_profile[dis]['pop_center'] = distance(df_c['cy'],df_w['wy'],df_c['cx'],df_w['wx'])
    
    for dis in dfList:
        gp_CD_init = df[df[District_ID]==dis]
        gp_CD_init = gpd.GeoDataFrame(gp_CD_init, geometry=dist_geo)
        df_wp_dis = df_wp[df_wp.index==dis]
        points2 = gp_CD_init.copy()
        points2 = points2.to_crs('epsg:4269')
        points2[dist_geo] = points2.exterior
        nearest_geoms = nearest_points(df_wp_dis.unary_union,points2.unary_union)
        ear_idx0 = nearest_geoms[0]
        ear_idx1 = nearest_geoms[1]
        district_profile[dis]['pop_boundry'] = distance(ear_idx0.y,ear_idx1.y,ear_idx0.x,ear_idx1.x)
        
    df_pointDistance = pd.DataFrame.from_dict(district_profile, orient='index')
    df_pointDistance['total_distance'] = df_pointDistance['pop_center']+df_pointDistance['pop_boundry']
    df_pointDistance['pop_compact'] = df_pointDistance['pop_center']/df_pointDistance['total_distance']
    df_pointDistance.to_csv('base_distance.csv')

def kmean_xSymetry(df, district_id, pop, lat, lon, geoid, district_geometry):
    dfList = list(set(df[district_id].tolist()))
    simp_set_all = df.loc[:, [district_id, pop, lat, lon, geoid]]
    df_kcluster = pd.DataFrame(columns=[district_id, pop, lat, lon, geoid,'Cluster_label'])
    for cd in dfList:
        simp = simp_set_all[simp_set_all[district_id]==cd]
        kmeans = KMeans(n_clusters = 2, n_init=50,max_iter=1000, init ='k-means++')
        lat_long = simp[simp.columns[3:4]]
        blk_size = simp[simp.columns[1]]
        simp_kmean_clusters = kmeans.fit(lat_long,sample_weight=blk_size)
        simp['Cluster_label'] = kmeans.predict(lat_long,sample_weight=blk_size)
        simp['Cluster_label'] = simp['Cluster_label']+1
        df_kcluster = df_kcluster.append(simp)
        clusterN = [1,2]
    kcObj = {i: {'1':{},'2':{}} for i in  dfList}
    for cd in dfList:
        for clu in clusterN:
            df_k = df_kcluster[(df_kcluster[district_id]==cd) & (df_kcluster['Cluster_label']==clu)]
            m = df_k[pop].sum()
            df_k['vy'] = df_k[pop]*df_k[lat].astype('float')
            df_k['vx'] = df_k[pop]*df_k[lon].astype('float')
            vy = df_k['vy'].sum()
            vx = df_k['vx'].sum()
            df_k_geo = gpd.GeoDataFrame(df_k, geometry=gpd.points_from_xy(df_k[lon], df_k[lat]))
            poly = Polygon([p for p in  df_k_geo[district_geometry].tolist()])
            kcObj[cd][str(clu)]['cx']= poly.centroid.x
            kcObj[cd][str(clu)]['cy']= poly.centroid.y
            kcObj[cd][str(clu)]['wy']= vy/m
            kcObj[cd][str(clu)]['wx']= vx/m
    dfKcc = pd.DataFrame(columns=['dist','Cluster','Center_Point','Weighted_Point'])
    for k,v in kcObj.items():
        for i,j in v.items():
            dfKcc = dfKcc.append({'dist':k,'Cluster':i,'Center_Point':Point(j['cx'],j['cy']),'Weighted_Point':Point(j['wx'],j['wy'])},ignore_index=True)
    dfKcc.to_csv('kmean_point.csv')


