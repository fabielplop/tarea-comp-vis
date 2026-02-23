import math
from src.base import BaseScene, Color
from src.shapes import Ball, PlaneUV, Box, Cylinder
from src.object_transform import ObjectTransform, Matrix3x3
from src.camera import Camera
from src.vector3d import Vector3D
from src.light import PointLight
from src.materials import SimpleMaterialWithShadows, CheckerboardMaterial

class Scene(BaseScene):
    def __init__(self):
        super().__init__("obj transform test")

        self.background = Color(0.1, 0.1, 0.12)
        self.ambient_light = Color(0.1, 0.1, 0.1)
        self.max_depth = 4

        self.camera = Camera(
            eye=Vector3D(0.0, -12.0, 6.5),
            look_at=Vector3D(0.0, 0.0, 1.0),
            up=Vector3D(0.0, 0.0, 1.0),
            fov=45,
            img_width=500,
            img_height=300
        )

        # luz lateral
        self.lights = [
            PointLight(position=Vector3D(-8.0, -8.0, 10.0), color=Color(1.0, 1.0, 1.0), intensity=1.5)
        ]

        floor_mat = CheckerboardMaterial(
            ambient_coefficient=0.1, diffuse_coefficient=0.8, square_size=2.0,
            white_color=Color(0.8, 0.8, 0.8), black_color=Color(0.3, 0.3, 0.3)
        )

        red_mat = SimpleMaterialWithShadows(0.1, 0.8, Color(0.8, 0.1, 0.1), 0.3, Color(1,1,1), 32)
        green_mat = SimpleMaterialWithShadows(0.1, 0.8, Color(0.1, 0.8, 0.1), 0.3, Color(1,1,1), 32)
        blue_mat = SimpleMaterialWithShadows(0.1, 0.8, Color(0.1, 0.2, 0.8), 0.3, Color(1,1,1), 32)

        # piso
        self.add(PlaneUV(point=Vector3D(0, 0, 0), normal=Vector3D(0, 0, 1), forward_direction=Vector3D(0, 1, 0)), floor_mat)

        # X = -3.5
        # esfera
        self.add(ObjectTransform(
            shape=Ball(Vector3D(0,0,0), 1.0),
            matrix=Matrix3x3.scale(1.0, 1.0, 1.0),
            translation=Vector3D(-3.5, -2.0, 1.0)
        ), red_mat)

        # elipsoide
        ellipsoid_matrix = Matrix3x3.rotate_y(math.pi/4) @ Matrix3x3.scale(0.5, 1.0, 1.5)
        self.add(ObjectTransform(
            shape=Ball(Vector3D(0,0,0), 1.0),
            matrix=ellipsoid_matrix,
            translation=Vector3D(-3.5, 2.0, 1.5)
        ), red_mat)

        # X = 0.0
        # caja normal
        self.add(ObjectTransform(
            shape=Box(Vector3D(0,0,0), Vector3D(2.0, 2.0, 2.0)),
            matrix=Matrix3x3.scale(1.0, 1.0, 1.0),
            translation=Vector3D(0.0, -2.0, 1.0)
        ), green_mat)

        # caja deformada
        obb_matrix = Matrix3x3.rotate_z(math.pi/6) @ Matrix3x3.scale(1.5, 0.5, 1.5)
        self.add(ObjectTransform(
            shape=Box(Vector3D(0,0,0), Vector3D(2.0, 2.0, 2.0)),
            matrix=obb_matrix,
            translation=Vector3D(0.0, 2.0, 2.0)
        ), green_mat)

        # X = 3.5
        # cilindro normal
        self.add(ObjectTransform(
            shape=Cylinder(Vector3D(0,0,0), 1.0, 2.0),
            matrix=Matrix3x3.scale(1.0, 1.0, 1.0),
            translation=Vector3D(3.5, -2.0, 1.0)
        ), blue_mat)

        # cilindro deformado
        tilted_cyl_matrix = Matrix3x3.rotate_z(math.pi/2) @ Matrix3x3.rotate_y(math.pi/3) @ Matrix3x3.scale(0.5, 0.5, 2.0)
        self.add(ObjectTransform(
            shape=Cylinder(Vector3D(0,0,0), 1.0, 2.0),
            matrix=tilted_cyl_matrix,
            translation=Vector3D(3.5, 2.0, 1.5)
        ), blue_mat)
