#import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# timelist = pd.read_csv("timedelay.csv",index_col="task")
# timelist = timelist.to_numpy()
# energylist = pd.read_csv("energycost.csv",index_col="task")
# energylist = energylist.to_numpy()
# offlist = pd.read_csv("offloadingcost.csv",index_col="task")
# offlist = offlist.to_numpy()
# t = timelist[:,0]

# mix = np.ones((len(timelist[:,1]),4), dtype=float)
# for i in range(len(timelist[:,1])):
#     for j in range(4):
#         mix[i,j] = pow(3,2)/4*(timelist[i,j+1]*energylist[i,j+1]
#                                   +timelist[i,j+1]*offlist[i,j+1]
#                                   +energylist[i,j+1]*offlist[i,j+1])/1000000


ePow_a = [31.07, 34.24, 39.34, 42.49, 45.95, 49.37, 51.70, 53.66, 56.12, 58.86, 61.44, 63.04, 65.80, 67.10, 68.00, 69.04, 69.71, 71.11, 72.22, 72.58, 73.44, 74.03, 74.34, 75.35, 75.95, 76.67, 76.73, 77.14, 77.72, 77.76, 78.53, 78.68, 78.64, 78.86, 79.41, 79.99, 79.93, 79.98, 79.85, 80.88, 81.37, 81.39, 81.26, 81.60, 81.59, 82.01, 81.72, 82.33, 82.43, 82.54, ]
ePow_t = [12.28, 24.36, 35.96, 47.71, 60.35, 72.23, 84.72, 96.90, 109.29, 121.14, 132.95, 144.90, 156.62, 168.11, 179.70, 191.52, 203.69, 215.60, 227.39, 239.18, 251.09, 263.26, 275.37, 287.40, 298.87, 310.63, 322.51, 334.40, 347.29, 358.81, 370.49, 382.71, 394.38, 406.18, 417.85, 429.98, 442.10, 453.57, 464.76, 476.59, 488.81, 500.48, 512.19, 524.00, 535.32, 546.78, 558.06, 569.83, 581.02, 592.85, ]
ePow_e = [0.83, 1.91, 2.83, 4.04, 5.24, 6.54, 8.73, 10.72, 12.46, 13.82, 15.87, 17.96, 19.88, 21.74, 23.63, 25.62, 27.77, 29.92, 31.85, 33.75, 35.77, 37.87, 40.21, 42.20, 43.83, 45.70, 47.50, 49.35, 51.97, 54.72, 57.31, 59.58, 61.86, 64.15, 66.42, 68.24, 70.04, 71.60, 73.24, 75.09, 76.72, 78.23, 80.17, 82.19, 84.06, 85.61, 87.07, 88.50, 90.03, 91.51, ]

Pow_a = [40.42, 43.10, 48.59, 52.07, 54.56, 56.62, 58.31, 59.83, 61.54, 63.21, 64.36, 65.64, 66.84, 67.28, 68.36, 69.05, 69.45, 69.96, 70.48, 71.12, 71.32, 71.91, 72.31, 72.70, 73.34, 73.38, 73.62, 73.93, 74.21, 74.36, 74.14, 74.48, 74.29, 74.65, 75.03, 75.35, 75.07, 75.26, 75.01, 75.51, 75.79, 76.19, 76.18, 76.08, 76.01, 76.22, 76.43, 76.36, 76.33, 76.74, ]
Pow_t = [12.76, 26.50, 42.04, 56.15, 71.03, 85.21, 99.48, 117.35, 134.47, 148.85, 162.67, 177.68, 191.93, 207.47, 221.94, 236.77, 252.60, 267.94, 282.36, 297.16, 314.21, 329.60, 344.65, 359.15, 374.27, 388.90, 403.34, 418.58, 432.81, 447.23, 463.21, 477.24, 498.30, 512.64, 528.03, 542.29, 556.42, 570.71, 584.64, 600.98, 617.16, 633.81, 648.55, 662.86, 677.09, 691.08, 706.49, 723.75, 737.98, 753.38, ]
Pow_e = [7.10, 8.40, 26.36, 27.88, 32.11, 34.26, 36.71, 71.66, 100.23, 102.16, 103.53, 111.48, 112.64, 122.36, 124.86, 130.54, 145.20, 153.46, 156.22, 160.39, 183.97, 195.60, 203.18, 207.51, 215.32, 218.46, 222.94, 229.28, 230.88, 233.09, 250.64, 251.83, 318.76, 321.85, 333.74, 336.62, 338.04, 341.16, 342.40, 360.62, 379.01, 403.34, 409.24, 414.50, 416.04, 418.13, 425.69, 455.45, 456.98, 469.54, ]

fig1 = plt.figure()
#plt.title('Timecost')
plt.xlabel('Time in seconds')
plt.ylabel('accuracy of testing')
plt.plot(ePow_t, ePow_a, marker='o', ms=5)
plt.plot(Pow_t, Pow_a, marker='^', ms=5)
# plt.plot(t, timelist[:,3], marker='s', ms=5)
# plt.plot(t, timelist[:,4], marker='d', ms=5)
plt.grid()
plt.legend(['ePow','Pow'])#,'DDG','NSGA3'])
plt.savefig('timedelay.jpg',bbox_inches='tight',
            dpi=300,pad_inches=0.02)
'''
fig2 = plt.figure()
plt.xlabel('Time slot')
plt.ylabel('Total energy consumption')
plt.plot(t, energylist[:,1], marker='o', ms=5)
plt.plot(t, energylist[:,2], marker='^', ms=5)
plt.plot(t, energylist[:,3], marker='s', ms=5)
plt.plot(t, energylist[:,4], marker='d', ms=5)
plt.legend(['CTAEA','MOEAD','DDG','NSGA3'])
plt.savefig('energycost.jpg',bbox_inches='tight',
            dpi=300,pad_inches=0.02)
fig3 = plt.figure()
plt.xlabel('Time slot')
plt.ylabel('Total offloading consumption')
plt.plot(t, offlist[:,1], marker='o', ms=5)
plt.plot(t, offlist[:,2], marker='^', ms=5)
plt.plot(t, offlist[:,3], marker='s', ms=5)
plt.plot(t, offlist[:,4], marker='d', ms=5)
plt.legend(['CTAEA','MOEAD','DDG','NSGA3'])
plt.savefig('offloadingcost.jpg',bbox_inches='tight',
            dpi=300,pad_inches=0.02)

fig4 = plt.figure()
#plt.title('Timecost')
plt.xlabel('Time slot')
plt.ylabel('Radar chart area with 3 element')
plt.plot(t, mix[:,0], marker='o', ms=5)
plt.plot(t, mix[:,1], marker='^', ms=5)
plt.plot(t, mix[:,2], marker='s', ms=5)
plt.plot(t, mix[:,3], marker='d', ms=5)
plt.legend(['CTAEA','MOEAD','DDG','NSGA3'])#RVEA->DDG
plt.savefig('3mix.jpg',bbox_inches='tight',
            dpi=300,pad_inches=0.02)
'''
            