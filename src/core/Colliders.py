from pygame import Vector2 as vec2


# Interface
class Collider:
    def __init__(self, size, pos) -> None:
        self.size = size
        self.pos = pos


class SegCollider(Collider):
    def __init__(self, p1: vec2, p2: vec2) -> None:
        self.p1 = p1
        self.p2 = p2
        self.dy = p2.y - p1.y
        self.dx = p2.x - p1.x

        self.min_y = min(p1.y, p2.y)
        self.max_y = max(p1.y, p2.y)

        self.min_x = min(p1.x, p2.x)
        self.max_x = max(p1.x, p2.x)

    # parallel shift
    def __add__(self, vec : vec2):
        p1 = self.p1 + vec
        p2 = self.p2 + vec

        return SegCollider(p1, p2)

    
    def top(self):
        return self.p1 if self.p1.y < self.p2.y else self.p2

    def bottom(self):
        return self.p1 if self.p1.y > self.p2.y else self.p2

    def center(self):
        return (self.p1 + self.p2)/2

    def p_list(self) -> tuple:
        return (self.p1, self.p2)

    def get_points(self):
        return self.p1, self.p2

    def inter_seg(self, other):

        def inter_with_vert(x0, min_y, max_y, seg):
            # we don't need this for now
            if seg.dx == 0:
                return None

            t2 = seg.dy / seg.dx

            y = (x0 - seg.p1.x) * t2 + seg.p1.y

            return vec2(x0, y) if min_y <= y <= max_y and \
                seg.min_x <= x0 <= seg.max_x else None

        if self.dx == 0:
            return inter_with_vert(self.p1.x, self.min_y, self.max_y, other)
        elif other.dx == 0:
            return inter_with_vert(other.p1.x, other.min_y, other.max_y, self)

        # if all of segments aren't verticals
        # (we don't have problems with horizontals)
        t1 = self.dy / self.dx
        t2 = other.dy / other.dx

        # if they're parallel
        if t1 == t2:
            return None

        # calculating roots
        x = (self.p1.x * t1 - other.p1.x * t2 -
             self.p1.y + other.p1.y) / (t1 - t2)
        y = (x - self.p1.x) * t1 + self.p1.y

        # print(f'{x=}, {y=}')

        in_x = min(self.p1.x, self.p2.x) <= x <= max(self.p1.x, self.p2.x)
        in_y = min(self.p1.y, self.p2.y) <= y <= max(self.p1.y, self.p2.y)

        # print(f'{in_x=}, {in_y=}')

        return vec2(x, y) if in_x and in_y else None


class RectCollider(Collider):
    def __init__(self, size: vec2, pos: vec2) -> None:
        super().__init__(size, pos)

    def left(self, inv=1):
        return self.pos - inv * vec2(self.size.x/2, 0)

    def right(self):
        return self.pos + vec2(self.size.x/2, 0)

    def top(self, inv=1):
        return self.pos - inv * vec2(0, self.size.y/2)

    def bottom(self):
        return self.pos + vec2(0, self.size.y/2)

    def center(self):
        return self.pos

    def top_left(self, inv=1):
        x = self.pos.x - self.size.x/2 * (inv)
        y = self.pos.y - self.size.y/2 * 1
        return vec2(x, y)

    def bottom_right(self):
        return self.pos + self.size / 2

    def top_right(self, inv=1):
        x = self.pos.x - self.size.x/2 * (-inv)
        y = self.pos.y - self.size.y/2 * 1
        return vec2(x, y)

    def bottom_left(self, inv=1):
        x = self.pos.x - self.size.x/2 * (inv)
        y = self.pos.y + self.size.y/2 * 1
        return vec2(x, y)

    def bottom_seg(self):
        return SegCollider(self.bottom_left(),
                           self.bottom_right())

    def top_seg(self, inv=1):
        return SegCollider(self.top_left(inv),
                           self.top_right(inv))

    def left_seg(self, inv=1):
        return SegCollider(self.bottom_left(inv),
                           self.top_left(inv))

    def right_seg(self):
        return SegCollider(self.bottom_right(),
                           self.top_right())

    def p_list(self) -> tuple:
        t = []
        t.append(self.top_left())
        t.append(self.top_right())
        t.append(self.bottom_left())
        t.append(self.bottom_right())

        return tuple(t)

    def collides_point(self, point: vec2) -> bool:
        in_x = point.x <= self.right.x and point.x >= self.left.x
        in_y = point.y <= self.top.y and point.y >= self.bottom.y

        return in_x and in_y

    def collides_rect(self, other) -> bool:
        res = False

        for p in self.p_list:
            res &= other.collides_point(p)
        for p in other.p_list:
            res &= self.collides_point(p)

        return res


# TODO delete and make EllipseCollider instead
class CircleColiider(Collider):
    def __init__(self, size: float, pos: vec2) -> None:
        super().__init__(size, pos)

    def collides_point(self, point: vec2) -> bool:
        point.magnitude_squared()
        return (point - self.pos).magnitude_squared() <= self.size**2

    def left(self):
        return self.pos - vec2(self.size/2, 0)

    def right(self):
        return self.pos + vec2(self.size/2, 0)

    def top(self):
        return self.pos - vec2(0, self.size/2)

    def bottom(self):
        return self.pos + vec2(0, self.size/2)

    def center(self):
        return self.pos

    def collides_rect(self, rect: RectCollider):
        for p in rect.p_list():
            if self.collides_point(p):
                return True

        return rect.collides_point(self.pos)
