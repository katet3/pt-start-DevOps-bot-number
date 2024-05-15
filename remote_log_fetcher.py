import paramiko

def get_latest_replication_logs():
    ssh_host = '192.168.1.60'  # IP сервера базы данных
    ssh_user = 'root'      # Пользователь для SSH
    ssh_password = '1861'  # Пароль для SSH
    log_file_path = '/var/log/postgresql/postgresql-15-main.log'
    
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(ssh_host, username=ssh_user, password=ssh_password)
        stdin, stdout, stderr = ssh.exec_command(f"sudo tail -n 20 {log_file_path}")
        logs = stdout.read().decode()
        logs += stderr.read().decode()
        ssh.close()
        return logs
    except Exception as e:
        return f"Ошибка при доступе к удаленному серверу: {str(e)}"
