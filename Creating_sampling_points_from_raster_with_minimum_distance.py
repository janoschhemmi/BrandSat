import gdal
import ogr
import os
import numpy as np
import matplotlib.pyplot as plt
import osr
import math


## Globals
#os.chdir("C:/Uni\Masterarbeit/03_Classification/01_01_Rasterbuilding")
wd = "V:/"

## read raster of tree species Brandenburg, single layer, single tree species
# ds = gdal.Open("V:/Data_Forst_Brandenburg/04_Rasterized_ForstGrundKarte/Brandenburg_15m_56ts_bereinigt.tif")
ds = gdal.Open("V:/BrandSat/01_Data/01_FGK/01_Rasterization/rasterized_20m.tif")
ds_sp = ds.GetProjection()
myarray = np.array(ds.GetRasterBand(1).ReadAsArray())

## read raster of age
#ds_age = gdal.Open("V:/Data_Forst_Sachsen/04_Rasterized_ForstGrundKarte/Saxony_aga_strat.tif")
#ds_sp_age = ds_age.GetProjection()
#myarray_age = np.array(ds_age.GetRasterBand(1).ReadAsArray())

## work around for only sampling int ts int without adopting function
myarray_age = myarray

## read raster of genus
#ds_genus = gdal.Open("V:/Data_Forst_Sachsen/04_Rasterized_ForstGrundKarte/Saxony_genus.tif")
#ds_sp_genus = ds_age.GetProjection()
#myarray_genus = np.array(ds_genus.GetRasterBand(1).ReadAsArray())
myarray_genus = myarray

'''
#### TEST empty input raster, place ones in the left down corner
myarray.fill(0)
myarray[0:100,0:100] = 1
myarray[1000:1100,1000:1100] = 2
'''

## get origin x and LL y of grid raster
#ds_grid = gdal.Open(r'V:\Force_Data\tiles_saxony.tif')
ds_grid = gdal.Open('V:/Force_Data/Force_Tiles_Brandenburg_raster.tif')

ds_grid_sp = ds_grid.GetProjection()

band1 = ds_grid.GetRasterBand
gt_band1 = ds_grid.GetGeoTransform()
gt_band1[0]
UL_x = gt_band1[0]+ 30000## in case of smaller raster extent, in this case one tile each
UL_y = gt_band1[3]- 30000 ## same

lrx = UL_x + (ds_grid.RasterXSize * 20)
lry = UL_y - (ds_grid.RasterYSize * 20)

## how many samples
number_of_ts = 22
list_of_n_samples = [500] * number_of_ts
#list_of_n_samples[14] = 200
#list_of_n_samples[15] = 400
#list_of_n_samples[17] = 200

list_of_lists = []

for i in range(1,(number_of_ts+1)):
    print(i)
    list_of_lists.append([i,i])


treespeciec_int_strat = [1,3,6,8,10,4,7,5,2,9,13,11,12,17,18,15,14,16,20,26,21,19]
# 1,2,3,4,5,6,7,8,9,10,14,17,22,25,32,35


# myarray[3000,3000] = 1
# myarray[6000,6000] = 1


########################## Function


def rand_sample_array_stratified(in_arr, in_arr_age, in_arr_genus,  n_samples, strata, min_dis, raster_cell_size, return_values):

    ''' in_arr    : array
        in_arr_age: age array of same extent
        n_samples : number of samples per strata
        strata    : list of values in array to pull samples from
        min_dis   : minimum distance between sampling points i n m
        raster_cell_size : length and heigth of raster cell in m
    '''

    # set up return variables
    samples_allstrata = []
    age_allstrata     = []
    genus_allstrata   = []
    values_allstrata = []
    overall_second_loop_dis_check_thrown_away = 0

    '''
    ## variables for check
    in_arr = myarray
    strata = treespeciec_int_strat[0]
    n_samples = list_of_n_samples
    min_dis = 5000
    raster_cell_size = 10
    return_values = True
    '''

    # loop through each stratum
    for i, stratum in enumerate(strata):
        j = i + 1
        print(j, "stratum", stratum)

        # create array that contains the row/col index pairs of all values that are within the current stratum
        #strat_cols, strat_rows = np.where(np.logical_and(in_arr >= stratum, in_arr <= stratum))
        strat_cols, strat_rows = np.where(np.logical_and(in_arr >= treespeciec_int_strat[i], in_arr <= treespeciec_int_strat[i]))
        #print(strat_rows)
        #print(strat_cols)

        sample_bowl = []

        for row, col in zip(strat_rows, strat_cols):
            sample_bowl.append([row, col])

        sample_bowl = np.column_stack((strat_rows, strat_cols))  ##gedauscht

        # draw random indices so select from the index pair array
        n_to_draw = n_samples[i]


        # break if number of values within the stratum is lower than_samples
        #print(len(strat_rows))
        if len(strat_rows) < n_to_draw:
            print("Warning: Sample size ({0}) is larger than the occurrence of values({1}) within"
                  "stratum {2}({3}).".format(n_to_draw, len(strat_rows), i, stratum))
        random_draws_out = []
        age_values = []
        one_draw = []
        lo = 0

        while (len(random_draws_out) < n_samples[i]) and lo < 10: ## set number of iteration, means tries to get samples


            # use np.unique to avoid sampling same pixel several times, re - draw until we have number of samples we need
            one_draw = (np.unique(np.random.choice(sample_bowl.shape[0],
                                                   n_to_draw, replace=True)).tolist())

            throw_away_count = 0

            ### get x and y values for draw
            one_draw_coordinates = sample_bowl[one_draw]
            checked_draws = []

            # loop over points in one draw
            for k, random_draw in enumerate(one_draw_coordinates):

                '''
                ### fuer test:
                random_draw = one_draw_coordinates[1]
                random_draw_check = one_draw_coordinates[3]
                '''

                ### check for distance to previous draws
                dis_not_ok = 0

                # loop over one draw for distance check
                for random_draw_check in one_draw_coordinates:


                    if math.sqrt((random_draw[0] - random_draw_check[0]) ** 2 + (random_draw[1] - random_draw_check[1]) ** 2) < (
                            min_dis / raster_cell_size):

                        if math.sqrt((random_draw[0] - random_draw_check[0]) ** 2 + (random_draw[1] - random_draw_check[1]) ** 2) != 0:
                            ## exclude self check
                            #print("Distance:")
                            #print(math.sqrt((random_draw[0] - random_draw_check[0]) ** 2 + (random_draw[1] - random_draw_check[1]) ** 2))
                            #print("to close, thrown away, number:",k, "in strata:", stratum)

                            throw_away_count = throw_away_count + 1
                            dis_not_ok = dis_not_ok + 1
                            break

                # check with existing previous random draw, here zero is allowed for self check (although it shouldnt be necessary)


                if len(random_draws_out) > 0 and dis_not_ok == 0:
                    #print("checking with previous draw")
                    for random_draw_check_2 in random_draws_out:

                        #print("len random draws out:", len(random_draws_out))
                        #print("len n to draw:", (n_to_draw))
                        #print("random_draw_check_2",random_draw_check_2,
                        #      "random_draw to check " , random_draw)

                        #print(checked_draws)
                        if math.sqrt((random_draw[0] - random_draw_check_2[0]) ** 2 + (random_draw[1] - random_draw_check_2[1]) ** 2) < (
                                min_dis / raster_cell_size):

                            throw_away_count = throw_away_count + 1
                            dis_not_ok = dis_not_ok + 1
                            overall_second_loop_dis_check_thrown_away = overall_second_loop_dis_check_thrown_away + 1
                            #print("to close, thrown away, count second loop:",
                             #     overall_second_loop_dis_check_thrown_away)
                            break


                # if dis not ok delete draw
                if dis_not_ok > 0:
                    print("mark sample for deleting ts:" )
                    one_draw_coordinates[k] = -999


            ##  delete rows with nan
            one_draw_coordinates =  one_draw_coordinates[one_draw_coordinates[:,1] != -999]
            print(one_draw_coordinates)
            '''
            for l in range(0, len(one_draw_coordinates)):

                print("aa")
                x = one_draw_coordinates[l]
                if (x[1] == -999.0)==True:
                    
                    one_draw_coordinates = np.delete(one_draw_coordinates, (l+1), axis=0)
                    print("deleting_sample")
                    print(one_draw_coordinates)
                
                for x in one_draw_coordinates[l]:
                    print("deleting the nan marked in one draw coordinates", l)
                    print(len(one_draw_coordinates))
                    print("x",x)

                    if l >= (len(one_draw_coordinates)-1):
                        print("break")
                        break
                    if (x == -999):
                        one_draw_coordinates = np.delete(one_draw_coordinates, l, axis=0)
                        print("deleting_sample")
                if l >= (len(one_draw_coordinates)-1 ):
                    break
                    '''

            ## write out to higher loop
            print("here")
            if len(random_draws_out)>0:
                print("random_draws_out",random_draws_out)
                print("one_draw_coordinates",one_draw_coordinates)
                random_draws_out = np.concatenate((random_draws_out,one_draw_coordinates), axis=0)
            print("here")
            if len(random_draws_out)==0:
                random_draws_out = one_draw_coordinates
            print("here")

            #print(checked_draws)
            # random_draw = np.unique(random_draw).tolist()

            print("random_draws_out", random_draws_out)

            if len(random_draws_out) == len(strat_rows):
                break
            print(i)
            print(len(random_draws_out))
            n_to_draw = n_samples[i] - len(random_draws_out)
            lo = lo + 1

        #samples = sample_bowl[random_draws_out]
        samples = random_draws_out

        print(samples)
        age_values = [in_arr_age[(sample[1]), (sample[0])] for sample in samples]
        age_values = [int(a) for a in age_values]

        genus_values = [in_arr_genus[(sample[1]), (sample[0])] for sample in samples]
        genus_values = [int(a) for a in genus_values]

        print("appending data of strata")
        samples_allstrata.append(samples)
        age_allstrata.append(age_values)
        genus_allstrata.append(genus_values)

        #if return_values is True:
        #    values_allstrata.append(values)
    #if return_values is True:
    #    return samples_allstrata, values_allstrata
    return samples_allstrata, age_allstrata , genus_allstrata

test_sample, age_values , genus_values = rand_sample_array_stratified(myarray,myarray_age, myarray_genus,
    strata = treespeciec_int_strat,n_samples = list_of_n_samples, min_dis = 100, raster_cell_size = 20,
                                           return_values = True)



###### create shapefile from points in array
## ## ## ## ## ## ### ### ### ### ### ## ### ##

## Create Output Shapefile
driver = ogr.GetDriverByName("ESRI Shapefile")
print("create shapefile")
shapefile = driver.CreateDataSource('V:/BrandSat/01_Data/02_Sampling/Sampling_Points_Brandenburg_15m_1000_samp_size_20m_spatial_res_test.shp')

### get spatial reference of test sample file from existing shapefile
dataset_proj = driver.Open('V:/Processing/02_Sampling/02_15m_40st_Brandenburg/Sampling_Points_Brandenburg_15m_500st_40ts.shp')
layer_proj = dataset_proj.GetLayer()
# set spatial reference
spatialRef = layer_proj.GetSpatialRef()
# spatialreference.ImportFromEPSG(3035)

# Create Layer
layer = shapefile.CreateLayer('points_layer', spatialRef, ogr.wkbPoint)
layerDefinition = layer.GetLayerDefn()

# Create Attribute Fields
layer.CreateField(ogr.FieldDefn("UID", ogr.OFTInteger))
layer.CreateField(ogr.FieldDefn("ID", ogr.OFTInteger))
layer.CreateField(ogr.FieldDefn("TreeS_int", ogr.OFTInteger))
layer.CreateField(ogr.FieldDefn("Age_int", ogr.OFTInteger))
layer.CreateField(ogr.FieldDefn("Genus_int", ogr.OFTInteger))

## create shapefile with points
o = 0
test_sample[0]
# k = 0
print("Task: Creating Shapefile")
for k in range(0, len(test_sample)):
    print("processing strata: ",k)
    #k = 0  ## test
    strata = (test_sample[k])
    strata_age = age_values[k]
    strata_genus = genus_values[k]

    tt = len(strata)
    if k > 0:
      o = o + tt  ## for uid , ansonsten immer 500 zuviel
    print(o)
    for i in range (0, len(strata)):
        # i = 1  ## test
        print("sample point: ", i, "strata: ", k)
        single_point = strata[i]
        single_age   = strata_age[i]
        single_genus = strata_genus[i]

        print(single_point)
        print("age:", single_age)

        feature = ogr.Feature(layer.GetLayerDefn())
        print("t")
        feature.SetField('UID', ( (o) + (i+1)))
        print("t")
        feature.SetField('ID', i + 1)
        print("t")
        feature.SetField('TreeS_int', treespeciec_int_strat[k])
        feature.SetField('Age_int',   single_age)
        feature.SetField('Genus_int', single_genus)
        # create wkt
        wkt = "POINT(%f %f)" % ((((float(single_point[0])) * 10) + UL_x + 5), ((UL_y - ((float(single_point[1])) * 10) - 5) ))
        # Create point from the Well Known Txt
        point_wkt = ogr.CreateGeometryFromWkt(wkt)
        feature.SetGeometry(point_wkt)
        # Create the features
        layer.CreateFeature(feature)
        feature = None

shapefile.Destroy()

##
print("finished")
