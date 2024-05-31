from geopy import distance

btf = (51.634253,12.317041)
lpz = (51.343732,12.380317)


print(distance.distance(btf, lpz).km)

from datetime import datetime
d0 = datetime.strptime("2022-05-30","%Y-%m-%d")
d1 = datetime.now()
delta = d1 - d0
print(delta.days)