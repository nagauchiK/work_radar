import struct
import glob
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import math
import numpy as np


#path = 'all/20190317000625_1ST.dat'
#path = 'all/20190317000805_1ST.dat'
#path = 'all/20190317000822_1ST.dat'
#path = 'all/20190317001001_1ST.dat'
#path = 'all/20190317001017_1ST.dat'
#path = 'all/20190317001158_1ST.dat'
#path = 'radar10/20171101095833_1ST.dat'
#path = 'radar5/20171107000108_1ST.dat'
short = []
long = []
#paths = glob.glob('radar5/2017110722????_1ST.dat')
paths = glob.glob('radar10/20171104??????_1ST.dat')
#paths = glob.glob('radar5/*.dat')
all_data = []
for path in paths:
    with open(path, 'rb') as f:

        """
        bytes = f.read(40)
        
        obs = bytes[0]     #観測データ
        ang = bytes[3:4]    #設定角度
        day = bytes[5]     #日
        mon = bytes[6]     #月
        yea = bytes[7:8]     #年
        sec = bytes[9]     #秒
        min = bytes[10]    #分
        hou = bytes[11]     #時
        
        print('{:x}'.format(bytes[3]))
        print(bytes[4])
        print(bytes[3:4])
        print('{:b}'.format(10010101))
        """
        
        obs = struct.unpack('h',f.read(2))[0]     #観測データ
        ang = struct.unpack('h',f.read(2))[0]*(360/65536)     #設定角度
        day = str(struct.unpack('b',f.read(1))[0])     #日
        mon = str(struct.unpack('b',f.read(1))[0])     #月
        yea = str(struct.unpack('h',f.read(2))[0])     #年
        sec = str(struct.unpack('b',f.read(1))[0])     #秒
        min = str(struct.unpack('b',f.read(1))[0])     #分
        hou = str(struct.unpack('h',f.read(2))[0])     #時
        
        azi = struct.unpack('H',f.read(2))[0]*(360/65536)     #方位角

        rpm = struct.unpack('h',f.read(2))[0]     #RPM
        
        start_ang = struct.unpack('H',f.read(2))[0]*(360/65536)   #開始仰角
        end_ang =   struct.unpack('H',f.read(2))[0]*(360/65536)   #終了仰角
        
        stg_prf1 = struct.unpack('h',f.read(2))[0]    #スタガ+PRF1
        prf2 = struct.unpack('h',f.read(2))[0]        #PRF2
        FFT_point_1 = struct.unpack('h',f.read(2))[0] #FFTポイント(PRF1)
        FFT_point_2 = struct.unpack('h',f.read(2))[0] #FFTポイント(PRF2)
        
        sector = struct.unpack('h',f.read(2))[0]      #セクタ数
        sweep = struct.unpack('h',f.read(2))[0]       #保存スイープデータ数
        
        short_ppr = struct.unpack('h',f.read(2))[0]   #短パルス処理レンジ
        long_ppr = struct.unpack('h',f.read(2))[0]    #長パルス処理レンジ
        reserve = struct.unpack('i',f.read(4))[0]     #予備
        
        print(f'観測データ:{obs} 設定角度:{ang}  {yea}-{mon}-{day} {hou}:{min}:{sec}')
        #print(f'方位角:{azi}  rpm:{rpm}')
        #print(f'スタートアングル:{start_ang},エンドアングル:{end_ang}')
        #print(f'スタガ+PRF1:{stg_prf1} PRF2:{prf2}')
        #print(f'FFTポイント(PRF1):{FFT_point_1} FFTポイント(PRF2):{FFT_point_2}')
        print(f'セクタ数:{sector}\n保存スイープデータ数:{sweep}\n短パルス処理レンジ:{short_ppr} \n長パルス処理レンジ:{long_ppr}')
        #print(f'観測データ:{obs} 方位角:{azi*(360/65536)} スタートアングル:{start_ang*(360/65536)},エンドアングル:{end_ang*(360/65536)} {yea}-{mon}-{day} {hou}:{min}:{sec}')
        header = {'observation_data':obs, 'setting_angle':ang, 'date':yea+'-'+mon+'-'+day, 'time':hou+":"+min+":"+sec,
                'azimuth':azi, 'rpm':rpm, 'start_angle':start_ang, 'end_angle':end_ang,
                'staga_prf1':stg_prf1, 'prf2':prf2, 'fftpoint_prf1':FFT_point_1, 'fftpoint_prf2':FFT_point_2,
                'sector':sector, 'sweep_data':sweep, 'shart_palse':short_ppr, 'long_palse':long_ppr}
        total_data =[]
        for p in range(256):
            swp = struct.unpack('H',f.read(2))[0]*(360/65536)     #スイープ開始角度
            sct = struct.unpack('h',f.read(2))[0]     #セクタ番号
            #print(f'スイープ開始角度:{swp*(360/65536)} セクタ番号:{sct}')
            sweep = {'sweep_angle':swp, 'sector_num':sct}
            #ショートレンジ
            short_range_data = []
            for i in range(80):
                Z_MTI = format(struct.unpack('h',f.read(2))[0]*0.01, '.3f')   #反射強度MTI
                Z_NOR = format(struct.unpack('h',f.read(2))[0]*0.01, '.3f')   #反射強度NOR
                R_MTI = round(struct.unpack('h',f.read(2))[0]*0.01)   #降雨強度MTI
                R_NOR = format(struct.unpack('h',f.read(2))[0]*0.01, '.3f')   #降雨強度NOR
                spe = struct.unpack('h',f.read(2))[0]          #速度
                spr = struct.unpack('bb',f.read(2))[0]         #速度幅
                #print(i)
                #print(f'反射強度MTI:{Z_MTI*0.01} 反射強度NOR:{Z_NOR*0.01} 降雨強度MTI:{R_MTI*0.01} 降雨強度NOR:{R_NOR*0.01}')
                #print(f'速度:{spe} 速度幅:{spr}')
                #print("\n")
                short_range = {'Z_MTI':Z_MTI, 'Z_NOR':Z_NOR, 'R_MTI':R_MTI, 'R_NOR':R_NOR, 'speed':spe, 'speed_range':spr}
                short_range_data.append(short_range)
            #ロングレンジ
            long_range_data = []
            for i in range(502):
                Z_MTI = format(struct.unpack('h',f.read(2))[0]*0.01, '.3f')   #反射強度MTI
                Z_NOR = format(struct.unpack('h',f.read(2))[0]*0.01, '.3f')   #反射強度NOR
                R_MTI = round(struct.unpack('h',f.read(2))[0]*0.01)   #降雨強度MTI
                R_NOR = format(struct.unpack('h',f.read(2))[0]*0.01, '.3f')   #降雨強度NOR
                spe = struct.unpack('h',f.read(2))[0]     #速度
                spr = struct.unpack('bb',f.read(2))[0]     #速度幅
                #print(i)
                #print(f'反射強度MTI:{Z_MTI*0.01} 反射強度NOR:{Z_NOR*0.01} 降雨強度MTI:{R_MTI*0.01} 降雨強度NOR:{R_NOR*0.01}')
                #print(f'速度:{spe} 速度幅:{spr}')
                #print("\n")
                long_range = {'Z_MTI':Z_MTI, 'Z_NOR':Z_NOR, 'R_MTI':R_MTI, 'R_NOR':R_NOR, 'speed':spe, 'speed_range':spr}
                long_range_data.append(long_range)
            data = [sweep, short_range_data, long_range_data]
            total_data.append(data)

    x = []
    y = []
    z = []
    s = []
    xx = []
    mat = []
    for a in range(256):
        z = []
        for b in range(502):
            #print(total_data[a][1][b]['Z_MTI'], total_data[a][2][b]['Z_MTI'])
            #x.append(total_data[a][1][b]['Z_MTI'])
            #y.append(total_data[a][1][b]['Z_NOR'])
            z.append(total_data[a][2][b]['R_MTI']/5)
            #all_data.append(total_data[a][1][b]['R_MTI'])
            #s.append(total_data[a][1][b]['R_NOR'])
            #plt.scatter(b, a, label="R_MTI", color=cm.jet(total_data[a][1][b]['R_MTI']), s=1)
        mat.append(z)
     

    #plt.scatter(mat, label="R_MTI", color=cm.jet(total_data[a][1][b]['R_MTI']), s=1)
    plt.figure()
    plt.imshow(mat,interpolation='nearest',vmin=0,vmax=1,cmap='jet')
    plt.colorbar()
    plt.ylim(0, 256)
    plt.xlim(0, 502)
    #plt.show()
    plt.savefig("img_long/"+path[7:21])
    



#plt.hist(all_data, range=(1, 50), bins=49)
#plt.show()
