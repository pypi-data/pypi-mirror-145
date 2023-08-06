import csv

class create_csv:
    """
    Initiate create CSV project.
    Please Pass the required params"""
    def __init__(self, location,chunk_name, camera_list,chunk_name_list, keyid_list,rows,chunk_name_real_2):
        self.location = location
        self.chunk_name = chunk_name
        self.camera_list = camera_list
        self.chunk_name_list = chunk_name_list
        self.keyid_list = keyid_list
        self.rows = rows
        self.chunk_name_real_2 = chunk_name_real_2
    def create_csv(location,chunk_name, camera_list,chunk_name_list, keyid_list,rows,chunk_name_real_2):
        with open(location + "\\" + chunk_name + "_Camera Accuracy.csv","w",newline="") as fp:
            a = csv.writer(fp, delimiter=",")
            fields = ["Chunk Name", "Keyid","Camera Name","Longitude","Latitude","Altitude","Longitude Accuracy", "Latitude Accuracy","Altitude Accuracy"]
            a.writerow(fields)
            for i in range(len(camera_list)):
                chunk_selected = chunk_name_list[i]
                camera_selected = camera_list[i]
                keyid_csv = keyid_list[i]
                for r in rows:
                    camera_raw = r[0]
                    latitude_raw = r[2]
                    longitude_raw = r[3]
                    altitude_raw = r[4]
                    latitude_acc_raw = r[5]
                    longitude_acc_raw = r[6]
                    altitude_acc_raw = r[7]
                    chunk_raw = r[8]
                    if chunk_selected == chunk_raw and camera_selected == camera_raw:
                        a.writerow([chunk_name_real_2,keyid_csv,camera_raw,longitude_raw,latitude_raw,altitude_raw,longitude_acc_raw,latitude_acc_raw,altitude_acc_raw])

