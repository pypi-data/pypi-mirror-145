import os


def timing_task_add(task_time, password):
    """ task_time: Cron expression,
        password: linux root_password
    """
    os.system(f'echo "{password}" | sudo -S sed -i "\$a{task_time}" /etc/crontab')
    os.system(f'server cron reload')
    os.system('cat /etc/crontab')


__all__ = [
    "timing_task_add"
]
