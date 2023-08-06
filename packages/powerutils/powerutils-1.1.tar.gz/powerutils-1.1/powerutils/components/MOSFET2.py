import numpy as np
from math import sqrt,pi
import pandas as pd  

unit_table = {
    'p':1e-12,
    'u':1e-6,
    'n':1e-9,
    'm':1e-3
}

FoM_Si = {
    '25':{
        '10V':38*1e-12,
        '5V':25*1e-12
    },
    '40':{
        '10V':76*1e-12,
        '5V':61*1e-12
    },
    '60':{
        '10V':113*1e-12,
        '5V':94*1e-12
    },
    '80':{
        '10V':180*1e-12,
        '5V':104*1e-12
    },
    '100':{
        '10V':211*1e-12,
        '5V':150*1e-12
    },
    '150':{
        '10V':300*1e-12,
        '5V':200*1e-12
    }
}
FoM_GaN = {
    '30':{
        '5V':28*1e-12*2
    },
    '40':{
        '5V':33*1e-12*2
    },
    '60':{
        '5V':39*1e-12*2
    },
    '80':{
        '5V':41*1e-12*2
    },
    '100':{
        '5V':47*1e-12*2
    },
    '200':{
        '5V':100*1e-12*2
    }
}
def find_minimum_loss(Nlevel):
    import pandas as pd
    df = pd.read_excel('database/EPC-Product-Table.xlsx')
    mos_dict = {}
    for index,rows in df.iterrows():
        MOS = MOSFET()
        ID = MOS.load_from_pandas_row(rows)
        mos_dict[ID] = MOS
    Po=240
    Vo=380
    Vinrms = 220
    fs = 120e3
    data = []
    attrs = ['ID','Vbr','Rdson','footprint','cap_loss','con_loss','on_loss','off_loss','dri_loss','total_loss']
    Irms = Po/Vinrms

    for (key,mos) in mos_dict.items():
    # Nlevel需要管子的耐压是Vstep的1.2倍以上
        if(mos.Vbr>=Vo/(Nlevel-1)*1.2):
            tmp_arr = []
            # 一个桥臂的容性损耗为2*1/2Coss*Vlevel^2，一共有Nlevel-1个桥臂
            cap_loss = mos.cap_loss(voltage2 = (Vo/(Nlevel-1))**2,fs = fs)*(Nlevel-1)
            # 导通损耗需要以电流的平方，乘以桥臂数量
            con_loss = mos.con_loss(Irms)*(Nlevel-1)
            # 驱动损耗
            dri_loss = mos.dri_loss(fs)*2*(Nlevel-1)
            # 先求输入电流的平均值，这里计算关断损耗忽略了电感的电流纹波
            Iinave = Irms*sqrt(2)*2/pi
            on_loss = mos.switch_on_loss(f=fs,vol_by_current=Vo/(Nlevel-1)*Iinave)*(Nlevel-1)
            off_loss = mos.switch_off_loss(f=fs,vol_by_current=Vo/(Nlevel-1)*Iinave)*(Nlevel-1)
            total_loss = cap_loss+con_loss+dri_loss+off_loss+on_loss
            tmp_arr.append(mos.ID)
            tmp_arr.append(mos.Vbr)
            tmp_arr.append(mos.Rdson)
            tmp_arr.append(mos.footprint)
            tmp_arr.append(cap_loss)
            tmp_arr.append(con_loss)
            tmp_arr.append(on_loss)
            tmp_arr.append(off_loss)
            tmp_arr.append(dri_loss)
            tmp_arr.append(total_loss)
            # print(tmp_arr)
            data.append(tmp_arr)
    df = pd.DataFrame(data=data,columns = attrs)
    return df.total_loss.min()

def convert_value(val):
    # 转换带n,u,m等单位的数据，比如nF,uF,mF这种
    try:
        if(type(val)==str):
            
            # 如果是字符串，那么肯定最后两个是单位
            return float(val[:-2])*unit_table[val[-2]]
        else:
            return val
    except ValueError as e:
        print(e)
        
class MOSFET:
    def __init__(self, **kwargs):
        self.prop_defaults = {
            "ID"        :'',
            "Rdson"     :0,
            "Qg"        : 0,
            "footprint" : '',
            "Vbr"       : 0,
            "Cosse"     : 0,
            "Cosst"     : 0,
            "Vgsth"     : 0,
            "Qgs2"      : 0,
            "Qgd"       : 0,
            "Qoss"      : 0,
            "Vplateau"  : 0,
            "Rg"        : 0,
            "Qrr"       : 0,
            "kdyn"      : 2,
            "ktemp"     : 1.3,
            "vgs"       : 5,
            "on_voltage":0,
            'on_current':0,
            'off_voltage':0,
            'off_current':0,
            'irms':0,
            'fs':0,
            'rgo_on':2.1,
            'rgo_off':0.6
        }
        for (prop, default) in self.prop_defaults.items():
            setattr(self, prop, kwargs.get(prop, default))

    def load_from_pandas_row(self,info):
        self.__init__(
            ID  =info['PartNumber'],
            Rdson=info['RDSon']*1e-3,
            Qg = info['Qg']*1e-9,
            footprint=info['Package(mm)'],
            Vbr=info['VDS'],
            Cosse = info['Coss(Energy)']*1e-12,
            Cosst = info['Coss(tr)']*1e-12,
            Vgsth = info['Vgsth'],
            Qgs2 = info['Qgs2']*1e-9,
            Qgd = info['Qgd']*1e-9,
            Qoss = info['Qoss']*1e-9,
            Vplateau = info['Vplateau'],
            Rg = info['Rg']
            )
        return self.ID
    def __str__(self) -> str:
        result =  "Rdson:%1.1e, footprint:%s"%(self.Rdson,self.footprint)
        result = self.ID+' '+result if self.ID else result
        return result

    def cap_loss(self):
        """返回容性损耗，如果是定频，就直接传入电压，fs代表开关频率
        如果是变频，就传入一个完整周期的电压信号，fs代表完整信号的频率

        Args:
            voltage (int, optional): [description]. Defaults to 0.
            fs (int, optional): [description]. Defaults to 0.

        Returns:
            [type]: [description]
        """
        # 如果是定频，那么返回单周期的损耗乘以频率
        return 0.5*self.Cosse*self.on_voltage**2
    def detail_info(self):
        result = ''
        for (key,value) in self.prop_defaults.items():
            result+=('\n%s: %s'%(key,str(getattr(self,key))))
        return result
        
    def con_loss(self):
        """返回一个桥臂的导通损耗

        Args:
            irms (A): 流经桥臂的电流的有效值
        """
        return self.Rdson*self.kdyn*self.ktemp*self.irms**2
    def dri_loss(self):
        """计算驱动损耗

        Args:
            fs (Hz): 开关频率
            cnt (int, optional): 如果cnt=1，表示是定频，如果不是，表示的是一个完整周期内的开关次数. Defaults to 1.

        Returns:
            [type]: 驱动损耗
        """
        return self.Qg*self.vgs
    def switch_off_loss(self,rgo=0.6):
        """计算一个桥臂的关断损耗

        Args:
            f (Hz): 1s内重复的次数
            vol_by_current (W): 关断瞬间的电压和电流的点积之和
            rgo (R): 外部的驱动电阻

        Returns:
            W: 一个桥臂的关断损耗
        """
        # 这个时间是和外部条件没有关系的。所以可以直接由外部计算再穿入
        t = self.Qgs2/((self.Vplateau+self.Vgsth)/2)+self.Qgd/(self.Vplateau)
        loss = self.off_current*self.off_voltage*(rgo+self.Rg)/2*t
        return loss

    def switch_on_loss(self,rgo = 2.1):
        """计算一个桥臂的开通损耗

        Args:
            f (Hz): 1s内重复的次数
            vol_by_current ([type]): 开通瞬间的电压和电流点积之和
            rgo (R, optional): [description]. Defaults to 0.15.

        Returns:
            W: 一个桥壁的开通损耗
        """
        t = self.Qgs2/(self.vgs-(self.Vplateau+self.Vgsth)/2)+self.Qgd/(self.vgs-self.Vplateau)
        loss = self.on_current*self.on_voltage*(rgo+self.Rg)/2*t
        return loss

    def Qrr_loss(self):
        return self.Qrr*self.on_voltage

    # def loss_breakdown(self,on_voltage,on_current,off_voltage,off_current,irms,fs,rgo_on = 2.1,rgo_off = 0.6):
    #     result = {
    #         "con_loss"      :   self.con_loss(irms),
    #         "sw_on_loss"    :   self.switch_on_loss(on_voltage,on_current,rgo=rgo_on)*fs,
    #         "sw_off_loss"   :   self.switch_off_loss(off_voltage,off_current,rgo = rgo_off)*fs,
    #         "cap_loss"      :   self.cap_loss(on_voltage)*fs,
    #         "dri_loss"      :   self.dri_loss()*fs
    #     }

    @property
    def NFoM(self):
        return self.Rdson*self.Cosst
    @property
    def FoM(self):
        return self.Rdson*self.Qg


class Si_MOS(MOSFET):
    def __init__(self, ID, Rdson, Qg, footprint, Vbr, Cosse, Cosst, Vgsth, Qgs2, Qgd, Qoss, Vplateau, Rg, Qrr, vgs=10,Qgl=0,Rdsonl=0) -> None:
        super().__init__(
            ID=ID, 
            Rdson=Rdson, 
            Qg=Qg, 
            footprint=footprint, 
            Vbr=Vbr, 
            Cosse=Cosse, 
            Cosst=Cosst, 
            Vgsth=Vgsth, 
            Qgs2=Qgs2, 
            Qgd=Qgd, 
            Qoss=Qoss, 
            Vplateau=Vplateau, 
            Rg=Rg, 
            Qrr=Qrr, 
            kdyn=1, 
            ktemp=1.3, 
            vgs=vgs
            )
        # 低压驱动的时候需要，如果不传入参数，认为以5V驱动，且Qg为10V的一半
        self.Qgl = Qgl if(Qgl) else self.Qg/2
        self.Rdsonl = Rdsonl if (Rdsonl) else self.Rdson

GaN_df = pd.read_excel('database/EPC-Product-Table.xlsx')
GaN_mos_dict = {}
for index,rows in GaN_df.iterrows():
    MOS = MOSFET()
    ID = MOS.load_from_pandas_row(rows)
    GaN_mos_dict[ID] = MOS

if __name__=='__main__':
    df = pd.read_excel('./EPC-Product-Table.xlsx')

    mos_dict = {}
    for index,rows in df.iterrows():
        MOS = MOSFET()
        ID = MOS.load_from_pandas_row(rows)
        mos_dict[ID] = MOS
        
    print(mos_dict['EPC2207'].con_loss())

    