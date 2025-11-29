# настройки подключения к RDS
MASTER_DB = {
    'host': 'project-rds-mysql-prod.cncoyq22m5uo.eu-central-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'password123!',
    'database': 'project_db'
}

READ_REPLICA_DB = {
    'host': '<READ_REPLICA_ENDPOINT>',
    'user': 'admin',
    'password': 'password123!',
    'database': 'project_db'
}
