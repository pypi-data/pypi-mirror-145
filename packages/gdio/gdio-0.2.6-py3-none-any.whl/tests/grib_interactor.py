from eccodes import *

path = '/home/rodrigo/anaconda3/envs/gdio/share/eccodes/samples/regular_ll_pl_grib2.tmpl'
path = '/home/rodrigo/projetos/gdio/tests/data/era5_20191226-27_lev.grib'
# path = '/home/rodrigo/data/wnd10m.01.2021030800.daily.grb2'
path = '/home/rodrigo/projetos/gdio/tests/test.grb2'

f = open(path, 'rb')

keys = [
    'Ni',
    'Nj',
    'latitudeOfFirstGridPointInDegrees',
    'longitudeOfFirstGridPointInDegrees',
    'latitudeOfLastGridPointInDegrees',
    'longitudeOfLastGridPointInDegrees',
    'paramId',
    'shortName',
    'cfVarName',
    'discipline',
    'parameterNumber',
    'parameterCategory',
    'significanceOfReferenceTime',
    'dataDate',
    'dataTime',
    'validityDate',
    'validityTime',
    'dataType'
]

while 1:
    gid = codes_grib_new_from_file(f)
    if gid is None:
        break

    for key in keys:
        try:
            print('  %s: %s' % (key, codes_get(gid, key)))
        except KeyValueNotFoundError as err:
            # Full list of exceptions here:
            #   https://confluence.ecmwf.int/display/ECC/Python+exception+classes
            print('  Key="%s" was not found: %s' % (key, err.msg))
        except CodesInternalError as err:
            print('Error with key="%s" : %s' % (key, err.msg))

    codes_release(gid)
    break



# while 1:
#     print()
#     gid = codes_grib_new_from_file(f)
#     if gid is None:
#         break
#     iterid = codes_keys_iterator_new(gid, 'ls')
#
#     # Different types of keys can be skipped
#     # codes_skip_computed(iterid)
#     # codes_skip_coded(iterid)
#     # codes_skip_edition_specific(iterid)
#     # codes_skip_duplicates(iterid)
#     # codes_skip_read_only(iterid)
#     # codes_skip_function(iterid)
#
#     while codes_keys_iterator_next(iterid):
#         keyname = codes_keys_iterator_get_name(iterid)
#         keyval = codes_get_string(gid, keyname)
#         print("%s = %s" % (keyname, keyval))
#
#     codes_keys_iterator_delete(iterid)
#     codes_release(gid)

# f.close()


