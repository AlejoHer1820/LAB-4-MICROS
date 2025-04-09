import tkinter as tk
from gpiozero import OutputDevice, Button
from time import sleep

class Elevator:
    def __init__(self, root):
        self.root = root
        self.root.title("Control de Ascensor")
        self.root.geometry("400x300")

        # Pines del motor (Puente H)
        self.motor_subir = OutputDevice(24)  # Motór sube
        self.motor_bajar = OutputDevice(23)  # Motor baja

        # Sensores de piso con lógica invertida (False = presente, True = ausente)
        self.sensor_p1 = Button(5, pull_up=True)   # Piso 1
        self.sensor_p2 = Button(6, pull_up=True)   # Piso 2
        self.sensor_p3 = Button(13, pull_up=True)  # Piso 3

        # Mapear sensores a pisos
        self.sensores_pisos = {
            1: self.sensor_p1,
            2: self.sensor_p2,
            3: self.sensor_p3
        }

        # Detectar piso actual al inicio
        self.current_floor = self.detect_current_floor()
        
        # Interfaz gráfica
        self.label = tk.Label(self.root, text=f"Piso actual: {self.current_floor}", font=("Arial", 14))
        self.label.pack(pady=10)
        
        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.pack(pady=20)

        for i in range(1, 4):
            btn = tk.Button(self.buttons_frame, text=f"Piso {i}", font=("Arial", 12), command=lambda i=i: self.go_to_floor(i))
            btn.grid(row=0, column=i-1, padx=10)

    def detect_current_floor(self):
        for piso, sensor in self.sensores_pisos.items():
            if not sensor.is_pressed:  # False = el ascensor está en ese piso
                return piso
        return 1  # En caso de fallo, asumir piso 1

    def move_up(self):
        self.motor_subir.on()
        self.motor_bajar.off()

    def move_down(self):
        self.motor_subir.off()
        self.motor_bajar.on()

    def stop_motor(self):
        self.motor_subir.off()
        self.motor_bajar.off()

    def go_to_floor(self, target_floor):
        if target_floor < 1 or target_floor > 3:
            return

        if target_floor > self.current_floor:
            self.move_up()
            while self.sensores_pisos[target_floor].is_pressed:
                sleep(0.1)
        elif target_floor < self.current_floor:
            self.move_down()
            while self.sensores_pisos[target_floor].is_pressed:
                sleep(0.1)

        self.stop_motor()
        self.current_floor = target_floor
        self.label.config(text=f"Piso actual: {self.current_floor}")

if __name__ == "__main__":
    root = tk.Tk()
    elevator = Elevator(root)
    root.mainloop()
