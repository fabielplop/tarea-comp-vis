import math
from src.base import BaseScene, Color
from src.shapes import PlaneUV, Box, Cylinder
from src.camera import Camera
from src.vector3d import Vector3D
from src.light import AreaLight
from src.materials import SimpleMaterialWithShadows, CheckerboardMaterial

class Scene(BaseScene):
    def __init__(self):
        super().__init__("figuras")

        self.background = Color(0.1, 0.1, 0.12)
        self.ambient_light = Color(0.1, 0.1, 0.1)
        self.max_depth = 5 

        self.camera = Camera(
            eye=Vector3D(12, 0, 5),
            look_at=Vector3D(0, 0, 1.5),
            up=Vector3D(0, 0, 1),
            fov=35,
            img_width=400,
            img_height=300
        )

        self.lights = [
            AreaLight(
                position=Vector3D(6, -6, 8),
                look_at=Vector3D(0, 0, 0),
                up=Vector3D(0, 0, 1),
                width=2.5,
                height=2.5,
                color=Color(1, 1, 1),
                intensity=2.2
            )
        ]

        cyl_material = SimpleMaterialWithShadows(
            ambient_coefficient=0.1, diffuse_coefficient=0.7, diffuse_color=Color(0.8, 0.2, 0.2),
            specular_coefficient=0.5, specular_color=Color(1, 1, 1), specular_shininess=32
        )
        self.add(Cylinder(
            center=Vector3D(0, -2.2, 1.5), 
            radius=1.2,
            height=3.0
        ), cyl_material)

        box_material = SimpleMaterialWithShadows(
            ambient_coefficient=0.1, diffuse_coefficient=0.8, diffuse_color=Color(0.2, 0.4, 0.8),
            specular_coefficient=0.5, specular_color=Color(1, 1, 1), specular_shininess=64
        )
        self.add(Box(
            center=Vector3D(0, 2.2, 1.0), 
            size=Vector3D(2.0, 2.0, 2.0)
        ), box_material)

        floor_material = CheckerboardMaterial(
            ambient_coefficient=0.5, diffuse_coefficient=0.8, square_size=2.0,
            white_color=Color(0.8, 0.8, 0.8), black_color=Color(0.2, 0.2, 0.2)
        )
        self.add(PlaneUV(point=Vector3D(0, 0, 0), normal=Vector3D(0, 0, 1), forward_direction=Vector3D(1, 1, 0)), floor_material)
