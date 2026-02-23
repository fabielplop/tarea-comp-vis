# world is right-handed, z is up
import math

from .ray import Ray

class Camera:
    def __init__(self, eye, look_at, up, fov, img_width, img_height):
        self.eye = eye
        # self.look_at = look_at
        # self.up = up
        # self.fov = fov
        # self.aspect_ratio = aspect_ratio
        self.img_width = img_width
        self.img_height = img_height

        aspect_ratio = img_height / img_width

        self.su = 2 * math.tan(math.radians(fov) / 2)
        self.sv = self.su * aspect_ratio

        self.w = (eye - look_at).normalize()
        up = up.normalize()
        #self.u = self.w.cross(up).normalize()
        self.u = up.cross(self.w).normalize()
        self.v = self.w.cross(self.u).normalize()

    def point_image2world(self, x, y):
        # from image coordinates to coordinates 
        # in the camera's view plane
        x_ndc = self.su * x / self.img_width - self.su / 2
        y_ndc = self.sv * y / self.img_height - self.sv / 2

        # from view plane to world coordinates
        return self.eye + self.u * x_ndc + self.v * y_ndc - self.w

    def ray(self, x, y):
        point_world = self.point_image2world(x, y)
        direction = (point_world - self.eye).normalize()
        return Ray(self.eye, direction)

import math
import random
from src.vector3d import Vector3D
from src.ray import Ray

def random_in_unit_disk() -> Vector3D:
    # Lema auxiliar: Búsqueda de un vector aleatorio dentro de un disco unitario z=0.
    # Demostración: El método de rechazo genera coordenadas uniformes en el rango [-1, 1].
    # Se descartan los vectores cuya norma al cuadrado supere el radio unitario (x^2 + y^2 >= 1).
    # La distribución resultante es estrictamente uniforme sobre la superficie del disco.
    while True:
        p = Vector3D(random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0), 0.0)
        if p.length_squared() < 1.0:
            return p

class ThinLensCamera:
    def __init__(self, eye: Vector3D, look_at: Vector3D, up: Vector3D, fov: float, img_width: int, img_height: int, lens_radius: float, focal_distance: float):
        self.eye = eye
        self.lens_radius = lens_radius
        self.focal_distance = focal_distance
        
        # Atributos públicos obligatorios para la orquestación del rasterizador
        self.img_width = img_width
        self.img_height = img_height
        
        theta = fov * math.pi / 180.0
        half_height = math.tan(theta / 2.0)
        aspect_ratio = img_width / img_height
        half_width = aspect_ratio * half_height
        
        self.w = (eye - look_at).normalize()
        self.u = up.cross(self.w).normalize()
        self.v = self.w.cross(self.u)
        
        self.lower_left_corner = self.eye - self.u * (half_width * focal_distance) - self.v * (half_height * focal_distance) - self.w * focal_distance
        self.horizontal = self.u * (2.0 * half_width * focal_distance)
        self.vertical = self.v * (2.0 * half_height * focal_distance)

    # El método get_ray se mantiene intact

    def ray(self, s: float, t: float) -> Ray:
        # Normalización estricta al espacio paramétrico [0, 1]
        u = s / self.img_width
        v = t / self.img_height
        
        rd = random_in_unit_disk() * self.lens_radius
        offset = self.u * rd.x + self.v * rd.y
        
        # Interpolación sobre el plano focal garantizada dentro de los límites
        p_focus = self.lower_left_corner + self.horizontal * u + self.vertical * v
        
        new_origin = self.eye + offset
        new_direction = (p_focus - new_origin).normalize()
        
        return Ray(new_origin, new_direction)

