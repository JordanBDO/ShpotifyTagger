from datetime import datetime

from pynamodb.models import Model
from pynamodb import connection
from pynamodb.attributes import (
    UnicodeAttribute, NumberAttribute, UnicodeSetAttribute, UTCDateTimeAttribute, ListAttribute
)

class Master(Model):
    class Meta:
        table_name = 'Master'
        region = 'ap-southeast-2'

    hash = UnicodeAttribute(hash_key=True)
    name = UnicodeAttribute(range_key=True)
    uri = UnicodeAttribute()
    items = ListAttribute()
    tags = ListAttribute()

# Master.delete_table()
Master.create_table(read_capacity_units=20, write_capacity_units=30, wait=True)


def getitem(table, hash, range, fields=None):
    # get_item key structure ['item']['field']['datatypecode']

    mydb = connection.Connection(
        region='ap-southeast-2'
    )
    record = {}
    if fields is None:
        record = mydb.get_item(table_name=table, hash_key=hash, range_key=range)['Item']
        for field in record:
            datatype = getattr(Master, field).attr_type
            try:
                value = mydb.get_item(table_name=table, hash_key=hash, range_key=range)['Item'][field][datatype]
            except:
                return 'Not found in db'
            if type(value) == list:
                vallist = []
                for i in value:
                    idatatype = list(i.keys())[0]
                    vallist.append(i[idatatype])
                    record[field] = vallist
            else:
                record[field] = value
        return record

    for field in fields:
        datatype = getattr(Master, field).attr_type
        try:
            value = mydb.get_item(table_name=table, hash_key=hash, range_key=range)['Item'][field][datatype]
        except:
            return 'not found in db'
        if type(value) == list:
            vallist = []
            for i in value:
                idatatype = list(i.keys())[0]
                vallist.append(i[idatatype])
                record[field] = vallist
        else:
            record[field] = value
    return record


# Master.delete_table()

# if not Master.exists():
#        Master.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)

# print(getitem(table='Master',hash='00e9af408462f047c77d34daca7f91dfbc2cb8d66c4b3e9cef3025069b854893',range='Come Alive (feat. Toro y Moi)Chromeo',fields=['hash','items','tags']))






# li = ['one','two']
# tg = ['S1','S2']
# Master_newitem = Master('test','test',items=li,tags=tg)
# Master_newitem.save()


# getitem(table='Master',hash='test',range='test',fields=['name'])

# get_item key structure ['item']['field']['datatypecode']
# print(mydb.get_item(table_name='Master',hash_key='test',range_key='test')['Item']['items']['L'])



#
# li = ['one','two']
# tg = []


# print(Master.get_item())

# test = Master.get(hash_key='test',range_key='test',attributes_to_get=['forum_name','subject','items'])
# print(test)





# Master_item = Master('Master')
# Master_item.save()