from re import S
import traci
import time
import traci.constants as tc
import pytz
import datetime
from random import randrange
import pandas as pd


def getdatetime():
        utc_now = pytz.utc.localize(datetime.datetime.utcnow())
        currentDT = utc_now.astimezone(pytz.timezone("Asia/Singapore"))
        DATIME = currentDT.strftime("%Y-%m-%d %H:%M:%S")
        return DATIME

def flatten_list(_2d_list):
    flat_list = []
    for element in _2d_list:
        if type(element) is list:
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list

def car_count(vehicles, datetime):
    car_in_lane = dict()
    for i in range(0,len(vehicles)):
        lane = traci.vehicle.getLaneID(vehicles[i])

        if lane not in car_in_lane.keys():
            car_in_lane[lane] = 1
        else:
            car_in_lane[lane] = car_in_lane[lane] + 1
    print(datetime)
    # for i, j in car_in_lane.items():
    #     print(i, "have ",j , "car")
    return car_in_lane
sumoCmd = ["sumo-gui", "-c", "osm.sumocfg"]
traci.start(sumoCmd)
tfl_lane = { "J0": ["E3_0", "-E2_0", "-E1_0", "-E0_0"], "J5": ["-E5_0", "E4_0", "-E6_0", "-E7_0"] }
tfl_duration = { "J0": {"E3_0": 42, "-E2_0": 42, "-E1_0": 42, "-E0_0": 42}, "J5": {"-E5_0": 42, "E4_0": 42, "-E6_0": 42, "-E7_0": 42}}
tfl_phase = { "J0": {"E3_0": "GGGrrrrrrrrr", "-E0_0": "rrrGGGrrrrrr", "-E1_0": "rrrrrrGGGrrr", "-E2_0": "rrrrrrrrrGGG"}, 
              "J5": {"-E5_0": "GGGrrrrrrrrr", "-E7_0":"rrrGGGrrrrrr", "-E6_0": "rrrrrrGGGrrr", "E4_0": "rrrrrrrrrGGG"}}
packVehicleData = []
packTLSData = []
packBigData = []
t = 0
while traci.simulation.getMinExpectedNumber() > 0:
       
        traci.simulationStep();
        t+=1
        
        vehicles=traci.vehicle.getIDList();
        trafficlights=traci.trafficlight.getIDList();
        if t >= 300:
            print(getdatetime())
            car_in_lane = car_count(vehicles, getdatetime())
            for k in range(0,len(trafficlights)):
                print(trafficlights[k])
                s = 0
                for e in tfl_lane[trafficlights[k]]:
                    if e in car_in_lane.keys():
                        print(e, "have", car_in_lane[e])
                    else:
                        car_in_lane[e] = 0
                        print(e, "have", car_in_lane[e])
                    s+= car_in_lane[e]
                print("sum", s)
                if s != 0:
                    for e in tfl_lane[trafficlights[k]]:
                        p = car_in_lane[e] * 106 // s
                        tfl_duration[trafficlights[k]][e] = p + 3
                        print(e, "duration", tfl_duration[trafficlights[k]][e])
            t = 0
        if t == 0:
            traci.trafficlight.setPhaseDuration("J0", tfl_duration["J0"]["E3_0"])
            traci.trafficlight.setRedYellowGreenState("J0", tfl_phase["J0"]["E3_0"])
            traci.trafficlight.setPhaseDuration("J5", tfl_duration["J5"]["-E5_0"])
            traci.trafficlight.setRedYellowGreenState("J5", tfl_phase["J5"]["-E5_0"])

        
        if t == tfl_duration["J0"]["E3_0"] * 2:
            traci.trafficlight.setPhaseDuration("J0", 3)
            traci.trafficlight.setRedYellowGreenState("J0", "yyyrrrrrrrrr")
        if t  == (tfl_duration["J0"]["E3_0"] + 3) * 2:
            traci.trafficlight.setPhaseDuration("J0", tfl_duration["J0"]["-E2_0"])
            traci.trafficlight.setRedYellowGreenState("J0", tfl_phase["J0"]["-E2_0"])
        if t == (tfl_duration["J0"]["E3_0"] + 3 + tfl_duration["J0"]["-E2_0"]) * 2:
            traci.trafficlight.setPhaseDuration("J0", 3)
            traci.trafficlight.setRedYellowGreenState("J0", "rrryyyrrrrrr")
        if t == (tfl_duration["J0"]["E3_0"] + 3 + tfl_duration["J0"]["-E2_0"] + 3) * 2:
            traci.trafficlight.setPhaseDuration("J0", tfl_duration["J0"]["-E1_0"])
            traci.trafficlight.setRedYellowGreenState("J0", tfl_phase["J0"]["-E1_0"])
        if t == (tfl_duration["J0"]["E3_0"] + 3 + tfl_duration["J0"]["-E2_0"] + 3 + tfl_duration["J0"]["-E1_0"]) * 2:
            traci.trafficlight.setPhaseDuration("J0", 3)
            traci.trafficlight.setRedYellowGreenState("J0", "rrrrrryyyrrr")     
        if t == (tfl_duration["J0"]["E3_0"] + 3 + tfl_duration["J0"]["-E2_0"] + 3 + tfl_duration["J0"]["-E1_0"] + 3) * 2:
            traci.trafficlight.setPhaseDuration("J0", tfl_duration["J0"]["-E0_0"])
            traci.trafficlight.setRedYellowGreenState("J0", tfl_phase["J0"]["-E0_0"])
        if t == (tfl_duration["J0"]["E3_0"] + 3 + tfl_duration["J0"]["-E2_0"] + 3 + tfl_duration["J0"]["-E1_0"] + 3 + tfl_duration["J0"]["-E0_0"])*2:
            traci.trafficlight.setPhaseDuration("J0", 3)
            traci.trafficlight.setRedYellowGreenState("J0", "rrrrrrrrryyy")
        if t == (tfl_duration["J0"]["E3_0"] + 3 + tfl_duration["J0"]["-E2_0"] + 3 + tfl_duration["J0"]["-E1_0"] + 3 + tfl_duration["J0"]["-E0_0"] + 3)*2:
            traci.trafficlight.setPhaseDuration("J0", tfl_duration["J0"]["E3_0"])
            traci.trafficlight.setRedYellowGreenState("J0", tfl_phase["J0"]["E3_0"])

        if t == (tfl_duration["J5"]["-E5_0"])*2:
            traci.trafficlight.setPhaseDuration("J5", 3)
            traci.trafficlight.setRedYellowGreenState("J5", "yyyrrrrrrrrr")
        if t == (tfl_duration["J5"]["-E5_0"] + 3)*2:
            traci.trafficlight.setPhaseDuration("J5", tfl_duration["J5"]["E4_0"])
            traci.trafficlight.setRedYellowGreenState("J5", tfl_phase["J5"]["E4_0"])
        if t == (tfl_duration["J5"]["-E5_0"] + 3 + tfl_duration["J5"]["E4_0"])*2:
            traci.trafficlight.setPhaseDuration("J5", 3)
            traci.trafficlight.setRedYellowGreenState("J5", "rrryyyrrrrrr")
        if t == (tfl_duration["J5"]["-E5_0"] + 3 + tfl_duration["J5"]["E4_0"] + 3)*2:
            traci.trafficlight.setPhaseDuration("J5", tfl_duration["J5"]["-E6_0"])
            traci.trafficlight.setRedYellowGreenState("J5", tfl_phase["J5"]["-E6_0"])
        if t == (tfl_duration["J5"]["-E5_0"] + 3 + tfl_duration["J5"]["E4_0"] + 3 + tfl_duration["J5"]["-E6_0"])*2:
            traci.trafficlight.setPhaseDuration("J5", 3)
            traci.trafficlight.setRedYellowGreenState("J5", "rrrrrryyyrrr")     
        if t == (tfl_duration["J5"]["-E5_0"] + 3 + tfl_duration["J5"]["E4_0"] + 3 + tfl_duration["J5"]["-E6_0"] + 3)*2:
            traci.trafficlight.setPhaseDuration("J5", tfl_duration["J5"]["-E7_0"])
            traci.trafficlight.setRedYellowGreenState("J5", tfl_phase["J5"]["-E7_0"])
        if t == (tfl_duration["J5"]["-E5_0"] + 3 + tfl_duration["J5"]["E4_0"] + 3 + tfl_duration["J5"]["-E6_0"] + 3 + tfl_duration["J5"]["-E7_0"])*2:
            traci.trafficlight.setPhaseDuration("J5", 3)
            traci.trafficlight.setRedYellowGreenState("J5", "rrrrrrrrryyy")
        if t == (tfl_duration["J5"]["-E5_0"] + 3 + tfl_duration["J5"]["E4_0"] + 3 + tfl_duration["J5"]["-E6_0"] + 3 + tfl_duration["J5"]["-E7_0"] + 3)*2:
            traci.trafficlight.setPhaseDuration("J5", tfl_duration["J5"]["-E5_0"])
            traci.trafficlight.setRedYellowGreenState("J5", tfl_phase["J5"]["-E5_0"])
         
            print(car_in_lane)
        car_count(vehicles, getdatetime())
        for i in range(0,len(vehicles)):

                #Function descriptions
                #https://sumo.dlr.de/docs/TraCI/Vehicle_Value_Retrieval.html
                #https://sumo.dlr.de/pydoc/traci._vehicle.html#VehicleDomain-getSpeed
                vehid = vehicles[i]
                x, y = traci.vehicle.getPosition(vehicles[i])
                coord = [x, y]
                lon, lat = traci.simulation.convertGeo(x, y)
                gpscoord = [lon, lat]
                spd = round(traci.vehicle.getSpeed(vehicles[i])*3.6,2)
                edge = traci.vehicle.getRoadID(vehicles[i])
                lane = traci.vehicle.getLaneID(vehicles[i])
                displacement = round(traci.vehicle.getDistance(vehicles[i]),2)
                turnAngle = round(traci.vehicle.getAngle(vehicles[i]),2)
                nextTLS = traci.vehicle.getNextTLS(vehicles[i])

                #Packing of all the data for export to CSV/XLSX
                vehList = [getdatetime(), vehid, coord, gpscoord, spd, edge, lane, displacement, turnAngle, nextTLS]
                
                
                idd = traci.vehicle.getLaneID(vehicles[i])

                tlsList = []
        
                  
                #Pack Simulated Data
                packBigDataLine = flatten_list([vehList, tlsList])
                packBigData.append(packBigDataLine)


                ##----------MACHINE LEARNING CODES/FUNCTIONS HERE----------##


                ##---------------------------------------------------------------##


                ##----------CONTROL Vehicles and Traffic Lights----------##

                #***SET FUNCTION FOR VEHICLES***
                #REF: https://sumo.dlr.de/docs/TraCI/Change_Vehicle_State.html
               

                #***SET FUNCTION FOR TRAFFIC LIGHTS***
                #REF: https://sumo.dlr.de/docs/TraCI/Change_Traffic_Lights_State.html
                # tfl1 = "J0"
                # traci.trafficlight.setPhaseDuration(tfl1, 10)
                # trafficsignal = ["rrrrrrGGGGgGGGrr", "rrrrrGGGGGGrrrrr", "GrrrrrrrrrrGGGGg"]
                # traci.trafficlight.setRedYellowGreenState(tfl1, trafficsignal[randrange(3)])

                ##------------------------------------------------------##

traci.close()

#Generate Excel file
columnnames = ['dateandtime', 'vehid', 'coord', 'gpscoord', 'spd', 'edge', 'lane', 'displacement', 'turnAngle', 'nextTLS', \
                       'tflight', 'tl_state', 'tl_phase_duration', 'tl_lanes_controlled', 'tl_program', 'tl_next_switch']
dataset = pd.DataFrame(packBigData, index=None, columns=columnnames)
dataset.to_excel("output.xlsx", index=False)
time.sleep(5)








