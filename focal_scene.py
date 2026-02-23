import math
import os
from src.base import BaseScene, Color
from src.shapes import Ball, Box, PlaneUV, Cylinder
from src.object_transform import ObjectTransform, Matrix3x3
from src.camera import ThinLensCamera
from src.vector3d import Vector3D
from src.light import PointLight
from src.materials import SimpleMaterialWithShadows, CheckerboardMaterial

class Scene(BaseScene):
    def __init__(self):
        super().__init__("Depth of Field - Sketch Mapping")

        self.background = Color(0.05, 0.05, 0.05)
        self.ambient_light = Color(0.15, 0.15, 0.15)
        self.max_depth = 3

        f_dist = float(os.environ.get('RAYTRACER_FOCAL_DISTANCE', 10.11))
        
        self.camera = ThinLensCamera(
            eye=Vector3D(0.0, -10.0, 3.0),
            look_at=Vector3D(0.0, 10.0, 3.0),
            up=Vector3D(0.0, 0.0, 1.0),
            fov=50,
            img_width=400,
            img_height=300,
            lens_radius=0.4, # Radio estático. Debes alterarlo independientemente para la tarea.
            focal_distance=f_dist
        )

        self.lights = [
            PointLight(position=Vector3D(0.0, -5.0, 15.0), color=Color(1.0, 1.0, 1.0), intensity=1.5),
            PointLight(position=Vector3D(-8.0, 5.0, 12.0), color=Color(0.8, 0.8, 0.9), intensity=1.0)
        ]

        floor_mat = CheckerboardMaterial(0.1, 0.8, 2.0, Color(0.8, 0.8, 0.8), Color(0.2, 0.2, 0.2))
        red_mat = SimpleMaterialWithShadows(0.1, 0.8, Color(0.9, 0.1, 0.1), 0.5, Color(1,1,1), 32)
        blue_mat = SimpleMaterialWithShadows(0.1, 0.8, Color(0.1, 0.3, 0.9), 0.5, Color(1,1,1), 32)
        gold_mat = SimpleMaterialWithShadows(0.1, 0.7, Color(0.8, 0.6, 0.1), 0.8, Color(1,1,1), 64)

        self.add(PlaneUV(Vector3D(0, 0, 0), Vector3D(0, 0, 1), Vector3D(0, 1, 0)), floor_mat)

        self.add(Ball(Vector3D(0.0, 0.0, 1.5), 1.5), red_mat)

        box_matrix = Matrix3x3.rotate_z(math.pi/4) @ Matrix3x3.rotate_x(math.pi/6)
        self.add(ObjectTransform(
            shape=Box(Vector3D(0,0,0), Vector3D(1.5, 1.5, 1.5)),
            matrix=box_matrix,
            translation=Vector3D(-4.0, 5.0, 5.0)
        ), blue_mat)

        cyl_matrix = Matrix3x3.rotate_y(math.pi/6) @ Matrix3x3.rotate_x(math.pi/4)
        self.add(ObjectTransform(
            shape=Cylinder(Vector3D(0,0,0), 1.0, 3.0),
            matrix=cyl_matrix,
            translation=Vector3D(4.0, 10.0, 6.0)
        ), gold_mat)
