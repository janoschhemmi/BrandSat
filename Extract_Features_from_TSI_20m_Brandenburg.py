import time
from multiprocessing.pool import Pool
from os.path import join
from random import randint
import numpy as np
from osgeo import gdal

#l2016 = len(list(range(0, 72 )))  ## 2016
#l2017 = (list(range(72, 145 ))) ## 2017
#l2018 = (list(range(145, 218)))
#len((list(range(145, 218))))
#ll = list(range(500))

#for k in l2018:
#    print("element of list year:", k)
#    test = ll[k]
#    print(test)

from force4qgis.hubforce.core.raster.rastercollection import RasterCollection
from force4qgis.hubforce.core.raster.resolution import Resolution
from force4qgis.hubforce.inputformats.forceraster import forceRaster
from force4qgis.hubforce.core.raster.gdalband import GdalBand


print("intro")
debug = True

'''
## number of bands 
ds = gdal.Open('//141.20.140.91/NAS_Rodinia/Croptype/X0052_Y0047/2016-2019_001-365_LEVEL4_TSA_LNDLG_NIR_TSI.tif')
ds.RasterCount
print (ds.GetMetadata())
'''

def main(tilename):
    tilenames = [tilename]
    #shapefile = r'\\141.20.140.91\NAS_Rodinia\Croptype\Sampling_Jan\2020-04-03\revisited_500st_Brandenburg_22ts_bereinigt_50mdis.shp'
    # shapefile = r'\\141.20.140.91\NAS_Rodinia\Croptype\Sampling_Jan\2020-04-18\Sampling_Points_Saxony_15m_50mdis_revisited.shp'

    # 20m Brandenburg:
    shapefile = r'\\141.20.140.91\NAS_Rodinia\Croptype\BrandSat\04_Sampling\2020-08-21_Sampling_20m_Brandenburg\Sampling_Points_Brandenburg_15m_500_samp_size_20m_spatial_res_test.shp'
    ##here unbereinigt
    #shapefile = r'\\141.20.140.91\NAS_Rodinia\Croptype\Sampling_Jan\2020-06-21_Brandenburg_nicht_bereinigt\Sampling_Points_Brandenburg_15m_500st_allts_bereinigt_50mdis.shp'

    ## shapefile test reihenfolge
    #shapefile = r'\\141.20.140.91\NAS_Rodinia\Croptype\Sampling_Jan\2020-06-02_Brandenburg_check\one_sample_for_indicy_check.shp'

    # tilenames = ['X0056_Y0041', 'X0056_Y0042']

    # open raster
    print('prepare raster')

    def bandNameFunc(gdalBand: GdalBand) -> str:
        return f'B{gdalBand.number}'

    rasters = list()

    # - TSI raster
    if True:
        bandList = list(range(1, 187 ))  # 2018 - 08 2020

        forceRasterPath = r'\\141.20.140.91\NAS_Rodinia\Croptype\BrandSat\03_Data_Level3\20200819_S2_20m'
        basenames = (
            #'2017-2019_001-365_HL_TSA_SEN2L_BLU_TSI.tif',
            #'2017-2019_001-365_HL_TSA_SEN2L_GRN_TSI.tif',
            #'2017-2019_001-365_HL_TSA_SEN2L_NIR_TSI.tif',
            #'2017-2019_001-365_HL_TSA_SEN2L_RED_TSI.tif',
            #'2017-2019_001-365_HL_TSA_SEN2L_SW1_TSI.tif',
            #'2017-2019_001-365_HL_TSA_SEN2L_SW2_TSI.tif',
            #'2017-2019_001-365_HL_TSA_SEN2L_NDV_TSI.tif',

            '2018-2020_001-365_HL_TSA_SEN2L_BLU_TSI.tif',
            '2018-2020_001-365_HL_TSA_SEN2L_GRN_TSI.tif',
            '2018-2020_001-365_HL_TSA_SEN2L_RED_TSI.tif',
            '2018-2020_001-365_HL_TSA_SEN2L_RE1_TSI.tif',
            '2018-2020_001-365_HL_TSA_SEN2L_RE2_TSI.tif',
            '2018-2020_001-365_HL_TSA_SEN2L_NIR_TSI.tif',
            '2018-2020_001-365_HL_TSA_SEN2L_SW1_TSI.tif',
            '2018-2020_001-365_HL_TSA_SEN2L_SW2_TSI.tif',
            '2018-2020_001-365_HL_TSA_SEN2L_NDV_TSI.tif',
            '2018-2020_001-365_HL_TSA_SEN2L_EVI_TSI.tif',
            '2018-2020_001-365_HL_TSA_SEN2L_ARV_TSI.tif',
            '2018-2020_001-365_HL_TSA_SEN2L_NBR_TSI.tif',
            '2018-2020_001-365_HL_TSA_SEN2L_NDM_TSI.tif',
            '2018-2020_001-365_HL_TSA_SEN2L_BNR_TSI.tif'

        )
        for basename in basenames:
            raster = forceRaster(
                forceRasterPath=forceRasterPath,
                basename=basename,
                tilenames=tilenames,
                resolution=Resolution(20, 20),
                bandList=bandList,
                bandNameFunc=bandNameFunc,
                debug=debug
            )
            rasters.append(raster)

    # - env vars
    if True:
        print("no")
        #forceRasterPath = r'\\141.20.140.91\NAS_Rodinia\Croptype'

        #basenames = (  # 'srtm_10m.tif', 'slope_10m.tif', 'aspect_10m.tif',
                        #'CECSOL_M_sl1_10m.tif', 'ORCDRC_M_sl1_10m.tif', 'PHIKCL_M_sl1_10m.tif',

                        #'bag5000ob.tif','bgl5000_v20.tif','boart1000_ob_v20.tif','buek1000de_v21.tif','gmk1000.tif','humus1000_ob_v20.tif',
                        #'buk200.tif',

                        #'forst_gl.tif', 'forst_wuchsgebiete_wuchsbezirke.tif',  ##forstliche grosslandschaften

                        #'Brandenburg_Bergbau.tif',

                        #'TAMM_13_1981_30_10m.tif',
                        #'TAMM_14_1981_30_10m.tif',
                        #'TAMM_15_1981_30_10m.tif',
                        #'TAMM_16_1981_30_10m.tif',

                        #'RSMS_13_1981_30_10m.tif',
                        #'RSMS_14_1981_30_10m.tif',
                        #'RSMS_15_1981_30_10m.tif',
                        #'RSMS_16_1981_30_10m.tif',

                        # 'TAMM_01_2017_01_10m.tif',
                        #'TAMM_02_2017_01_10m.tif',
                        #'TAMM_03_2017_01_10m.tif',
                        #'TAMM_04_2017_01_10m.tif',
                        #'TAMM_05_2017_01_10m.tif',
                        #'TAMM_06_2017_01_10m.tif',
                        #'TAMM_07_2017_01_10m.tif',
                        #'TAMM_08_2017_01_10m.tif',
                        #'TAMM_09_2017_01_10m.tif',
                        #'TAMM_10_2017_01_10m.tif',
                        #'TAMM_11_2017_01_10m.tif',
                        # 'TAMM_12_2017_01_10m.tif',

                        # 'TAMM_01_2018_01_10m.tif',
                        #'TAMM_02_2018_01_10m.tif',
                        #'TAMM_03_2018_01_10m.tif',
                        #'TAMM_04_2018_01_10m.tif',
                        #'TAMM_05_2018_01_10m.tif',
                        #'TAMM_06_2018_01_10m.tif',
                        #'TAMM_07_2018_01_10m.tif',
                        #'TAMM_08_2018_01_10m.tif',
                        #'TAMM_09_2018_01_10m.tif',
                        #'TAMM_10_2018_01_10m.tif',
                        #'TAMM_11_2018_01_10m.tif',
                        # 'TAMM_12_2018_01_10m.tif',

                        # 'rad_2017_01_10m.tif',
                        #'rad_2017_02_10m.tif', 'rad_2017_03_10m.tif', 'rad_2017_04_10m.tif',
                        #'rad_2017_05_10m.tif', 'rad_2017_06_10m.tif', 'rad_2017_07_10m.tif', 'rad_2017_08_10m.tif',
                        #'rad_2017_09_10m.tif', 'rad_2017_10_10m.tif', 'rad_2017_11_10m.tif',
                        # 'rad_2017_12_10m.tif',

                        # 'rad_2018_01_10m.tif',
                        # 'rad_2018_02_10m.tif', 'rad_2018_03_10m.tif', 'rad_2018_04_10m.tif',
                        # 'rad_2018_05_10m.tif', 'rad_2018_06_10m.tif', 'rad_2018_07_10m.tif', 'rad_2018_08_10m.tif',
                        # 'rad_2018_09_10m.tif', 'rad_2018_10_10m.tif', 'rad_2018_11_10m.tif',
                        # 'rad_2018_12_10m.tif',

                        #'grids_germany_monthly_soil_moist_201701_10m.tif',
                        #'grids_germany_monthly_soil_moist_201702_10m.tif',
                        #'grids_germany_monthly_soil_moist_201703_10m.tif',
                        #'grids_germany_monthly_soil_moist_201704_10m.tif',
                        #'grids_germany_monthly_soil_moist_201705_10m.tif',
                        #'grids_germany_monthly_soil_moist_201706_10m.tif',
                        #'grids_germany_monthly_soil_moist_201707_10m.tif',
                        #'grids_germany_monthly_soil_moist_201708_10m.tif',
                        #'grids_germany_monthly_soil_moist_201709_10m.tif',
                        #'grids_germany_monthly_soil_moist_201710_10m.tif',
                        #'grids_germany_monthly_soil_moist_201711_10m.tif',
                        #'grids_germany_monthly_soil_moist_201712_10m.tif',

                        #'grids_germany_monthly_soil_moist_201801_10m.tif',
                        #'grids_germany_monthly_soil_moist_201802_10m.tif',
                        #'grids_germany_monthly_soil_moist_201803_10m.tif',
                        #'grids_germany_monthly_soil_moist_201804_10m.tif',
                        #'grids_germany_monthly_soil_moist_201805_10m.tif',
                        #'grids_germany_monthly_soil_moist_201806_10m.tif',
                        #'grids_germany_monthly_soil_moist_201807_10m.tif',
                        #'grids_germany_monthly_soil_moist_201808_10m.tif',
                        #'grids_germany_monthly_soil_moist_201809_10m.tif',
                        #'grids_germany_monthly_soil_moist_201810_10m.tif',
                        #'grids_germany_monthly_soil_moist_201811_10m.tif',
                        #'grids_germany_monthly_soil_moist_201812_10m.tif',

                        ## monthly air temperature:
                        #'TAMM_2017_01_10m.tif', 'TAMM_2017_02_10m.tif', 'TAMM_2017_03_10m.tif', 'TAMM_2017_04_10m.tif', 'TAMM_2017_05_10m.tif', 'TAMM_2017_06_10m.tif',  'TAMM_2017_07_10m.tif','TAMM_2017_08_10m.tif', 'TAMM_2017_09_10m.tif', 'TAMM_2017_10_10m.tif', 'TAMM_2017_11_10m.tif', 'TAMM_2017_12_10m.tif',
                        #'TAMM_2018_01_10m.tif', 'TAMM_2018_02_10m.tif', 'TAMM_2018_03_10m.tif', 'TAMM_2018_04_10m.tif', 'TAMM_2018_05_10m.tif', 'TAMM_2018_06_10m.tif',  'TAMM_2018_07_10m.tif','TAMM_2018_08_10m.tif', 'TAMM_2018_09_10m.tif', 'TAMM_2018_10_10m.tif', 'TAMM_2018_11_10m.tif', 'TAMM_2018_12_10m.tif',
                        #'TAMM_2019_01_10m.tif', 'TAMM_2019_02_10m.tif', 'TAMM_2019_03_10m.tif', 'TAMM_2019_04_10m.tif', 'TAMM_2019_05_10m.tif', 'TAMM_2019_06_10m.tif', 'TAMM_2019_07_10m.tif','TAMM_2019_08_10m.tif', 'TAMM_2019_09_10m.tif', 'TAMM_2019_10_10m.tif', 'TAMM_2019_11_10m.tif', 'TAMM_2019_12_10m.tif',
                        ## monthly precipittion
                        #'RSMS_2017_01_10m.tif', 'RSMS_2017_02_10m.tif', 'RSMS_2017_03_10m.tif', 'RSMS_2017_04_10m.tif', 'RSMS_2017_05_10m.tif', 'RSMS_2017_06_10m.tif', 'RSMS_2017_07_10m.tif', 'RSMS_2017_08_10m.tif', 'RSMS_2017_09_10m.tif', 'RSMS_2017_10_10m.tif', 'RSMS_2017_11_10m.tif','RSMS_2017_12_10m.tif',
                        #'RSMS_2018_01_10m.tif', 'RSMS_2018_02_10m.tif', 'RSMS_2018_03_10m.tif', 'RSMS_2018_04_10m.tif', 'RSMS_2018_05_10m.tif', 'RSMS_2018_06_10m.tif', 'RSMS_2018_07_10m.tif', 'RSMS_2018_08_10m.tif', 'RSMS_2018_09_10m.tif', 'RSMS_2018_10_10m.tif', 'RSMS_2018_11_10m.tif', 'RSMS_2018_12_10m.tif',
                        #'RSMS_2019_01_10m.tif', 'RSMS_2019_02_10m.tif', 'RSMS_2019_03_10m.tif', 'RSMS_2019_04_10m.tif', 'RSMS_2019_05_10m.tif', 'RSMS_2019_06_10m.tif', 'RSMS_2019_07_10m.tif', 'RSMS_2019_08_10m.tif', 'RSMS_2019_09_10m.tif', 'RSMS_2019_10_10m.tif', 'RSMS_2019_11_10m.tif', 'RSMS_2019_12_10m.tif',

                        ## monthly soil moist
                        #'monthly_soil_moist_2017_01_10m.tif',
                        # 'monthly_soil_moist_2017_02_10m.tif', 'monthly_soil_moist_2017_03_10m.tif',
                        # 'monthly_soil_moist_2017_04_10m.tif', 'monthly_soil_moist_2017_05_10m.tif',
                        # 'monthly_soil_moist_2017_06_10m.tif', 'monthly_soil_moist_2017_07_10m.tif',
                        # 'monthly_soil_moist_2017_08_10m.tif', 'monthly_soil_moist_2017_09_10m.tif',
                        # 'monthly_soil_moist_2017_10_10m.tif', 'monthly_soil_moist_2017_11_10m.tif',
                        # 'monthly_soil_moist_2017_12_10m.tif', 'monthly_soil_moist_2018_01_10m.tif',
                        # 'monthly_soil_moist_2018_02_10m.tif', 'monthly_soil_moist_2018_03_10m.tif',
                        # 'monthly_soil_moist_2018_04_10m.tif', 'monthly_soil_moist_2018_05_10m.tif',
                        # 'monthly_soil_moist_2018_06_10m.tif', 'monthly_soil_moist_2018_07_10m.tif',
                        # 'monthly_soil_moist_2018_08_10m.tif', 'monthly_soil_moist_2018_09_10m.tif',
                        # 'monthly_soil_moist_2018_10_10m.tif', 'monthly_soil_moist_2018_11_10m.tif',
                        # 'monthly_soil_moist_2018_12_10m.tif', 'monthly_soil_moist_2019_01_10m.tif',
                        # 'monthly_soil_moist_2019_02_10m.tif', 'monthly_soil_moist_2019_03_10m.tif',
                        # 'monthly_soil_moist_2019_04_10m.tif', 'monthly_soil_moist_2019_05_10m.tif',
                        # 'monthly_soil_moist_2019_06_10m.tif', 'monthly_soil_moist_2019_07_10m.tif',
                        # 'monthly_soil_moist_2019_08_10m.tif', 'monthly_soil_moist_2019_09_10m.tif',
                        # 'monthly_soil_moist_2019_10_10m.tif', 'monthly_soil_moist_2019_11_10m.tif',
                        # 'monthly_soil_moist_2019_12_10m.tif'
                      #  ) #[:2]
        #for basename in basenames:
         #   raster = forceRaster(
          #      forceRasterPath=forceRasterPath,
           #     basename=basename,
            #    tilenames=tilenames,
             #   resolution=Resolution(20, 20),
              #  bandNameFunc=bandNameFunc,
               # debug=debug
            #)
           # rasters.append(raster)

    raster = RasterCollection.fromRasters(rasters=rasters, gridTol=1e-1).toBands()
    #print(raster.bandNames)

    # sample points
    #print('sample')
    print(tilename)
    return raster.sampleFeatures(filename=shapefile, debug=True)


if __name__ == '__main__':

    print("hallo")

    # old:
    #tilenames = ['X0065_Y0040', 'X0065_Y0041', 'X0066_Y0040', 'X0066_Y0041', 'X0066_Y0042', 'X0067_Y0040', 'X0067_Y0041',
    #             'X0067_Y0042', 'X0067_Y0043', 'X0067_Y0044', 'X0067_Y0045', 'X0068_Y0040', 'X0068_Y0041', 'X0068_Y0042',
    #             'X0068_Y0043', 'X0068_Y0044', 'X0068_Y0045', 'X0069_Y0040', 'X0069_Y0041', 'X0069_Y0042', 'X0069_Y0043',
    #             'X0069_Y0044', 'X0069_Y0045', 'X0069_Y0046', 'X0069_Y0047', 'X0070_Y0039', 'X0070_Y0040', 'X0070_Y0041',
    #             'X0070_Y0042', 'X0070_Y0043', 'X0070_Y0044', 'X0070_Y0045', 'X0070_Y0046', 'X0070_Y0047', 'X0071_Y0039',
    #             'X0071_Y0040', 'X0071_Y0041', 'X0071_Y0042', 'X0071_Y0043', 'X0071_Y0044', 'X0071_Y0045', 'X0071_Y0046',
    #             'X0071_Y0047', 'X0072_Y0040', 'X0072_Y0042', 'X0072_Y0043', 'X0072_Y0044', 'X0072_Y0045', 'X0072_Y0046',
    #             'X0072_Y0047', 'X0073_Y0044', 'X0073_Y0045', 'X0073_Y0046' ]#[4:7]

    # new:
    tilenames = ["X0065_Y0039", "X0065_Y0040", "X0065_Y0041", "X0066_Y0039", "X0066_Y0040",
     "X0066_Y0041", "X0066_Y0042", "X0067_Y0039", "X0067_Y0040", "X0067_Y0041", "X0067_Y0042",
     "X0067_Y0043", "X0067_Y0044", "X0067_Y0045", "X0068_Y0039", "X0068_Y0040", "X0068_Y0041",
     "X0068_Y0042", "X0068_Y0043", "X0068_Y0044", "X0068_Y0045", "X0069_Y0039", "X0069_Y0040",
     "X0069_Y0041", "X0069_Y0042", "X0069_Y0043", "X0069_Y0044", "X0069_Y0045", "X0069_Y0046",
     "X0069_Y0047", "X0070_Y0039", "X0070_Y0040", "X0070_Y0041", "X0070_Y0042", "X0070_Y0043",
     "X0070_Y0044", "X0070_Y0045", "X0070_Y0046", "X0070_Y0047", "X0071_Y0039", "X0071_Y0040",
     "X0071_Y0041", "X0071_Y0042", "X0071_Y0043", "X0071_Y0044", "X0071_Y0045", "X0071_Y0046",
     "X0071_Y0047", "X0072_Y0040", "X0072_Y0041", "X0072_Y0042", "X0072_Y0043", "X0072_Y0044",
     "X0072_Y0045", "X0072_Y0046", "X0073_Y0044", "X0073_Y0045", "X0073_Y0046" ]

    ## check reihenfolge
    # tilenames = [ 'X0069_Y0042', 'X0069_Y0043']

    ## Saxony:
    #tilenames = ['X0070_Y0050', 'X0071_Y0049', 'X0070_Y0048','X0070_Y0049']

    t0 = time.time()
    if 0:
        pool = Pool()
        result = pool.map(func=main, iterable=tilenames)
    else:
        result = list(map(main, tilenames))
        print(result)

    print("Hallo2")
    result = [r for r in result if r is not None]
    features = np.hstack([r[0] for r in result])
    labels = {k: np.hstack([r[1][k] for r in result]) for k in result[0][1].keys()}
    print(round(time.time() - t0), 'sec')

    #np.savetxt(r'\\141.20.140.91\NAS_Rodinia\Croptype\Sampling_Jan\2020-06-21_Brandenburg_nicht_bereinigt\features_20200526.txt', features.T, fmt='%i', delimiter=', ')
    np.savetxt(
        r'\\141.20.140.91\NAS_Rodinia\Croptype\BrandSat\04_Sampling\2020-08-21_Sampling_20m_Brandenburg\2020-08-21_20m_500n_100m.txt',
        features.T, fmt='%i', delimiter=', ')
    for name, label in labels.items():
        # np.savetxt(join(r'\\141.20.140.91\NAS_Rodinia\Croptype\Sampling_Jan\2020-06-21_Brandenburg_nicht_bereinigt', name + '20200526.txt'), label, fmt='%i', delimiter=', ')
        np.savetxt(join(r'\\141.20.140.91\NAS_Rodinia\Croptype\BrandSat\04_Sampling\2020-08-21_Sampling_20m_Brandenburg',
                        name + '2020-08-21_20m_500n_100m.txt'), label, fmt='%i', delimiter=', ')
    print('Done')
    pool.terminate()
print('Finished')
# 170 sec für 1 Band alle Tiles


## list all files
import os
path = 'U:/X0070_Y0049/'
files = [i for i in os.listdir(path) if os.path.isfile(os.path.join(path,i)) and \
         'monthly_soil_moist_' in i]

print(files)