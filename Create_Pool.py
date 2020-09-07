from multiprocessing import Pool


def mp_worker(filename):
    with open(filename) as f:
        text = f.read()
    m = re.findall("x+", text)
    count = len(max(m, key=len))
    return filename, count

pool_file = open("U:/BrandSat/02_ParameterFiles/Katja_Level2_Koreg/S2_nd.pool")
pool_file = open("U:/BrandSat/02_ParameterFiles/Katja_Level2_Koreg/S2_2017.pool")
text = pool_file.read()
text
pool_file.Pool()
print(text)

i = 0
for file in text:
    i = i+ 1

## open list of files from Katja pool for footprint list
with open('U:/BrandSat/02_ParameterFiles/Katja_Level2_Koreg/S2_nd.pool') as f:
    mylist = list(f)

## ini empty list
foot_prints = []

# split into name parts, get footprint
for file in mylist:
    print(file)
    splitted = file.split("/")
    print(splitted)
    tt = splitted[6]
    foot_prints.append(tt)
    print(tt)

## get unique footprints
unique = list()

for foot in foot_prints:
    if foot not in unique:
        print(foot)
        unique.append(foot)

## get all scenes from 2017 in these folders
list_of_level1 = open("U:/BrandSat/02_ParameterFiles/list_all_level1.txt")
# test_level1 = list(list_of_level1)[1:100]
list_of_level1 = list(list_of_level1)

list_2017 = []
for file in list_of_level1:
    #print(file)

    if file.endswith('.SAFE\n'): #check for .SAFE
        print(file)
        splitted = file.split("/")
        print(splitted)

        footprint = splitted[1]
        if footprint in unique:
            print(file)
            print("hello")

            scene = splitted[2]
            splitted_scene = scene.split("_")
            date = splitted_scene[2]
            print(date)
            year = date[:4]
            print(year)

            if year == '2017':
                print("jo")

                this = '/data/Earth/edc/level1/sentinel2/' + file[2:-1]
                print(this)
                list_2017.append(this + " " + "QUEUED")
                #list_2017.append("QUEUED")
                #list_2017.append("\n,")

print(list_2017)
print(mylist)

with open('U:/BrandSat/02_ParameterFiles/S2_2017.pool', 'w') as f:
    for item in list_2017:
        f.write("%s\n" % item)

## test
pool_test = open('U:/BrandSat/02_ParameterFiles/S2_2017.pool')
pool_test = list(pool_test)

with open("U:/BrandSat/02_ParameterFiles/Katja_Level2_Koreg/S2_2017.pool") as f:
    mylist = list(f)


#----------------- change projection

import gdal
import osr

path = r"U:\BrandSat\03_Data_Level3\20200819_S2_20m\X0065_Y0041\2018-2020_001-365_HL_TSA_SEN2L_ARV_TSI.tif"
d = gdal.Open(path)
proj = osr.SpatialReference(wkt=d.GetProjection())

path = r"U:\BrandSat\05_FGK\01_Rasterize\Brandenburg_15m_18ts_bereinigt_2.tif"
d_2 = gdal.Open(path)
proj_2 = osr.SpatialReference(wkt=d_2.GetProjection())
d_2.SetSpatialReference(proj)
OGRErrSetLCC()

osr.ImportFromWkt(proj_2)
d.SetProjection(proj_2.ImportFromWkt())

inSRS_converter = osr.SpatialReference()  # makes an empty spatial ref object
inSRS_converter.ImportFromWkt(p)  # populates the spatial ref object with our WKT SRS
inSRS_forPyProj = proj_2.ExportToProj4()  # Exports an SRS ref as a Proj4 string


### compare S2_2017 in two level 2 folders

# K:\nd\level2\X0070_Y0045 ### katja
# K:\edc\level2\X0070_Y0045 ## other

tilenames = ['X0065_Y0040', 'X0065_Y0041', 'X0066_Y0040', 'X0066_Y0041', 'X0066_Y0042', 'X0067_Y0040', 'X0067_Y0041',
                 'X0067_Y0042', 'X0067_Y0043', 'X0067_Y0044', 'X0067_Y0045', 'X0068_Y0040', 'X0068_Y0041', 'X0068_Y0042',
                 'X0068_Y0043', 'X0068_Y0044', 'X0068_Y0045', 'X0069_Y0040', 'X0069_Y0041', 'X0069_Y0042', 'X0069_Y0043',
                 'X0069_Y0044', 'X0069_Y0045', 'X0069_Y0046', 'X0069_Y0047', 'X0070_Y0039', 'X0070_Y0040', 'X0070_Y0041',
                 'X0070_Y0042', 'X0070_Y0043', 'X0070_Y0044', 'X0070_Y0045', 'X0070_Y0046', 'X0070_Y0047', 'X0071_Y0039',
                 'X0071_Y0040', 'X0071_Y0041', 'X0071_Y0042', 'X0071_Y0043', 'X0071_Y0044', 'X0071_Y0045', 'X0071_Y0046',
                 'X0071_Y0047', 'X0072_Y0040', 'X0072_Y0042', 'X0072_Y0043', 'X0072_Y0044', 'X0072_Y0045', 'X0072_Y0046',
                  'X0073_Y0044', 'X0073_Y0045', 'X0073_Y0046'
                   ]
import glob


tilenames_t = os.listdir("K:/nd/level2/")

included_extensions = ['X']
    tilenames = [fn for fn in tilenames_t
                  if any(fn.startswith(ext) for ext in included_extensions)]

import os

list_nd_2017  = []
list_edc_2017 = []

for tile in tilenames:

    list_nd = []
    list_edc = []

    path_nd  = "K:/nd/level2/" + tile + "/"
    path_edc = "K:/edc/level2/" + tile + "/"

    included_extensions = ['BOA.tif']
    file_names_nd = [fn for fn in os.listdir(path_nd)
                  if any(fn.endswith(ext) for ext in included_extensions)]
    file_names_edc = [fn for fn in os.listdir(path_edc)
                     if any(fn.endswith(ext) for ext in included_extensions)]

    for file in file_names_nd:
        list_nd_2017.append(file)

    for file in file_names_edc:
        list_edc_2017.append(file)

    print(tile + " finished...")


nd_2017 = []
for scene in list_nd_2017:
    splitted = scene.split("_")
    print(splitted)

    date = splitted[0]
    year = date[:4]
    sensor = splitted[2]

    print(year, sensor)

    if year == '2017' and sensor == 'SEN2A' or year == '2017' and sensor == 'SEN2B':
            nd_2017.append(scene)

edc_2017 = []
for scene in list_edc_2017:
    splitted = scene.split("_")
    print(splitted)

    date = splitted[0]
    sensor = splitted[2]
    year = date[:4]

    print(year, sensor)

    if year == '2017' and sensor == 'SEN2A' or year == '2017' and sensor == 'SEN2B':
        edc_2017.append(scene)

## vergleichen
not_in = []
for scene in edc_2017:
    print(scene)
    if scene not in nd_2017:
          not_in.append(scene)

unique = []

for da in not_in:
    if da not in unique:
        print("ko")
        unique.append(da)

print(unique)