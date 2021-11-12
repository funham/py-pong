from src.core.Colliders import *
import matplotlib.pyplot as plt


x11, y11 = 0, 0
x12, y12 = 0, 10

x21, y21 = -10, 0
x22, y22 = 10, 1

s1 = SegCollider(vec2(x11, y11), vec2(x12, y12))
s2 = SegCollider(vec2(x21, y21), vec2(x22, y22))


print(s1.inter_seg(s2))
print(s2.inter_seg(s1))

plt.plot([x11, x12], [y11, y12])
plt.plot([x21, x22], [y21, y22])


plt.show()
