import socket
import pygame
import math
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox

pygame.init()


def scroll(event):
    global color
    color = combo.get()
    style.configure("TCombobox", fieldbackground=color, background="white")


def login():
    global name
    name = row.get()
    if name and color:
        root.destroy()
        root.quit()
    else:
        tk.messagebox.showerror("Ошибка", "Ты не выбрал цвет или не ввёл имя!")


def find(vector: str):
    first = None
    for num, sign in enumerate(vector):
        if sign == "<":
            first = num
        if sign == ">" and first is not None:
            second = num
            result = vector[first + 1:second]
            return result
    return ""


def draw_bacteries(data: list[str]):
    for num, bact in enumerate(data):
        data_parts = bact.split(" ")
        if len(data_parts) >= 4:
            x = CC[0] + int(data_parts[0])
            y = CC[1] + int(data_parts[1])
            size = int(data_parts[2])
            color = data_parts[3]
            pygame.draw.circle(screen, color, (x, y), size)


name = ""
color = ""

root = tk.Tk()
root.title("Логин")
root.geometry("300x200")

style = ttk.Style()
style.theme_use('clam')

name_label = tk.Label(root, text="Введи свой никнейм:")
name_label.pack()
row = tk.Entry(root, width=30, justify="center")
row.pack()
color_label = tk.Label(root, text="Выбери цвет:")
color_label.pack()
colors = ['Maroon', 'DarkRed', 'FireBrick', 'Red', 'Salmon', 'Tomato', 'Coral', 'OrangeRed', 'Chocolate', 'SandyBrown',
          'DarkOrange', 'Orange', 'DarkGoldenrod', 'Goldenrod', 'Gold', 'Olive', 'Yellow', 'YellowGreen', 'GreenYellow',
          'Chartreuse', 'LawnGreen', 'Green', 'Lime', 'SpringGreen', 'MediumSpringGreen', 'Turquoise', 'LightSeaGreen',
          'MediumTurquoise', 'Teal', 'DarkCyan', 'Aqua', 'Cyan', 'DeepSkyBlue', 'DodgerBlue', 'RoyalBlue', 'Navy',
          'DarkBlue', 'MediumBlue']

combo = ttk.Combobox(root, values=colors, textvariable=color)
combo.bind("<<ComboboxSelected>>", scroll)
combo.pack()
name_btn = tk.Button(root, text="Зайти в игру", command=login)
name_btn.pack()
root.mainloop()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
sock.connect(("localhost", 10000))

# Отправляем цвет и имя
sock.send(("color:<" + name + "," + color + ">").encode())

WIDTH = 800
HEIGHT = 600

radius = 50
CC = (WIDTH // 2, HEIGHT // 2)
old = (0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Бактерии")

# Делаем сокет неблокирующим
sock.setblocking(False)

clock = pygame.time.Clock()
run = True

while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Обработка мыши
    if pygame.mouse.get_focused():
        pos = pygame.mouse.get_pos()
        vector = pos[0] - CC[0], pos[1] - CC[1]
        lenv = math.sqrt(vector[0] ** 2 + vector[1] ** 2)

        if lenv <= radius:
            vector = (0, 0)
        else:
            vector = (vector[0] / lenv, vector[1] / lenv)

        if vector != old:
            old = vector
            msg = f"<{vector[0]},{vector[1]}>"
            print("Отправляю:", msg)
            try:
                sock.send(msg.encode())
            except:
                print("Ошибка отправки")

    # Получение данных от сервера (неблокирующее)
    try:
        data = sock.recv(1024).decode()
        print('Получил:', data)

        if data:
            parsed_data = find(data)
            if parsed_data:
                data_list = parsed_data.split(",")
                screen.fill('gray')
                pygame.draw.circle(screen, color, CC, radius)
                draw_bacteries(data_list)
            else:
                print("Нет данных для отрисовки")
        else:
            print("Сервер отключился")
            run = False

    except BlockingIOError:
        # Нет данных для чтения - это нормально
        pass
    except ConnectionResetError:
        print("Сервер отключился")
        run = False
    except Exception as e:
        print(f"Ошибка: {e}")

    pygame.display.update()
    clock.tick(60)  # Ограничение FPS

pygame.quit()
sock.close()