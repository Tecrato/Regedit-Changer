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
            {"option_text":"Icono barra lateral", "tooltip":"Crear icono en la barra lateral"},
            {"option_text":"Opcion menu contextual", "tooltip":"Crear opcion en el menu contextual"},
            {"option_text":"Opcion para carpeta en el Menu contextual", "tooltip":"Crear acceso directo en\nel menu contextualal Hacer click derecho\nen una carpeta"},
        ]
    @override
    def generate_objs(self) -> None:
        self.text_main_title = uti_pygame.Text("Regedit Changer", 24, self.config.fonts["mononoki"], (self.config.resolution[0]//2, 20))
        self.text_main_otro1 = uti_pygame.Text("Otro", 24, self.config.fonts["mononoki"], (self.config.resolution[0]//2, 40))

        self.bloque_main_opciones = uti_pygame.Bloque(
            (0,50),
            (self.config.resolution[0]//4, self.config.resolution[1]-50),
            dire='topleft',
            border_width=2,
            border_color=(255,255,255,255),
        )

        for i,x in enumerate(self.lista_opciones_registro):
            self.bloque_main_opciones.add(
                uti_pygame.Button(
                    text=x["option_text"],
                    size=11, 
                    font=self.config.fonts["mononoki"], 
                    pos=(2,25*i + 20), 
                    padding=5, 
                    dire='left', 
                    color='white', 
                    border_width=-1, 
                    with_rect=True, 
                    toggle_rect=True,
                    color_rect_active='darkgreen',
                    func_to_hover=lambda i=i,txt=x["tooltip"]:self.spawn_tooltip(txt, (self.config.resolution[0]//4,25*i + 20 + self.bloque_main_opciones.top)),
                    func_out_hover=lambda txt=x["tooltip"]: self.despawn_tooltip(txt),
                )
            , f'(2,25*{i} + 20)', clicking=True)


        self.lists_screens['main']["draw"] = [
            self.text_main_title, self.text_main_otro1, self.bloque_main_opciones
        ]
        self.lists_screens['main']["update"] = self.lists_screens['main']["draw"]
        self.lists_screens['main']["click"] = [
            self.bloque_main_opciones
        ]

    @override
    def otro_evento(self, actual_screen, evento):
        if evento.type == pag.KEYDOWN and evento.key == pag.K_ESCAPE:
            self.exit()

    def spawn_tooltip(self, tooltip: str, pos: tuple[int,int], size: tuple[int,int]=(200,80), **kwargs) -> None:
        self.Mini_GUI_manager.add(
            uti_pygame.mini_GUI.more_objs.aviso1(pos=pos, dire='left', text=tooltip, size=size),
            group='tooltip_'+tooltip
        )
    def despawn_tooltip(self, tooltip: str, **kwargs) -> None:
        self.Mini_GUI_manager.clear_group('tooltip_'+tooltip)
        self.redraw = True

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