from src.base import Shape, HitRecord, CastEpsilon
from src.vector3d import Vector3D

class AlgebraicSurface(Shape):
    def __init__(self, bounds: Vector3D, step_size: float = 0.05, max_bisection_steps: int = 20):
        super().__init__("algebraic_surface")
        self.bounds = bounds 
        self.step_size = step_size
        self.max_bisection_steps = max_bisection_steps

    def evaluate(self, point: Vector3D) -> float:
        raise NotImplementedError("Subclases deben implementar la función de nivel cero.")

    def gradient(self, point: Vector3D) -> Vector3D:
        eps = 1e-4
        dx = self.evaluate(Vector3D(point.x + eps, point.y, point.z)) - self.evaluate(Vector3D(point.x - eps, point.y, point.z))
        dy = self.evaluate(Vector3D(point.x, point.y + eps, point.z)) - self.evaluate(Vector3D(point.x, point.y - eps, point.z))
        dz = self.evaluate(Vector3D(point.x, point.y, point.z + eps)) - self.evaluate(Vector3D(point.x, point.y, point.z - eps))
        return Vector3D(dx, dy, dz)

    def hit(self, ray):
        t_min = float('-inf')
        t_max = float('inf')

        axes = [
            (ray.origin.x, ray.direction.x, self.bounds.x),
            (ray.origin.y, ray.direction.y, self.bounds.y),
            (ray.origin.z, ray.direction.z, self.bounds.z)
        ]

        for o, d, bound in axes:
            if abs(d) > 1e-6:
                inv_d = 1.0 / d
                t0 = (-bound - o) * inv_d
                t1 = (bound - o) * inv_d
                if t0 > t1:
                    t0, t1 = t1, t0
                t_min = max(t_min, t0)
                t_max = min(t_max, t1)

                if t_min > t_max:
                    return HitRecord(False, float('inf'), None, None)
            elif abs(o) > bound:
                return HitRecord(False, float('inf'), None, None)

        if t_max < CastEpsilon:
            return HitRecord(False, float('inf'), None, None)

        t_in = max(t_min, CastEpsilon)
        t_out = t_max

        t_current = t_in
        f_current = self.evaluate(ray.point_at_parameter(t_current))

        while t_current < t_out:
            t_next = t_current + self.step_size
            if t_next > t_out:
                t_next = t_out

            f_next = self.evaluate(ray.point_at_parameter(t_next))

            if f_current * f_next <= 0:
                t_a = t_current
                t_b = t_next
                for _ in range(self.max_bisection_steps):
                    t_mid = (t_a + t_b) * 0.5
                    f_mid = self.evaluate(ray.point_at_parameter(t_mid))

                    if f_mid == 0.0:
                        t_a = t_mid
                        break
                    elif (f_current * f_mid) < 0:
                        t_b = t_mid
                    else:
                        t_a = t_mid
                        f_current = f_mid

                t_hit = t_a
                hit_point = ray.point_at_parameter(t_hit)
                normal_vec = self.gradient(hit_point)

                try:
                    hit_normal = normal_vec.normalize()
                except ValueError:
                    return HitRecord(False, float('inf'), None, None)

                return HitRecord(True, t_hit, hit_point, hit_normal)

            t_current = t_next
            f_current = f_next

        return HitRecord(False, float('inf'), None, None)


class MitchelSurface(AlgebraicSurface):
    def __init__(self):
        super().__init__(bounds=Vector3D(2.5, 2.5, 2.5), step_size=0.02)

    def evaluate(self, p: Vector3D) -> float:
        x2 = p.x * p.x
        y2 = p.y * p.y
        z2 = p.z * p.z

        y2_z2 = y2 + z2
        x4 = x2 * x2

        return 4.0 * (x4 + y2_z2 * y2_z2 + 17.0 * x2 * y2_z2) - 20.0 * (x2 + y2 + z2) + 17.0


class HeartSurface(AlgebraicSurface):
    def __init__(self):
        super().__init__(bounds=Vector3D(1.5, 1.5, 1.5), step_size=0.02)

    def evaluate(self, p: Vector3D) -> float:
        x2 = p.x * p.x
        y2 = p.y * p.y
        z2 = p.z * p.z
        z3 = z2 * p.z

        base = x2 + 2.25 * y2 + z2 - 1.0
        return (base * base * base) - (x2 * z3) - (0.1125 * y2 * z3)
