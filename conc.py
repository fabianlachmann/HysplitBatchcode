import csv
import math
from tkinter import Tk
from tkinter.filedialog import askopenfilename


Dates = []
Coordinates = []

filename = askopenfilename()
newfile = askopenfilename()
#CANCER = 0
i=0




Runtime = -72
Height = 10
fromDate = [7,12,22]
toDate = [9,12,22]
numbrofP = 30000
heightoflevel = 500




with open(filename) as file:
    csv_reader = csv.reader(file,delimiter=",")
    for row in csv_reader:
        #CANCER =0
        if row == []:
            continue
        if row[0]=='Month' or row[0]=='Timecode':
            continue

        #print(i)
        #print(row)
        if (int(row[1])*10000+int(row[2])*100+int(row[3])>=fromDate[0]*10000+fromDate[1]*100+fromDate[2]) and (int(row[1])*10000+int(row[2])*100+int(row[3])<=toDate[0]*10000+toDate[1]*100+toDate[2]):
            Coordinates.append([row[26],row[27]])
            Dates.append([row[1],row[2],row[3]])
        i+=1

print(Coordinates)
print(Dates)






scriptfile = open(newfile,'w')


for k in range(len(Dates)):
    Month = Dates[k][0]
    Day = Dates[k][1]
    Hour = Dates[k][2]

    Lon = Coordinates[k][0]
    Lat = Coordinates[k][1]

    lines = []
    lines.append("SET SYR=" + str(20) + "\n")
    lines.append("SET SMO=" + Month + "\n")
    lines.append("SET SDA=" + Day + "\n")
    lines.append("SET SHR=" + Hour + "\n")

    lines.append("SET LAT=" + Lat + "\n")
    lines.append("SET LON=" + Lon + "\n")
    lines.append("SET LVL=" + str(Height)+'.0' + "\n")

    lines.append("SET RUN=" + str(Runtime) + "\n")
    lines.append("SET TOP=" + '10000.0' + "\n")

    lines.append("SET MET=" + r"D:\HYSPLIT\metereology files" + "\n")


    numbroffiles = 0


    # if int(Month)==7:
    #     numbroffiles = 1
    #     lines.append("SET DAT" + str(0) + "=" + "RP2020" + '0' + Month +".gbl" + "\n")
    # elif int(Month) == 8:
    #     numbroffiles =2
    #     lines.append("SET DAT" + str(0) + "=" + "RP2020" + '0' + str(int(Month)-1) +".gbl" + "\n")
    #     lines.append("SET DAT" + str(1) + "=" + "RP2020" + '0' + Month +".gbl" + "\n")
    # elif int(Month) == 9:
    #     numbroffiles = 2
    #     lines.append("SET DAT" + str(0) + "=" + "RP2020" + '0' + str(int(Month)-1) +".gbl" + "\n")
    #     lines.append("SET DAT" + str(1) + "=" + "RP2020" + '0' + Month +".gbl" + "\n")


    for i in range(5):
        numbroffiles+=1
        metDay = int(Day)-i+1
        metMonth = int(Month)


        if int(Month)==7:
            if metDay>31:
                metDay = metDay-31
                metMonth+=1

        elif int(Month)==8:
            if metDay<1:
                metDay = 31+metDay
                metMonth =+ -1
            elif metDay>31:
                metDay = metDay-31
                metMonth+=1


        elif int(Month) == 9:
            if metDay<1:
                metDay = 31+metDay
                metMonth =+ -1

        if metDay<10:
            metDay = '0'+str(metDay)

        lines.append("SET DAT" + str(i) + "=" + "2020" + '0' + str(metMonth) +str(metDay) + "_gfs0p25" + "\n")

    if int(Day) < 10:
        Day = '0'+Day
    if int(Hour) < 10:
        Hour = '0'+Hour

    lines.append("IF EXIST CONTROL DEL CONTROL \n")
    lines.append("echo %SYR% %SMO% %SDA% %SHR%  >CONTROL\n")
    lines.append("echo 1                       >>CONTROL\n")
    lines.append("echo %LAT% %LON% %LVL%       >>CONTROL\n")
    lines.append("echo %RUN%                   >>CONTROL\n")
    lines.append("echo 0                       >>CONTROL\n")
    lines.append("echo %TOP%                   >>CONTROL\n")
    lines.append("echo " + str(numbroffiles) + "                       >>CONTROL\n")
    for i in range(numbroffiles):
        lines.append("echo %MET%\                  >>CONTROL\n")
        lines.append("echo %DAT" + str(i) + "%                  >>CONTROL\n")

    lines.append("echo 1                      >>CONTROL\n")
    lines.append("echo TRAJ                   >>CONTROL\n")
    lines.append("echo " +str(numbrofP/3)+"                      >>CONTROL\n")
    lines.append("echo 3.0                    >>CONTROL\n")
    lines.append("echo 00 00 00 00 00         >>CONTROL\n")

    lines.append("echo 1                      >>CONTROL\n")
    lines.append("echo 0.0 0.0                >>CONTROL\n")
    lines.append("echo 0.1 0.1                >>CONTROL\n")
    lines.append("echo 60.0 60.0              >>CONTROL\n")

    lines.append("echo .\                     >>CONTROL\n")
    lines.append("echo " + 'cdump_' + Month + Day + Hour + "_" + str(numbrofP) + "_" + str(Runtime) + "                   >>CONTROL\n")
    lines.append("echo 1                      >>CONTROL\n")
    lines.append("echo "+str(heightoflevel)+"                      >>CONTROL\n")
    lines.append("echo 00 00 00 00            >>CONTROL\n")
    lines.append("echo 00 00 00 00            >>CONTROL\n")
    lines.append("echo 00 12 00               >>CONTROL\n")

    lines.append("echo 1                      >>CONTROL\n")
    lines.append("echo 0.0 0.0 0.0            >>CONTROL\n")
    lines.append("echo 0.0 0.0 0.0 0.0 0.0    >>CONTROL\n")
    lines.append("echo 0.0 0.0 0.0            >>CONTROL\n")
    lines.append("echo 0.0                    >>CONTROL\n")
    lines.append("echo 0.0                    >>CONTROL\n")


    lines.append("IF EXIST " + 'cdump_' + Month + Day + Hour + "_" + str(numbrofP) + "_" + str(Runtime) + " DEL " + 'cdump_' + Month + Day + Hour + "_" + str(numbrofP) + "_" + str(Runtime) + "\n")
    lines.append("%PGM%\exec\hycs_std\n")
    lines.append("timeout /t 10\n")
    lines.append("   \n")


    scriptfile.writelines(lines)



scriptfile.close()