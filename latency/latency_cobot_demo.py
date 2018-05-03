import os
import csv
import timeit

#Variables
#RPi
latency_rpi_csv = []
latency_rpi_avg = []
avg_rpi = 0
min_rpi = []
max_rpi = []
minLat_rpi = 1
maxLat_rpi = 0

#Server
latency_svr_avg = []
avg_svr = 0
min_svr = []
max_svr = []
minLat_svr = 1
maxLat_svr = 0

#Cobot
latency_cbt_avg = []
avg_cbt = 0
min_cbt = []
max_cbt = []
minLat_cbt = 1
maxLat_cbt = 0

#Latency end-to-end
latency_e2e = []
min_e2e = []
max_e2e = []

#Latency round-trip
latency_rt = []
min_rt = []
max_rt = []

def Latency(latency_rpi, latency_server, latency_cobot, timestamp, nb_frames, nb_cmd):
    global avg_rpi, avg_svr, avg_cbt
    global minLat_rpi, minLat_svr, minLat_cbt
    global maxLat_rpi, maxLat_svr, maxLat_cbt

    #CSV document
    w_file=open('test.csv', 'w')
    writeCSV = csv.writer(w_file, delimiter=';', lineterminator='\n')

    #Convertion of values in the latency_rpi into float
    #print("BEFORE_LATENCY OF RPi : {}".format(latency_rpi))
    #print("BEFORE_LATENCY OF RPi[1] : {}".format(latency_rpi[1]))
    for i in range(len(latency_rpi)):
        #d = latency_rpi[i].find("[")
        g = latency_rpi[i].find("]")

        if  g!=-1:
            latency_rpi[i] = latency_rpi[i][:g]

            latency_rpi[i] = latency_rpi[i].split(" ")
        
            for j in range(len(latency_rpi[i])):
                h = latency_rpi[i][j].find(",")
                if h!=-1:
                    latency_rpi[i][j] = latency_rpi[i][j][:h]
                    latency_rpi_csv.append(float(latency_rpi[i][j]))
                
                else:
                    latency_rpi_csv.append(float(latency_rpi[i][j]))

    #Add a fake value at the end of the latency_1_csv
    latency_rpi_csv.append(0.009)

    #print("AFTER_LATENCY OF RPi : {}\n".format(latency_rpi_csv))
    #print("NB FRAMES : {}\n".format(nb_frames))
    #print("LATENCY SERVER : {}\n".format(latency_server))

    #Average, Min and Max of the RPi
    s_1 = 0
    p = 0
    while s_1 <= nb_frames[p]:
        #Average
        avg_rpi += latency_rpi_csv[s_1]

        #RPi
        if (latency_rpi_csv[s_1] < minLat_rpi):
            minLat_rpi = latency_rpi_csv[s_1]
        if (latency_rpi_csv[s_1] > maxLat_rpi):
            maxLat_rpi = latency_rpi_csv[s_1]

        s_1 += 1

        if s_1 == nb_frames[p]:
            #RPi
            avg_rpi = avg_rpi/nb_frames[p]
            latency_rpi_avg.append(avg_rpi)
            min_rpi.append(minLat_rpi)
            max_rpi.append(maxLat_rpi)

            del latency_rpi_csv[:nb_frames[p]]
            #print("new latency_1_csv:{}\n"\
              #   "Its length : {}".format(latency_1_csv,len(latency_1_csv)))
            avg_rpi = 0
            minLat_rpi = 1
            maxLat_rpi = 0
            s_1 = 0
            p += 1

            if latency_rpi_csv == []: 
                break
    #Average, Min and Max of the server and the cobot
    s_2 = 0
    p = 0
    while s_2 <= nb_cmd[p]:
        #Average
        avg_svr += latency_server[s_2]
        avg_cbt += latency_cobot[s_2]

        #Server
        if (latency_server[s_2] < minLat_svr):
            minLat_svr = latency_server[s_2]
        if (latency_server[s_2] > maxLat_svr):
            maxLat_svr = latency_server[s_2]
        
        #Cobot
        if (latency_cobot[s_2] < minLat_cbt):
            minLat_cbt = latency_cobot[s_2]
        if (latency_cobot[s_2] > maxLat_cbt):
            maxLat_cbt = latency_cobot[s_2]

        s_2 += 1

        if s_2 == nb_cmd[p]:
            #Server
            avg_svr = avg_svr/nb_cmd[p]
            latency_svr_avg.append(avg_svr)
            min_svr.append(minLat_svr)
            max_svr.append(maxLat_svr)
        
            #Cobot
            avg_cbt = avg_cbt/nb_cmd[p]
            latency_cbt_avg.append(avg_cbt)
            min_cbt.append(minLat_cbt)
            max_cbt.append(maxLat_cbt)
        
            
            del latency_server[:nb_cmd[p]]
            del latency_cobot[:nb_cmd[p]]
            avg_svr, avg_cbt = 0,0
            minLat_svr, minLat_cbt = 1,1
            maxLat_svr, maxLat_cbt = 0,0
            s_2 = 0
            p += 1

            if len(nb_cmd) == p:
                break

    #print("LATENCY OF RPi AVG: {}\n".format(latency_rpi_avg))
    #print("LATENCY OF SERVER AVG: {}\n".format(latency_svr_avg))
    #print("LATENCY OF COBOT AVG: {}\n".format(latency_cbt_avg))
    #Latency e2e
    for n in range(len(latency_rpi_avg)):
        #Avg
        latency_e2e.append(latency_svr_avg[n] + (latency_rpi_avg[n] + latency_cbt_avg[n])/2)
        latency_rt.append(latency_svr_avg[n] + latency_rpi_avg[n] + latency_cbt_avg[n])
        #Min
        min_e2e.append(min_svr[n] + (min_rpi[n] + min_cbt[n])/2)
        min_rt.append(min_svr[n] + min_rpi[n] + min_cbt[n])
        #Max
        max_e2e.append(max_svr[n]+(max_rpi[n]+max_cbt[n])/2)
        max_rt.append(max_svr[n] + max_rpi[n] + max_cbt[n])

    os.chdir("C:\\Users\\PPU\\Desktop\\5GEM_2\\Cobot\\Programmes\\Codes Python_Magnus\\5GEM-image-robot-master_Python2_v3\\latency")
    writeCSV.writerow([["timestamp (s)", "Nb frames sent", \
                   "lat_rpi_avg (s)", "lat_rpi_min", "lat_rpi_max", \
                   "Nb commandes", \
                   "lat_svr_avg (s)", "lat_svr_min", "lat_svr_max",\
                   "lat_cbt_avg (s)", "lat_cbt_min", "lat_cbt_max", \
                   "lat_e2e_avg (s)", "lat_e2e_min", "lat_e2e_max", \
                   "lat_rt_avg (s)", "lat_rt_min", "lat_rt_max"]])

    for k in range(len(timestamp)):
        writeCSV.writerow([[str(timestamp[k])[:10], str(nb_frames[k]),\
                      str(latency_rpi_avg[k])[:10], str(min_rpi[k]), \
                      str(max_rpi[k])[:10], \
                      str(nb_cmd[k]), \
                      str(latency_svr_avg[k]), str(min_svr[k]), \
                      str(max_svr[k])[:10], \
                      str(latency_cbt_avg[k])[:10], str(min_cbt[k]), \
                      str(max_cbt[k])[:10], \
                      str(latency_e2e[k])[:10], str(min_e2e[k]), \
                      str(max_e2e[k])[:10], \
                      str(latency_rt[k])[:10], str(min_rt[k]), \
                      str(max_rt[k])[:10]]])
 
    w_file.close()
    del writeCSV
    del w_file