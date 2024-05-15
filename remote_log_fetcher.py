import os
from dotenv import load_dotenv

load_dotenv()

def get_latest_replication_logs():
    ssh_host = os.getenv('DB_HOST')
    ssh_user = os.getenv('SSH_USER')
    ssh_password = os.getenv('SSH_PASSWORD')
    log_file_path = '/var/log/postgresql/postgresql-15-main.log'

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ssh_host, username=ssh_user, password=ssh_password)
        stdin, stdout, stderr = ssh.exec_command(f"sudo tail -n 20 {log_file_path}")
        logs = stdout.read().decode() + stderr.read().decode()
        ssh.close()
        return logs
    except Exception as e:
        return f"Ошибка при доступе к удаленному серверу: {str(e)}"
