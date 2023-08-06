import sqlite3 as sq
import pandas as pd

def execute_cmd(db,sql):
    conn = sq.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    conn.close()

def find_by_para(db,table,para,value):
    conn = sq.connect(db)
    sql_text = f'''
    SELECT * FROM {table} WHERE {para}='{value}'
    '''
    result = pd.read_sql(sql_text,conn)
    conn.close()
    return result

def update_db(db,table,id,id_value,para,para_value):
    sql = f'''UPDATE {table} 
        SET {para}='{para_value}'
        WHERE {id}=='{id_value}'
        '''
    execute_cmd(db,sql)

if __name__ =='__main__':
    update_db('database/NCC_all_of_ripple.db','CAP','ID','EKMH100LGC684MFE0U','RIPPLE',13)
    cap_info = find_by_para('database/NCC_all_of_ripple.db',"CAP","ID",'EKMH100LGC684MFE0U')
    
    print(cap_info)
