# author: Romain Carl
# created on: 03/06/2022
# edited by:

# description:
# A class that allows setting an HDRI image as world texture


import bpy
from math import radians

class Background:    
    def __init__(self, 
                 hdri_path: str):
        self.world = bpy.data.worlds["World"]
        self.world.use_nodes = True
        node_tree = self.world.node_tree
    
        environment_texture_node = node_tree.nodes.new(type="ShaderNodeTexEnvironment")
        
        texture_coordinates_node = node_tree.nodes.new(type="ShaderNodeTexCoord")
        mapping_node = node_tree.nodes.new(type="ShaderNodeMapping")
    
        node_tree.links.new(texture_coordinates_node.outputs["Generated"], mapping_node.inputs["Vector"])
        node_tree.links.new(mapping_node.outputs["Vector"], environment_texture_node.inputs["Vector"])
        node_tree.links.new(environment_texture_node.outputs["Color"], node_tree.nodes["Background"].inputs["Color"])
        
        self.environment_texture_node = environment_texture_node
        self.mapping_node = mapping_node
        
        self.set_image(hdri_path)
    
    # sets the background image to image specified by hdri_path    
    def set_image(self, hdri_path: str) -> None:
        self.environment_texture_node.image = bpy.data.images.load(hdri_path)
        
    # rotates background image around global Z axis
    # angle: degree, image moves to the right if positive
    def pan_horizontal(self, angle: float) -> None:
        self.mapping_node.inputs["Rotation"].default_value[2] += radians(angle)
        
    # rotates background image around global Y axis
    # can only be sensibly used when camera is located on X axis
    # angle: degree, image moves down if positive
    def pan_vertical(self, angle: float) -> None:
        self.mapping_node.inputs["Rotation"].default_value[1] += radians(angle)

    # static function to set the background brightness (parameter has to be a positiv value)
    def setBrightness(self, newStrength : float) -> None:
        if newStrength == None:
            print("setBackgroundStrength: parameter is None")
        elif newStrength < 0:
            print("Background strength can only have positiv values")
        else:
            self.world.node_tree.nodes['Background'].inputs[1].default_value = newStrength

