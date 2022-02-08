import string, StartUp, Game, pygame
from KeyboardController import *


class Button(object):
    def __init__(self, rect, command, **kwargs):
        self.rect = pygame.Rect(rect)
        self.command = command
        self.clicked = False
        self.hovered = False
        self.hover_text = None
        self.clicked_text = None
        self.process_kwargs(kwargs)
        self.render_text()

    def process_kwargs(self, kwargs):
        settings = {
            "color": pygame.Color('red'),
            "text": None,
            "font": None,  # pygame.font.Font(None,16),
            "call_on_release": True,
            "hover_color": None,
            "clicked_color": None,
            "font_color": pygame.Color("white"),
            "hover_font_color": None,
            "clicked_font_color": None,
            "click_sound": None,
            "hover_sound": None,
            'border_color': pygame.Color('black'),
            'border_hover_color': pygame.Color('yellow'),
            'disabled': False,
            'disabled_color': pygame.Color('grey'),
            'radius': 3,
        }
        for kwarg in kwargs:
            if kwarg in settings:
                settings[kwarg] = kwargs[kwarg]
            else:
                raise AttributeError("{} has no keyword: {}".format(self.__class__.__name__, kwarg))
        self.__dict__.update(settings)

    def render_text(self):
        if self.text:
            if self.hover_font_color:
                color = self.hover_font_color
                self.hover_text = self.font.render(self.text, True, color)
            if self.clicked_font_color:
                color = self.clicked_font_color
                self.clicked_text = self.font.render(self.text, True, color)
            self.text = self.font.render(self.text, True, self.font_color)

    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.on_click(event)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.on_release(event)

    def on_click(self, event):
        if self.rect.collidepoint(event.pos):
            self.clicked = True
            if not self.call_on_release:
                self.function()

    def on_release(self, event):
        if self.clicked and self.call_on_release:
            # if user is still within button rect upon mouse release
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.command()
        self.clicked = False

    def check_hover(self):
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            if not self.hovered:
                self.hovered = True
                if self.hover_sound:
                    self.hover_sound.play()
        else:
            self.hovered = False

    def draw(self, surface):
        color = self.color
        text = self.text
        border = self.border_color
        self.check_hover()
        if not self.disabled:
            if self.clicked and self.clicked_color:
                color = self.clicked_color
                if self.clicked_font_color:
                    text = self.clicked_text
            elif self.hovered and self.hover_color:
                color = self.hover_color
                if self.hover_font_color:
                    text = self.hover_text
            if self.hovered and not self.clicked:
                border = self.border_hover_color
        else:
            color = self.disabled_color

        # if not self.rounded:
        #    surface.fill(border,self.rect)
        #    surface.fill(color,self.rect.inflate(-4,-4))
        # else:
        if self.radius:
            rad = self.radius
        else:
            rad = 0
        self.round_rect(surface, self.rect, border, rad, 1, color)
        if self.text:
            text_rect = text.get_rect(center=self.rect.center)
            surface.blit(text, text_rect)

    def round_rect(self, surface, rect, color, rad=20, border=0, inside=(0, 0, 0, 0)):
        rect = pygame.Rect(rect)
        zeroed_rect = rect.copy()
        zeroed_rect.topleft = 0, 0
        image = pygame.Surface(rect.size).convert_alpha()
        image.fill((0, 0, 0, 0))
        self._render_region(image, zeroed_rect, color, rad)
        if border:
            zeroed_rect.inflate_ip(-2 * border, -2 * border)
            self._render_region(image, zeroed_rect, inside, rad)
        surface.blit(image, rect)

    def _render_region(self, image, rect, color, rad):
        corners = rect.inflate(-2 * rad, -2 * rad)
        for attribute in ("topleft", "topright", "bottomleft", "bottomright"):
            pygame.draw.circle(image, color, getattr(corners, attribute), rad)
        image.fill(color, rect.inflate(-2 * rad, 0))
        image.fill(color, rect.inflate(0, -2 * rad))

    def update(self):
        # for completeness
        pass




def scaleImage(image, screenW, screenH):
    oldWidth, oldHeight = pygame.Surface.get_size(image)
    newWidth = int(oldWidth * (1920 / screenW))
    newHeight = int(oldHeight * (1080 / screenW))
    newImage = pygame.transform.scale(image, (newWidth, newHeight))
    return newImage

def main():
    screenW, screenH, fps = StartUp.giveDisplayInfo()
    pygame.init()
    screen, clock = StartUp.start()
    done = False

    btn_settings = {
        "clicked_font_color": (0, 0, 0),
        "hover_font_color": (0, 0, 0),
        'font': pygame.font.Font(None, 48),
        'font_color': (255, 255, 255),
        'border_color': (0, 0, 0),
    }


    btn = Button(rect=((screenW // 2) - 200, (screenH * .37) - 40, 400, 80), command=lambda: Game.main(screen, screenW, screenH, fps, clock), text='Enter the ARENA', **btn_settings)
    textLogo = scaleImage(pygame.image.load('Images/TextLogo.png'), screenW, screenH)
    logo = scaleImage(pygame.image.load('Images/Logo.png'), screenW, screenH)
    usingControllers = (pygame.joystick.get_count() == 2)
    if usingControllers:
        controller = pygame.joystick.Joystick(0)
        controller2 = pygame.joystick.Joystick(1)
        controller.init()
        controller2.init()
    else:
        controller = KeyboardController(pygame.K_q, pygame.K_e, pygame.K_SPACE, pygame.K_a,
                                        pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_LSHIFT, pygame.K_x)
        controller2 = KeyboardController(pygame.K_COMMA, pygame.K_PERIOD, pygame.K_SLASH, pygame.K_LEFT,
                                        pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_RSHIFT, pygame.K_m)
    
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or pygame.key.get_pressed()[27]:
                done = True
            btn.get_event(event)

        if usingControllers:
            if controller.get_button(0) or controller2.get_button(0):
                btn.command()
        else:
            if any(pygame.key.get_pressed()):
                btn.command()
                
        btn.draw(screen)
        screen.blit(textLogo, ((screenW // 2) - (textLogo.get_width() // 2), 0))
        screen.blit(logo, ((screenW // 2) - (logo.get_width() // 2), (screenH * 1/2)))
        pygame.display.update()
    pygame.quit()

main()
