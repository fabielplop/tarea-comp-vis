

from src.base import Shape, HitRecord, CastEpsilon
from src.ray import Ray
from src.vector3d import Vector3D

class Matrix3x3:
    def __init__(self, m):
        self.m = m

    def multiply_vector(self, v: Vector3D) -> Vector3D:
        return Vector3D(
            self.m[0][0]*v.x + self.m[0][1]*v.y + self.m[0][2]*v.z,
            self.m[1][0]*v.x + self.m[1][1]*v.y + self.m[1][2]*v.z,
            self.m[2][0]*v.x + self.m[2][1]*v.y + self.m[2][2]*v.z
        )

    def determinant(self) -> float:
        m = self.m
        return (m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) -
                m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) +
                m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0]))

    def inverse(self) -> 'Matrix3x3':
        det = self.determinant()
        if abs(det) < 1e-8:
            raise ValueError("Matriz singular")
        inv_det = 1.0 / det
        m = self.m
        inv = [
            [(m[1][1]*m[2][2] - m[1][2]*m[2][1])*inv_det, (m[0][2]*m[2][1] - m[0][1]*m[2][2])*inv_det, (m[0][1]*m[1][2] - m[0][2]*m[1][1])*inv_det],
            [(m[1][2]*m[2][0] - m[1][0]*m[2][2])*inv_det, (m[0][0]*m[2][2] - m[0][2]*m[2][0])*inv_det, (m[0][2]*m[1][0] - m[0][0]*m[1][2])*inv_det],
            [(m[1][0]*m[2][1] - m[1][1]*m[2][0])*inv_det, (m[0][1]*m[2][0] - m[0][0]*m[2][1])*inv_det, (m[0][0]*m[1][1] - m[0][1]*m[1][0])*inv_det]
        ]
        return Matrix3x3(inv)

    def transpose(self) -> 'Matrix3x3':
        m = self.m
        return Matrix3x3([
            [m[0][0], m[1][0], m[2][0]],
            [m[0][1], m[1][1], m[2][1]],
            [m[0][2], m[1][2], m[2][2]]
        ])

    def __matmul__(self, other: 'Matrix3x3') -> 'Matrix3x3':
        m1 = self.m
        m2 = other.m
        return Matrix3x3([
            [sum(m1[0][k]*m2[k][0] for k in range(3)), sum(m1[0][k]*m2[k][1] for k in range(3)), sum(m1[0][k]*m2[k][2] for k in range(3))],
            [sum(m1[1][k]*m2[k][0] for k in range(3)), sum(m1[1][k]*m2[k][1] for k in range(3)), sum(m1[1][k]*m2[k][2] for k in range(3))],
            [sum(m1[2][k]*m2[k][0] for k in range(3)), sum(m1[2][k]*m2[k][1] for k in range(3)), sum(m1[2][k]*m2[k][2] for k in range(3))]
        ])

    @staticmethod
    def scale(sx: float, sy: float, sz: float) -> 'Matrix3x3':
        return Matrix3x3([
            [sx, 0.0, 0.0],
            [0.0, sy, 0.0],
            [0.0, 0.0, sz]
        ])

    @staticmethod
    def rotate_x(angle_rad: float) -> 'Matrix3x3':
        import math
        c = math.cos(angle_rad)
        s = math.sin(angle_rad)
        return Matrix3x3([
            [1.0, 0.0, 0.0],
            [0.0, c, -s],
            [0.0, s, c]
        ])

    @staticmethod
    def rotate_y(angle_rad: float) -> 'Matrix3x3':
        import math
        c = math.cos(angle_rad)
        s = math.sin(angle_rad)
        return Matrix3x3([
            [c, 0.0, s],
            [0.0, 1.0, 0.0],
            [-s, 0.0, c]
        ])

    @staticmethod
    def rotate_z(angle_rad: float) -> 'Matrix3x3':
        import math
        c = math.cos(angle_rad)
        s = math.sin(angle_rad)
        return Matrix3x3([
            [c, -s, 0.0],
            [s, c, 0.0],
            [0.0, 0.0, 1.0]
        ])


class ObjectTransform(Shape):
    def __init__(self, shape: Shape, matrix: Matrix3x3, translation: Vector3D):
        super().__init__("transform")
        self.shape = shape
        self.translation = translation

        self.inv_matrix = matrix.inverse()
        self.inv_trans_matrix = self.inv_matrix.transpose()

    def hit(self, ray: Ray) -> HitRecord:
        local_origin_shifted = ray.origin - self.translation
        local_origin = self.inv_matrix.multiply_vector(local_origin_shifted)

        local_direction_raw = self.inv_matrix.multiply_vector(ray.direction)
        direction_magnitude = local_direction_raw.length()

        local_ray = Ray(local_origin, local_direction_raw, ray.depth)

        hit_rec = self.shape.hit(local_ray)

        if not hit_rec.hit:
            return HitRecord(False, float('inf'), None, None)

        t_global = hit_rec.t / direction_magnitude

        if t_global < CastEpsilon:
            return HitRecord(False, float('inf'), None, None)

        global_point = ray.point_at_parameter(t_global)
        global_normal = self.inv_trans_matrix.multiply_vector(hit_rec.normal).normalize()

        return HitRecord(True, t_global, global_point, global_normal, uv=getattr(hit_rec, 'uv', None))

