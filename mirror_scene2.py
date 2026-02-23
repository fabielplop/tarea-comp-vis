import math
import os
from src.base import BaseScene, Color
from src.shapes import Ball, Box, PlaneUV, Cylinder
from src.object_transform import ObjectTransform, Matrix3x3
from src.camera import Camera
from src.vector3d import Vector3D
from src.light import PointLight
from src.materials import SimpleMaterialWithShadows, CheckerboardMaterial
from src.materials import MirrorMaterial

class Scene(BaseScene):
    def __init__(self):
        super().__init__("espejo tunel2")

        self.background = Color(0.01, 0.01, 0.01)
        self.ambient_light = Color(0.1, 0.1, 0.1)
        self.max_depth = int(os.environ.get('RAYTRACER_MAX_DEPTH', 12)) 

        self.camera = Camera(
            eye=Vector3D(0.0, -8.0, 5.0),
            look_at=Vector3D(0.0, 15.0, 1.5),
            up=Vector3D(0.0, 0.0, 1.0),
            fov=60,
            img_width=500,
            img_height=400
        )

        self.lights = [
            PointLight(position=Vector3D(0.0, -5.0, 8.0), color=Color(1.0, 1.0, 1.0), intensity=1.2),
            PointLight(position=Vector3D(0.0, 5.0, 8.0), color=Color(0.9, 0.9, 1.0), intensity=1.2),
            PointLight(position=Vector3D(0.0, 15.0, 8.0), color=Color(1.0, 0.8, 0.6), intensity=1.5)
        ]

        mirror_mat = MirrorMaterial(reflection_coefficient=0.95) # 95% de reflejo para que se oscurezca al fondo
        floor_mat = CheckerboardMaterial(0.1, 0.7, 2.0, Color(0.9, 0.9, 0.9), Color(0.1, 0.1, 0.1))

        red_mat = SimpleMaterialWithShadows(0.1, 0.8, Color(0.9, 0.1, 0.1), 0.7, Color(1,1,1), 64)
        blue_mat = SimpleMaterialWithShadows(0.1, 0.8, Color(0.1, 0.2, 0.9), 0.7, Color(1,1,1), 64)
        gold_mat = SimpleMaterialWithShadows(0.1, 0.6, Color(0.8, 0.6, 0.1), 0.9, Color(1,1,1), 128)

        # piso
        self.add(PlaneUV(Vector3D(0, 0, 0), Vector3D(0, 0, 1), Vector3D(0, 1, 0)), floor_mat)

        # espejo frontal
        self.add(ObjectTransform(
            shape=Box(Vector3D(0,0,0), Vector3D(2.0, 2.0, 2.0)),
            matrix=Matrix3x3.scale(12.0, 0.1, 12.0),
            translation=Vector3D(0.0, 20.0, 10.0)
        ), mirror_mat)

        # espejo atras
        self.add(ObjectTransform(
            shape=Box(Vector3D(0,0,0), Vector3D(2.0, 2.0, 2.0)),
            matrix=Matrix3x3.scale(12.0, 0.1, 12.0),
            translation=Vector3D(0.0, -12.0, 10.0)
        ), mirror_mat)

        box_shape = Box(Vector3D(0,0,0), Vector3D(2.0, 2.0, 2.0))
        cyl_shape = Cylinder(Vector3D(0,0,0), 1.0, 2.0)

        m_box_top = Matrix3x3.rotate_y(-math.pi/4) @ Matrix3x3.scale(0.5, 0.5, 2.0)
        self.add(ObjectTransform(
            shape=box_shape,
            matrix=m_box_top,
            translation=Vector3D(-3.0, 5.0, 5.0)
        ), red_mat)

        m_box_bot = Matrix3x3.rotate_y(math.pi/4) @ Matrix3x3.scale(0.5, 0.5, 2.0)
        self.add(ObjectTransform(
            shape=box_shape,
            matrix=m_box_bot,
            translation=Vector3D(-3.0, 5.0, 1.5)
        ), red_mat)

        m_cyl_top = Matrix3x3.rotate_y(math.pi/4) @ Matrix3x3.scale(0.6, 0.6, 2.0)
        self.add(ObjectTransform(
            shape=cyl_shape,
            matrix=m_cyl_top,
            translation=Vector3D(3.0, 5.0, 5.0)
        ), gold_mat)

        m_cyl_bot = Matrix3x3.rotate_y(-math.pi/4) @ Matrix3x3.scale(0.6, 0.6, 2.0)
        self.add(ObjectTransform(
            shape=cyl_shape,
            matrix=m_cyl_bot,
            translation=Vector3D(3.0, 5.0, 1.5)
        ), gold_mat)
