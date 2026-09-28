# -*- coding: utf-8 -*-
"""任务6（v2 大修版）：定积分阿达玛不等式 × 三阶导数 —— 极值点偏移的一般解法
例题：f'(x) = (x−1)(eˣ+2a)（a>0），f 的极值点为 x₀=1，
      f(x) 在 (0,2) 内有两个零点 x₁<x₂，求证 x₁+x₂ < 2。
方法链：f(x₁)=f(x₂) ⇒ ∫f'=0（导数平均值）
        ⇒ f'''=(x+1)eˣ>0 ⇒ f' 严格凸 ⇒ 阿达玛左半 f'(mid) < 平均 = 0 = f'(1)
        ⇒ f''=xeˣ+2a>0 ⇒ f' 递增 ⇒ (x₁+x₂)/2 < 1 ⇒ x₁+x₂<2 ∎（左偏）
数值验证：a=0.1，f(x)=(x−2)eˣ+0.1(x²−2x)+2.4 ⇒ x₁≈0.3507, x₂≈1.4620, 和≈1.8127
        f'(mid)≈−0.25 < 平均 0 < 端点平均 0.517；凹例 g'=(x−1)(2.2−x) ⇒ 和≈2.13>2（右偏）
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skill_base import *

A_PAR = 0.1
fp = lambda x: (x - 1) * (np.exp(x) + 2 * A_PAR)
F = lambda x: (x - 2) * np.exp(x) + A_PAR * (x * x - 2 * x) + 2.4
X1, X2 = 0.3507, 1.4620


class ExtremumShiftHadamard(SkillScene):

    def construct(self):
        self.camera.background_color = BG
        self.opening()
        self.problem_page()
        self.key_idea_page()
        self.hadamard_page()
        self.fprime_visual_page()
        self.step_convex_page()
        self.step_apply_page()
        self.step_mono_page()
        self.graph_page()
        self.template_page()
        self.general_theorem_page()
        self.general_proof_page()
        self.ending()

    # ───────────── S0 开场 ─────────────
    def opening(self):
        title = self.zh("阿达玛不等式 × 三阶导数", font_size=58, weight=BOLD)
        title.to_edge(UP, buff=0.5)
        sub = self.mixed(
            ("text", "极值点偏移的一般解法：", MUTED),
            ("text", "一个积分等式 + 两个符号判断", YELLOW),
            text_size=38, math_size=42)
        sub.next_to(title, DOWN, buff=0.3)
        self.play(Write(title), run_time=1.0)
        self.play(FadeIn(sub), run_time=0.8)

        axes = Axes(x_range=[0, 1, 0.5], y_range=[0, 1.2, 0.5],
                    x_length=5.6, y_length=2.4,
                    axis_config={"color": MUTED, "stroke_width": 1.5,
                                 "include_ticks": False})
        axes.move_to([-2.6, -1.9, 0])
        g = lambda x: 0.35 + 0.9 * (x - 0.5) ** 2 + 0.15 * (x - 0.5)
        curve = axes.plot(g, x_range=[0, 1, 0.01], color=BLUE, stroke_width=3.5)
        chord = DashedLine(axes.c2p(0, g(0)), axes.c2p(1, g(1)),
                           color=MUTED, stroke_width=2, dash_length=0.1)
        dotm = Dot(axes.c2p(0.5, g(0.5)), color=RED, radius=0.06)
        dotc = Dot(axes.c2p(0.5, (g(0) + g(1)) / 2), color=GREEN, radius=0.06)
        vline = DashedLine(axes.c2p(0.5, 0), axes.c2p(0.5, 1.05),
                           color=MUTED, stroke_width=1.5, dash_length=0.09)
        self.play(Create(axes), Create(curve), run_time=1.1)
        self.play(Create(chord), Create(vline), FadeIn(dotm), FadeIn(dotc), run_time=1.0)
        tag = self.mixed(
            ("text", "凸函数的中点值 ", RED),
            ("text", "＜", INK),
            ("text", " 积分平均值 ", GREEN),
            ("text", "＜", INK),
            ("text", " 端点平均 —— 今天全靠它", MUTED),
            text_size=32, math_size=36)
        tag.move_to([3.4, -1.9, 0])
        self.fit(tag, width=7.6)
        self.play(FadeIn(tag), run_time=0.8)
        self.wait(2.0)
        self.clear_scene()

    # ───────────── S1 例题 ─────────────
    def problem_page(self):
        bar = self.title_bar("例题 · 一道经典的左偏证明题", color=BLUE)
        self.play(Write(bar), run_time=0.8)
        l1 = self.mixed(
            ("text", "已知 ", INK),
            ("math", r"f'(x)=(x-1)\big(e^{x}+2a\big)", YELLOW),
            ("text", "（", INK),
            ("math", r"a>0", INK),
            ("text", "），f(x) 的极值点为 ", INK),
            ("math", r"x_0=1", GREEN),
            text_size=36, math_size=44)
        l2 = self.mixed(
            ("text", "若 f(x) 在 (0, 2) 内有两个零点 ", INK),
            ("math", r"x_1<x_2", RED),
            ("text", "，求证：", INK),
            ("math", r"x_1+x_2<2", GREEN),
            text_size=36, math_size=46)
        l3 = self.mixed(
            ("text", "预备：", INK),
            ("math", r"e^{x}+2a>0", INK),
            ("text", " 恒成立 ⇒ ", INK),
            ("math", r"f'(x)=0\iff x=1", INK),
            ("text", "，唯一极小值点", INK),
            text_size=34, math_size=42)
        l4 = self.mixed(
            ("text", "两零点的平均若小于 1，就是「左偏」—— 本题要证的就是它", ORANGE),
            text_size=34, math_size=40)
        content = self.layout_below(bar, l1, l2, l3, l4)
        for line in (l1, l2, l3, l4):
            self.write_formula(line, run_time=1.05)
        self.wait(2.0)
        self.clear_scene()

    # ───────────── S2 核心思想 ─────────────
    def key_idea_page(self):
        bar = self.title_bar("核心思想 · 把「等高」翻译成「积分」", color=TEAL)
        self.play(Write(bar), run_time=0.8)
        l1 = self.mixed(
            ("text", "牛顿–莱布尼茨：", INK),
            ("math", r"\int_{x_1}^{x_2}f'(x)\,dx=f(x_2)-f(x_1)", YELLOW),
            text_size=38, math_size=48)
        l2 = self.mixed(
            ("text", "而 ", INK),
            ("math", r"f(x_1)=f(x_2)", INK),
            ("text", "（两个零点）⇒ 右边恰好为 0：", INK),
            text_size=36, math_size=44)
        l3 = self.mixed(
            ("math", r"\frac{1}{x_2-x_1}\int_{x_1}^{x_2}f'(x)\,dx=0", GREEN),
            text_size=40, math_size=52)
        l4 = self.mixed(
            ("text", "导函数 f′ 在 [x₁, x₂] 上的", INK),
            ("text", "平均值恒等于零", YELLOW),
            ("text", " —— 这就是全部的出发点", INK),
            text_size=34, math_size=40)
        content = self.layout_below(bar, l1, l2, l3, l4)
        for line in (l1, l2, l3, l4):
            self.write_formula(line, run_time=1.1)
        self.wait(2.0)
        self.clear_scene()

    # ───────────── S3 阿达玛不等式 ─────────────
    def hadamard_page(self):
        bar = self.title_bar("新武器 · 阿达玛（Hermite–Hadamard）不等式", color=VIOLET)
        self.play(Write(bar), run_time=0.8)
        l1 = self.mixed(
            ("text", "若 g 在 [a, b] 上二阶可导且 ", INK),
            ("math", r"g''(x)>0", BLUE),
            ("text", "（严格凸），则：", INK),
            text_size=36, math_size=44)
        l2 = self.mt(
            r"g\Big(\frac{a+b}{2}\Big)\ <\ \frac{1}{b-a}\int_a^b g(x)\,dx\ <\ \frac{g(a)+g(b)}{2}",
            font_size=50, color=YELLOW)
        l3 = self.mixed(
            ("text", "中点函数值", INK),
            ("text", " ＜ ", RED),
            ("text", "积分平均值", INK),
            ("text", " ＜ ", RED),
            ("text", "端点平均 —— 凸图像恒在弦下方", MUTED),
            text_size=32, math_size=38)
        l4 = self.mixed(
            ("text", "凹函数（", MUTED),
            ("math", r"g''<0", MUTED),
            ("text", "）时不等号全部反向 —— 一把双刃剑", MUTED),
            text_size=32, math_size=38)
        content = self.layout_below(bar, l1, l2, l3, l4)
        for line in (l1, l2, l3, l4):
            self.write_formula(line, run_time=1.15)
        self.wait(2.2)
        self.clear_scene()

    # ───────────── S4 f' 的阿达玛直观 ─────────────
    def fprime_visual_page(self):
        bar = self.title_bar("放进本题 · f′ 的平均值是 0", color=BLUE)
        self.play(Write(bar), run_time=0.8)
        axes = Axes(x_range=[0.2, 1.6, 0.2], y_range=[-1.3, 2.5, 0.5],
                    x_length=11.6, y_length=4.5,
                    axis_config={"color": MUTED, "stroke_width": 2})
        axes.move_to([0, -1.1, 0])
        curve = axes.plot(fp, x_range=[X1, X2, 0.005], color=BLUE, stroke_width=4)
        zero_line = Line(axes.c2p(0.2, 0), axes.c2p(1.6, 0),
                         color=GREEN, stroke_width=2)
        self.play(Create(axes), Create(curve), Create(zero_line), run_time=1.2)

        chord = DashedLine(axes.c2p(X1, fp(X1)), axes.c2p(X2, fp(X2)),
                           color=MUTED, stroke_width=2.2, dash_length=0.12)
        mid = (X1 + X2) / 2
        vmid = DashedLine(axes.c2p(mid, -1.3), axes.c2p(mid, 2.5),
                          color=MUTED, stroke_width=1.5, dash_length=0.1)
        d1 = Dot(axes.c2p(mid, fp(mid)), color=RED, radius=0.075)
        d2 = Dot(axes.c2p(mid, 0), color=GREEN, radius=0.075)
        t1 = self.mixed(("math", r"f'\big(\tfrac{x_1+x_2}{2}\big)\approx-0.25", RED),
                        text_size=28, math_size=32)
        t1.next_to(d1, DOWN, buff=0.18)
        t2 = self.mixed(
            ("math", r"\text{avg}=0=f'(1)", GREEN), text_size=28, math_size=32)
        t2.next_to(d2, UP, buff=0.15)
        t3 = self.mixed(("text", "弦中点（端点平均）≈ +0.52", MUTED),
                        text_size=28, math_size=32)
        t3.move_to(axes.c2p(0.62, 2.15))
        self.play(Create(chord), Create(vmid), run_time=0.9)
        self.play(FadeIn(d1), Write(t1), FadeIn(d2), Write(t2), FadeIn(t3), run_time=1.1)
        note = self.mixed(
            ("text", "红色（中点值）被死死压在绿色零线以下 —— 阿达玛的直观", MUTED),
            text_size=30, math_size=34)
        note.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(2.2)
        self.clear_scene()

    # ───────────── S5 第一步：三阶导定凸性 ─────────────
    def step_convex_page(self):
        bar = self.title_bar("第一步 · 三阶导数：给 f′ 做凹凸鉴定", color=GREEN)
        self.play(Write(bar), run_time=0.8)
        l1 = self.mixed(
            ("math", r"f''(x)=xe^{x}+2a", INK),
            ("text", "　⇒　", INK),
            ("math", r"f'''(x)=(x+1)\,e^{x}", YELLOW),
            text_size=40, math_size=50)
        l2 = self.mixed(
            ("text", "在题目给定的 ", INK),
            ("math", r"0<x<2", INK),
            ("text", " 内：", INK),
            ("math", r"x+1>0,\ e^{x}>0\ \Rightarrow\ f'''(x)>0", RED),
            text_size=36, math_size=44)
        l3 = self.mixed(
            ("text", "结论：", INK),
            ("math", r"f'", INK),
            ("text", " 在 (0, 2) 上是", INK),
            ("text", "严格凸函数", BLUE),
            ("text", " —— 阿达玛不等式拿捏", INK),
            text_size=36, math_size=44)
        l4 = self.mixed(
            ("text", "注意分工：f‴ 只负责「凹凸」，不碰单调；各司其职，互不打架", MUTED),
            text_size=32, math_size=38)
        content = self.layout_below(bar, l1, l2, l3, l4)
        for line in (l1, l2, l3, l4):
            self.write_formula(line, run_time=1.1)
        self.wait(2.0)
        self.clear_scene()

    # ───────────── S6 第二步：套不等式 ─────────────
    def step_apply_page(self):
        bar = self.title_bar("第二步 · 套阿达玛（左半边）", color=ORANGE)
        self.play(Write(bar), run_time=0.8)
        l1 = self.mixed(
            ("text", "取 ", INK),
            ("math", r"g=f'", INK),
            ("text", "，[a, b] = [", INK),
            ("math", r"x_1,\ x_2", INK),
            ("text", "]，凸性已由 f‴＞0 保证：", INK),
            text_size=36, math_size=44)
        l2 = self.mixed(
            ("math",
             r"f'\Big(\frac{x_1+x_2}{2}\Big)<\frac{1}{x_2-x_1}\int_{x_1}^{x_2}f'(x)\,dx",
             YELLOW),
            text_size=40, math_size=50)
        l3 = self.mixed(
            ("text", "而右边的平均值恰为 0（核心思想），且 ", INK),
            ("math", r"f'(1)=0", INK),
            ("text", "，于是", INK),
            text_size=36, math_size=44)
        l4 = self.mixed(
            ("math", r"f'\Big(\frac{x_1+x_2}{2}\Big)<0=f'(1)", GREEN),
            text_size=44, math_size=56)
        content = self.layout_below(bar, l1, l2, l3, l4)
        for line in (l1, l2, l3, l4):
            self.write_formula(line, run_time=1.1)
        self.wait(2.0)
        self.clear_scene()

    # ───────────── S7 第三步：单调性收网 ─────────────
    def step_mono_page(self):
        bar = self.title_bar("第三步 · f″ 管单调，一锤定音", color=RED)
        self.play(Write(bar), run_time=0.8)
        l1 = self.mixed(
            ("math", r"f''(x)=xe^{x}+2a>0\quad(0<x<2)", BLUE),
            ("text", "　（x>0, eˣ>0, a>0）", MUTED),
            text_size=38, math_size=46)
        l2 = self.mixed(
            ("text", "故 f′ 在 (0, 2) 上", INK),
            ("text", "严格单调递增", BLUE),
            ("text", "；中点与 1 都在其中，比较函数值即比较自变量：", INK),
            text_size=34, math_size=42)
        l3 = self.mixed(
            ("math", r"f'\Big(\frac{x_1+x_2}{2}\Big)<f'(1)\ \Longrightarrow\ \frac{x_1+x_2}{2}<1",
             YELLOW),
            text_size=40, math_size=50)
        l4 = self.mixed(
            ("math", r"x_1+x_2<2", GREEN),
            ("text", "　∎　（左偏得证）", GREEN),
            text_size=44, math_size=56)
        content = self.layout_below(bar, l1, l2, l3, l4)
        for line in (l1, l2, l3, l4):
            self.write_formula(line, run_time=1.1)
        note = self.mixed(
            ("text", "全程只用了：一次牛顿–莱布尼茨 + 两个符号（f‴、f″）—— 这就是「快」的秘密", MUTED),
            text_size=32, math_size=38)
        note.next_to(content, DOWN, buff=0.55)
        self.fit(note)
        self.play(FadeIn(note), run_time=0.9)
        self.wait(2.2)
        self.clear_scene()

    # ───────────── S8 图像总览 ─────────────
    def graph_page(self):
        bar = self.title_bar("数值对账 · a = 0.1 的完整图像", color=TEAL)
        self.play(Write(bar), run_time=0.8)
        axes = Axes(x_range=[-0.15, 2.15, 0.5], y_range=[-0.8, 2.7, 0.5],
                    x_length=11.4, y_length=4.3,
                    axis_config={"color": MUTED, "stroke_width": 2})
        axes.move_to([0, -1.15, 0])
        curve = axes.plot(F, x_range=[0, 2, 0.005], color=YELLOW, stroke_width=4)
        self.play(Create(axes), Create(curve), run_time=1.2)
        d1 = Dot(axes.c2p(X1, 0), color=RED, radius=0.08)
        d2 = Dot(axes.c2p(X2, 0), color=RED, radius=0.08)
        t1 = self.mixed(("math", r"x_1\approx 0.35", RED), text_size=28, math_size=32)
        t1.next_to(d1, DOWN, buff=0.15)
        t2 = self.mixed(("math", r"x_2\approx 1.46", RED), text_size=28, math_size=32)
        t2.next_to(d2, DOWN, buff=0.15)
        vmin = Dot(axes.c2p(1, F(1)), color=GREEN, radius=0.08)
        tv = self.mixed(("math", r"x_0=1", GREEN), text_size=28, math_size=32)
        tv.next_to(vmin, UP, buff=0.15)
        mirror_x = 2 - X1
        dm = Dot(axes.c2p(mirror_x, F(mirror_x)), color=VIOLET, radius=0.08)
        tm = self.mixed(("math", r"2-x_1\approx 1.65", VIOLET), text_size=28, math_size=32)
        tm.next_to(dm, UP, buff=0.15)
        self.play(FadeIn(d1), Write(t1), FadeIn(d2), Write(t2), run_time=1.0)
        self.play(FadeIn(vmin), Write(tv), run_time=0.8)
        self.play(FadeIn(dm), Write(tm), run_time=0.9)
        note = self.mixed(
            ("text", "镜像点 2−x₁≈1.65 在 x₂≈1.46 的右边：f(2−x₁)>0=f(x₂) ⇒ 左偏", MUTED),
            ("text", "；数值和 1.81 < 2", GREEN),
            text_size=30, math_size=36)
        note.to_edge(DOWN, buff=0.3)
        self.fit(note)
        self.play(FadeIn(note), run_time=0.9)
        self.wait(2.2)
        self.clear_scene()

    # ───────────── S9 一般模板与方向法则 ─────────────
    def template_page(self):
        bar = self.title_bar("一般性方法 · 四步模板 + 方向法则", color=BLUE)
        self.play(Write(bar), run_time=0.8)
        steps = [
            ("① 积分等式", "f(x₁)=f(x₂) ⇒ ∫ f′ dx = 0（平均值归零）", TEAL),
            ("② 凸性鉴定", "算 f‴：f‴＞0 ⇒ f′ 凸（阿达玛正向）；f‴＜0 ⇒ 凹（反向）", ORANGE),
            ("③ 中点比较", "f′(中点) ＜/＞ 平均值 = f′(x₀)，把大小关系读出来", RED),
            ("④ 单调收网", "算 f″ 定 f′ 的增减 ⇒ 中点与 x₀ 比大小 ⇒ 偏移方向 ∎", GREEN),
        ]
        rows = []
        for head, desc, col in steps:
            row = self.mixed(
                ("text", head + "　", col),
                ("text", desc, INK),
                text_size=34, math_size=40)
            rows.append(row)
        content = self.layout_below(bar, *rows)
        for row in rows:
            self.play(FadeIn(row, shift=LEFT * 0.3), run_time=0.7)
        rule = self.mixed(
            ("text", "方向速查：", MUTED),
            ("text", "f′ 递增 + 凸 ⇒ 左偏；f′ 递增 + 凹 ⇒ 右偏（f′ 递减时左右对调）", YELLOW),
            text_size=32, math_size=38)
        rule.to_edge(DOWN, buff=0.72)
        self.fit(rule)
        self.play(FadeIn(rule), run_time=0.8)
        check = self.mixed(
            ("text", "凹例核验：", MUTED),
            ("math", r"g'(x)=(x-1)(2.2-x)", MUTED),
            ("text", "（g″>0 且 g‴<0）⇒ 数值零点和 ≈ 2.13 > 2，右偏 ✓", MUTED),
            text_size=30, math_size=36)
        check.next_to(rule, DOWN, buff=0.32)
        self.fit(check)
        self.play(FadeIn(check), run_time=0.8)
        self.wait(2.2)
        self.clear_scene()

    # ───────────── S9.5 一般化定理 ─────────────
    def general_theorem_page(self):
        bar = self.title_bar("一般化 · 什么样的 f 能这样秒杀？", color=VIOLET)
        self.play(Write(bar), run_time=0.8)
        l1 = self.mixed(
            ("text", "定理：设 f 在含 ", INK),
            ("math", r"x_0", GREEN),
            ("text", " 与两零点 ", INK),
            ("math", r"x_1<x_0<x_2", RED),
            ("text", " 的区间 I 上三阶可导，且", INK),
            text_size=36, math_size=44)
        l2 = self.mixed(
            ("text", "① ", INK),
            ("math", r"f'(x_0)=0", INK),
            ("text", "（x₀ 为极值点；f(x₁)=f(x₂) 等值即可）；", INK),
            text_size=34, math_size=42)
        l3 = self.mixed(
            ("text", "② ", INK),
            ("math", r"f''", BLUE),
            ("text", " 在 I 上不变号（f′ 严格单调）；　③ ", INK),
            ("math", r"f'''", RED),
            ("text", " 在 I 上不变号（f′ 定凹凸）", INK),
            text_size=34, math_size=42)
        l4 = self.mixed(
            ("text", "则偏移方向由两个符号的乘积一举判定：", INK),
            ("math", r"\mathrm{sign}(f'')\cdot\mathrm{sign}(f''')", YELLOW),
            text_size=36, math_size=44)
        content = self.layout_below(bar, l1, l2, l3, l4)
        for line in (l1, l2, l3, l4):
            self.write_formula(line, run_time=1.05)
        self.wait(2.0)
        self.clear_scene()

    # ───────────── S9.7 一般化定理证明与结论 ─────────────
    def general_proof_page(self):
        bar = self.title_bar("一口气证明 · 大小链一张表", color=GREEN)
        self.play(Write(bar), run_time=0.8)
        l1 = self.mixed(
            ("text", "平均值恒为零（f(x₁)=f(x₂) 等值即可）：", INK),
            ("math", r"A=\frac{1}{x_2-x_1}\!\int_{x_1}^{x_2}\! f'=0=f'(x_0)", YELLOW),
            text_size=32, math_size=40)
        l2 = self.mixed(
            ("text", "阿达玛：", INK),
            ("math", r"f'''>0\Rightarrow f'(m)<A", BLUE),
            ("text", "；", INK),
            ("math", r"f'''<0\Rightarrow f'(m)>A", BLUE),
            ("text", "（m 为中点）", MUTED),
            text_size=32, math_size=40)
        l3 = self.mixed(
            ("text", "f″>0（f′ 增）⇒ 不等号同向传给自变量；f″<0（f′ 减）⇒ 反向", INK),
            text_size=32, math_size=40)
        l4 = self.mixed(
            ("text", "合并（左偏）：", INK),
            ("math", r"\mathrm{sign}(f'')\cdot\mathrm{sign}(f''')>0\iff x_1+x_2<2x_0", GREEN),
            text_size=32, math_size=40)
        l5 = self.mixed(
            ("text", "合并（右偏）：", INK),
            ("math", r"\mathrm{sign}(f'')\cdot\mathrm{sign}(f''')<0\iff x_1+x_2>2x_0", RED),
            text_size=32, math_size=40)
        content = self.layout_below(bar, l1, l2, l3, l4, l5)
        for line in (l1, l2, l3, l4, l5):
            self.write_formula(line, run_time=1.0)
        note = self.mixed(
            ("text", "例题即 ", MUTED),
            ("math", r"f''>0,\ f'''>0", MUTED),
            ("text", "（同号）⇒ 左偏；凹例 ", MUTED),
            ("math", r"g''>0,\ g'''<0", MUTED),
            ("text", "（异号）⇒ 右偏 —— 完全一致", MUTED),
            text_size=30, math_size=36)
        note.next_to(content, DOWN, buff=0.5)
        self.fit(note)
        self.play(FadeIn(note), run_time=0.9)
        self.wait(2.2)
        self.clear_scene()

    # ───────────── S10 结尾 ─────────────
    def ending(self):
        t1 = self.zh("等高即零平均，凸凹定乾坤", font_size=52, weight=BOLD)
        t1.move_to([0, 1.5, 0])
        t2 = self.mixed(
            ("text", "阿达玛：把偏移问题变成「三个数的大小链」", ORANGE),
            text_size=36, math_size=40)
        t2.next_to(t1, DOWN, buff=0.45)
        self.play(Write(t1), run_time=1.0)
        self.play(FadeIn(t2), run_time=0.8)

        axes = Axes(x_range=[0, 1, 0.5], y_range=[0, 1.2, 0.5],
                    x_length=6.4, y_length=2.6,
                    axis_config={"color": MUTED, "stroke_width": 1.5,
                                 "include_ticks": False})
        axes.move_to([0, -2.2, 0])
        g = lambda x: 0.35 + 0.9 * (x - 0.5) ** 2 + 0.15 * (x - 0.5)
        curve = axes.plot(g, x_range=[0, 1, 0.01], color=BLUE, stroke_width=3.5)
        chord = DashedLine(axes.c2p(0, g(0)), axes.c2p(1, g(1)),
                           color=MUTED, stroke_width=2, dash_length=0.1)
        self.play(Create(axes), Create(curve), Create(chord), run_time=1.3)
        self.wait(2.4)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
        self.wait(0.3)
