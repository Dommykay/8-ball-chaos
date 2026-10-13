import pygame
pygame.init()
from Spritesheet import *
from Converters import CentreOrigin
from FadeScreen import Fade
from Main import frame_rate, DEBUG

class Buttons:
    currently_instanciated = []
    button_id = 0
    def __init__(self, top_left_position = None, text = None, text_size = 90, bottom_right_position = None, width_and_height = None, centre_position = None, style = None, border = 2, shadow = False, enable = True, bg_enable = True):
        
        # Differenciate this button from others
        self.id = Buttons.button_id
        Buttons.button_id += 1
        
        #Giving the button a style
        if style is None:
            self.style = {
                "normal" : {
                    "border_colour" : [107,56,25],
                    "centre_colour" : [74,165,55],
                    "shadow_colour" : [45,120,35],
                    "text_colour" : [255,255,255]
                    },
                
                "hover" : {
                    "border_colour" : [137,60,16],
                    "centre_colour" : [72,193,54],
                    "shadow_colour" : [57,153,42],
                    "text_colour" : [255,255,255]
                    },
                
                "pressed" : {
                    "border_colour" : [86,47,24],
                    "centre_colour" : [45,86,38],
                    "shadow_colour" : [30,53,26],
                    "text_colour" : [255,255,255]
                    },
                "text_font" : "Resources\Text\Jersey_15\Jersey15-Regular.ttf"
                }
        else:
            self.style = style
        self.font = pygame.font.Font(self.style["text_font"], text_size)
        self.text = text
        self.bg_enable = bg_enable
        self.enable = enable
        # Takes two of either the bottom right position, width and height, top left position or centre position as it uses all three but can figure one out from the others
        if bottom_right_position is None and width_and_height is not None and top_left_position is not None:
            self.b_r_p = (top_left_position[0] + width_and_height[0],top_left_position[1] + width_and_height[1])
            self.w_h = width_and_height
            self.t_l_p = top_left_position
            self.cent_p = (top_left_position[0] + (width_and_height[0]/2), top_left_position[1] + (width_and_height[1]/2))
        elif width_and_height is None and bottom_right_position is not None and top_left_position is not None:
            self.w_h = (bottom_right_position[0] - top_left_position[0], bottom_right_position[1] - top_left_position[1])
            self.b_r_p = bottom_right_position
            self.t_l_p = top_left_position
            self.cent_p = (top_left_position[0] + (self.w_h[0]/2), top_left_position[1] + (self.w_h[1]/2))
        elif top_left_position is None and width_and_height is None and bottom_right_position is not None:
            self.t_l_p = (bottom_right_position[0] - width_and_height[0], bottom_right_position[1] - width_and_height[1])
            self.w_h = width_and_height
            self.b_r_p = bottom_right_position
            self.cent_p = (self.t_l_p[0] + (width_and_height[0]/2), self.t_l_p[1] + (width_and_height[1]/2))
        elif width_and_height is not None and centre_position is not None:
            self.t_l_p = (centre_position[0] - (width_and_height[0]/2), centre_position[1] - (width_and_height[1]/2))
            self.b_r_p = (centre_position[0] + (width_and_height[0]/2), centre_position[1] + (width_and_height[1]/2))
            self.w_h = width_and_height
            self.cent_p = centre_position
        else:
            self.bg_enable = False

        #Broke away from the naming convention for a minute with centre_position for hopefully obvious reasons

        self.shadow = shadow
        self.border = border
        
        # cs - Means current state and will let the return info method know whether the it should output the normal, hover or pressed state of the button.
        # 0 means normal, 1 means hover, 2 means pressed.
        self.cs = 0

        # Bake positions and text info so it does not get re-calculated every frame
        if self.text != None:
            self.BakeTextRenderInfo()
        self.BakeButtonRenderInfo()
        
        # Make the instanciated object accessible from a list that is accessible via classmethod.
        Buttons.currently_instanciated.append(self)
        
    @classmethod
    def ReturnInstanciatedButtons(cls, button_to_return_id = None):
        if button_to_return_id is None:
            return cls.currently_instanciated
        else:
            for instance in cls.currently_instanciated:
                if instance.id == button_to_return_id:
                    return instance
        
    def BakeTextRenderInfo(self):
        # Assume not pressed by default

        if self.cs == 1:
            text = self.font.render(self.text, True, self.style["hover"]["text_colour"])
        elif self.cs == 2:
            text = self.font.render(self.text, True, self.style["pressed"]["text_colour"])
        else:
            text = self.font.render(self.text, True, self.style["normal"]["text_colour"])

        size = self.font.size(self.text)
        text_blit_location = (self.t_l_p[0] + self.w_h[0] / 2 - size[0] / 2, self.t_l_p[1] + self.w_h[1] / 2 - size[1] / 2)
        
        self.button_text_baked = (text, text_blit_location)

    def BakeButtonRenderInfo(self):
        # Calculating button sizes
        half_border = self.border / 2
        outer = pygame.Rect(self.t_l_p[0] - half_border,self.t_l_p[1] - half_border, self.w_h[0] + self.border, self.w_h[1] + self.border)

        inner = pygame.Rect(self.t_l_p[0] + half_border,self.t_l_p[1] + half_border, self.w_h[0] - self.border, self.w_h[1] - self.border)

        if self.shadow:
            shadow_rect_1 = pygame.Rect(self.t_l_p[0] + half_border, self.b_r_p[1] - self.border, self.w_h[0] - self.border, half_border)
            shadow_rect_2 = pygame.Rect(self.b_r_p[0] - self.border, self.t_l_p[1] + half_border, half_border, self.w_h[1] - self.border)
        else:
            shadow_rect_1, shadow_rect_2 = None, None

        self.button_positions_baked = (outer, inner, shadow_rect_1, shadow_rect_2)
        

    def Render(self, surface):
        if self.enable:
            if self.bg_enable:
                if self.cs == 1:
                    pygame.draw.rect(surface, self.style["hover"]["border_colour"], self.button_positions_baked[0])
                    pygame.draw.rect(surface, self.style["hover"]["centre_colour"], self.button_positions_baked[1])
                    if self.shadow:
                        pygame.draw.rect(surface, self.style["hover"]["shadow_colour"], self.button_positions_baked[2])
                        pygame.draw.rect(surface, self.style["hover"]["shadow_colour"], self.button_positions_baked[3])
                elif self.cs == 2:
                    pygame.draw.rect(surface, self.style["pressed"]["border_colour"], self.button_positions_baked[0])
                    pygame.draw.rect(surface, self.style["pressed"]["centre_colour"], self.button_positions_baked[1])
                    if self.shadow:
                        pygame.draw.rect(surface, self.style["pressed"]["shadow_colour"], self.button_positions_baked[2])
                        pygame.draw.rect(surface, self.style["pressed"]["shadow_colour"], self.button_positions_baked[3])
                else:
                    pygame.draw.rect(surface, self.style["normal"]["border_colour"], self.button_positions_baked[0])
                    pygame.draw.rect(surface, self.style["normal"]["centre_colour"], self.button_positions_baked[1])
                    if self.shadow:
                        pygame.draw.rect(surface, self.style["normal"]["shadow_colour"], self.button_positions_baked[2])
                        pygame.draw.rect(surface, self.style["normal"]["shadow_colour"], self.button_positions_baked[3])
            if self.text != None:
                surface.blit(self.button_text_baked[0], self.button_text_baked[1])
    
    def Enable(self):
        self.enable = True
    
    def Disable(self):
        self.enable = False
    
    def ToggleEnable(self):
        self.enable = not self.enable
    

    def BeingHoveredOver(self, point):
        if self.button_positions_baked[0].collidepoint(point):
            return True
        else:
            return False

    def ForgetThis(cls, self):
        new_instanciated_list = []
        for button in cls.currently_instanciated:
            if button.id != self.id:
                new_instanciated_list.append(button)
        cls.currently_instanced = new_instanciated_list

    @classmethod
    def ForgetAll(cls):
        cls.currently_instanced = []
        cls.button_id = 0

    @classmethod
    def CurrentlyCollidingWithPoint(cls, point):
        hovered_over = []
        for button in cls.currently_instanciated:
            if button.BeingHoveredOver(point):
                hovered_over.append(button.id)
        return hovered_over

class Balls:
    ball_id = 0
    balls_sprite_sheet = SpriteSheet("Resources\In_Game_Assets\Balls.png")
    def __init__(self, texture, position, ball_type = "White", size = None, mass = 160, velocity = [0.0,0.0], enabled = True, shadow = "Resources\In_Game_Assets\Ball_shadow.png"):
        self.ball_type = ball_type
        self.velocity = velocity
        self.mass = mass
        self.org_mass = mass
        self.texture_name = texture
        self.texture = Balls.balls_sprite_sheet.ReturnSpriteAndData("Balls",texture + ".png")

        if size is not None:
            self.size = size
        else:
            self.size = self.texture.get_width() / 2  

        self.org_size = self.size
        self.shadow = pygame.image.load(shadow)
        self.shadow.set_alpha(64)
        self.position = [position[0] - self.size, position[1] - self.size]
        self.old_position = position

        self.enabled = enabled
        self.is_falling = False
        self.picked_up = False
        self.progress = 255
        self.fallen_before = False
        self.ball_id = Balls.ball_id
        Balls.ball_id += 1

    def __RecursiveCollisionCheckWall(self, rect, old_position, ball_vector, level_of_accuracy, max_level_of_accuracy):
        progress = 0
        if level_of_accuracy > 1:
            ball_vector = (ball_vector[0]/2,ball_vector[1]/2)
            mid_position = (old_position[0] + ball_vector[0],old_position[1] + ball_vector[1])
            self.collision_rect = pygame.Rect((mid_position[0] + ball_vector[0],mid_position[1] + ball_vector[1]),(self.size * 2,self.size * 2))
            if rect.colliderect(self.collision_rect):
                progress = self.__RecursiveCollisionCheckWall(rect, old_position, ball_vector, level_of_accuracy - 1, max_level_of_accuracy)
                return progress
            else:
                progress = self.__RecursiveCollisionCheckWall(rect, mid_position, ball_vector, level_of_accuracy - 1, max_level_of_accuracy)
                return progress + 1/2**(max_level_of_accuracy-level_of_accuracy)
        else:
            return progress


    def DetermineTimeOfCollisionWall(self, rect, rect_origin_top_left = True):
        max_level_of_accuracy, level_of_accuracy = 10,10
        position = self.position
        old_position = self.old_position
        if rect_origin_top_left:
            position = (self.position[0] - (self.size/2),self.position[1] + (self.size/2))
            old_position = (self.old_position[0] - (self.size/2),self.old_position[1] + (self.size/2))
        ball_vector = (position[0] - old_position[0],position[1] - old_position[1])
        self.old_collision_rect = pygame.Rect((self.position[0],self.position[1]),(self.size * 2,self.size * 2))
        return self.__RecursiveCollisionCheckWall(rect, old_position, ball_vector, level_of_accuracy, max_level_of_accuracy)
    

    def __RecursiveCollisionCheckBall(self,old_position, ball_vector, col_ball_old_pos, col_ball_vector, col_ball_size, level_of_accuracy, max_level_of_accuracy):
        progress = 0
        if level_of_accuracy > 1:
            ball_vector = (ball_vector[0]/2,ball_vector[1]/2)
            col_ball_vector = (col_ball_vector[0]/2,col_ball_vector[1]/2)
            mid_position = (old_position[0] + ball_vector[0],old_position[1] + ball_vector[1])
            col_ball_mid_pos = (col_ball_old_pos[0] + col_ball_vector[0],col_ball_old_pos[1] + col_ball_vector[1])
            mid_colliding_vector = (col_ball_mid_pos[0] - mid_position[0], col_ball_mid_pos[1] - mid_position[1])
            distance = mid_colliding_vector[0]**2 + mid_colliding_vector[1]**2
            min_non_collision_distance = self.size**2 + col_ball_size**2
            if distance > min_non_collision_distance:
                progress = self.__RecursiveCollisionCheckBall(old_position, ball_vector, col_ball_old_pos, col_ball_vector, col_ball_size, level_of_accuracy - 1, max_level_of_accuracy)
                return progress
            else:
                progress = self.__RecursiveCollisionCheckBall(mid_position, ball_vector, col_ball_mid_pos, col_ball_vector, col_ball_size, level_of_accuracy - 1, max_level_of_accuracy)
                return progress + 1/2**(max_level_of_accuracy-level_of_accuracy)
        else:
            return progress



    def UnCollideBalls(self, colliding_ball):
        max_level_of_accuracy, level_of_accuracy = 10,10
        position = (self.position[0] - (self.size/2),self.position[1] + (self.size/2))
        old_position = (self.old_position[0] - (self.size/2),self.old_position[1] + (self.size/2))
        col_ball_pos = (colliding_ball.position[0] - (colliding_ball.size/2), colliding_ball.position[1] - (colliding_ball.size/2))
        col_ball_old_pos = (colliding_ball.old_position[0] - (colliding_ball.size/2),colliding_ball.old_position[1] + (colliding_ball.size/2))
        ball_vector = (position[0] - old_position[0],position[1] - old_position[1])
        col_ball_vector = (col_ball_pos[0] - col_ball_old_pos[0],col_ball_pos[1] - col_ball_old_pos[1])
        mult = self.__RecursiveCollisionCheckBall(old_position, ball_vector, col_ball_old_pos, col_ball_vector, colliding_ball.size, level_of_accuracy, max_level_of_accuracy)
        new_pos = [self.old_position[0] + (ball_vector[0] * mult), self.old_position[1] + (ball_vector[1] * mult)]
        new_col_pos = [colliding_ball.old_position[0] + (col_ball_vector[0] * mult), colliding_ball.old_position[1] + (col_ball_vector[1] * mult)]
        return new_pos, new_col_pos

    def Render(self, surface):
        if self.is_falling:
            if DEBUG:
                print(self.progress, self.ball_id)
            temp_texture = pygame.transform.scale(self.texture, (self.size*2 * (self.progress/255),self.size*2 * (self.progress/255)))
            temp_texture.set_alpha(self.progress)
            temp_shadow = pygame.transform.scale(self.shadow, (self.size*2 * (self.progress/255),self.size*2 * (self.progress/255)))
            temp_shadow.set_alpha((self.progress/255)*64)
            surface.blit(temp_shadow,(self.position[0] + (self.size*((255-self.progress)/255)) + 3, self.position[1] + (self.size*((255-self.progress)/255)) + 3))
            surface.blit(temp_texture,(self.position[0] + (self.size*((255-self.progress)/255)),self.position[1] + (self.size*((255-self.progress)/255))))
            self.velocity *= (1 - 1/frame_rate*15)
        if self.enabled or (self.ball_type == "White" and self.picked_up):
            temp_texture = pygame.transform.scale(self.texture, (self.size*2,self.size*2))
            temp_shadow = pygame.transform.scale(self.shadow, (self.size*2,self.size*2))
            surface.blit(temp_shadow,(self.position[0] + 3, self.position[1] + 3))
            surface.blit(temp_texture,self.position)

    def ChangeSize(self, size):
        self.size = size
        self.texture = pygame.transform.scale(self.texture, (size,size))
    
    def ResetSize(self):
        self.size = self.org_size
        self.texture = pygame.transform.scale(self.texture, (self.size,self.size))

    def ProgressFall(self):
        if not self.picked_up:
            if not self.fallen_before:
                if DEBUG:
                    print("Entered the except")
                self.fall_progression = Fade(time_in_seconds= 0.6,fade_in=True, tween= "quadratic_in", frame_rate= frame_rate)
                self.enabled = False
                self.is_falling = True
                self.fallen_before = True
            else:
                if len(self.fall_progression) > 0:
                    self.progress = self.fall_progression.pop()
                    if DEBUG:
                        print(self.progress, self.ball_id)
                else:
                    if self.ball_type == "White":
                        self.picked_up = True
                    self.is_falling = False
                if DEBUG:
                    print(self.fall_progression)
                    print(self.progress)
                    print(self.ball_id, self.is_falling, self.progress)
        


class Player:
    cues_sprite_sheet = SpriteSheet("Resources\In_Game_Assets\Cues.png")
    frames_sprite_sheet = SpriteSheet("Resources\In_Game_Assets\PFP_frames.png")
    BFG = cues_sprite_sheet.ReturnSpriteAndData("Cues","BFG.png")
    BFG = pygame.transform.scale(BFG, (BFG.get_width()*4,BFG.get_height()*4))
    def __init__(self, player_num, ball_type = None, cue_name = "Default", pfp = pygame.image.load("Resources\Menu\DefaultPFP.png").convert()):
        self.ball_type = ball_type
        self.player_num = player_num
        self.cue_name = cue_name
        self.cue_texture = Player.cues_sprite_sheet.ReturnSpriteAndData("Cues",cue_name + ".png")
        self.frame_texture = Player.frames_sprite_sheet.ReturnSpriteAndData("Frames","Player_" + str(player_num) + ".png")
        self.frame_texture = pygame.transform.scale(self.frame_texture, (120,120))
        self.pfp = pygame.transform.scale(pfp, (96,96))
        self.frame_shadow = pygame.image.load("Resources\In_Game_Assets\PFP_frames_shadow.png").convert_alpha()
        self.frame_shadow = pygame.transform.scale(self.frame_shadow, (120,120))
        self.frame_shadow.set_alpha(64)
        self.cue_texture = pygame.transform.scale(self.cue_texture, (self.cue_texture.get_width()*4,self.cue_texture.get_height()*4))
        self.cue_angle = 0
    def ReturnRotatedCue(self,angle):
        return pygame.transform.rotate(self.cue_texture, angle)
    def ReturnRotatedBFG(self,angle):
        return pygame.transform.rotate(Player.BFG, angle)

        