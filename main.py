import os
import pygame as pag
import Utilidades as uti
import Utilidades_pygame as uti_pygame
from typing import override

from Utilidades_pygame.base_app_class import Base_class

from sound import Set_sounds

class RegeditChanger(Base_class):
    @override
    def otras_variables(self) -> None:

        self.sonidos = Set_sounds()

        self.lista_opciones_registro: list[str] = [
            {"option_text":"Barra lateral", "tooltip":"Crear Acceso directo a la carpeta deseada en la barra lateral del explorador de windos"},
            {"option_text":"Menu contextual", "tooltip":"Crear opciones nuevas en el menu contextual al hacer click derecho en el explorador de archivos de windows"},
            {"option_text":"Aplicacion de inicio", "tooltip":"Ejecuta el programa o archivo seleccionado al iniciar windows"},
        ]
        self.moving_tooltip = False


    @override
    def generate_objs(self) -> None:
        self.text_main_title = uti_pygame.Text("Regedit Changer", 24, self.config.fonts["mononoki"], (self.config.resolution[0]//2, 20))


        self.text_tooltip = uti_pygame.Text(
            "Tooltip", 12, self.config.fonts["mononoki"], (self.config.resolution[0]//4,-500), border_radius=30, max_width=150,
            border_width=2, border_color = 'black', padding=20, color_rect=(10,10,10)
            )
        self.text_tooltip.smothmove(1,1,1)

        self.bloque_main_opciones = uti_pygame.Bloque(
            (0,50),
            (self.config.resolution[0]//4, self.config.resolution[1]-50),
            dire='topleft',
            # border_width=2,
            border_color=(255,255,255,255),
        )

        self.bloque_main_opciones.add(
            uti_pygame.Text(
                "Opciones", 16, self.config.fonts["mononoki"], (self.config.resolution[0]//8,50),
                min_width=self.bloque_main_opciones.width-1,
            ),
            f'(self.rect.w/2,15)',
        )
        for i,x in enumerate(self.lista_opciones_registro):
            if i <= 0:
                top = 20*2
            else:
                top = self.bloque_main_opciones.list_objs[-1]["GUI"].rect.bottom
            self.bloque_main_opciones.add(
                uti_pygame.Button(
                    text=x["option_text"],
                    size=12, 
                    font=self.config.fonts["mononoki"], 
                    pos=(0,top), 
                    padding=5, 
                    dire='topleft', 
                    color='black', 
                    border_width=-1,
                    border_radius=-1, 
                    min_width=self.bloque_main_opciones.width,
                    max_width=self.bloque_main_opciones.width,
                    min_height=30,
                    with_rect=True, 
                    wrap=True,
                    color_rect_active='lightgreen',
                    func_to_hover=lambda top=top,txt=x["tooltip"]:self.spawn_tooltip(txt, (self.config.resolution[0]//4 +1,top+50), 'left'),
                    func_out_hover=lambda txt=x["tooltip"]: self.despawn_tooltip(txt),
                )
            , f'(0,{top})', clicking=True)

        self.lists_screens['main']["draw"] = [
            self.text_main_title, self.bloque_main_opciones,
        ]
        self.lists_screens['main']["update"] = self.lists_screens['main']["draw"]
        self.lists_screens['main']["click"] = [
            self.bloque_main_opciones
        ]

        self.overlay = [
            self.text_tooltip
        ]

    @override
    def otro_evento(self, actual_screen, evento):
        if evento.type == pag.KEYDOWN and evento.key == pag.K_ESCAPE:
            self.exit()
        elif evento.type == pag.MOUSEMOTION:
            if self.moving_tooltip:
                self.moving_tooltip = False

    def spawn_tooltip(self, tooltip: str, pos: tuple[int,int], dire: str = 'left') -> None:
        self.text_tooltip.text = tooltip
        self.text_tooltip.pos = pos
        self.text_tooltip.dire = dire
        self.moving_tooltip = True

    def despawn_tooltip(self, tooltip: str, **kwargs) -> None:
        if self.moving_tooltip:
            return
        self.text_tooltip.pos = (self.config.resolution[0]//4,-100)

if __name__ == '__main__':
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    config = uti_pygame.Config(
        title="Regedit Changer",
        author="Edouard Sandoval",
        my_company="Edouard Sandoval",
        copyright="2025 Edouard Sandoval",
        version="1.0",
        description="Un programa para cambiar valores en el registro de windows",
        fonts={"mononoki":r".\Data\fonts\mononoki Bold Nerd Font Complete Mono.ttf"},
        icon="./Data/images/Logo.png"
    )
    RegeditChanger(config=config)