import numpy as np
import pyproj
# import matplotlib.pyplot as plt
import itertools

# np.set_printoptions(precision=1)

nx = 111
ny = 101

lon1 = 300
lon2 = 330
lat1 = -30
lat2 = 0

projparams = {}
projparams['a'] = 6371229.0
projparams['b'] = 6371229.0

# regular
projparams['proj'] = 'cyl'
projparams['proj'] = 'merc'
# projparams['proj'] = 'lcc'


print("@:", projparams['proj'])


if projparams['proj'] in ['merc']:

    # mercator
    projparams['lat_ts'] = 0
    projparams['lon_0'] = 0.5 * (lon1 + lon2)
    pj = pyproj.Proj(projparams)
    llcrnrx, llcrnry = pj(lon1, lat1)
    urcrnrx, urcrnry = pj(lon2, lat2)
    dx = (urcrnrx - llcrnrx) / (nx - 1)
    dy = (urcrnry - llcrnry) / (ny - 1)
    x = llcrnrx + dx * np.arange(nx)
    y = llcrnry + dy * np.arange(ny)

elif projparams['proj'] in ['lcc']:

    # lambert
    projparams['lon_0'] = lon1+(lon2-lon1)/2 # LoVInDegrees
    projparams['lat_0'] = lat1+(lat2-lat1)/2 # LaDInDegrees
    projparams['lat_1'] = lat1+(lat2-lat1)/3 # Latin1InDegrees
    projparams['lat_2'] = lat2-(lat2-lat1)/3 # Latin2InDegrees
    dx = 50000 # DxInMetres
    dy = 50000 # DyInMetres
    pj = pyproj.Proj(projparams)
    llcrnrx, llcrnry = pj(lon1, lat1)
    x = llcrnrx + dx * np.arange(nx)
    y = llcrnry + dy * np.arange(ny)

elif projparams['proj'] in ['cyl']:
    dx = (lon2 - lon1) / (nx - 1)
    dy = (lat2 - lat1) / (ny - 1)

    y = np.arange(lat1, lat2, dy)
    x = np.arange(lon1, lon2, dx)




if projparams['proj'] not in ['cyl']:
    x, y = np.meshgrid(x, y)
    lons, lats = pj(x, y, inverse=True)
else:
    lons, lats = np.meshgrid(x, y)



d2lon = np.diff(lons, n=2, axis=1)
d2lat = np.diff(lats, n=2, axis=0)



np.set_printoptions(precision=3)
print("dlon",np.max(d2lon), lons[0,::10], d2lon[0,::10])
print(np.isclose(d2lon, 0.0).all())

print("dlat", np.max(d2lat), lats[::10,0],d2lat[::10,0])
print(np.isclose(d2lat, 0.0).all())


def argmin(data):
    _min = data[0, 0]
    x = 0
    y = 0

    for j in range(data.shape[1]):
        for i in range(data.shape[0]):
            if data[i, j] < _min:
                _min = data[i, j]
                x = i
                y = j

    return x, y, _min



def near_yx0(data, lats=None, lons=None):
    '''
    Find the nearst coordinate i/j given a lat/lon coordinate
    Warning error with lat/lon parameter with dims>1, only works with
    mercator, regular lat-lon
    :param lat:     float
                    latitude
    :param lon:     float
                    longitude
    :return:        float tuple lat, lon
                    nearest grid point y/x
    '''

    lats = lats if isinstance(lats, list) else [lats]
    lons = lons if isinstance(lons, list) else [lons]

    lons = [(_lo + 360) % 360 if not _lo is None else _lo for _lo in lons]

    x = []
    y = []

    if 'lat' in data.keys() or \
            'lon' in data.keys():

        _lat = data['lat']
        _lon = data['lon']

    elif 'latitude' in data.keys() or \
            'longitude' in data.keys():

        _lat = data['latitude']
        _lon = data['longitude']

    # convert -180,180 to 0,360 format
    _lon = (_lon + 360) % 360

    for lat, lon in itertools.zip_longest(lats, lons):

        _y = None
        _x = None

        if not lat is None:
            if np.min(_lat) <= lat and np.max(_lat) >= lat:
                _y = np.nanargmin(np.abs(_lat - lat)) if lat is not None else lat


        if not lon is None:
            if np.min(_lon) <= lon and np.max(_lon) >= lon:
                _x = np.nanargmin(np.abs(_lon - lon)) if lon is not None else lon

        x.append(_x)
        y.append(_y)

    return y, x

def near_yx(data, lats=None, lons=None):
    '''
    Find the nearst coordinate i/j given a lat/lon coordinate
    Warning error with lat/lon parameter with dims>1, only works with
    mercator, regular lat-lon
    :param data:    dict
                    latitude and longitude mesh data
    :param lat:     float
                    latitude
    :param lon:     float
                    longitude
    :return:        float tuple lat, lon
                    nearest grid point y/x
    '''

    lats = lats if isinstance(lats, list) else [lats]
    lons = lons if isinstance(lons, list) else [lons]

    lons = [(_lo + 360) % 360 if not _lo is None else _lo for _lo in lons]

    x = []
    y = []

    _lat = data['latitude']
    _lon = data['longitude']
    print(_lat.shape, _lon.shape)
    if _lat.ndim == 1 or _lon.ndim == 1:
        dims = (_lon.size, _lat.size)

        _lat = np.tile(_lat, (dims[0], 1)).T
        _lon = np.tile(_lon, (dims[1], 1))
    print(_lat.shape, _lon.shape)

    cut_domain_roll = -10

    # convert -180,180 to 0,360 format
    _lon = (_lon + 360) % 360

    for lat, lon in itertools.zip_longest(lats, lons):

        _x = np.zeros(_lon.shape)
        _y = np.zeros(_lat.shape)

        if not lat is None:
            if np.min(_lat) <= lat and np.max(_lat) >= lat:
                _y = np.abs(_lat - lat)
            else:
                lat = None

        if not lon is None:
            if np.min(_lon) <= lon and np.max(_lon) >= lon:
                _x = np.abs(_lon - lon)
            else:
                lon = None


        xy_min = np.nanargmin((_y + _x))

        #convert the 1D index to 2D index system
        lat_index = xy_min // _lon.shape[1]
        lon_index = xy_min - (lat_index * _lon.shape[1])

        lat_index = None if lat is None else lat_index
        lon_index = None if lon is None else lon_index

        # print(lat, lon)
        x.append(lon_index)
        y.append(lat_index)


        # np.set_printoptions(precision=0)
        # print("!", _x[::10, ::10])
        # print("!", _y[::10, ::10])
        # print("!!", (_y + _x)[::10,::10],(_y + _x).flatten()[xy_min],(_y + _x)[lat_index,lon_index],(_y + _x).shape )
        #
        # print("!!!", xy_min, lat_index, lon_index, argmin((_y + _x)))

    return y, x

# print("lon",lons[0,::10])
# print("lat",lats[::10,0])





# lat1, lon1, lat2, lon2 = (-10, 280, 5, 290)
# x = near_yx({'latitude': lats[:,0], 'longitude': lons[0,:]}, lats=[0,10], lons=[290,300])
# print(x)
# x = near_yx0({'latitude': lats[:, 0], 'longitude': lons[0,:]}, lats=[0,10], lons=[290,300])
# print(x)

# for j in range(0,lats.shape[0],10):
#     row = str()
#     for i in range(0,lats.shape[1],10):
#         row += f'{lats[j,i]: 04.0f},{(lons[j,i] + 360) % 360:04.0f} '
#     print(row)


# plt.plot(dlon, label="dlon")
# plt.plot(dlat, label="dlat")
#
# plt.legend(loc="upper left")
# plt.show()


