
import math
from src.base import BaseScene, Color
from src.shapes import PlaneUV
from src.object_transform import ObjectTransform, Matrix3x3
from src.surfaces import MitchelSurface, HeartSurface
from src.camera import Camera
from src.vector3d import Vector3D
from src.light import PointLight
from src.materials import SimpleMaterialWithShadows, CheckerboardMaterial

class Scene(BaseScene):
    def __init__(self):
        super().__init__("Algebraic Surfaces")

        self.background = Color(0.05, 0.05, 0.05)
        self.ambient_light = Color(0.1, 0.1, 0.1)
        self.max_depth = 4

        self.camera = Camera(
            eye=Vector3D(0.0, -10.0, 1.5),
            look_at=Vector3D(0.0, 0.0, 0.5),
            up=Vector3D(0.0, 0.0, 1.0),
            fov=45,
            img_width=400,
            img_height=300
        )

        self.lights = [
            PointLight(position=Vector3D(-4.0, -6.0, 6.0), color=Color(1.0, 1.0, 1.0), intensity=1.5),
            PointLight(position=Vector3D(4.0, -6.0, 6.0), color=Color(1.0, 1.0, 1.0), intensity=1.5)
        ]

        floor_mat = CheckerboardMaterial(
            ambient_coefficient=0.1, diffuse_coefficient=0.6, square_size=1.0,
            white_color=Color(0.7, 0.7, 0.7), black_color=Color(0.2, 0.2, 0.2)
        )

        red_mat = SimpleMaterialWithShadows(
            ambient_coefficient=0.1, diffuse_coefficient=0.8, diffuse_color=Color(0.8, 0.05, 0.05),
            specular_coefficient=0.6, specular_color=Color(1.0, 0.8, 0.8), specular_shininess=64
        )

        metal_mat = SimpleMaterialWithShadows(
            ambient_coefficient=0.1, diffuse_coefficient=0.5, diffuse_color=Color(0.6, 0.6, 0.7),
            specular_coefficient=0.9, specular_color=Color(1.0, 1.0, 1.0), specular_shininess=128
        )

        # piso
        self.add(PlaneUV(point=Vector3D(0, 0, -1.5), normal=Vector3D(0, 0, 1), forward_direction=Vector3D(0, 1, 0)), floor_mat)

        # corazon
        heart_matrix = Matrix3x3.scale(1.2, 1.2, 1.2)
        self.add(ObjectTransform(
            shape=HeartSurface(),
            matrix=heart_matrix,
            translation=Vector3D(-2.0, 0.0, 0.0)
        ), red_mat)

        # mitchel
        mitchel_matrix = Matrix3x3.scale(1.0, 1.0, 1.0)
        self.add(ObjectTransform(
            shape=MitchelSurface(),
            matrix=mitchel_matrix,
            translation=Vector3D(2.0, 0.0, 0.0)
        ), metal_mat)
