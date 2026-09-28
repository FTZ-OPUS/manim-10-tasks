# -*- coding: utf-8 -*-
"""任务8：四面体余弦定理（平面余弦定理的立体推广）—— 3D 科普
定理：S₀² = S₁²+S₂²+S₃² − 2S₁S₂cosθ₁₂ − 2S₂S₃cosθ₂₃ − 2S₃S₁cosθ₃₁
     （S₀ 为对面 ABC 面积，Sᵢ 为共享顶点 O 的三个面，θᵢⱼ 为相应二面角）
证明：面积向量闭合 ΣS⃗=0（每条棱正反两次抵消）⇒ 移项取模长平方。
特例：三直角四面体（墙角）⇒ de Gua 定理 S₀²=S₁²+S₂²+S₃²。
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skill_base import *

# 数值算例（可解析验证）：O=(0,0,0), A=(4,0,0), B=(0,3,0), C=(0,0,2.4)
OA, OB, OC = 4.0, 3.0, 2.4
S1 = OB * OC / 2   # 面 OBC
S2 = OC * OA / 2   # 面 OCA
S3 = OA * OB / 2   # 面 OAB
S0 = 0.5 * np.linalg.norm(np.cross(np.array([0, 3, 0.]) - np.array([4, 0, 0.]),
                                   np.array([0, 0, 2.4]) - np.array([4, 0, 0.])))
TH12 = np.pi / 2   # 沿 OC 棱的二面角（两坐标面互相垂直）→ cos=0
TH23 = np.pi / 2
TH31 = np.pi / 2


class TetraCosine(SkillScene3D):

    def construct(self):
        self.camera.background_color = BG
        self.opening()
        self.recap_2d()
        self.analogy_page()
        self.closure_page()
        self.derivation_page()
        self.dihedral_3d()
        self.vector_3d()
        self.example_3d()
        self.degua_page()
        self.extension_page()
        self.ending()

    # ───────────── S0 开场 ─────────────
    def opening(self):
        self.set_camera_orientation(phi=64 * DEGREES, theta=-45 * DEGREES)
        title = self.zh("四面体余弦定理", font_size=62, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        sub = self.zh("—— 余弦定理的立体升级版", font_size=38, color=MUTED)
        sub.next_to(title, DOWN, buff=0.25)
        self.add_fixed_in_frame_mobjects(title, sub)
        self.play(Write(title), run_time=1.0)
        self.play(FadeIn(sub), run_time=0.8)

        A = np.array([2.6, 0.0, 0.0]); B = np.array([0.0, 2.0, 0.0]); C = np.array([0.0, 0.0, 1.7])
        O = np.array([0.0, 0.0, 0.0])
        faces = VGroup(
            Polygon(O, B, C, fill_color=BLUE, fill_opacity=0.45, stroke_width=1.5),
            Polygon(O, C, A, fill_color=GREEN, fill_opacity=0.45, stroke_width=1.5),
            Polygon(O, A, B, fill_color=ORANGE, fill_opacity=0.45, stroke_width=1.5),
            Polygon(A, B, C, fill_color=YELLOW, fill_opacity=0.45, stroke_width=1.5),
        )
        self.begin_ambient_camera_rotation(rate=0.12)
        self.play(Create(faces[0]), Create(faces[1]), Create(faces[2]), run_time=1.2)
        self.play(Create(faces[3]), run_time=1.0)
        tag = self.zh("边长 → 面积，夹角 → 二面角：公式还能活着吗？", font_size=32, color=MUTED)
        self.add_fixed_in_frame_mobjects(tag)
        tag.to_edge(DOWN, buff=0.4)
        self.play(FadeIn(tag), run_time=0.8)
        self.wait(2.0)
        self.stop_ambient_camera_rotation()
        self.clear_scene()

    # ───────────── S1 平面版复习 ─────────────
    def recap_2d(self):
        # 相机先回正对 xy 平面
        self.move_camera(phi=0.0, theta=-90 * DEGREES, run_time=0.1)
        bar = self.title_bar("起点 · 平面余弦定理（向量证明 10 秒版）")
        self.play(Write(bar), run_time=0.8)
        l1 = self.mixed(
            ("math", r"c^{2}=a^{2}+b^{2}-2ab\cos C", YELLOW),
            ("text", "，其中 C 是边 a、b 的夹角", INK),
            text_size=38, math_size=48)
        l2 = self.mixed(
            ("text", "向量证明：令 ", INK),
            ("math", r"\vec{c}=\vec{a}-\vec{b}", INK),
            ("text", "，则", INK),
            text_size=36, math_size=44)
        l3 = self.mixed(
            ("math", r"c^{2}=|\vec{a}-\vec{b}|^{2}=a^{2}+b^{2}-2\,\vec{a}\cdot\vec{b}", TEAL),
            text_size=36, math_size=44)
        content = self.layout_below(bar, l1, l2, l3)
        for line in (l1, l2, l3):
            self.write_formula(line, run_time=1.05)
        self.wait(1.8)
        self.clear_scene()

    # ───────────── S2 类比页 ─────────────
    def analogy_page(self):
        bar = self.title_bar("升维 · 换掉三样东西", color=BLUE)
        self.play(Write(bar), run_time=0.8)
        l1 = self.mixed(
            ("text", "三角形 → 四面体（多一个面）；", INK),
            ("text", "边长 → 面积；", ORANGE),
            ("text", "内角 → 二面角", GREEN),
            text_size=36, math_size=42)
        l2 = self.mixed(
            ("text", "四面体 O-ABC 中，记三个侧面的面积为 ", INK),
            ("math", r"S_1,\ S_2,\ S_3", BLUE),
            ("text", "，底面为 ", INK),
            ("math", r"S_0", YELLOW),
            text_size=34, math_size=42)
        l3 = self.mixed(
            ("text", "θ₁₂ 是 S₁ 与 S₂ 所夹的二面角（沿公共棱 OC），共三个", INK),
            text_size=34, math_size=42)
        l4 = self.mixed(
            ("text", "那么猜想：", MUTED),
            ("math", r"S_0^{2}\ \overset{?}{=}\ S_1^{2}+S_2^{2}+S_3^{2}-2\sum S_iS_j\cos\theta_{ij}", RED),
            text_size=32, math_size=40)
        content = self.layout_below(bar, l1, l2, l3, l4)
        for line in (l1, l2, l3, l4):
            self.write_formula(line, run_time=1.05)
        self.wait(2.0)
        self.clear_scene()

    # ───────────── S3 关键工具：面积向量闭合 ─────────────
    def closure_page(self):
        bar = self.title_bar("关键工具 · 面积向量闭合法则", color=TEAL)
        self.play(Write(bar), run_time=0.8)
        l1 = self.mixed(
            ("text", "给每个面定义「面积向量」：方向为", INK),
            ("text", "外法线", TEAL),
            ("text", "，长度为面积：", INK),
            ("math", r"\vec{S}", INK),
            text_size=34, math_size=42)
        l2 = self.mixed(
            ("math", r"\vec{S}_0+\vec{S}_1+\vec{S}_2+\vec{S}_3=\vec{0}", YELLOW),
            ("text", "（闭合曲面的总通量为零）", MUTED),
            text_size=36, math_size=44)
        l3 = self.mixed(
            ("text", "初等验证：每条棱都属于两个面，绕向一正一反，", INK),
            ("text", "叉积逐棱抵消", TEAL),
            text_size=34, math_size=42)
        l4 = self.mixed(
            ("text", "平面版的老朋友：三角形三边向量首尾相接和为零 —— 这是它在「面积语言」里的样子", MUTED),
            text_size=32, math_size=38)
        content = self.layout_below(bar, l1, l2, l3, l4)
        for line in (l1, l2, l3, l4):
            self.write_formula(line, run_time=1.05)
        self.wait(2.2)
        self.clear_scene()

    # ───────────── S4 推导 ─────────────
    def derivation_page(self):
        bar = self.title_bar("推导 · 三行结束战斗", color=GREEN)
        self.play(Write(bar), run_time=0.8)
        l1 = self.mixed(
            ("text", "移项：", INK),
            ("math", r"\vec{S}_0=-\,(\vec{S}_1+\vec{S}_2+\vec{S}_3)", INK),
            ("text", "，取模长平方：", INK),
            text_size=34, math_size=42)
        l2 = self.mixed(
            ("math", r"S_0^{2}=S_1^{2}+S_2^{2}+S_3^{2}+2\!\!\sum_{i<j}\!\!\vec{S}_i\cdot\vec{S}_j", INK),
            text_size=34, math_size=42)
        l3 = self.mixed(
            ("text", "关键观察：相邻两面的外法线夹角 = π − 二面角，故", INK),
            ("math", r"\vec{S}_i\cdot\vec{S}_j=-\,S_iS_j\cos\theta_{ij}", RED),
            text_size=34, math_size=42)
        l4 = self.mixed(
            ("math", r"\boxed{\,S_0^{2}=S_1^{2}+S_2^{2}+S_3^{2}-2\!\!\sum_{i<j}\!\!S_iS_j\cos\theta_{ij}\,}", YELLOW),
            text_size=40, math_size=52)
        content = self.layout_below(bar, l1, l2, l3, l4)
        for line in (l1, l2, l3, l4):
            self.write_formula(line, run_time=1.1)
        note = self.mixed(
            ("text", "负号正是「内角语言」的痕迹：与平面余弦定理一模一样的气质", MUTED),
            text_size=32, math_size=38)
        note.next_to(content, DOWN, buff=0.55)
        self.fit(note)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(2.2)
        self.clear_scene()

    # ───────────── S4.5 二面角可视化（3D） ─────────────
    def dihedral_3d(self):
        self.set_camera_orientation(phi=66 * DEGREES, theta=-55 * DEGREES)
        bar = self.zh("看清主角 · 什么是二面角 θ₁₂", font_size=42, color=ORANGE, weight=BOLD)
        self.add_fixed_in_frame_mobjects(bar)
        bar.to_edge(UP, buff=0.4)
        self.play(FadeIn(bar), run_time=0.7)

        O = np.array([0.0, 0.0, 0.0])
        A = np.array([3.2, 0.0, 0.0]); B = np.array([0.0, 2.5, 0.0]); C = np.array([0.0, 0.0, 2.0])
        f1 = Polygon(O, B, C, fill_color=BLUE, fill_opacity=0.55, stroke_width=1.5)
        f2 = Polygon(O, C, A, fill_color=GREEN, fill_opacity=0.55, stroke_width=1.5)
        f0 = Polygon(A, B, C, fill_color=YELLOW, fill_opacity=0.25, stroke_width=1.0)
        self.play(Create(f1), Create(f2), Create(f0), run_time=1.4)
        self.begin_ambient_camera_rotation(rate=0.08)

        e = C / np.linalg.norm(C)
        p1 = B - np.dot(B, e) * e
        p1 /= np.linalg.norm(p1)
        p2 = A - np.dot(A, e) * e
        p2 /= np.linalg.norm(p2)
        P0 = C * 0.55
        r = 0.85

        def q(t):
            ang = (np.pi / 2) * t
            K = np.array([[0, -e[2], e[1]], [e[2], 0, -e[0]], [-e[1], e[0], 0]])
            R = np.eye(3) + np.sin(ang) * K + (1 - np.cos(ang)) * (K @ K)
            return P0 + r * (R @ p1)
        arc = ParametricFunction(q, t_range=[0, 1, 0.02], color=RED, stroke_width=5)
        edge = Line(O, C, color=RED, stroke_width=5)
        self.play(Create(edge), run_time=0.7)
        self.play(Create(arc), run_time=1.2)
        lab = self.mixed(
            ("text", "沿公共棱 ", MUTED),
            ("math", r"OC", MUTED),
            ("text", " 切一刀，两个面张开的角度就是二面角 ", MUTED),
            ("math", r"\theta_{12}", RED),
            text_size=30, math_size=36)
        self.add_fixed_in_frame_mobjects(lab)
        lab.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(lab), run_time=0.9)
        self.wait(2.4)
        self.stop_ambient_camera_rotation()
        self.clear_scene()

    # ───────────── S4.7 面积向量可视化（3D） ─────────────
    def vector_3d(self):
        self.set_camera_orientation(phi=64 * DEGREES, theta=-45 * DEGREES)
        bar = self.zh("秘密武器 · 四个面积向量首尾闭合", font_size=42, color=TEAL, weight=BOLD)
        self.add_fixed_in_frame_mobjects(bar)
        bar.to_edge(UP, buff=0.4)
        self.play(FadeIn(bar), run_time=0.7)

        O = np.array([0.0, 0.0, 0.0])
        A = np.array([3.2, 0.0, 0.0]); B = np.array([0.0, 2.5, 0.0]); C = np.array([0.0, 0.0, 2.0])
        faces = VGroup(
            Polygon(O, B, C, fill_color=BLUE, fill_opacity=0.35, stroke_width=1.2),
            Polygon(O, C, A, fill_color=GREEN, fill_opacity=0.35, stroke_width=1.2),
            Polygon(O, A, B, fill_color=ORANGE, fill_opacity=0.35, stroke_width=1.2),
            Polygon(A, B, C, fill_color=YELLOW, fill_opacity=0.35, stroke_width=1.2),
        )
        self.play(Create(faces), run_time=1.3)
        self.begin_ambient_camera_rotation(rate=0.10)

        n1 = np.array([-1.0, 0.0, 0.0])
        n2 = np.array([0.0, -1.0, 0.0])
        n3 = np.array([0.0, 0.0, -1.0])
        n0 = np.array([1.0, 1.0, 1.0]) / np.sqrt(3)
        arrs = VGroup()
        for nrm, cen, col, ln in [
                (n1, (O + B + C) / 3, BLUE, 1.5),
                (n2, (O + C + A) / 3, GREEN, 2.0),
                (n3, (O + A + B) / 3, ORANGE, 2.5),
                (n0, (A + B + C) / 3, YELLOW, 3.4)]:
            ar = Arrow3D(cen - 0.2 * nrm, cen + ln * nrm, color=col, thickness=0.015)
            arrs.add(ar)
        self.play(Create(arrs[0]), Create(arrs[1]), Create(arrs[2]), run_time=1.2)
        self.play(Create(arrs[3]), run_time=0.9)
        l1 = self.mixed(
            ("text", "箭头 = 外法线，长度 = 面积；四个箭头合力为零：", MUTED),
            ("math", r"\vec{S}_0+\vec{S}_1+\vec{S}_2+\vec{S}_3=\vec{0}", YELLOW),
            text_size=30, math_size=38)
        self.add_fixed_in_frame_mobjects(l1)
        l1.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(l1), run_time=0.9)
        self.wait(2.4)
        self.stop_ambient_camera_rotation()
        self.clear_scene()

    # ───────────── S5 数值例子（3D） ─────────────
    def example_3d(self):
        self.set_camera_orientation(phi=66 * DEGREES, theta=-50 * DEGREES)
        bar = self.zh("实测 · 直角墙角四面体", font_size=44, color=BLUE, weight=BOLD)
        self.add_fixed_in_frame_mobjects(bar)
        bar.to_edge(UP, buff=0.4)
        self.play(FadeIn(bar), run_time=0.7)

        O = np.array([0.0, 0.0, 0.0])
        A = np.array([OA, 0.0, 0.0]); B = np.array([0.0, OB, 0.0]); C = np.array([0.0, 0.0, OC])
        f1 = Polygon(O, B, C, fill_color=BLUE, fill_opacity=0.5, stroke_width=1.5)
        f2 = Polygon(O, C, A, fill_color=GREEN, fill_opacity=0.5, stroke_width=1.5)
        f3 = Polygon(O, A, B, fill_color=ORANGE, fill_opacity=0.5, stroke_width=1.5)
        f0 = Polygon(A, B, C, fill_color=YELLOW, fill_opacity=0.5, stroke_width=1.5)
        axes3 = ThreeDAxes(x_range=[0, 5, 1], y_range=[0, 4, 1], z_range=[0, 3, 1],
                           x_length=5.2, y_length=4.0, z_length=3.0,
                           axis_config={"color": MUTED, "stroke_width": 1.5,
                                        "include_ticks": False})
        self.begin_ambient_camera_rotation(rate=0.10)
        self.play(Create(axes3), run_time=0.8)
        self.play(Create(f1), Create(f2), Create(f3), run_time=1.3)
        self.play(Create(f0), run_time=1.0)

        l1 = self.mixed(
            ("text", "取 ", MUTED),
            ("math", r"OA=4,\ OB=3,\ OC=2.4", MUTED),
            ("text", "，三个侧面两两垂直（像墙角）", MUTED),
            text_size=30, math_size=36)
        self.add_fixed_in_frame_mobjects(l1)
        l1.to_edge(DOWN, buff=1.35)
        self.play(FadeIn(l1), run_time=0.8)
        l2 = self.mixed(
            ("math", r"S_1=3.6,\ \ S_2=4.8,\ \ S_3=6.0", BLUE),
            ("text", "；二面角全为 90°，cos 项全部消失", GREEN),
            text_size=30, math_size=36)
        self.add_fixed_in_frame_mobjects(l2)
        l2.next_to(l1, DOWN, buff=0.25)
        self.play(FadeIn(l2), run_time=0.8)
        self.wait(1.2)
        l3 = self.mixed(
            ("math", r"S_0^{2}=3.6^{2}+4.8^{2}+6.0^{2}=73.8\ \Rightarrow\ S_0\approx 8.59", YELLOW),
            text_size=30, math_size=38)
        self.add_fixed_in_frame_mobjects(l3)
        l3.next_to(l2, DOWN, buff=0.25)
        self.play(Write(l3), run_time=1.1)
        l4 = self.mixed(
            ("text", "直接计算 △ABC 面积：", MUTED),
            ("math", r"\tfrac12\,|\vec{AB}\times\vec{AC}|=\tfrac12\sqrt{73.8}\approx 8.59", GREEN),
            ("text", "　吻合 ∎", GREEN),
            text_size=30, math_size=36)
        self.add_fixed_in_frame_mobjects(l4)
        l4.next_to(l3, DOWN, buff=0.25)
        self.play(Write(l4), run_time=1.1)
        self.wait(2.2)
        self.stop_ambient_camera_rotation()
        self.clear_scene()

    # ───────────── S6 de Gua 定理 ─────────────
    def degua_page(self):
        self.move_camera(phi=0.0, theta=-90 * DEGREES, run_time=0.1)
        bar = self.title_bar("意外收获 · 三维勾股定理（de Gua，1783）", color=RED)
        self.play(Write(bar), run_time=0.8)
        l1 = self.mixed(
            ("text", "当三个侧面两两垂直（cosθ 全为 0）时，公式坍缩成：", INK),
            text_size=36, math_size=42)
        l2 = self.mixed(
            ("math", r"S_0^{2}=S_1^{2}+S_2^{2}+S_3^{2}", YELLOW),
            text_size=48, math_size=60)
        l3 = self.mixed(
            ("text", "「斜面面积的平方 = 三条直角边面面积的平方和」—— 勾股定理的面积版表兄", TEAL),
            text_size=34, math_size=40)
        l4 = self.mixed(
            ("text", "更一般地：只要某个顶点处的三个二面角都是直角，它就精确成立", INK),
            text_size=34, math_size=40)
        content = self.layout_below(bar, l1, l2, l3, l4)
        for line in (l1, l2, l3, l4):
            self.write_formula(line, run_time=1.15)
        self.wait(2.2)
        self.clear_scene()

    # ───────────── S7 拓展 ─────────────
    def extension_page(self):
        bar = self.title_bar("拓展 · 这条定理的亲戚们", color=VIOLET)
        self.play(Write(bar), run_time=0.8)
        l1 = self.mixed(
            ("text", "球面余弦定理：球面上 ", INK),
            ("math", r"\cos c=\cos a\cos b+\sin a\sin b\cos C", TEAL),
            ("text", " —— 三面角沿单位球切出的 spherical 三角形", INK),
            text_size=32, math_size=40)
        l2 = self.mixed(
            ("text", "四面体余弦定理 = 球面余弦定理换算到「面积语言」，二者互为表里", INK),
            text_size=34, math_size=40)
        l3 = self.mixed(
            ("text", "n 维单形同样有「各侧面体积 + 二面角」版本的余弦定理（更高维照常生效）", INK),
            text_size=34, math_size=40)
        l4 = self.mixed(
            ("text", "工程掠影：有限元网格质量评估、计算机图形学的法向量闭合检查，用的正是面积向量", TEAL),
            text_size=34, math_size=40)
        content = self.layout_below(bar, l1, l2, l3, l4)
        for line in (l1, l2, l3, l4):
            self.write_formula(line, run_time=1.05)
        self.wait(2.2)
        self.clear_scene()

    # ───────────── S8 结尾 ─────────────
    def ending(self):
        self.move_camera(phi=58 * DEGREES, theta=-40 * DEGREES, run_time=0.1)
        t1 = self.zh("维度会变，代数不变", font_size=54, weight=BOLD)
        self.add_fixed_in_frame_mobjects(t1)
        t1.move_to([0, 1.6, 0])
        t2 = self.mixed(
            ("math", r"S_0^{2}=\sum S_i^{2}-2\sum S_iS_j\cos\theta_{ij}", YELLOW),
            text_size=40, math_size=50)
        self.add_fixed_in_frame_mobjects(t2)
        t2.next_to(t1, DOWN, buff=0.5)
        self.play(Write(t1), run_time=1.0)
        self.play(Write(t2), run_time=1.2)

        A = np.array([2.4, 0.0, 0.0]); B = np.array([0.0, 1.9, 0.0]); C = np.array([0.0, 0.0, 1.6])
        O = np.array([0.0, 0.0, 0.0])
        faces = VGroup(
            Polygon(O, B, C, fill_color=BLUE, fill_opacity=0.4, stroke_width=1.2),
            Polygon(O, C, A, fill_color=GREEN, fill_opacity=0.4, stroke_width=1.2),
            Polygon(O, A, B, fill_color=ORANGE, fill_opacity=0.4, stroke_width=1.2),
            Polygon(A, B, C, fill_color=YELLOW, fill_opacity=0.4, stroke_width=1.2),
        )
        self.begin_ambient_camera_rotation(rate=0.12)
        self.play(Create(faces), run_time=1.6)
        self.wait(2.4)
        self.stop_ambient_camera_rotation()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
        self.wait(0.3)
