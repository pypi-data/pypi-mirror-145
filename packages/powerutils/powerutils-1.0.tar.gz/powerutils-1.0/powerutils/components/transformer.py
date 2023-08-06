import  numpy as np
class Transformer():
    rho_cu = 17.2*1e-9
    oz=35*1e-6*3
    Kac=3
    Kfe=2

    # Pv=np.power(10,c1)*np.power((1000*Bmax),b1)*1000
    selected_mag = 'DMR_51w'
    magnetic_material = {
        'DMR_51w':{
            'c1':-3.6653,
            'b1':3.465
        }
    }
    
    
    def __init__(self,a,b,c,Noz=3):
        """参考CPES的论文中的图形定义

        Args:
            a (m): 矩形Ae的长边
            b (m): 矩形Ae的短边
            c (m): 绕组的宽度
            W (m): 变压器整体的宽度
            Y (m): 变压器整体的长度
        """
        self.a = a
        self.b = b
        self.c = c
        self.W = self.b*2+self.c*2
        self.Y = self.a+self.c*2
        self.oz=self.oz*Noz
    
    def Ae(self):
        """返回Ae面积

        Returns:
            m^2: Ae面积
        """
        return self.a*self.b
    
    def Bmax(self,fs,vs):
        """返回Bmax

        Args:
            fs (Hz): 开关频率
            vs (volt): 副边单匝的电压

        Returns:
            T: 返回Bmax的单边峰值
        """
        return vs*(0.5*1/fs)/(self.Ae())/2

    def DCR(self,turn = 1):
        a = self.a
        b = self.b
        c = self.c
        rho_cu = self.rho_cu
        oz = self.oz
        if(turn == 1):
            # 采用细条切分，求电导，积分，最后求倒数
            return 8*rho_cu/oz*(1/np.log((a+b+4*c)/(a+b)))

    def footprint(self):
        """返回变压器面积

        Returns:
            float: 面积，单位mm2
        """
        return self.W*self.Y
    
    def mag_loss_volume(self):
        pcb_height = 2e-3
        # 先假定变压器的整体厚度就是7mm，然后PCB厚度2mm，所以单个I片是2.5mm
        I_slice_thickness_max=0.0025
        winding_width = self.c
        ae_core_width = self.b

        mag_path_len = 2*((winding_width*2+ae_core_width)+I_slice_thickness_max)+pcb_height*2

        return mag_path_len*self.Ae()

    def winding_loss_pri(self,Irms):
        return self.DCR()*(Irms**2)*self.Kac

    def core_loss_density(self,fs,vs):
        """磁芯损耗密度

        Args:
            fs (Hz): 开关频率
            vs (V): 副边的单匝电压

        Returns:
            W/m3: 损耗密度
        """
        c1 = self.magnetic_material[self.selected_mag]['c1']
        b1 = self.magnetic_material[self.selected_mag]['b1']
        return np.power(10,c1)*np.power((1000*self.Bmax(fs,vs)),b1)*1000

    def core_loss(self,fs,vs):
        return self.core_loss_density(fs,vs)*self.mag_loss_volume()
class Round_transformer():
    rho_cu = 17.2*1e-9
    # 使用3oz的铜
    oz_unit=35*1e-6
    Kac=3
    Kfe=2

    # Pv=np.power(10,c1)*np.power((1000*Bmax),b1)*1000
    selected_mag = 'DMR_51w'
    magnetic_material = {
        'DMR_51w':{
            'c1':-3.6653,
            'b1':3.465
        }
    }
    def __init__(self,r,w,Noz = 3):
        self.r = r
        self.w = w
        self.oz = self.oz_unit*Noz
        self.W = (4*w+4*r)
        self.Y = (2*w+2*r)

    def Ae(self):
        """返回Ae面积

        Returns:
            m^2: Ae面积
        """
        return self.r**2*np.pi
    
    def Bmax(self,fs,vs):
        """返回Bmax

        Args:
            fs (Hz): 开关频率
            vs (volt): 副边单匝的电压

        Returns:
            T: 返回Bmax的单边峰值
        """
        return vs*(0.5*1/fs)/(self.Ae())/2

    def DCR(self,turn = 1):
        r = self.r
        w = self.w
        rho_cu = self.rho_cu
        oz = self.oz
        # 采用细条切分，求电导，积分，最后求倒数
        # 切分为n匝之后，总的DCR就是原来的turn平方倍。
        return 2*np.pi*rho_cu/oz/np.log((1+w/r))*(turn**2)

    def footprint(self):
        """返回变压器面积

        Returns:
            float: 面积，单位mm2
        """
        return self.W*self.Y
    def I_slice_height(self):
        return self.Ae()/self.Y
    def mag_loss_volume(self):
        PCB_thickness = 2e-3
        mag_path_len = 2*(2*self.r+2*self.w)+2*(PCB_thickness+self.I_slice_height())

        return mag_path_len*self.Ae()

    def winding_loss(self,Irms,turn=1):
        return self.DCR(turn=turn)*(Irms**2)*self.Kac

    def core_loss_density(self,fs,vs):
        """磁芯损耗密度

        Args:
            fs (Hz): 开关频率
            vs (V): 副边的单匝电压

        Returns:
            W/m3: 损耗密度
        """
        c1 = self.magnetic_material[self.selected_mag]['c1']
        b1 = self.magnetic_material[self.selected_mag]['b1']
        return np.power(10,c1)*np.power((1000*self.Bmax(fs,vs)),b1)*1000

    def core_loss(self,fs,vs):
        return self.core_loss_density(fs,vs)*self.mag_loss_volume()

if __name__ == '__main__':
    trans0 = Transformer(a=11e-3,b=4e-3,c=6.5e-3)
    trans1 = Round_transformer(r=5e-3,w= 5e-3)

    fs = 1e6
    vs = 12

    print(trans1.core_loss(fs,vs))
    # print(trans0.core_loss(fs,vs))
