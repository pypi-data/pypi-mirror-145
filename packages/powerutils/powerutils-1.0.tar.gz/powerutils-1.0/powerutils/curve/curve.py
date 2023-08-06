import os
import  numpy as np
def load_curve(filename):
    with open(filename,'r')as f:
        datas = f.readlines()
        c_arr = []
        v_arr = []
        for data in datas:
            [x,y] = data.split(';')
            [x,y] = [float(x),float(y)]
            c_arr.append(y)
            v_arr.append(x)
        return[v_arr,c_arr]
def energy(v,c,vmax,vmin = 0):
    """根据C-V曲线计算等效，根据C*V*deltaV计算

    Args:
        v (list)): 电压数组
        c (list): 电容数组
        vmax (float): 电压最大值
        vmin (float, optional): 电压最小值. Defaults to 0.
    """
    cv2_sum = 0
    voltage_prev = vmin
    c_prev = c[0]
    assert(len(c)==len(v))
    length = len(v)
    for i in range(0,length):
        if(v[i]<vmin):
            continue
        if(v[i]>vmax):
            break
        v_aver = (v[i]+voltage_prev)/2
        c_aver = (c[i]+c_prev)/2
        cv2_sum+=c_aver*v_aver*(v[i]-voltage_prev)
        c_prev = c[i]
        voltage_prev = v[i]
    # 由于能量等于1/2*C*vmax**2，所以要除以vmax**2并乘以2

    # 计算最后一个点的平均能量
    # 首先计算斜率，然后乘以deltav
    if(v[i]-voltage_prev):
        c_last = (c[i]-c_prev)/(v[i]-voltage_prev)*(vmax-voltage_prev)+c_prev
        # 计算最后一个点的平均电压
        v_last = (vmax+voltage_prev)/2
        cv2_sum+=c_last*v_last*(vmax-voltage_prev)
    return cv2_sum
def charge(v,c,vmax,vmin = 0):
    cv_sum = 0
    voltage_prev = vmin
    c_prev = c[0]
    assert(len(c)==len(v))
    length = len(v)
    for i in range(0,length):
        if(v[i]<vmin):
            continue
        if(v[i]>vmax):
            break
        c_aver = (c[i]+c_prev)/2
        cv_sum+=c_aver*(v[i]-voltage_prev)
        c_prev = c[i]
        voltage_prev = v[i]
    # 计算最后一个点的平均能量
    # 首先计算斜率，然后乘以deltav
    if(v[i]-voltage_prev):
        c_last = (c[i]-c_prev)/(v[i]-voltage_prev)*(vmax-voltage_prev)+c_prev
        # 计算最后一个点的平均电压
        cv_sum+=c_last*(vmax-voltage_prev)
        # 由于电荷等于C*vmax，所以要除以vmax
    return cv_sum
def energy_equivalent(v,c,vmax,vmin=0):
    """根据C-V曲线计算能量等效电容，根据C*V*deltaV计算能量

    Args:
        v (list): 电压数组
        c (list): 电容数组
        vmax (float): 电压最大值
        vmin (float, optional): 电压最小值. Defaults to 0.

    Returns:
        float: 能量等效电容
    """
    return energy(v,c,vmax,vmin)/vmax**2*2
    
def time_equivalent(v,c,vmax,vmin=0):
    """根据C-V曲线计算时间等效电容，根据C*deltaV计算等效电荷

    Args:
        v (list): 电压数组
        c (list): 电容数组
        vmax (float): 电压最大值
        vmin (float, optional): 电压最小值. Defaults to 0.

    Returns:
        float: 时间等效电容
    """
    return charge(v,c,vmax,vmin)/vmax

def curve_get(name,category='mos'):
    root_path = os.path.dirname(os.path.abspath(__file__))
    if(category == 'mos'):
        file_path = root_path+'/../components/database/mosfet_coss/'+name+'.txt'
    elif ((category == 'mlcc') or (category == 'cap')):
        file_path = root_path+'/../components/database/mlcc/'+name+'.txt'
    assert(os.path.exists(file_path))
    return load_curve(file_path)

def energy_equi_from_id(id,vmax,vmin= 0,category = 'mos'):
    """计算能量等效电容，输入参数为ID，根据ID查找数据库

    Args:
        id (string): MOS的ID名字
        vmax (float): 最大电压
        vmin (float, optional): 最低电压. Defaults to 0.

    Returns:
        float: 能量等效电容
    """
    curve_arr = curve_get(id,category)
    return energy_equivalent(curve_arr[0],curve_arr[1],vmax,vmin)
def energy_from_id(id,vmax,vmin= 0,category = 'mos'):
    """计算能量等效电容，输入参数为ID，根据ID查找数据库

    Args:
        id (string): MOS的ID名字
        vmax (float): 最大电压
        vmin (float, optional): 最低电压. Defaults to 0.

    Returns:
        float: 能量等效电容
    """
    curve_arr = curve_get(id,category)
    return energy(curve_arr[0],curve_arr[1],vmax,vmin)

def time_equi_from_id(id,vmax,vmin= 0,category = 'mos'):
    """计算能量等效电容，输入参数为ID，根据ID查找数据库

    Args:
        id (string): MOS的ID名字
        vmax (float): 最大电压
        vmin (float, optional): 最低电压. Defaults to 0.

    Returns:
        float: 能量等效电容
    """
    curve_arr = curve_get(id,category)
    return time_equivalent(curve_arr[0],curve_arr[1],vmax,vmin)

def charge_from_id(id,vmax,vmin= 0,category = 'mos'):
    """计算能量等效电容，输入参数为ID，根据ID查找数据库

    Args:
        id (string): MOS的ID名字
        vmax (float): 最大电压
        vmin (float, optional): 最低电压. Defaults to 0.

    Returns:
        float: 能量等效电容
    """
    curve_arr = curve_get(id,category)
    return charge(curve_arr[0],curve_arr[1],vmax,vmin)
def power_func(x,k,a,b):
    """用于拟合的幂指数函数,y=k*x^a+b

    Args:
        x (float): x
        k (float): k
        a (float): a
        b (float): b

    Returns:
        float: y
    """
    return k*np.power(x,a)*x+b

if __name__ == '__main__':
    curve_arr = energy_equi_from_id('EPC2019',vmax=100,category = 'mos')
    print(curve_arr)
