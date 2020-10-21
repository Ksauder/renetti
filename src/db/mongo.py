from mongoengine import connect, register_connection


client = register_connection(alias='renetti', name='renetti', host='mongo', port=27017, )
