import pymysql
from utils import dict2str
class MysqlDb:
    def __init__(self, User, Password, Db, Host, Port=3306):
        try:
            self._conn = pymysql.connect(host=Host, port=Port, user=User, password=Password, db=Db, charset='utf8')
        except Exception as e:
            print(e.what)
            raise e
    def set_table(self, table):
        self._table = table
        return self
    def insert(self, dataDict):
        sql = 'insert into ' + self._table 
        fields = '('
        values = '('
        for field in dataDict:
            fields += field
            fields += ','
            if isinstance(dataDict[field], str):
                values += '"' + dataDict[field] + '"'
            else:
                values += str(dataDict[field])
            values += ','
        fields = fields[0: -1]
        values = values[0:-1] 
        fields += ')'  
        values += ')'
        sql += fields + ' values ' + values + ';commit'
        print(sql)
        try:
            self._conn.query(sql)
        except Exception as e:
            print(e)
            return False
        return True
    def update(self, dataDict, condDict):
        sql = 'update ' + self._table + ' set '
    
    def query(self, fieldList, condDict=None):
        sql = 'select '
        if isinstance(fieldList, str) and fieldList == '*':
            sql += fieldList + ' from '
        elif isinstance(fieldList, list):
            for field in fieldList:
                sql += field + ',' 
            sql = sql[0:-1] + ' from '
        else:
            print('error')
            return False
        sql += self._table
        if condDict != None:
            sql += ' where ' + dict2str(condDict)
        print(sql)
        cursor = self._conn.cursor()
        cursor.execute(sql)
        return cursor  
            
if __name__ == '__main__':
    db = MysqlDb('root', 'zcm890211', 'lagou', '127.0.0.1', 3306)
    db.set_table('job')
    res = db.query('*', {'job_id': 1})
    for item in res:
        print(item)