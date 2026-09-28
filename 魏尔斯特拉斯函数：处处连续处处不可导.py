# -*- coding: utf-8 -*-
"""任务3：魏尔斯特拉斯函数 —— 处处连续、处处不可导
作图参数：a=0.9, b=7，满足魏尔斯特拉斯原始条件 ab=6.3 > 1+3π/2≈5.712
         （即所画函数确实是原定理意义下处处不可导的）
W(x)=Σ a^n cos(b^n π x)
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skill_base import *

A_PAR = 0.9
B_PAR = 7


def W_partial(x, n_max, a=A_PAR, b=B_PAR):
    """部分和 Σ_{k=0}^{n_max} a^k cos(b^k π x)，向量化"""
    t = np.zeros_like(x)
    amp = 1.0
    freq = 1.0
    for k in range(n_max + 1):
        t += amp * np.cos(freq * np.pi * x)
        amp *= a
        freq *= b
    return t


class WeierstrassFunction(SkillScene):

    def construct(self):
        self.camera.background_color = BG
        self.opening()
        self.history_page()
        self.definition_page()
        self.stack_page()
        self.compare_page()
        self.continuity_page()
        self.nondiff_page()
        self.tangent_fail_page()
        self.zoom_page()
        self.fractal_page()
        self.brownian_page()
        self.ending()

    # ───────────── S0 开场 ─────────────
    def opening(self):
        title = self.zh("魏尔斯特拉斯函数", font_size=62, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        sub = self.mixed(
            ("text", "处处连续，却处处不可导 —— 一条没有切线的连续曲线", YELLOW),
            text_size=36, math_size=40)
        sub.next_to(title, DOWN, buff=0.3)
        self.play(Write(title), run_time=1.0)
        self.play(FadeIn(sub), run_time=0.8)

        axes = Axes(x_range=[-2.3, 2.3, 1], y_range=[-4.8, 4.8, 2],
                    x_length=13.6, y_length=4.6,
                    axis_config={"color": MUTED, "stroke_width": 1.5,
                                 "include_ticks": False})
        axes.move_to([0, -1.6, 0])
        curve = axes.plot(lambda x: W_partial(x, 4), x_range=[-2.2, 2.2, 0.001],
                          color=YELLOW, stroke_width=2.0)
        self.play(Create(axes), run_time=0.9)
        self.play(Create(curve), run_time=2.2)
        tag = self.mixed(
            ("math", r"W(x)=\sum_{n=0}^{\infty}a^{n}\cos(b^{n}\pi x)", YELLOW),
            text_size=30, math_size=38)
        tag.to_edge(DOWN, buff=0.3)
        self.play(Write(tag), run_time=1.0)
        self.wait(2.2)
        self.clear_scene()

    # ───────────── S1 历史冲击 ─────────────
    def history_page(self):
        bar = self.title_bar("1872 · 一条曲线震动了整个数学界", color=RED)
        self.play(Write(bar), run_time=0.8)
        l1 = self.mixed(
            ("text", "当时的主流直觉（柯西等）：连续函数几乎总有切点，「病态」只是例外", INK),
            text_size=36, math_size=42)
        l2 = self.mixed(
            ("text", "1872 年，魏尔斯特拉斯在柏林科学院公布：存在", INK),
            ("text", "处处连续却处处不可导", RED),
            ("text", "的函数", INK),
            text_size=36, math_size=42)
        l3 = self.mixed(
            ("text", "庞加莱惊呼：直觉在此「翻车」—— 分析学从此进入严格化时代", ORANGE),
            text_size=36, math_size=42)
        l4 = self.mixed(
            ("text", "埃米尔特坦言：「在充满荆棘的函数世界里，我转身逃离那个令人恐惧的『无处可导』。」", MUTED),
            text_size=32, math_size=38)
        content = self.layout_below(bar, l1, l2, l3, l4)
        for line in (l1, l2, l3, l4):
            self.write_formula(line, run_time=1.0)
        self.wait(2.2)
        self.clear_scene()

    # ───────────── S2 定义 ─────────────
    def definition_page(self):
        bar = self.title_bar("函数定义与参数", color=BLUE)
        self.play(Write(bar), run_time=0.8)
        l1 = self.mt(r"W(x)=\sum_{n=0}^{\infty}a^{n}\cos\!\big(b^{n}\pi x\big)",
                     font_size=60, color=YELLOW)
        l2 = self.mixed(
            ("text", "取 ", INK),
            ("math", r"0<a<1", INK),
            ("text", "，b 为奇数，且 ", INK),
            ("math", r"ab>1+\dfrac{3\pi}{2}\approx 5.71", RED),
            ("text", "（魏尔斯特拉斯 1872 原始条件）", MUTED),
            text_size=34, math_size=42)
        l3 = self.mixed(
            ("text", "作图取 ", INK),
            ("math", r"a=0.9,\ b=7", GREEN),
            ("text", "，此时 ", INK),
            ("math", r"ab=6.3>5.71", GREEN),
            ("text", "，正是定理适用的情形", INK),
            text_size=34, math_size=42)
        l4 = self.mixed(
            ("text", "物理图像：振幅按 ", INK),
            ("math", r"a^{n}", INK),
            ("text", " 衰减、频率按 ", INK),
            ("math", r"b^{n}", INK),
            ("text", " 膨胀的余弦波，一层层叠加", INK),
            text_size=34, math_size=42)
        content = self.layout_below(bar, l1, l2, l3, l4)
        for line in (l1, l2, l3, l4):
            self.write_formula(line, run_time=1.15)
        self.wait(2.2)
        self.clear_scene()

    # ───────────── S3 部分和逐层叠加 ─────────────
    def stack_page(self):
        bar = self.title_bar("逐层叠加：锯齿是怎样炼成的", color=TEAL)
        self.play(Write(bar), run_time=0.8)
        axes = Axes(x_range=[-1.05, 1.05, 0.5], y_range=[-6.5, 6.5, 2],
                    x_length=13.8, y_length=4.9,
                    axis_config={"color": MUTED, "stroke_width": 1.5,
                                 "include_ticks": False})
        axes.move_to([0, -1.35, 0])
        self.play(Create(axes), run_time=0.9)

        cols = [BLUE, GREEN, ORANGE, VIOLET, RED, YELLOW]
        tag = None
        prev_sum = None
        for n in range(6):
            col = cols[n]

            def f(x, n=n):
                return W_partial(x, n)
            curve = axes.plot(f, x_range=[-1.02, 1.02, 0.001], color=col,
                              stroke_width=2.6 if n < 5 else 3.0)
            if prev_sum is None:
                self.play(Create(curve), run_time=1.1)
            else:
                self.play(Transform(prev_sum, curve), run_time=1.1)
                curve = prev_sum
            prev_sum = curve
            new_tag = self.mixed(
                ("text", "加到第 ", INK),
                ("math", r"n=%d" % n, col),
                ("text", " 项（频率 ", INK),
                ("math", r"7^{%d}" % n, col),
                ("text", "）", INK),
                text_size=32, math_size=38)
            if tag is None:
                new_tag.move_to([0, 1.45, 0])
                tag = new_tag
                self.play(FadeIn(tag), run_time=0.35)
            else:
                new_tag.move_to(tag)
                self.play(Transform(tag, new_tag), run_time=0.35)
            self.wait(1.5 if n < 4 else 2.0)

        note = self.mixed(
            ("text", "每一层都更小、更密 —— 无穷层叠完，就再没有一处光滑", RED),
            text_size=32, math_size=38)
        note.to_edge(DOWN, buff=0.12)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(2.2)
        self.clear_scene()

    # ───────────── S3.5 对比：个别尖角 vs 处处尖角 ─────────────
    def compare_page(self):
        bar = self.title_bar("从「个别尖角」到「处处尖角」", color=ORANGE)
        self.play(Write(bar), run_time=0.8)

        axL = Axes(x_range=[-2.4, 2.4, 1], y_range=[-0.6, 2.6, 1],
                   x_length=6.2, y_length=2.6,
                   axis_config={"color": MUTED, "stroke_width": 1.5,
                                "include_ticks": False})
        axL.move_to([-3.6, -0.7, 0])
        cL = axL.plot(lambda x: abs(x), x_range=[-2.3, 2.3, 0.01],
                      color=BLUE, stroke_width=3.5)
        tL = self.mixed(("math", r"y=|x|", BLUE),
                        ("text", "：只有一个尖角（x=0）", INK),
                        text_size=32, math_size=38)
        tL.next_to(axL, DOWN, buff=0.4)

        axR = Axes(x_range=[-2.4, 2.4, 1], y_range=[-4.8, 4.8, 2],
                   x_length=6.2, y_length=2.6,
                   axis_config={"color": MUTED, "stroke_width": 1.5,
                                "include_ticks": False})
        axR.move_to([3.6, -0.7, 0])
        cR = axR.plot(lambda x: W_partial(x, 4), x_range=[-2.3, 2.3, 0.001],
                      color=YELLOW, stroke_width=2.2)
        tR = self.mixed(("math", r"W(x)", YELLOW),
                        ("text", "：每一个点都是尖角", RED),
                        text_size=32, math_size=38)

        self.play(Create(axL), Create(cL), Write(tL), run_time=1.2)
        self.play(Create(axR), Create(cR), Write(tR), run_time=1.2)
        bottom = self.mixed(
            ("text", "「连续」与「可导」就此正式分家：", INK),
            ("text", "连续只需不「断」，可导还要求处处「平」", YELLOW),
            text_size=34, math_size=38)
        bottom.to_edge(DOWN, buff=0.5)
        self.fit(bottom)
        self.play(FadeIn(bottom), run_time=0.9)
        self.wait(2.2)
        self.clear_scene()

    # ───────────── S4 处处连续：一致收敛 ─────────────
    def continuity_page(self):
        bar = self.title_bar("为什么处处连续？—— 一致收敛压阵", color=BLUE)
        self.play(Write(bar), run_time=0.8)
        l1 = self.mixed(
            ("text", "每项都是连续函数，但无穷多项相加需要「控制总量」", INK),
            text_size=36, math_size=42)
        l2 = self.mixed(
            ("text", "优级数判别法（M-判别法）：", INK),
            ("math", r"\big|a^{n}\cos(b^{n}\pi x)\big|\le a^{n}", INK),
            ("text", "，且", INK),
            ("math", r"\sum_{n\ge0}a^{n}=\frac{1}{1-a}<\infty", GREEN),
            text_size=34, math_size=42)
        l3 = self.mixed(
            ("text", "级数在整条数轴上一致收敛 ⇒ 和函数 W(x) 处处连续 ∎", YELLOW),
            text_size=36, math_size=42)
        content = self.layout_below(bar, l1, l2, l3)
        for line in (l1, l2, l3):
            self.write_formula(line, run_time=1.1)
        l4 = self.mixed(
            ("text", "直白地说：每一层的振幅上界 aⁿ 求和有限，「抖动总量」被牢牢锁住", MUTED),
            text_size=32, math_size=38)
        l4.next_to(content, DOWN, buff=0.75)
        self.fit(l4)
        self.play(FadeIn(l4), run_time=0.8)
        self.wait(2.0)
        self.clear_scene()

    # ───────────── S5 处处不可导：差商要点 ─────────────
    def nondiff_page(self):
        bar = self.title_bar("为什么处处不可导？—— 差商被高频层劫持", color=RED)
        self.play(Write(bar), run_time=0.8)
        l1 = self.mixed(
            ("text", "可导 = 差商极限存在：", INK),
            ("math", r"\lim_{h\to0}\frac{W(x+h)-W(x)}{h}", YELLOW),
            text_size=36, math_size=44)
        l2 = self.mixed(
            ("text", "取一列特殊步长 ", INK),
            ("math", r"h_{n}=\pm\,b^{-n}", RED),
            ("text", "（恰好对准第 n 层的波峰波谷），则", INK),
            text_size=36, math_size=42)
        l3 = self.mixed(
            ("math", r"\frac{W(x+h_n)-W(x)}{h_n}", INK),
            ("text", " 中，第 n 层贡献出 ~", INK),
            ("math", r"a^{n}b^{n}=(ab)^{n}", RED),
            ("text", " 量级的巨大摆动", INK),
            text_size=34, math_size=42)
        l4 = self.mixed(
            ("text", "由于 ", INK),
            ("math", r"ab>1", RED),
            ("text", "，差商随 n 发散（可证明上界 3π/2 被突破）⇒ 极限不存在 ∎", INK),
            text_size=34, math_size=42)
        content = self.layout_below(bar, l1, l2, l3, l4)
        for line in (l1, l2, l3, l4):
            self.write_formula(line, run_time=1.1)
        note = self.mixed(
            ("text", "直观版：无论放大多少倍，脚下永远有「还没看清的更细锯齿」把切线方向搅乱", MUTED),
            text_size=32, math_size=38)
        note.next_to(content, DOWN, buff=0.6)
        self.fit(note)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(2.2)
        self.clear_scene()

    # ───────────── S5.5 在一点作切线：屡战屡败 ─────────────
    def tangent_fail_page(self):
        bar = self.title_bar("现场实验 · 在一点作切线，屡战屡败", color=RED)
        self.play(Write(bar), run_time=0.8)
        axes = Axes(x_range=[-1.15, 1.15, 0.5], y_range=[-6.5, 6.5, 2],
                    x_length=13.8, y_length=4.9,
                    axis_config={"color": MUTED, "stroke_width": 1.5,
                                 "include_ticks": False})
        axes.move_to([0, -1.35, 0])
        self.play(Create(axes), run_time=0.8)
        x0 = -0.282
        curve = axes.plot(lambda x: W_partial(x, 5), x_range=[-1.1, 1.1, 0.0009],
                          color=YELLOW, stroke_width=2.4)
        self.play(Create(curve), run_time=1.2)
        y0 = W_partial(np.array([x0]), 5)[0]
        pd = Dot(axes.c2p(x0, y0), color=RED, radius=0.09)
        pl = self.mixed(("text", "割线斜率（越小越应该像切线）", MUTED),
                        text_size=30, math_size=34)
        pl.move_to([0, 1.52, 0])
        self.play(FadeIn(pd), FadeIn(pl), run_time=0.7)

        sec = None
        stag = None
        for h in (0.45, 0.18, 0.07, 0.028, 0.011):
            m = (W_partial(np.array([x0 + h]), 5)[0] - y0) / h
            def line_fn(t, m=m):
                return y0 + m * (t - x0)
            secant = axes.plot(line_fn, x_range=[-1.12, 1.12, 0.01],
                               color=RED, stroke_width=2.4)
            if sec is None:
                self.play(Create(secant), run_time=0.8)
            else:
                self.play(Transform(sec, secant), run_time=0.8)
            sec = secant
            new_tag = self.mixed(
                ("math", r"h=%.3f:\ \ \frac{\Delta W}{\Delta x}\approx %+.1f" % (h, m), RED),
                text_size=30, math_size=36)
            if stag is None:
                new_tag.move_to([5.0, 1.52, 0])
                stag = new_tag
                self.play(FadeIn(stag), run_time=0.3)
            else:
                new_tag.move_to(stag)
                self.play(Transform(stag, new_tag), run_time=0.3)
            self.wait(1.2)
        note = self.mixed(
            ("text", "步长越小，斜率越癫 —— 割线的极限根本不存在", RED),
            text_size=32, math_size=38)
        note.to_edge(DOWN, buff=0.12)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(2.0)
        self.clear_scene()

    # ───────────── S7.5 后话：布朗运动 ─────────────
    def brownian_page(self):
        bar = self.title_bar("后话：随机世界里的「魏尔斯特拉斯」", color=TEAL)
        self.play(Write(bar), run_time=0.8)
        rng = np.random.default_rng(42)
        npts = 4000
        path = np.cumsum(rng.normal(0.0, 0.05, npts))
        xs = np.linspace(0.0, 1.0, npts)

        def bf(u):
            return np.interp((u + 2.2) / 4.4, xs, path)
        axes = Axes(x_range=[-2.3, 2.3, 1], y_range=[-1.6, 1.6, 1],
                    x_length=13.6, y_length=4.0,
                    axis_config={"color": MUTED, "stroke_width": 1.5,
                                 "include_ticks": False})
        axes.move_to([0, -1.3, 0])
        curve = axes.plot(bf, x_range=[-2.2, 2.2, 0.001],
                          color=TEAL, stroke_width=1.8)
        self.play(Create(axes), run_time=0.8)
        self.play(Create(curve), run_time=2.2)
        l1 = self.mixed(
            ("text", "布朗运动（维纳过程）的样本路径：以概率 1 ", INK),
            ("text", "处处连续、处处不可导", YELLOW),
            text_size=36, math_size=40)
        l2 = self.mixed(
            ("text", "维纳 1923 年的严格证明，让当年的「怪物」成为随机现象的常态", MUTED),
            text_size=34, math_size=38)
        panel = VGroup(l1, l2).arrange(DOWN, buff=0.5).to_edge(DOWN, buff=0.35)
        for line in panel:
            self.fit(line)
            self.play(FadeIn(line), run_time=0.8)
        self.wait(2.2)
        self.clear_scene()

    # ───────────── S6 分形放大：自相似 ─────────────
    def zoom_page(self):
        bar = self.title_bar("无限放大：每一层都藏着完整的自己", color=VIOLET)
        self.play(Write(bar), run_time=0.8)
        axes = Axes(x_range=[-1.15, 1.15, 0.5], y_range=[-6.5, 6.5, 2],
                    x_length=13.8, y_length=4.9,
                    axis_config={"color": MUTED, "stroke_width": 1.5,
                                 "include_ticks": False})
        axes.move_to([0, -1.35, 0])
        self.play(Create(axes), run_time=0.8)
        curve = axes.plot(lambda x: W_partial(x, 5),
                          x_range=[-1.1, 1.1, 0.0009],
                          color=YELLOW, stroke_width=2.2)
        self.play(Create(curve), run_time=1.4)

        stages = [
            (-0.4, 0.55, 5, "放大 2 倍"),
            (-0.28, 0.055, 6, "再放大 10 倍"),
            (-0.282, 0.00275, 7, "继续放大 20 倍"),
            (-0.28195, 0.0001375, 8, "再放大 20 倍 · 结构依旧"),
        ]
        for cx, half, n_terms, label in stages:
            def f(x, cx=cx, half=half, n_terms=n_terms):
                return W_partial(cx - half + (x + 1) * half, n_terms)
            new_curve = axes.plot(f, x_range=[-1.1, 1.1, 0.0009], color=YELLOW,
                                  stroke_width=2.2)
            lbl = self.zh(label, font_size=30, color=VIOLET)
            lbl.move_to([0, 1.52, 0])
            if hasattr(self, "_zl"):
                self.play(Transform(self._zl, lbl), Transform(curve, new_curve),
                          run_time=1.3)
            else:
                self._zl = lbl
                self.play(FadeIn(lbl), Transform(curve, new_curve), run_time=1.3)
            self.wait(1.55)
        cap = self.mixed(
            ("text", "自相似：任何一段放大数百倍，仍与整体一样粗糙 —— 处处不可导的直观根源", MUTED),
            text_size=30, math_size=36)
        cap.to_edge(DOWN, buff=0.1)
        self.play(FadeIn(cap), run_time=0.8)
        self.wait(2.0)
        self.clear_scene()

    # ───────────── S7 分形维数与观念冲击 ─────────────
    def fractal_page(self):
        bar = self.title_bar("余波：从「病态」到分形几何的先声", color=GREEN)
        self.play(Write(bar), run_time=0.8)
        l1 = self.mixed(
            ("text", "图像的盒维数：", INK),
            ("math", r"\dim_B = 2+\frac{\ln a}{\ln b}", YELLOW),
            ("text", "（本题 ", INK),
            ("math", r"\approx 1.95", YELLOW),
            ("text", "，比光滑曲线的 1 更高维）", INK),
            text_size=34, math_size=42)
        l2 = self.mixed(
            ("text", "此后「病态函数」层出不穷：皮亚诺曲线填满正方形、不可求长曲线……", INK),
            text_size=34, math_size=40)
        l3 = self.mixed(
            ("text", "数学家被迫收紧每一个概念：极限、连续、可导、积分全部重新奠基", INK),
            text_size=34, math_size=40)
        l4 = self.mixed(
            ("text", "分形几何（曼德博，1967 起）：海岸线、雪花、股价 —— 粗糙本身成了研究对象", TEAL),
            text_size=34, math_size=40)
        content = self.layout_below(bar, l1, l2, l3, l4)
        for line in (l1, l2, l3, l4):
            self.write_formula(line, run_time=1.05)
        self.wait(2.2)
        self.clear_scene()

    # ───────────── S8 结尾 ─────────────
    def ending(self):
        t1 = self.zh("连续 ≠ 可以作切线", font_size=58, weight=BOLD)
        t1.move_to([0, 1.6, 0])
        t2 = self.zh("魏尔斯特拉斯函数：直觉止步之处，严格由此开始",
                     font_size=36, color=MUTED)
        t2.next_to(t1, DOWN, buff=0.45)
        self.play(Write(t1), run_time=1.0)
        self.play(FadeIn(t2), run_time=0.8)

        axes = Axes(x_range=[-2.3, 2.3, 1], y_range=[-4.8, 4.8, 2],
                    x_length=13.0, y_length=3.6,
                    axis_config={"color": MUTED, "stroke_width": 1.2,
                                 "include_ticks": False})
        axes.move_to([0, -2.2, 0])
        curve = axes.plot(lambda x: W_partial(x, 5), x_range=[-2.2, 2.2, 0.001],
                          color=YELLOW, stroke_width=1.8)
        self.play(Create(curve), run_time=2.0)
        self.wait(3.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
        self.wait(0.3)
