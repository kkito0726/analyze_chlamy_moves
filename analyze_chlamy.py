import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.signal import find_peaks
# from matplotlib import cm

def read_data(spot_csv, track_csv, frame=601):
    spot = pd.read_csv(spot_csv, encoding="shift-jis")
    track = pd.read_csv(track_csv, encoding="shift-jis")
    spots = spot.iloc[3:,2:].astype(float)
    tracks = track.iloc[3:,1:].astype(float)
    
    #frameと一致するtrackを抽出
    tracks_frame = tracks[tracks.NUMBER_SPOTS == frame]
    #track_frameのTRACK_IDを抽出
    tracks_TRACK_ID = tracks_frame["TRACK_ID"]
    #tracksTRACK_IDに当てはまるspotsを抽出
    spots_ID = spots[spots["TRACK_ID"].isin(tracks_TRACK_ID)]
    #spots_IDをTRACK_ID→POSITION_Tの優先順位で並び変え
    data = spots_ID.sort_values(['TRACK_ID', 'POSITION_T'])
    
    return data

def draw_moves(data, movie_height=841.59, threshold=230, dpi=300):
    id = np.unique(data["TRACK_ID"].values)  
    '''
    TRACK_IDが同じものごとにグループ化
    [
        [TRACK_ID = 0 のデータ],
        [TRACK_ID = 1 のデータ],
        [TRACK_ID = 2 のデータ],
        .
        .
        .
    ]
    '''
    x_list = [data[data["TRACK_ID"] == i]["POSITION_X"].values for i in id]
    y_list = [data[data["TRACK_ID"] == i]["POSITION_Y"].values for i in id]
    
    plt.figure(dpi=dpi)
    for i in range(len(x_list)):
        x_diff = np.diff(x_list[i])
        y_diff = np.diff(y_list[i])
        # 移動距離の合計を算出
        move_sum = np.sqrt(x_diff**2 + y_diff**2).sum()
        
        if move_sum > threshold:
            z = range(len(x_list[i]))
            mp = plt.scatter(x_list[i], movie_height - y_list[i], c=z, s=0.1)
            plt.xlabel("X (μm)")
            plt.ylabel("Y (μm)")
            plt.xlim(0,1200)
            plt.ylim(0,1200)
    plt.show()
    
    
if __name__ == '__main__':
    spot_csv = "./spot_1-601.csv"
    track_csv = "./track_1-601.csv"
    
    data = read_data(spot_csv, track_csv)
    
    draw_moves(data)