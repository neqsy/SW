import tkinter
import socket
import asyncio
import nest_asyncio
import threading

BLOCK = True


class Evb(tkinter.Frame):

    def __init__(self, main, connection):
        tkinter.Frame.__init__(self, main)
        self.__main_window = main
        self.__main_window.geometry("1000x612")
        self.__main_window.resizable(0, 0)
        self.__main_window.title('evb')
        self.__connection = connection
        self.__window_background_img = tkinter.PhotoImage(file="Przechwytywanie.PNG")
        self.__pixel = tkinter.PhotoImage(width=1, height=1)
        self.__text_var = " "
        self.__led = []
        self.__lcd = None
        self.__rgb = None
        nest_asyncio.apply()
        self.loop()

    def th(self, loop):
        loop.run_until_complete(self.led_loop())

    def th2(self, loop2):
        loop2.run_until_complete(self.text_loop())

    def th3(self, loop3):
        loop3.run_until_complete(self.rgb_loop())

    def loop(self):
        window_background = tkinter.Label(self.__main_window)
        window_background.config(image=self.__window_background_img)
        window_background.place(relwidth=1, relheight=1)
        button1 = tkinter.Button(self.__main_window, text='1', command=lambda: self.click(0),
                                 compound=tkinter.CENTER, image=self.__pixel, width=4, height=16)
        button1.place(relx=0.547, rely=0.943, anchor=tkinter.CENTER)
        button2 = tkinter.Button(self.__main_window, text='2', command=lambda: self.click(1),
                                 compound=tkinter.CENTER, image=self.__pixel, width=4, height=16)
        button2.place(relx=0.5815, rely=0.943, anchor=tkinter.CENTER)
        button3 = tkinter.Button(self.__main_window, text='3', command=lambda: self.click(2),
                                 compound=tkinter.CENTER, image=self.__pixel, width=4, height=16)
        button3.place(relx=0.616, rely=0.943, anchor=tkinter.CENTER)
        button4 = tkinter.Button(self.__main_window, text='4', command=lambda: self.click(3),
                                 compound=tkinter.CENTER, image=self.__pixel, width=4, height=16)
        button4.place(relx=0.6505, rely=0.943, anchor=tkinter.CENTER)
        button5 = tkinter.Button(self.__main_window, text='5', command=lambda: self.click(4),
                                 compound=tkinter.CENTER, image=self.__pixel, width=4, height=16)
        button5.place(relx=0.685, rely=0.943, anchor=tkinter.CENTER)
        button6 = tkinter.Button(self.__main_window, text='6', command=lambda: self.click(5),
                                 compound=tkinter.CENTER, image=self.__pixel, width=4, height=16)
        button6.place(relx=0.7195, rely=0.943, anchor=tkinter.CENTER)
        button7 = tkinter.Button(self.__main_window, text='7', command=lambda: self.click(6),
                                 compound=tkinter.CENTER, image=self.__pixel, width=4, height=16)
        button7.place(relx=0.754, rely=0.943, anchor=tkinter.CENTER)
        button8 = tkinter.Button(self.__main_window, text='8', command=lambda: self.click(7),
                                 compound=tkinter.CENTER, image=self.__pixel, width=4, height=16)
        button8.place(relx=0.7885, rely=0.943, anchor=tkinter.CENTER)
        volume_button1 = tkinter.Button(self.__main_window, text='-', command=lambda: self.f1(1),
                                        compound=tkinter.CENTER, image=self.__pixel, width=1, height=20)
        volume_button1.place(relx=0.836, rely=0.947, anchor=tkinter.CENTER)
        volume_button2 = tkinter.Button(self.__main_window, text='+', command=lambda: self.f1(2),
                                        compound=tkinter.CENTER, image=self.__pixel, width=1, height=20)
        volume_button2.place(relx=0.864, rely=0.947, anchor=tkinter.CENTER)
        self.__lcd = tkinter.Label(self.__main_window, bg='grey', text=self.__text_var, width=57, height=7)
        self.__lcd.place(relx=0.718, rely=0.24, anchor=tkinter.CENTER)

        for i in range(8):
            led = tkinter.Label(self.__main_window, bg="#003200", image=self.__pixel, width=8, height=15)
            self.__led.append(led)
            led.place(relx=0.4207 + i * 0.0174, rely=0.573, anchor=tkinter.CENTER)

        self.__rgb = tkinter.Label(self.__main_window, bg="#ffff9f", image=self.__pixel, width=35, height=35)
        self.__rgb.place(relx=0.587, rely=0.549, anchor=tkinter.CENTER)
        l1 = asyncio.get_event_loop()
        l2 = asyncio.get_event_loop()
        l3 = asyncio.get_event_loop()
        threading.Thread(target=self.th, args=(l1,)).start()
        threading.Thread(target=self.th2, args=(l2,)).start()
        threading.Thread(target=self.th3, args=(l3,)).start()

    def click(self, number):
        "przyciski"
        self.f4(number)

    async def led_loop(self):
        while True:
            try:
                self.f2()
                await asyncio.sleep(0.2)
            except Exception as e:
                pass

    async def rgb_loop(self):
        while True:
            try:
                self.f6()
                await asyncio.sleep(1)
            except Exception as e:
                pass

    async def text_loop(self):
        while True:
            try:
                self.f3()
                await asyncio.sleep(1.5)
            except Exception as e:
                pass

    def f1(self, what):
        "ustawianie audio , what(-/=)"

        global BLOCK
        if BLOCK:
            BLOCK = False
            self.__connection.send(bytes(f"1{what}", "utf-8"))
            r = self.__connection.recv(64)
            BLOCK = True

    def f2(self):
        global BLOCK
        vol = 0
        if BLOCK:
            BLOCK = False
            self.__connection.send(bytes("2", "utf-8"))
            r = self.__connection.recv(64)
            r.decode("utf-8")
            vol = r[1:]
            temp = round(8 * int(vol) / 100)
            for led in range(temp):
                self.__led[led].config(bg="#00ff00")
            for led in range(temp, len(self.__led)):
                self.__led[led].config(bg="#003200")
            BLOCK = True

    def f3(self):
        global BLOCK
        if BLOCK:
            BLOCK = False
            self.__connection.send(bytes("3", "utf-8"))
            r = self.__connection.recv(64)
            r = r.decode("utf-8")
            self.__text_var = r[1:]
            self.__lcd.config(text=self.__text_var)
            BLOCK = True

    def f4(self, number):
        global BLOCK
        if BLOCK:
            BLOCK = False
            self.__connection.send(bytes("4{}".format(number), "utf-8"))
            r = self.__connection.recv(64)
            BLOCK = True
            
    def f5(self):
    global BLOCK
        if BLOCK:
            BLOCK = False
            self.__connection.send(bytes("5", "utf-8"))
            r = self.__connection.recv(64)
            r = r.decode("utf-8")
            self.__text_var = r[1:]
            self.__lcd.config(text=self.__text_var)
            BLOCK = True
            
    def f6(self):
        global BLOCK
        if BLOCK:
            BLOCK = False
            self.__connection.send(bytes("6", "utf-8"))
            color = self.__connection.recv(64)
            color = color.decode("utf-8")
            self.__rgb.config(bg=color)
            BLOCK = True
