"""Программа для проверки пинга"""
import os
import json
from urllib import parse, request
import ping3


class Ping:
    chat_id = os.getenv('ADMIN_ID')  # Telegram ID
    token = os.getenv('TOKEN_BOT')  # Bot token
    path_os = ('' if os.name == 'nt' else '/home/user/mybot1/')

    def start(self):
        if self.chat_id and self.token:
            self.ping_check()
        else:
            print("Ошибка! Не указан chat_id или token. Проверьте переменные окружения.")

    def ping_check(self):
        # Чтение данных из JSON
        with open(f"{self.path_os}ping.json", encoding="utf-8") as file:
            data = json.load(file)
            ip_list = data.keys()

        for ip in ip_list:
            ping = str(ping3.ping(ip, unit='ms', size=1470))

            if ping == 'False':
                if data[ip]["online_flag"] == 1:
                    data[ip]["online_flag"] = 0
                    response = f'❗ Worker {ip} ({data[ip]["name"]}) offline'
                    print(response)
                    url = (f'https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chat_id}&'
                           f'text={parse.quote(response)}')
                    request.urlopen(url)
                elif data[ip]["online_flag"] == 0:
                    print(f'{ip} ({data[ip]["name"]}) . . . Offline')

            elif ping != 'False':
                if data[ip]["online_flag"] == 0:
                    data[ip]["online_flag"] = 1
                    response = f'✅ Worker {ip} ({data[ip]["name"]}) booted'
                    print(response)
                    url = (f'https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chat_id}&'
                           f'text={parse.quote(response)}')
                    request.urlopen(url)
                elif data[ip]["online_flag"] == 1:
                    print(f'{ip} ({data[ip]["name"]}) . . . OK')

            else:
                raise Exception('Unknown error!')

        # Запись изменений в JSON
        with open(f"{self.path_os}ping.json", "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)


if __name__ == "__main__":
    do_ping = Ping()
    do_ping.start()
