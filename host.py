import socket
import subprocess
import os

PORT = 65002


def functions(message):
    f = int(message[0])
    if f == 1:
        what = int(message[1])
        if what == 1:
            cmd = "amixer -D pulse sset Master 10%-"
        else:
            cmd = "amixer -D pulse sset Master 10%+"
        subprocess.call(cmd, shell=True)
        return "1"
    if f == 2:
        cmd = "amixer -D pulse get Master | awk -F 'Left:|[][]' '{ print $3 }' | tr -d '%' | tr -d '\n' > temp"
        subprocess.run(cmd, shell=True)
        with open("temp", 'r') as file:
            vol = file.read()
        os.remove("temp")
        return "{}{}".format(2, vol[:len(vol)-1])
    if f == 3:
        subprocess.call("date +'%S' > time", shell=True)
        with open("time", "r") as file:
            choice = int(file.readline()) % 10
        os.remove("time")
        if 0 <= choice <= 3:
            cmd = r"""iostat | awk 'FNR==4{print $1 "%"}' | sed 's/^/CPU USAGE: /' > host_info"""
        elif 3 < choice <= 6:
            cmd = r"""free | awk 'FNR==2{print $3/$2 * 100 "%"}' | sed 's/^/RAM USAGE: /' > host_info"""
        elif 6 < choice <= 9:
            cmd = "sensors | grep 'Core' | cut -d ' ' -f 1,2,10 | sed 2,4d | awk '{print $3}'| sed 's/^/CPU TEMP: /' > host_info"
        subprocess.call(cmd, shell=True)
        with open("host_info", "r") as file:
            text = file.read()
        os.remove("host_info")
        return "{}{}".format(3, text)

    if f == 4:
        number = int(message[1])
        commands = ["xdg-open https://www.pk.edu.pl/index.php?lang=pl", # odpala przegladarke
                    "code",                                             # odpala vscode
                    "xdg-open http://elf2.pk.edu.pl/",                  # i to tez
                    "gnome-terminal -- vi",                             # otwiera vi
                    "spotify &disown",                                  # otwiera spotify
                    "date",                                             # date
                    "cal",                                              # odpala kalendarz
                    "killall -I python3 plytka.py"]                     # wylancza
        subprocess.run(commands[number], shell=True)
        return "4"
    if f == 5:
        pass
    if f == 6:
        pass


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as host_socket:
    host_socket.bind(('localhost', PORT))
    host_socket.listen(1)
    connection, address = host_socket.accept()
    with connection:
        print('Connected by', address)
        data = ''
        while True:
            msg = connection.recv(1024)
            #print(msg)
            msg = msg.decode("utf-8")
            #print(msg)
            data += msg
            if len(data) > 0:
                func = functions(data)
                to_send = "{}".format(func)
                connection.send(bytes(to_send, "utf-8"))
                data = ''
