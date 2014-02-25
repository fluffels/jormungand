__author__ = 'adam.jorgensen.za@gmail.com'

try:
    from psycopg2ct import compat
    compat.register()
except:
    pass
