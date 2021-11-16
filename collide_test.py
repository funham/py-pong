from src.core.Colliders import *
import matplotlib.pyplot as plt

# (19.83, 0)  (19.32, 0)
# (27.5, 2.5) (27.5, -2.5)
x11, y11 = 19.83, 0
x12, y12 = 19.32, 0

x21, y21 = 27.5, 2.5
x22, y22 = 27.5, -2.5

s1 = SegCollider(vec2(x11, y11), vec2(x12, y12))
s2 = SegCollider(vec2(x21, y21), vec2(x22, y22))


print(s1.inter_seg(s2))
print(s2.inter_seg(s1))

plt.plot([x11, x12], [y11, y12])
plt.plot([x21, x22], [y21, y22])


plt.show()
