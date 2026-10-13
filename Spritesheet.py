import pygame
import json

# I USED THIS TUTORIAL TO HELP ME MAKE SPRITESHEETS https://www.youtube.com/watch?v=ePiMYe7JpJo

class SpriteSheet:
    def __init__(self, sprite_sheet_file_path, sprite_sheet_json = "Resources\In_Game_Assets\Textures_JSON.json"):
        self.sprite_sheet_file_path = sprite_sheet_file_path
        self.sprite_sheet = pygame.image.load(sprite_sheet_file_path).convert()
        open_file = open(sprite_sheet_json)
        self.data = json.load(open_file)
        open_file.close()
        
    def GetSpriteFromSheet(self, top_left_x, top_left_y, width, height):
        sprite = pygame.Surface((width, height))
        sprite.set_colorkey((0,0,0))
        sprite.blit(self.sprite_sheet,(0,0),(top_left_x, top_left_y, width, height))
        return sprite
    
    def ReturnSpriteAndData(self, sprite_category, sprite_name):
        sprite = self.data[sprite_category][sprite_name]["data"]
        return self.GetSpriteFromSheet(sprite["top_left_x"], sprite["top_left_y"], sprite["width"], sprite["height"])