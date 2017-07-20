import os

debug          = True
xheaders       = True

log_prefix     = os.environ.get('GREEDO_LOG_PREFIX', 'greedo.log')
port           = os.environ.get('GREEDO_PORT', '41282')
template_dir   = os.environ.get('GREEDO_TEMPLATE_DIR', 'template')
sql_dir        = os.environ.get('GREEDO_SQL_DIR', 'sql')

mysql_host     = os.environ.get('MYSQL_HOST')
mysql_password = os.environ.get('MYSQL_PASSWORD')
mysql_db       = os.environ.get('MYSQL_DB')
mysql_user     = os.environ.get('MYSQL_USER')
