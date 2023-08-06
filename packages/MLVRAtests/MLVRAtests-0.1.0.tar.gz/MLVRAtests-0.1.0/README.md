Machine Learning Voting Right Act Tests
====

Centernoid X-Symetry

Uses weighted centernoid and K-Mean Clustering to determin the compactness of a district by mesuring the distance from Geographic Center and Boundry 

```Python
weighted_centroind(df, District_ID, GEOID='GEOID20', Population='POP100', Lat='INTPTLAT20', Lon='INTPTLON20', dist_geo='geometry')
```

```Python 
kmean_xSymetry(df, district_id, pop, lat, lon, geoid, district_geometry)
```

Ecological Inference 

Uses Elecologic Ingernce Model from King 1999 using a default covariate as target vote share and lmbda as 0.5 to match what was writen in [King's Paper]('https://dash.harvard.edu/bitstream/handle/1/4125130/binom.pdf;sequence=2')

```Pyhton
ecological_inference(Total_Population_Col, Target_Population_Col, 
                        Target_Vote_Share_Percentage, covariate=None, lmbda=0.5)
```