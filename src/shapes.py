from src.vector3d import Vector3D
from .base import Shape, HitRecord, CastEpsilon

class Ball(Shape):
    def __init__(self, center, radius):
        super().__init__("ball")
        self.center = center
        self.radius = radius

    def hit(self, ray):
        # Ray-sphere intersection
        oc = ray.origin - self.center
        a = ray.direction.dot(ray.direction)
        b = 2.0 * oc.dot(ray.direction)
        c = oc.dot(oc) - self.radius * self.radius
        discriminant = b * b - 4 * a * c
        if discriminant < 0:
            return HitRecord(False, float('inf'), None, None)
        else:
            hit, point, normal = False, None, None
            t = (-b - discriminant**0.5) / (2.0 * a)
            if t > CastEpsilon:
                hit = True
                point = ray.point_at_parameter(t)
                normal = (point - self.center).normalize()
            else:
                t = (-b + discriminant**0.5) / (2.0 * a)
                if t > CastEpsilon:
                    hit = True
                    point = ray.point_at_parameter(t)
                    normal = (point - self.center).normalize()

            return HitRecord(hit, t, point, normal)

class Plane(Shape):
    def __init__(self, point, normal):
        super().__init__("plane")
        self.point = point
        self.normal = normal.normalize()

    def hit(self, ray):
        denom = self.normal.dot(ray.direction)
        if abs(denom) > 1e-6:
            t = (self.point - ray.origin).dot(self.normal) / denom
            if t >= CastEpsilon:
                point = ray.point_at_parameter(t)
                return HitRecord(True, t, point, self.normal)
        return HitRecord(False, float('inf'), None, None)

class PlaneUV(Shape):
    def __init__(self, point, normal, forward_direction):
        super().__init__("plane")
        self.point = point
        self.normal = normal.normalize()
        self.forward_direction = forward_direction.normalize()
        # compute right direction
        self.right_direction = self.normal.cross(self.forward_direction).normalize()

    def hit(self, ray):
        denom = self.normal.dot(ray.direction)
        if abs(denom) > 1e-6:
            t = (self.point - ray.origin).dot(self.normal) / denom
            if t >= CastEpsilon:
                point = ray.point_at_parameter(t)
                # Calculate UV coordinates
                vec = point - self.point
                u = vec.dot(self.right_direction)
                v = vec.dot(self.forward_direction)
                uv = Vector3D(u, v, 0)
                return HitRecord(True, t, point, self.normal, uv=uv)
        return HitRecord(False, float('inf'), None, None)

class ImplicitFunction(Shape):
    def __init__(self, function):
        super().__init__("implicit_function")
        self.func = function

    def in_out(self, point):
        return self.func(point) <= 0



class Box(Shape):
    def __init__(self, center: Vector3D, size: Vector3D):
        super().__init__("box")
        self.center = center
        self.half_size = size * 0.5

    def hit(self, ray):
        local_origin = ray.origin - self.center
        
        def calc_slab(o_axis, d_axis, half_s):
            if abs(d_axis) < 1e-6:
                if abs(o_axis) > half_s:
                    return float('inf'), float('-inf')
                return float('-inf'), float('inf')
            inv_d = 1.0 / d_axis
            t0 = (-half_s - o_axis) * inv_d
            t1 = (half_s - o_axis) * inv_d
            return (t0, t1) if t0 < t1 else (t1, t0)

        tx_close, tx_far = calc_slab(local_origin.x, ray.direction.x, self.half_size.x)
        ty_close, ty_far = calc_slab(local_origin.y, ray.direction.y, self.half_size.y)
        tz_close, tz_far = calc_slab(local_origin.z, ray.direction.z, self.half_size.z)

        t_close = max(tx_close, ty_close, tz_close)
        t_far = min(tx_far, ty_far, tz_far)

        if t_close > t_far or t_far < CastEpsilon:
            return HitRecord(False, float('inf'), None, None)

        t_hit = t_close if t_close >= CastEpsilon else t_far
        if t_hit < CastEpsilon:
            return HitRecord(False, float('inf'), None, None)

        global_point = ray.point_at_parameter(t_hit)
        
        # normal
        local_point = local_origin + ray.direction * t_hit
        epsilon = 1e-4
        normal = Vector3D(0, 0, 0)
        if abs(local_point.x + self.half_size.x) < epsilon: normal = Vector3D(-1, 0, 0)
        elif abs(local_point.x - self.half_size.x) < epsilon: normal = Vector3D(1, 0, 0)
        elif abs(local_point.y + self.half_size.y) < epsilon: normal = Vector3D(0, -1, 0)
        elif abs(local_point.y - self.half_size.y) < epsilon: normal = Vector3D(0, 1, 0)
        elif abs(local_point.z + self.half_size.z) < epsilon: normal = Vector3D(0, 0, -1)
        elif abs(local_point.z - self.half_size.z) < epsilon: normal = Vector3D(0, 0, 1)

        return HitRecord(True, t_hit, global_point, normal)



class Cylinder(Shape):
    def __init__(self, center: Vector3D, radius: float, height: float):
        super().__init__("cylinder")
        self.center = center
        self.radius = radius
        self.half_height = height * 0.5

    def hit(self, ray):
        local_origin = ray.origin - self.center
        
        t_closest = float('inf')
        hit_normal = None
        has_hit = False

        dx, dy, dz = ray.direction.x, ray.direction.y, ray.direction.z
        ox, oy, oz = local_origin.x, local_origin.y, local_origin.z

        a = dx**2 + dy**2
        if abs(a) > 1e-6:
            b = 2.0 * (ox * dx + oy * dy)
            c = ox**2 + oy**2 - self.radius**2
            discriminant = b**2 - 4 * a * c

            if discriminant >= 0:
                sqrt_d = discriminant**0.5
                inv_2a = 1.0 / (2.0 * a)
                
                # Evaluacion de la primera raiz
                t0 = (-b - sqrt_d) * inv_2a
                if CastEpsilon < t0 < t_closest:
                    z_proj = oz + t0 * dz
                    if -self.half_height <= z_proj <= self.half_height:
                        t_closest = t0
                        has_hit = True
                        hit_normal = Vector3D(ox + t0 * dx, oy + t0 * dy, 0).normalize()

                # Evaluacion de la segunda raiz
                if not has_hit:
                    t1 = (-b + sqrt_d) * inv_2a
                    if CastEpsilon < t1 < t_closest:
                        z_proj = oz + t1 * dz
                        if -self.half_height <= z_proj <= self.half_height:
                            t_closest = t1
                            has_hit = True
                            hit_normal = Vector3D(ox + t1 * dx, oy + t1 * dy, 0).normalize()

        if abs(dz) > 1e-6:
            inv_dz = 1.0 / dz
            
            # Tapa inferior 
            t_bottom = (-self.half_height - oz) * inv_dz
            if CastEpsilon < t_bottom < t_closest:
                px = ox + t_bottom * dx
                py = oy + t_bottom * dy
                if px**2 + py**2 <= self.radius**2:
                    t_closest = t_bottom
                    has_hit = True
                    hit_normal = Vector3D(0, 0, -1)

            # Tapa superior
            t_top = (self.half_height - oz) * inv_dz
            if CastEpsilon < t_top < t_closest:
                px = ox + t_top * dx
                py = oy + t_top * dy
                if px**2 + py**2 <= self.radius**2:
                    t_closest = t_top
                    has_hit = True
                    hit_normal = Vector3D(0, 0, 1)

        if has_hit:
            global_point = ray.point_at_parameter(t_closest)
            return HitRecord(True, t_closest, global_point, hit_normal)
        
        return HitRecord(False, float('inf'), None, None)
