# -*- coding: utf-8 -*-
"""任务1：闭区间套定理 ⇒ 三角形三中线共点
核心证明（严格）：
  T₀=ABC，逐次取三边中点得中点三角形序列 T₀⊃T₁⊃T₂⊃⋯，直径减半→0。
  重心坐标不变量：A_n=(1-2p_n,p_n,p_n), B_n=(p_n,1-2p_n,p_n), C_n=(p_n,p_n,1-2p_n)，
  故每层顶点分别落在原三角形中线 m_a,m_b,m_c 上；p_{n+1}=(1-p_n)/2→1/3。
  投影 x/y 坐标得两列闭区间套 ⇒ 唯一 ξ 属于一切 T_n；中线为闭集 ⇒ ξ∈m_a∩m_b∩m_c。∎
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skill_base import *


class NestedMedianProof(SkillScene):

    def construct(self):
        self.camera.background_color = BG
        self.opening()
        self.theorem_page()
        self.counterexample_page()
        self.strategy_page()
        self.construction_page()
        self.invariant_a()
        self.invariant_b()
        self.sliding_page()
        self.closure_page()
        self.ratio_moment()
        self.classic_view()
        self.extension_proof()
        self.extension_thoughts()
        self.ending()

    # ───────────────────────── S0 开场 ─────────────────────────
    def opening(self):
        title = self.zh("闭区间套定理", font_size=64, weight=BOLD)
        title.to_edge(UP, buff=0.55)
        sub = self.zh("—— 巧证三角形三中线共点", font_size=40, color=MUTED)
        sub.next_to(title, DOWN, buff=0.25)
        self.play(Write(title), run_time=1.0)
        self.play(FadeIn(sub, shift=UP * 0.3), run_time=0.8)

        A = np.array([-3.4, -1.6, 0]); B = np.array([3.6, -1.6, 0]); C = np.array([1.6, 1.9, 0])
        tri = Polygon(A, B, C, color=INK, stroke_width=3)
        grp = VGroup(tri).move_to([0, -1.0, 0]).scale(0.9)
        A2, B2, C2 = (tri.get_vertices()[0], tri.get_vertices()[1], tri.get_vertices()[2])
        Ma, Mb, Mc = (B2 + C2) / 2, (C2 + A2) / 2, (A2 + B2) / 2
        m1 = Line(A2, Ma, color=BLUE, stroke_width=2.2)
        m2 = Line(B2, Mb, color=GREEN, stroke_width=2.2)
        m3 = Line(C2, Mc, color=ORANGE, stroke_width=2.2)
        G = tri.get_vertices().mean(axis=0)
        dot = Dot(G, color=YELLOW, radius=0.09)
        tag = self.zh("实数完备性 · 几何共点 · 一网打尽", font_size=30, color=MUTED)
        tag.to_edge(DOWN, buff=0.45)
        self.play(Create(tri), run_time=1.3)
        self.play(Create(m1), run_time=0.6)
        self.play(Create(m2), Create(m3), run_time=0.9)
        self.play(FadeIn(dot), Flash(dot, color=YELLOW, flash_radius=0.45), run_time=0.9)
        self.play(FadeIn(tag), run_time=0.7)
        self.wait(2.2)
        self.clear_scene()

    # ───────────────────── S1 定理叙述 + 数轴演示 ─────────────────────
    def theorem_page(self):
        bar = self.title_bar("闭区间套定理（实数完备性）")
        self.play(Write(bar), run_time=0.8)

        l1 = self.mixed(
            ("math", r"[a_1,b_1]\supseteq[a_2,b_2]\supseteq\cdots\supseteq[a_n,b_n]\supseteq\cdots", INK),
            text_size=36, math_size=46)
        l2 = self.mixed(
            ("text", "且长度", INK),
            ("math", r"b_n-a_n\to 0\quad(n\to\infty)", YELLOW),
            text_size=36, math_size=46)
        l3 = self.mixed(
            ("text", "则存在唯一的实数", INK),
            ("math", r"\xi", YELLOW),
            ("text", "，同时属于一切区间，即", INK),
            ("math", r"\xi\in\bigcap_{n=1}^{\infty}[a_n,b_n]", GREEN),
            text_size=36, math_size=46)
        content = self.layout_below(bar, l1, l2, l3)
        for line in (l1, l2, l3):
            self.write_formula(line, run_time=0.95)
        l4 = self.mixed(
            ("text", "「闭」保证端点取得到，「套」保证层层收缩 —— 两个条件缺一不可", MUTED),
            text_size=32, math_size=38)
        l4.next_to(content, DOWN, buff=0.75)
        self.fit(l4)
        self.play(FadeIn(l4), run_time=0.7)
        self.wait(1.0)

        # 数轴上的嵌套演示
        line = NumberLine(x_range=[-5, 5, 1], length=13.6, color=MUTED,
                          stroke_width=2, include_ticks=True, tick_size=0.08)
        line.move_to([0, -3.35, 0])
        nums = line.get_number_mobjects(-4, -2, 0, 2, 4, font_size=24, color=MUTED)
        self.play(Create(line), FadeIn(nums), run_time=1.0)

        data = [(-4.3, 4.6, INK, "a_1", "b_1"),
                (-1.9, 2.5, BLUE, None, None),
                (0.1, 1.6, GREEN, None, None),
                (0.5, 1.05, ORANGE, None, None),
                (0.62, 0.83, VIOLET, None, None)]
        y = -2.82
        segs = VGroup()
        for i, (a, b, col, la, lb) in enumerate(data):
            seg = Line([a, y, 0], [b, y, 0], color=col, stroke_width=8)
            segs.add(seg)
            if la:
                t1 = self.mt(la, font_size=28, color=MUTED).next_to(seg.get_start(), LEFT, buff=0.15)
                t2 = self.mt(lb, font_size=28, color=MUTED).next_to(seg.get_end(), RIGHT, buff=0.15)
                self.play(Create(seg), FadeIn(t1), FadeIn(t2), run_time=0.7)
            else:
                self.play(Create(seg), run_time=0.65)
            y += 0.38
        xi = Dot(line.number_to_point(0.7), color=YELLOW, radius=0.1)
        xl = self.mt(r"\xi", font_size=40, color=YELLOW).next_to(xi, DOWN, buff=0.25)
        self.play(FadeIn(xi), Flash(xi, color=YELLOW, flash_radius=0.5), Write(xl), run_time=0.9)
        cap = self.mixed(("text", "区间越套越短，最后只剩一个点 —— 这就是「套」的力量", MUTED),
                         text_size=32, math_size=36)
        cap.to_edge(DOWN, buff=0.32)
        self.play(FadeIn(cap), run_time=0.7)
        self.wait(2.0)
        self.clear_scene()

    # ───────────────── S1.5 反例：为什么必须「闭」 ─────────────────
    def counterexample_page(self):
        bar = self.title_bar("追问 · 为什么必须「闭」？", color=RED)
        self.play(Write(bar), run_time=0.8)
        l1 = self.mixed(
            ("text", "反例：取开区间列 ", RED),
            ("math", r"\big(0,\ \tfrac{1}{n}\big)", RED),
            ("text", "，同样层层嵌套、长度趋于 0", INK),
            text_size=38, math_size=46)
        content = self.layout_below(bar, l1)
        self.write_formula(l1, run_time=1.0)

        line = NumberLine(x_range=[-0.3, 1.3, 0.5], length=11.0, color=MUTED,
                          stroke_width=2, include_ticks=True, tick_size=0.08)
        line.move_to([0, -0.9, 0])
        lab0 = self.mt("0", font_size=28, color=MUTED).next_to(line.number_to_point(0), DOWN, buff=0.15)
        lab1 = self.mt("1", font_size=28, color=MUTED).next_to(line.number_to_point(1), DOWN, buff=0.15)
        self.play(Create(line), FadeIn(lab0), FadeIn(lab1), run_time=0.9)
        y = 0.15
        ends = VGroup()
        for i, b in enumerate([1.0, 0.5, 0.25, 0.125, 0.0625]):
            col = [INK, BLUE, GREEN, ORANGE, VIOLET][i]
            seg = Line(line.number_to_point(0) + np.array([0, y, 0]),
                       line.number_to_point(b) + np.array([0, y, 0]),
                       color=col, stroke_width=7)
            e1 = Circle(radius=0.055, color=col, stroke_width=3).move_to(
                line.number_to_point(0) + np.array([0, y, 0]))
            e2 = Circle(radius=0.055, color=col, stroke_width=3).move_to(
                line.number_to_point(b) + np.array([0, y, 0]))
            ends.add(e1, e2)
            self.play(Create(seg), FadeIn(e1), FadeIn(e2), run_time=0.55)
            y += 0.4
        qm = self.zh("？", font_size=44, color=RED).move_to(line.number_to_point(0) + np.array([0, 2.1, 0]))
        l2 = self.mixed(
            ("text", "端点 0 永远「取不到」：", INK),
            ("math", r"\bigcap_{n\ge1}\big(0,\ \tfrac{1}{n}\big)=\varnothing", RED),
            ("text", "，交集竟是空的！", INK),
            text_size=38, math_size=46)
        l2.next_to(line, DOWN, buff=1.15)
        self.fit(l2)
        self.play(Write(l2), FadeIn(qm), run_time=1.1)
        self.wait(1.6)
        l3 = self.mixed(
            ("text", "「闭」+「长度归零」", YELLOW),
            ("text", "，才能稳稳套住那唯一的一点", YELLOW),
            text_size=38, math_size=44)
        l3.next_to(l2, DOWN, buff=0.55)
        self.fit(l3)
        self.play(Write(l3), run_time=0.9)
        self.wait(2.0)
        self.clear_scene()

    # ───────────────── S5.5 直观：顶点沿中线滑动 ─────────────────
    def sliding_page(self):
        bar = self.title_bar("直观演示 · 顶点被中线「锁住」")
        self.play(Write(bar), run_time=0.8)
        A = np.array([-5.6, -2.6, 0.0]); B = np.array([2.6, -2.6, 0.0]); C = np.array([0.2, 2.2, 0.0])
        tri = Polygon(A, B, C, color=INK, stroke_width=3)
        Ma, Mb, Mc = (B + C) / 2, (C + A) / 2, (A + B) / 2
        m_a = Line(A, Ma, color=BLUE, stroke_width=2.2)
        m_b = Line(B, Mb, color=GREEN, stroke_width=2.2)
        m_c = Line(C, Mc, color=ORANGE, stroke_width=2.2)
        self.play(Create(tri), Create(m_a), Create(m_b), Create(m_c), run_time=1.1)

        la = self.mt("A", font_size=32).next_to(A, DL, buff=0.1)
        lb = self.mt("B", font_size=32).next_to(B, DR, buff=0.1)
        lc = self.mt("C", font_size=32).next_to(C, UP, buff=0.1)
        self.play(FadeIn(la), FadeIn(lb), FadeIn(lc), run_time=0.5)

        cur = (A, B, C)
        seqs = ([], [], [])
        for i in range(6):
            A2 = (cur[1] + cur[2]) / 2
            B2 = (cur[2] + cur[0]) / 2
            C2 = (cur[0] + cur[1]) / 2
            seqs[0].append(Dot(A2, radius=0.06, color=BLUE))
            seqs[1].append(Dot(B2, radius=0.06, color=GREEN))
            seqs[2].append(Dot(C2, radius=0.06, color=ORANGE))
            cur = (A2, B2, C2)
        for i in range(6):
            self.play(*[FadeIn(s[i]) for s in seqs], run_time=0.42)
        G = (A + B + C) / 3
        gd = Dot(G, color=YELLOW, radius=0.1)
        gl = self.mt("G", font_size=36, color=YELLOW).next_to(gd, DOWN, buff=0.12)
        self.play(FadeIn(gd), Flash(gd, color=YELLOW, flash_radius=0.5), Write(gl), run_time=0.9)

        r1 = self.mixed(
            ("text", "每一层的三个顶点（蓝绿橙点）分别落在三条中线上", INK),
            text_size=36, math_size=42)
        r2 = self.mixed(
            ("text", "随层级加深，它们一同滑向同一个点 —— 这正是要证明的事情", MUTED),
            text_size=36, math_size=42)
        r3 = self.mixed(
            ("text", "但「看起来在收拢」不等于「真的共点」，收官必须靠", MUTED),
            ("text", "「闭区间套定理」", YELLOW),
            text_size=36, math_size=44)
        panel = VGroup(r1, r2, r3).arrange(DOWN, buff=0.62).move_to([4.6, 0.9, 0])
        for line in (r1, r2, r3):
            self.fit(line, width=6.6)
            self.play(FadeIn(line, shift=LEFT * 0.3), run_time=0.8)
        self.wait(2.2)
        self.clear_scene()

    # ───────────────────── S2 思路分析 ─────────────────────
    def strategy_page(self):
        bar = self.title_bar("证明思路分析")
        self.play(Write(bar), run_time=0.8)
        s1 = self.mixed(("text", "一、升维：逐次取三边中点，构造嵌套三角形序列 ", BLUE),
                        ("math", r"T_0\supset T_1\supset T_2\supset\cdots", BLUE),
                        text_size=38, math_size=44)
        s2 = self.mixed(("text", "二、不变量：每一层的三个新顶点，恰好始终落在原三角形的三条中线上", GREEN),
                        text_size=38, math_size=44)
        s3 = self.mixed(("text", "三、收网：直径每次减半 ", ORANGE),
                        ("math", r"\to 0", ORANGE),
                        ("text", "，由区间套思想，交集收缩为唯一的点 ", ORANGE),
                        ("math", r"\xi", ORANGE),
                        text_size=38, math_size=44)
        s4 = self.mixed(("text", "四、收官：", VIOLET),
                        ("math", r"\xi", VIOLET),
                        ("text", " 被锁在三条中线上 ⇒ 三中线共点（即重心）", VIOLET),
                        text_size=38, math_size=44)
        content = self.layout_below(bar, s1, s2, s3, s4)
        for line in (s1, s2, s3, s4):
            self.play(Write(line), run_time=0.9)
            self.wait(0.95)
        self.wait(1.8)
        self.clear_scene()

    # ───────────────────── S3 构造嵌套三角形套 ─────────────────────
    def construction_page(self):
        bar = self.title_bar("第一步：构造嵌套的三角形套")
        self.play(Write(bar), run_time=0.8)

        A = np.array([-4.6, -2.9, 0.0]); B = np.array([4.2, -2.9, 0.0]); C = np.array([1.5, 2.15, 0.0])
        T0 = Polygon(A, B, C, color=INK, stroke_width=3.5)
        la = self.mt("A", font_size=34).next_to(A, DL, buff=0.1)
        lb = self.mt("B", font_size=34).next_to(B, DR, buff=0.1)
        lc = self.mt("C", font_size=34).next_to(C, UP, buff=0.1)
        self.play(Create(T0), FadeIn(la), FadeIn(lb), FadeIn(lc), run_time=1.0)

        Ma, Mb, Mc = (B + C) / 2, (C + A) / 2, (A + B) / 2
        m_a = Line(A, Ma, color=BLUE, stroke_width=2.4)
        m_b = Line(B, Mb, color=GREEN, stroke_width=2.4)
        m_c = Line(C, Mc, color=ORANGE, stroke_width=2.4)
        mla = self.mt(r"m_a", font_size=32, color=BLUE).move_to([6.75, 2.2, 0])
        mlb = self.mt(r"m_b", font_size=32, color=GREEN).move_to([6.75, 1.55, 0])
        mlc = self.mt(r"m_c", font_size=32, color=ORANGE).move_to([6.75, 0.9, 0])
        key1 = Line([6.0, 2.2, 0], [6.42, 2.2, 0], color=BLUE, stroke_width=4)
        key2 = Line([6.0, 1.55, 0], [6.42, 1.55, 0], color=GREEN, stroke_width=4)
        key3 = Line([6.0, 0.9, 0], [6.42, 0.9, 0], color=ORANGE, stroke_width=4)
        self.play(Create(m_a), Create(m_b), Create(m_c),
                  FadeIn(mla), FadeIn(mlb), FadeIn(mlc),
                  FadeIn(key1), FadeIn(key2), FadeIn(key3), run_time=1.2)

        cols = [YELLOW, VIOLET, TEAL, PINK]
        cur = (A, B, C)
        polys = []
        dots_prev = VGroup()
        for i in range(4):
            A2 = (cur[1] + cur[2]) / 2
            B2 = (cur[2] + cur[0]) / 2
            C2 = (cur[0] + cur[1]) / 2
            poly = Polygon(A2, B2, C2, color=cols[i], stroke_width=2.6)
            polys.append(poly)
            dots = VGroup(Dot(A2, radius=0.055, color=BLUE),
                          Dot(B2, radius=0.055, color=GREEN),
                          Dot(C2, radius=0.055, color=ORANGE))
            tlabel = None
            if i < 2:
                tlabel = self.mt("T_%d" % (i + 1), font_size=30, color=cols[i])
                tlabel.move_to((A2 + B2 + C2) / 3 + np.array([1.3, 0.35, 0]))
            self.play(Create(poly), FadeIn(dots), run_time=0.7)
            if tlabel is not None:
                self.play(FadeIn(tlabel), run_time=0.35)
            self.wait(1.25 if i < 2 else 0.9)
            cur = (A2, B2, C2)
            dots_prev.add(dots)

        G = (A + B + C) / 3
        gdot = Dot(G, color=YELLOW, radius=0.09)
        cap = self.mixed(
            ("text", "每深入一层：直径减半，面积缩为", MUTED),
            ("math", r"\tfrac{1}{4}", MUTED),
            ("text", "；", MUTED),
            ("math", r"d(T_n)=d(T_0)\,/\,2^{n}\to 0", MUTED),
            text_size=32, math_size=40)
        cap.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(cap), FadeIn(gdot), run_time=0.8)
        self.wait(1.2)

        grp = VGroup(T0, la, lb, lc, m_a, m_b, m_c, *polys, dots_prev, gdot)
        self.play(grp.animate.scale(2.7, about_point=G), run_time=1.8)
        self.wait(1.2)
        self.play(grp.animate.scale(1 / 2.7, about_point=G), run_time=1.2)
        self.wait(1.6)
        self.clear_scene()

    # ───────────────────── S4 不变量（上）：亲手算两层 ─────────────────────
    def invariant_a(self):
        bar = self.title_bar("第二步 · 不变量（上）：亲手算两层")
        self.play(Write(bar), run_time=0.8)
        l1 = self.zh("对三边取中点（重心坐标：三个数之和为 1）", font_size=38)
        l2 = self.mt_small(
            r"A_1=\big(0,\ \tfrac{1}{2},\ \tfrac{1}{2}\big)\in m_a,\ \ "
            r"B_1=\big(\tfrac{1}{2},\ 0,\ \tfrac{1}{2}\big)\in m_b,\ \ "
            r"C_1=\big(\tfrac{1}{2},\ \tfrac{1}{2},\ 0\big)\in m_c",
            font_size=44)
        l3 = self.mixed(
            ("text", "再取中点，", INK),
            ("math", r"A_2=\tfrac{1}{2}(B_1+C_1)=\big(\tfrac{1}{2},\ \tfrac{1}{4},\ \tfrac{1}{4}\big)", YELLOW),
            ("text", "—— 第 2、3 坐标仍相等，仍在", INK),
            ("math", r"m_a", BLUE),
            ("text", "上！", INK),
            text_size=38, math_size=44)
        content = self.layout_below(bar, l1, l2, l3)
        self.write_text(l1)
        self.write_formula(l2, run_time=1.3)
        self.write_formula(l3, run_time=1.2)
        hint = self.zh("中点的重心坐标 = 两端坐标逐个取平均（线性性）", font_size=32, color=MUTED)
        hint.next_to(content, DOWN, buff=0.75)
        self.fit(hint)
        self.play(FadeIn(hint), run_time=0.7)
        self.wait(2.0)
        self.clear_scene()

    # ───────────────────── S5 不变量（下）：归纳锁死 ─────────────────────
    def invariant_b(self):
        bar = self.title_bar("第二步 · 不变量（下）：归纳锁死")
        self.play(Write(bar), run_time=0.8)
        l1 = self.mt_small(
            r"A_n=(1-2p_n,\ p_n,\ p_n),\ \ B_n=(p_n,\ 1-2p_n,\ p_n),\ \ C_n=(p_n,\ p_n,\ 1-2p_n)",
            font_size=42)
        l2 = self.mixed(
            ("text", "中点 = 坐标取平均 ⇒ ", INK),
            ("math", r"A_{n+1}=\Big(p_n,\ \tfrac{1-p_n}{2},\ \tfrac{1-p_n}{2}\Big)", YELLOW),
            ("text", "，B、C 两顶点同理", INK),
            text_size=38, math_size=44)
        l3 = self.mixed(
            ("text", "「第 2、3 坐标相等」这一特征逐层保持 ⇒ 每层顶点分别骑在 ", INK),
            ("math", r"m_a,\,m_b,\,m_c", INK),
            ("text", " 上", INK),
            text_size=38, math_size=44)
        l4 = self.mixed(
            ("text", "公共值", MUTED),
            ("math", r"p_{n+1}=\tfrac{1-p_n}{2}:\ \ \tfrac{1}{2},\ \tfrac{1}{4},\ \tfrac{3}{8},\ \tfrac{5}{16},\ \cdots\ \to\ \tfrac{1}{3}", YELLOW),
            ("text", "（重心在望）", MUTED),
            text_size=34, math_size=42)
        content = self.layout_below(bar, l1, l2, l3, l4)
        for line in (l1, l2, l3, l4):
            self.write_formula(line, run_time=1.05)
        self.wait(2.0)
        self.clear_scene()

    # ───────────────────── S6 区间套收网 ─────────────────────
    def closure_page(self):
        bar = self.title_bar("第三步：闭区间套定理收网")
        self.play(Write(bar), run_time=0.8)
        l1 = self.mixed(
            ("text", "把每个三角形投影到 x 轴，则", INK),
            ("math", r"\pi_x(T_0)\supseteq\pi_x(T_1)\supseteq\cdots", INK),
            ("text", "，长度", INK),
            ("math", r"\le d(T_0)/2^{\,n}\to 0", INK),
            ("text", "，构成闭区间套", INK),
            text_size=36, math_size=42)
        l2 = self.mixed(
            ("text", "由闭区间套定理：存在唯一的", INK),
            ("math", r"\xi=(\xi_x,\ \xi_y)", YELLOW),
            ("text", "，落在所有", INK),
            ("math", r"T_n", INK),
            ("text", "中", INK),
            text_size=36, math_size=42)
        l3 = self.mixed(
            ("math", r"A_n\in m_a,\ \ A_n\to\xi", INK),
            ("text", "，而中线是闭集 ⇒ ", INK),
            ("math", r"\xi\in m_a", BLUE),
            ("text", "；同理 ", INK),
            ("math", r"\xi\in m_b,\ \xi\in m_c", INK),
            text_size=36, math_size=42)
        l4 = self.mixed(
            ("math", r"\xi\in m_a\cap m_b\cap m_c", GREEN),
            ("text", "，三条中线共点 ∎", GREEN),
            text_size=40, math_size=48)
        content = self.layout_below(bar, l1, l2, l3, l4)
        for line in (l1, l2, l3):
            self.write_formula(line, run_time=1.0)
        self.play(Write(l4), run_time=1.0)
        self.wait(2.4)
        self.clear_scene()

    # ───────────────────── S7 附赠 2:1 分割比 ─────────────────────
    def ratio_moment(self):
        top = self.mixed(
            ("text", "附赠：交点恰把每条中线分成 2 : 1 —— 它就是重心 ", YELLOW),
            ("math", r"G", YELLOW),
            text_size=40, math_size=48)
        top.to_edge(UP, buff=0.7)
        self.play(Write(top), run_time=0.9)

        A = np.array([-2.6, -2.5, 0.0]); B = np.array([2.8, -2.5, 0.0]); C = np.array([1.3, 1.9, 0.0])
        tri = Polygon(A, B, C, color=INK, stroke_width=3)
        Ma = (B + C) / 2
        med = Line(A, Ma, color=BLUE, stroke_width=3)
        G = (A + B + C) / 3
        gd = Dot(G, color=YELLOW, radius=0.1)
        gl = self.mt("G", font_size=38, color=YELLOW).next_to(gd, RIGHT, buff=0.12)
        t2 = self.mt("2", font_size=40, color=BLUE).move_to(A + 0.62 * (G - A) + np.array([-0.42, 0.28, 0]))
        t1 = self.mt("1", font_size=40, color=ORANGE).move_to(G + 0.58 * (Ma - G) + np.array([0.4, 0.22, 0]))
        side = VGroup(self.mt(r"\big(\tfrac13,\ \tfrac13,\ \tfrac13\big)", font_size=36, color=MUTED))
        bot = self.mixed(
            ("math", r"p_n\to\tfrac{1}{3}", MUTED),
            ("text", "直接读出：三条中线交于一点，且向顶点方向占 2 份", MUTED),
            text_size=34, math_size=42)
        bot.to_edge(DOWN, buff=0.5)
        grp = VGroup(tri, med, gd, gl, t2, t1)
        self.play(Create(tri), Create(med), run_time=0.9)
        self.play(FadeIn(gd), Write(gl), run_time=0.6)
        self.play(Indicate(t2, color=BLUE), Indicate(t1, color=ORANGE), run_time=1.0)
        self.play(FadeIn(bot), run_time=0.7)
        self.wait(2.4)
        self.clear_scene()

    # ───────────────────── S8 拓展：定理完整证明 ─────────────────────
    def extension_proof(self):
        bar = self.title_bar("拓展 · 闭区间套定理的完整证明", color=VIOLET)
        self.play(Write(bar), run_time=0.8)
        l1 = self.mixed(
            ("text", "存在性：数列", VIOLET),
            ("math", r"\{a_n\}", INK),
            ("text", " 递增、有上界 ", INK),
            ("math", r"b_1", INK),
            ("text", "，由确界原理，", INK),
            ("math", r"\xi=\sup_{n}\{a_n\}", YELLOW),
            ("text", " 存在", INK),
            text_size=36, math_size=44)
        l2 = self.mixed(
            ("text", "对任意 n 及 m ≥ n，", INK),
            ("math", r"a_n\le a_m\le \xi\le b_m\le b_n", INK),
            ("text", "，故 ", INK),
            ("math", r"\xi\in[a_n,b_n]", INK),
            ("text", "，进而", INK),
            ("math", r"\xi\in\bigcap_{n\ge1}[a_n,b_n]", GREEN),
            text_size=36, math_size=44)
        l3 = self.mixed(
            ("text", "唯一性：若 ", INK),
            ("math", r"\eta\ne\xi", INK),
            ("text", " 同属交集，则 ", INK),
            ("math", r"b_n-a_n\ \ge\ |\eta-\xi|\ >\ 0", RED),
            ("text", " 恒成立，与 ", INK),
            ("math", r"b_n-a_n\to 0", INK),
            ("text", " 矛盾 ∎", INK),
            text_size=36, math_size=44)
        content = self.layout_below(bar, l1, l2, l3)
        for line in (l1, l2, l3):
            self.write_formula(line, run_time=1.1)
        l4 = self.mixed(
            ("text", "应用：二分法求根、零点存在性、紧性论证 —— 一切从「长度归零」开始", MUTED),
            text_size=32, math_size=38)
        l4.next_to(content, DOWN, buff=0.8)
        self.fit(l4)
        self.play(FadeIn(l4), run_time=0.7)
        self.wait(2.2)
        self.clear_scene()

    # ───────────────── S8.5 对比：传统证法一瞥 ─────────────────
    def classic_view(self):
        bar = self.title_bar("对比 · 传统证法一瞥", color=ORANGE)
        self.play(Write(bar), run_time=0.8)
        l1 = self.mixed(
            ("text", "位似法：两中线交于 G，中位线 ", INK),
            ("math", r"A'B'\parallel AB", INK),
            ("text", " ⇒ ", INK),
            ("math", r"\triangle GAB\sim\triangle GA'B'", INK),
            ("text", "（比 2 : 1）", INK),
            text_size=36, math_size=44)
        l2 = self.mixed(
            ("text", "面积法：", INK),
            ("math", r"[GBC]=[GCA]=\tfrac{1}{3}[ABC]", INK),
            ("text", " ⇒ A、B 到直线 GC 等距 ⇒ GC 过 AB 中点", INK),
            text_size=36, math_size=44)
        l3 = self.mixed(
            ("text", "区间套证法的独特之处：不用相似形，只用「中点 + 完备性」", TEAL),
            text_size=36, math_size=44)
        l4 = self.mixed(
            ("text", "因而能原样推广到高维单形 —— 单形的各「中线」必共点", TEAL),
            text_size=36, math_size=44)
        content = self.layout_below(bar, l1, l2, l3, l4)
        for line in (l1, l2, l3, l4):
            self.write_formula(line, run_time=1.0)
        self.wait(2.0)
        self.clear_scene()

    # ───────────────────── S9 拓展：延伸思考 ─────────────────────
    def extension_thoughts(self):
        bar = self.title_bar("拓展 · 延伸思考：实数完备性「全家福」", color=GREEN)
        self.play(Write(bar), run_time=0.8)
        names = ["确界原理", "单调有界定理", "闭区间套定理", "有限覆盖定理", "聚点原理", "柯西收敛准则"]
        boxes = VGroup()
        for s in names:
            t = self.zh(s, font_size=30)
            box = RoundedRectangle(corner_radius=0.18, width=t.width + 0.55,
                                   height=0.85, color=TEAL, stroke_width=2)
            box.add(t.move_to(box))
            boxes.add(box)
        row1 = VGroup(boxes[0], boxes[1], boxes[2]).arrange(RIGHT, buff=0.55)
        row2 = VGroup(boxes[3], boxes[4], boxes[5]).arrange(RIGHT, buff=0.55)
        web = VGroup(row1, row2).arrange(DOWN, buff=1.0).move_to([0, 0.4, 0])
        arrows1 = VGroup(*[Arrow(row1[i].get_right(), row1[i + 1].get_left(),
                                 buff=0.06, stroke_width=3, color=MUTED,
                                 max_tip_length_to_length_ratio=0.35) for i in range(2)])
        arrows2 = VGroup(*[Arrow(row2[i].get_right(), row2[i + 1].get_left(),
                                 buff=0.06, stroke_width=3, color=MUTED,
                                 max_tip_length_to_length_ratio=0.35) for i in range(2)])
        link = self.mt(r"\Longleftrightarrow", font_size=44, color=YELLOW).move_to(
            [(row1[2].get_x() + row2[2].get_x()) / 2 + 0.0, (row1.get_y() + row2.get_y()) / 2, 0])
        diag1 = Arrow(row2[0].get_top(), row1[0].get_bottom(), buff=0.08,
                      stroke_width=3, color=MUTED, max_tip_length_to_length_ratio=0.25)
        diag2 = Arrow(row1[2].get_bottom(), row2[2].get_top(), buff=0.08,
                      stroke_width=3, color=MUTED, max_tip_length_to_length_ratio=0.25)
        for b in boxes:
            self.play(FadeIn(b, scale=0.8), run_time=0.42)
        self.play(Create(arrows1), Create(arrows2), Write(link),
                  Create(diag1), Create(diag2), run_time=1.0)
        bottom = self.zh("六条定理相互等价，共同刻画实数系的完备性 —— 极限理论坚实的地基",
                         font_size=34, color=MUTED)
        bottom.to_edge(DOWN, buff=0.5)
        self.play(FadeIn(bottom), run_time=0.7)
        self.wait(2.2)
        self.clear_scene()

    # ───────────────────── S10 结尾 ─────────────────────
    def ending(self):
        t1 = self.zh("区间套：以有限驾驭无限", font_size=58, weight=BOLD)
        t1.move_to([0, 1.3, 0])
        t2 = self.zh("升维 · 不变量 · 收网", font_size=42, color=YELLOW)
        t2.next_to(t1, DOWN, buff=0.5)
        self.play(Write(t1), run_time=1.0)
        self.play(FadeIn(t2, shift=UP * 0.3), run_time=0.8)
        A = np.array([-1.7, -2.1, 0]); B = np.array([1.7, -2.1, 0]); C = np.array([0.7, 0.4, 0])
        tri = Polygon(A, B, C, color=INK, stroke_width=2.5).move_to([0, -2.9, 0])
        v = tri.get_vertices()
        G = v.mean(axis=0)
        m1 = Line(v[0], (v[1] + v[2]) / 2, color=BLUE, stroke_width=2)
        m2 = Line(v[1], (v[2] + v[0]) / 2, color=GREEN, stroke_width=2)
        m3 = Line(v[2], (v[0] + v[1]) / 2, color=ORANGE, stroke_width=2)
        gd = Dot(G, color=YELLOW, radius=0.08)
        grp = VGroup(tri, m1, m2, m3, gd)
        self.play(Create(grp), run_time=1.0)
        self.play(Flash(gd, color=YELLOW, flash_radius=0.5), run_time=0.8)
        self.wait(2.6)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
        self.wait(0.3)
