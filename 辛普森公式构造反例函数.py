from manim import *
import numpy as np

# ============ 全局配置：横屏 16:9 大字 ============
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16.0
config.frame_height = 9.0

ZH_FONT = "Kaiti SC"   # macOS 楷体（Windows 下为 KaiTi）
BG     = "#0F1720"
INK    = "#F6F2EA"
MUTED  = "#A9B4C2"
BLUE   = "#5DADEC"
GREEN  = "#66D19E"
YELLOW = "#FFD166"
ORANGE = "#F59E62"
RED    = "#FF6B6B"
VIOLET = "#B79CFF"
READ_PAUSE = 2.3


class SpikeCounterexample(Scene):
    """构造非负连续 f：∫f 收敛但 ∫f² 发散 —— 三角形尖峰 + 辛普森公式"""

    # ================= 辅助方法 =================
    def zh(self, content, font_size=42, color=INK, weight=NORMAL):
        return Text(content, font=ZH_FONT, font_size=font_size, color=color, weight=weight)

    def mt(self, content, font_size=56, color=INK, stroke_width=1):
        return MathTex(content, font_size=font_size, color=color, stroke_width=stroke_width)

    def mt_small(self, content, font_size=50, color=INK):
        return self.mt(content, font_size=font_size, color=color)

    def mixed(self, *items, text_size=38, math_size=44, buff=0.08):
        parts = []
        for kind, content, color in items:
            if kind == "text":
                parts.append(self.zh(content, font_size=text_size, color=color))
            else:
                parts.append(self.mt(content, font_size=math_size, color=color))
        return VGroup(*parts).arrange(RIGHT, buff=buff)

    def fit(self, mob, width=None, height=None):
        target_width = width if width is not None else config.frame_width - 1.2
        target_height = height if height is not None else config.frame_height - 1.0
        if mob.width > target_width:
            mob.scale_to_fit_width(target_width)
        if mob.height > target_height:
            mob.scale_to_fit_height(target_height)
        return mob

    def title_bar(self, text, color=BLUE):
        title = self.zh(text, font_size=52, color=color, weight=BOLD)
        title.to_edge(UP, buff=0.38)
        return VGroup(title)

    def layout_below(self, bar, *lines):
        n = len(lines)
        for line in lines:
            self.fit(line, width=config.frame_width - 1.2)
        if n <= 2:
            buff = 1.1
        elif n == 3:
            buff = 0.95
        else:
            buff = 0.72
        content = VGroup(*lines).arrange(DOWN, buff=buff, aligned_edge=LEFT)
        content.next_to(bar, DOWN, buff=0.65)
        return content

    def wait_formula(self):
        self.wait(READ_PAUSE)

    def write_formula(self, mob, run_time=0.9):
        self.play(Write(mob), run_time=run_time)
        self.wait_formula()

    def write_text(self, mob, run_time=0.75):
        self.play(Write(mob), run_time=run_time)

    def clear_scene(self):
        if self.mobjects:
            self.play(*[FadeOut(mob) for mob in self.mobjects], run_time=0.5)

    # ================= 主流程 =================
    def construct(self):
        self.camera.background_color = BG
        self.opening()
        self.strategy()
        self.graph_construction()
        self.integral_f()
        self.simpson_origin()
        self.simpson_exactness()
        self.apply_to_spike()
        self.verify_simpson()
        self.choose_a()
        self.partial_sums()
        self.trig_example()
        self.compare()
        self.principle()
        self.summary()

    # ---------- 开场：彩色抛题 + 抄题 ----------
    def opening(self):
        q = self.zh("你能构造出这样的函数吗？", font_size=58, color=YELLOW, weight=BOLD)
        q.to_edge(UP, buff=1.0)
        self.play(Write(q), run_time=1.0)
        self.wait(0.8)

        row = self.mixed(
            ("text", "构造 ", BLUE),
            ("text", "非负且连续的 ", INK),
            ("math", r"f(x)", YELLOW),
            ("text", "，使 ", INK),
            ("math", r"\int_0^{+\infty}f(x)\,dx", GREEN),
            ("text", " 收敛，但 ", INK),
            ("math", r"\int_0^{+\infty}f^2(x)\,dx", RED),
            ("text", " 发散", INK),
        )
        self.fit(row, width=config.frame_width - 1.2)
        row.next_to(q, DOWN, buff=1.1)
        self.write_formula(row, run_time=1.3)

        sub = self.zh("—— 一个积分收敛、平方后却爆炸的经典反例 ——", font_size=34, color=MUTED)
        sub.next_to(row, DOWN, buff=0.75)
        self.write_text(sub)

        hook = self.zh("今天请出一位“意外嘉宾”：数值积分的辛普森公式", font_size=38, color=ORANGE, weight=BOLD)
        hook.next_to(sub, DOWN, buff=0.7)
        self.play(Write(hook), run_time=0.9)
        self.wait(2.0)
        self.clear_scene()

    # ---------- 思路分析 ----------
    def strategy(self):
        bar = self.title_bar("证明思路分析")
        self.play(Write(bar), run_time=0.8)

        s1 = self.mixed(
            ("text", "一、构造：在 ", BLUE),
            ("math", r"x=1,2,3,\cdots", BLUE),
            ("text", " 处放三角形尖峰，底宽 ", BLUE),
            ("math", r"\frac{2}{2^n}", BLUE),
            ("text", "，高 ", BLUE),
            ("math", r"a_n", BLUE),
            ("text", " 待定", BLUE),
        text_size=36, math_size=42)
        s2 = self.mixed(
            ("text", "二、算一阶：", GREEN),
            ("math", r"\int_0^{+\infty}f\,dx=\sum_{n=1}^{\infty}S_n=\sum_{n=1}^{\infty}\frac{a_n}{2^n}", GREEN),
            ("text", "，几何级数好控制", GREEN),
        text_size=36, math_size=42)
        s3 = self.mixed(
            ("text", "三、算平方：每个尖峰的半边上 ", ORANGE),
            ("math", r"f^2", ORANGE),
            ("text", " 恰是二次函数 → 辛普森公式“精确”求积", ORANGE),
        text_size=36, math_size=42)
        s4 = self.mixed(
            ("text", "四、选高度：", VIOLET),
            ("math", r"a_n=(\sqrt{2})^n", VIOLET),
            ("text", "，一个收敛一个发散，反例到手", VIOLET),
        text_size=36, math_size=42)

        content = self.layout_below(bar, s1, s2, s3, s4)
        for line in [s1, s2, s3, s4]:
            self.play(Write(line), run_time=0.9)
            self.wait(0.8)
        self.wait(2.0)
        self.clear_scene()

    # ---------- 构造图像：多彩三角形 ----------
    def graph_construction(self):
        bar = self.title_bar("第一步：把 f 造成一串三角形尖峰")
        self.play(Write(bar), run_time=0.8)

        axes = Axes(
            x_range=[0, 6.9, 1],
            y_range=[0, 4.6, 1],
            x_length=12.8, y_length=5.6,
            axis_config={"color": MUTED, "stroke_width": 2.5, "include_ticks": False},
        )
        axes.move_to([0.2, -0.65, 0])
        self.play(Create(axes), run_time=0.9)

        xlab = self.mt(r"x", 34, MUTED)
        xlab.next_to(axes.x_axis.get_end(), RIGHT, buff=0.15)
        ylab = self.mt(r"y", 34, MUTED)
        ylab.next_to(axes.y_axis.get_end(), UP, buff=0.15)
        self.play(FadeIn(xlab), FadeIn(ylab), run_time=0.4)

        # 真实尖峰 n=1..4：a_n = (√2)^n；宽度按 2^{-n} 递减（图中略有夸张以便观看）
        params = [
            (1, 0.50, 2 ** 0.5, BLUE),
            (2, 0.32, 2 ** 1.0, GREEN),
            (3, 0.20, 2 ** 1.5, YELLOW),
            (4, 0.13, 2 ** 2.0, ORANGE),
        ]
        for c, w, h, col in params:
            tri = Polygon(
                axes.c2p(c - w, 0), axes.c2p(c, h), axes.c2p(c + w, 0),
            )
            tri.set_fill([col, "#1E3A5F"], opacity=0.55)
            tri.set_stroke(col, width=4)
            self.play(DrawBorderThenFill(tri), run_time=0.65)

        # 第 n 个尖峰（示意，红色）
        c, w, h = 5.85, 0.45, 3.35
        tri_n = Polygon(axes.c2p(c - w, 0), axes.c2p(c, h), axes.c2p(c + w, 0))
        tri_n.set_fill([RED, "#3A1E2A"], opacity=0.55)
        tri_n.set_stroke(RED, width=4)
        ell = self.zh("……", font_size=34, color=MUTED).move_to(axes.c2p(4.85, 0.22))
        self.play(Write(ell), run_time=0.4)
        self.play(DrawBorderThenFill(tri_n), run_time=0.7)

        # 底角圆点（前三个尖峰）
        dots = VGroup()
        for cc, ww, hh, col in params[:3]:
            for xx in (cc - ww, cc + ww):
                dots.add(Dot(axes.c2p(xx, 0), radius=0.055, color=col))
        self.play(FadeIn(dots), run_time=0.5)

        # 峰顶标注
        p1 = self.mt(r"(1,\,a_1)", 30, BLUE).next_to(axes.c2p(1, 2 ** 0.5), UP, buff=0.18).shift(LEFT * 0.35)
        p2 = self.mt(r"(2,\,a_2)", 30, GREEN).next_to(axes.c2p(2, 2.0), UP, buff=0.18).shift(LEFT * 0.3)
        pn = self.mt(r"(n,\,a_n)", 34, RED).next_to(axes.c2p(c, h), UP, buff=0.18)
        self.play(FadeIn(p1), FadeIn(p2), FadeIn(pn), run_time=0.7)

        # 面积记号 S1 S2
        s1lab = self.mt(r"S_1", 32, INK).move_to(axes.c2p(1.0, 0.42))
        s2lab = self.mt(r"S_2", 32, INK).move_to(axes.c2p(2.0, 0.55))
        snlab = self.mt(r"S_n", 32, INK).move_to(axes.c2p(c, 0.75))
        self.play(FadeIn(s1lab), FadeIn(s2lab), FadeIn(snlab), run_time=0.6)

        # 底边刻度标注：外标上行，中心标下行
        ax_y = axes.c2p(0, 0)[1]
        row1_y, row2_y = ax_y - 0.36, ax_y - 0.72
        lb = [
            (self.mt(r"1-\frac{1}{2}", 28, MUTED), axes.c2p(0.5, 0)[0], row1_y),
            (self.mt(r"1+\frac{1}{2}", 28, MUTED), axes.c2p(1.5, 0)[0], row1_y),
            (self.mt(r"1", 28, MUTED), axes.c2p(1.0, 0)[0], row2_y),
            (self.mt(r"n-\frac{1}{2^n}", 28, MUTED), axes.c2p(c - w, 0)[0], row1_y),
            (self.mt(r"n+\frac{1}{2^n}", 28, MUTED), axes.c2p(c + w, 0)[0], row1_y),
            (self.mt(r"n", 28, MUTED), axes.c2p(c, 0)[0], row2_y),
        ]
        labs = VGroup()
        for mob, xx, yy in lb:
            mob.move_to([xx, yy, 0])
            labs.add(mob)
        self.play(FadeIn(labs), run_time=0.8)

        note = VGroup(
            self.zh("底宽按 ", 26, MUTED),
            self.mt(r"2^{-n}", 32, MUTED),
            self.zh(" 急剧缩小（图中略有夸张），高度 ", 26, MUTED),
            self.mt(r"a_n", 30, MUTED),
            self.zh(" 待定", 26, MUTED),
        ).arrange(RIGHT, buff=0.08)
        note.move_to([0.2, axes.c2p(0, 0)[1] - 1.15, 0])
        self.write_text(note, run_time=0.8)
        self.wait(2.0)
        self.clear_scene()

    # ---------- 第一步计算：∫f = Σ an/2^n ----------
    def integral_f(self):
        t1 = self.zh("第二步：", font_size=52, color=GREEN, weight=BOLD)
        t2 = self.mt(r"\int_0^{+\infty}f(x)\,dx", font_size=52, color=GREEN, stroke_width=1)
        t3 = self.zh(" ＝ 面积之和", font_size=52, color=GREEN, weight=BOLD)
        bar = VGroup(t1, t2, t3).arrange(RIGHT, buff=0.12)
        bar.to_edge(UP, buff=0.38)
        self.play(Write(bar), run_time=0.9)

        l1 = self.mt(r"S_n=\frac{1}{2}\times\frac{2}{2^n}\times a_n=\frac{a_n}{2^n}", font_size=56)
        l2 = self.mixed(
            ("text", "f 非负连续，积分即面积求和：", INK),
            ("math", r"\int_0^{+\infty}f(x)\,dx=\sum_{n=1}^{\infty}\frac{a_n}{2^n}", INK),
        )
        l3 = self.mixed(
            ("text", "高度 ", MUTED),
            ("math", r"a_n", MUTED),
            ("text", " 先留着不定 —— 最后再挑！", MUTED),
        )
        content = self.layout_below(bar, l1, l2, l3)
        self.write_formula(l1)
        self.write_formula(l2)
        self.write_text(l3)
        self.wait(2.0)
        self.clear_scene()

    # ---------- 辛普森公式从哪来 ----------
    def simpson_origin(self):
        bar = self.title_bar("关键武器：辛普森（Simpson）公式从哪来？", color=YELLOW)
        self.play(Write(bar), run_time=0.8)

        formula = self.mt(
            r"\int_a^b f(x)\,dx=\frac{b-a}{6}\Big[f(a)+4f\Big(\frac{a+b}{2}\Big)+f(b)\Big]",
            font_size=54, color=YELLOW,
        )
        self.fit(formula, width=config.frame_width - 1.6)
        formula.next_to(bar, DOWN, buff=0.55)
        self.write_formula(formula, run_time=1.2)

        # 左下：曲线 + 抛物线插值
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 3, 1],
            x_length=6.8, y_length=4.0,
            axis_config={"color": MUTED, "stroke_width": 2.5, "include_ticks": False},
        )
        axes.move_to([-4.2, -1.35, 0])
        self.play(Create(axes), run_time=0.8)

        def f(x):
            return 1.1 + 0.62 * np.sin(1.6 * x - 0.4) + 0.18 * x

        a, b = 0.9, 3.1
        m = (a + b) / 2
        curve = axes.plot(f, x_range=[0.55, 3.45], color=INK, stroke_width=5)
        self.play(Create(curve), run_time=1.0)

        coeffs = np.polyfit([a, m, b], [f(a), f(m), f(b)], 2)
        para = axes.plot(lambda x: np.polyval(coeffs, x), x_range=[a, b],
                         color=YELLOW, stroke_width=4)
        self.play(Create(para), run_time=1.0)

        vlines = VGroup(*[
            DashedLine(axes.c2p(xx, 0), axes.c2p(xx, f(xx)), color=MUTED, stroke_width=2)
            for xx in (a, m, b)
        ])
        dpts = VGroup(*[Dot(axes.c2p(xx, f(xx)), radius=0.07, color=YELLOW) for xx in (a, m, b)])
        alab = self.mt(r"a", 32, MUTED).move_to(axes.c2p(a, -0.3))
        mlab = self.mt(r"\frac{a+b}{2}", 30, MUTED).move_to(axes.c2p(m, -0.42))
        blab = self.mt(r"b", 32, MUTED).move_to(axes.c2p(b, -0.3))
        self.play(Create(vlines), run_time=0.6)
        self.play(FadeIn(dpts), FadeIn(alab), FadeIn(mlab), FadeIn(blab), run_time=0.6)

        # 右侧说明
        r1 = self.mixed(
            ("text", "① 过三点作唯一的抛物线 ", INK),
            ("math", r"P_2(x)", YELLOW),
        )
        r2 = self.zh("② 抛物线下的面积可以精确算出", font_size=36, color=INK)
        r3 = self.mixed(
            ("text", "③ 权重恰为 ", INK),
            ("math", r"1:4:1", ORANGE),
            ("text", "，所以又叫“1-4-1 法则”", INK),
        )
        r4 = self.zh("对二次函数：它不是近似，是恒等式！", font_size=36, color=YELLOW, weight=BOLD)
        right = VGroup(r1, r2, r3, r4).arrange(DOWN, buff=0.62, aligned_edge=LEFT)
        self.fit(right, width=7.6)
        right.next_to(formula, DOWN, buff=0.7).to_edge(RIGHT, buff=0.75)
        for r in [r1, r2, r3, r4]:
            self.write_text(r, run_time=0.7)
            self.wait(0.7)
        self.wait(2.0)
        self.clear_scene()

    # ---------- 代数精度证明 ----------
    def simpson_exactness(self):
        bar = self.title_bar("代数精度：对二次函数 100% 精确", color=YELLOW)
        self.play(Write(bar), run_time=0.8)

        l1 = self.mixed(
            ("text", "等式两边对 f 都线性；平移伸缩不妨取 ", INK),
            ("math", r"[-1,1]", INK),
            ("text", "，只需验证三个基：", INK),
        )
        chk = lambda: self.mt(r"\checkmark", 46, GREEN)
        l2 = VGroup(self.mt(r"f=1:\quad \int_{-1}^{1}1\,dx=2=\frac{2}{6}\big[1+4+1\big]", 46), chk()).arrange(RIGHT, buff=0.25)
        l3 = VGroup(self.mt(r"f=x:\quad \int_{-1}^{1}x\,dx=0=\frac{2}{6}\big[-1+0+1\big]", 46), chk()).arrange(RIGHT, buff=0.25)
        l4 = VGroup(self.mt(r"f=x^2:\quad \int_{-1}^{1}x^2\,dx=\frac{2}{3}=\frac{2}{6}\big[1+0+1\big]", 46), chk()).arrange(RIGHT, buff=0.25)
        content = self.layout_below(bar, l1, l2, l3, l4)
        self.write_text(l1, run_time=0.9)
        for l in [l2, l3, l4]:
            self.write_formula(l, run_time=1.0)
        self.wait(1.2)
        self.clear_scene()

        # 彩蛋：精度恰为 3 次
        bar2 = self.title_bar("彩蛋：精度到底几次？", color=ORANGE)
        self.play(Write(bar2), run_time=0.8)
        b1 = VGroup(self.mt(r"f=x^3:\quad \int_{-1}^{1}x^3\,dx=0=\frac{2}{6}\big[(-1)^3+0+1^3\big]", 44),
                    self.mt(r"\checkmark", 44, GREEN)).arrange(RIGHT, buff=0.25)
        b2 = VGroup(self.mt(r"f=x^4:\quad \frac{2}{5}\neq\frac{2}{6}\big[1+0+1\big]=\frac{2}{3}", 46, RED),
                    self.zh("失效！", font_size=40, color=RED, weight=BOLD)).arrange(RIGHT, buff=0.3)
        b3 = self.zh("结论：代数精度恰为 3 次 —— 我们只用二次，绰绰有余", font_size=36, color=MUTED)
        content = self.layout_below(bar2, b1, b2, b3)
        self.write_formula(b1, run_time=1.0)
        self.write_formula(b2, run_time=1.0)
        self.write_text(b3)
        self.wait(2.0)
        self.clear_scene()

    # ---------- 应用到尖峰：图像 + 推导 ----------
    def apply_to_spike(self):
        bar = self.title_bar("第三步：辛普森公式 × 尖峰 ＝ 精确面积", color=ORANGE)
        self.play(Write(bar), run_time=0.8)

        # 左：半边放大图
        axes = Axes(
            x_range=[0, 2.1, 1],
            y_range=[0, 4.7, 1],
            x_length=5.8, y_length=5.6,
            axis_config={"color": MUTED, "stroke_width": 2.5, "include_ticks": False},
        )
        axes.move_to([-4.85, -0.95, 0])
        self.play(Create(axes), run_time=0.8)

        # 三角形：底 [0.2, 2.0]，顶 (1.1, 2.0)
        tri = Polygon(axes.c2p(0.2, 0), axes.c2p(1.1, 2.0), axes.c2p(2.0, 0))
        tri.set_fill(BLUE, opacity=0.22)
        tri.set_stroke(BLUE, width=4)
        self.play(DrawBorderThenFill(tri), run_time=0.9)

        # 左半边：f 线性（蓝）与 f² 抛物线（红）
        line_f = Line(axes.c2p(0.2, 0), axes.c2p(1.1, 2.0), color=BLUE, stroke_width=5)
        para = axes.plot(lambda x: 4.0 * ((x - 0.2) / 0.9) ** 2, x_range=[0.2, 1.1],
                         color=RED, stroke_width=5)
        area = axes.get_area(para, x_range=[0.2, 1.1], color=RED, opacity=0.30)
        self.play(Create(line_f), run_time=0.6)
        self.play(Create(para), FadeIn(area), run_time=1.0)

        # 辛普森三点
        v1 = DashedLine(axes.c2p(0.65, 0), axes.c2p(0.65, 1.0), color=MUTED, stroke_width=2)
        v2 = DashedLine(axes.c2p(1.1, 0), axes.c2p(1.1, 4.0), color=MUTED, stroke_width=2)
        d1 = Dot(axes.c2p(0.2, 0.0), radius=0.07, color=YELLOW)
        d2 = Dot(axes.c2p(0.65, 1.0), radius=0.07, color=YELLOW)
        d3 = Dot(axes.c2p(1.1, 4.0), radius=0.07, color=YELLOW)
        t1 = self.mt(r"0", 30, INK).next_to(d1, UL, buff=0.12)
        t2 = self.mt(r"\Big(\frac{a_n}{2}\Big)^{2}", 30, RED).next_to(d2, RIGHT, buff=0.18)
        t3 = self.mt(r"a_n^{2}", 32, RED).next_to(d3, UR, buff=0.12)
        self.play(Create(v1), Create(v2), run_time=0.5)
        self.play(FadeIn(d1), FadeIn(d2), FadeIn(d3), FadeIn(t1), FadeIn(t2), FadeIn(t3), run_time=0.7)

        cap = VGroup(
            self.zh("蓝线 ", 24, BLUE),
            self.mt(r"f", 28, BLUE),
            self.zh(" 线性 → ", 24, MUTED),
            self.zh("红线 ", 24, RED),
            self.mt(r"f^2", 28, RED),
            self.zh(" 二次", 24, MUTED),
        ).arrange(RIGHT, buff=0.06)
        cap.move_to(axes.c2p(2.05, 4.55), aligned_edge=RIGHT)
        self.write_text(cap, run_time=0.7)

        xlabels = VGroup(
            self.mt(r"n-\frac{1}{2^n}", 24, MUTED).move_to(axes.c2p(0.2, -0.38)),
            self.mt(r"n-\frac{1}{2^{n+1}}", 24, MUTED).move_to(axes.c2p(0.65, -0.5)),
            self.mt(r"n", 26, MUTED).move_to(axes.c2p(1.1, -0.38)),
        )
        self.play(FadeIn(xlabels), run_time=0.5)

        # 右：推导
        r1 = self.mixed(
            ("text", "每半边上 f 是一次函数 ", INK),
            ("math", r"\Longrightarrow", ORANGE),
            ("math", r"f^2", INK),
            ("text", " 是二次函数 ", INK),
            ("text", "→ 辛普森精确", ORANGE),
        )
        r2 = self.mixed(
            ("text", "对左半边 ", INK),
            ("math", r"\Big[n-\frac{1}{2^n},\; n\Big]", INK),
            ("text", " 用辛普森，三点高度 ", INK),
            ("math", r"0,\ \frac{a_n}{2},\ a_n", INK),
            ("text", "：", INK),
        )
        r3 = self.mt(
            r"\int_{n-\frac{1}{2^n}}^{n}f^2\,dx=\frac{1}{6}\cdot\frac{1}{2^n}\Big[0+4\Big(\frac{a_n}{2}\Big)^{2}+a_n^2\Big]",
            font_size=44,
        )
        r4 = self.mt(
            r"S_n=2\times\frac{1}{6}\cdot\frac{1}{2^n}\cdot 2a_n^2=\frac{2}{3}\cdot\frac{(a_n)^2}{2^n}",
            font_size=50, color=YELLOW,
        )
        right = VGroup(r1, r2, r3, r4).arrange(DOWN, buff=0.58, aligned_edge=LEFT)
        self.fit(right, width=9.2)
        right.next_to(bar, DOWN, buff=0.6).to_edge(RIGHT, buff=0.6)
        self.write_text(r1, run_time=0.9)
        self.write_text(r2, run_time=1.0)
        self.write_formula(r3, run_time=1.2)
        self.write_formula(r4, run_time=1.2)
        box = SurroundingRectangle(r4, color=YELLOW, buff=0.18)
        self.play(Create(box), run_time=0.6)
        self.wait(2.0)
        self.clear_scene()

    # ---------- 双保险：直接积分验证 ----------
    def verify_simpson(self):
        bar = self.title_bar("双保险：直接积分验证辛普森", color=BLUE)
        self.play(Write(bar), run_time=0.8)

        v1 = self.mixed(
            ("text", "左半边换元 ", INK),
            ("math", r"t=x-\big(n-\frac{1}{2^n}\big)", INK),
            ("text", "，直接积分：", INK),
        )
        v2 = self.mt(
            r"\int_{0}^{\frac{1}{2^n}}a_n^2\Big(1-\frac{t}{2^{-n}}\Big)^{2}dt"
            r"=a_n^2\cdot 2^{-n}\int_0^1(1-u)^2du=\frac{a_n^2}{3\cdot 2^{n}}",
            font_size=44,
        )
        v3 = self.mixed(
            ("text", "右半边对称：", INK),
            ("math", r"S_n=2\times\frac{a_n^2}{3\cdot 2^{n}}=\frac{2}{3}\cdot\frac{(a_n)^2}{2^n}", GREEN),
            ("text", " —— 与辛普森完全一致！", GREEN),
            text_size=38, math_size=46)
        v4 = self.zh("辛普森不是碰巧近似得好 —— 它对二次函数是恒等式", font_size=36, color=MUTED)
        content = self.layout_below(bar, v1, v2, v3, v4)
        self.write_text(v1, run_time=0.9)
        self.write_formula(v2, run_time=1.3)
        self.write_formula(v3, run_time=1.3)
        self.write_text(v4)
        self.wait(2.0)
        self.clear_scene()

    # ---------- 选参数 + 结论 ----------
    def choose_a(self):
        t1 = self.zh("第四步：选高度 ", font_size=52, color=GREEN, weight=BOLD)
        t2 = self.mt(r"a_n=(\sqrt{2})^n", font_size=52, color=GREEN, stroke_width=1)
        bar = VGroup(t1, t2).arrange(RIGHT, buff=0.15)
        bar.to_edge(UP, buff=0.38)
        self.play(Write(bar), run_time=0.9)

        l1 = self.mt(r"a_n=(\sqrt{2})^n\ \Longrightarrow\ (a_n)^2=2^n", font_size=52)
        l2 = VGroup(
            self.mt(r"\int_0^{+\infty}f\,dx=\sum_{n=1}^{\infty}\frac{(\sqrt{2})^n}{2^n}=\sum_{n=1}^{\infty}\Big(\frac{1}{\sqrt{2}}\Big)^{n}=1+\sqrt{2}", 44, GREEN),
            self.zh("收敛", font_size=40, color=GREEN, weight=BOLD),
        ).arrange(RIGHT, buff=0.25)
        l3 = VGroup(
            self.mt(r"\int_0^{+\infty}f^2\,dx=\sum_{n=1}^{\infty}\frac{2}{3}\cdot\frac{2^n}{2^n}=\sum_{n=1}^{\infty}\frac{2}{3}=+\infty", 44, RED),
            self.zh("发散", font_size=40, color=RED, weight=BOLD),
        ).arrange(RIGHT, buff=0.25)
        l4 = VGroup(
            self.zh("非负、连续的反例构造完成！", font_size=44, color=GREEN, weight=BOLD),
            self.mt(r"\blacksquare", 44, GREEN),
        ).arrange(RIGHT, buff=0.3)
        content = self.layout_below(bar, l1, l2, l3, l4)
        self.write_formula(l1)
        self.write_formula(l2, run_time=1.2)
        self.write_formula(l3, run_time=1.2)
        box = SurroundingRectangle(VGroup(l3, l4), color=GREEN, buff=0.22)
        self.play(Write(l4), run_time=1.0)
        self.play(Create(box), run_time=0.7)
        self.wait(2.0)
        self.clear_scene()

    # ---------- 动态感受：部分和柱状图 ----------
    def partial_sums(self):
        bar = self.title_bar("动态感受：一个爬向定值，一个永远停不下来", color=GREEN)
        self.play(Write(bar), run_time=0.8)

        base_y = -2.4
        N = 9
        bar_w, gap = 0.38, 0.2
        scale_L, scale_R = 0.82, 0.38

        sums_L, sums_R, cur = [], [], 0.0
        for k in range(1, N + 1):
            cur += 2 ** (-k / 2)
            sums_L.append(cur)
            sums_R.append((2 / 3) * k)

        title_L = self.mt(r"\sum_{k=1}^{N}\frac{a_k}{2^k}", 40, GREEN)
        title_R = self.mt(r"\sum_{k=1}^{N}\frac{2}{3}\cdot\frac{(a_k)^2}{2^k}", 40, RED)
        title_L.move_to([-4.6, 1.7, 0])
        title_R.move_to([4.6, 1.7, 0])

        axes_L = Line([-7.0, base_y, 0], [-1.45, base_y, 0], color=MUTED, stroke_width=2)
        axes_R = Line([2.2, base_y, 0], [7.75, base_y, 0], color=MUTED, stroke_width=2)
        self.play(FadeIn(title_L), FadeIn(title_R), Create(axes_L), Create(axes_R), run_time=0.8)

        bars_L, bars_R = VGroup(), VGroup()
        for k in range(N):
            hL = sums_L[k] * scale_L
            hR = sums_R[k] * scale_R
            xL = -6.85 + k * (bar_w + gap)
            xR = 2.35 + k * (bar_w + gap)
            bars_L.add(Rectangle(width=bar_w, height=hL, fill_color=GREEN, fill_opacity=0.75,
                                 stroke_width=0).move_to([xL + bar_w / 2, base_y + hL / 2, 0]))
            bars_R.add(Rectangle(width=bar_w, height=hR, fill_color=RED, fill_opacity=0.75,
                                 stroke_width=0).move_to([xR + bar_w / 2, base_y + hR / 2, 0]))
        self.play(FadeIn(bars_L, lag_ratio=0.12), FadeIn(bars_R, lag_ratio=0.12), run_time=3.0)

        lim_y = (1 + np.sqrt(2)) * scale_L
        lim_line = DashedLine([-7.0, base_y + lim_y, 0], [-1.5, base_y + lim_y, 0],
                              color=YELLOW, stroke_width=3)
        lim_lab = self.mt(r"1+\sqrt{2}", 36, YELLOW).next_to(lim_line, UP, buff=0.15)
        inf_lab = self.mt(r"\longrightarrow +\infty", 40, RED).next_to(bars_R, UP, buff=0.2)
        self.play(Create(lim_line), Write(lim_lab), run_time=0.8)
        self.play(Write(inf_lab), run_time=0.8)

        note = self.zh("（两图纵坐标比例不同）", font_size=26, color=MUTED)
        note.move_to([6.2, 2.95, 0])
        self.play(FadeIn(note), run_time=0.4)

        bottom = self.zh("左边每一步都更小，乖乖停在 1+√2；右边每一步都是同样的 2/3 —— 永远走不完！",
                         font_size=36, color=ORANGE, weight=BOLD)
        self.fit(bottom, width=config.frame_width - 1.2)
        bottom.to_edge(DOWN, buff=0.42)
        self.write_text(bottom, run_time=1.0)
        self.wait(2.0)
        self.clear_scene()

    # ---------- 另一种解法：sin² 光滑凸起 ----------
    def trig_example(self):
        bar = self.title_bar("另一种经典反例：光滑的 sin² 凸起", color=VIOLET)
        self.play(Write(bar), run_time=0.8)

        axes = Axes(
            x_range=[0, 6.9, 1],
            y_range=[0, 3.8, 1],
            x_length=12.8, y_length=4.6,
            axis_config={"color": MUTED, "stroke_width": 2.5, "include_ticks": False},
        )
        axes.move_to([0.2, -0.95, 0])
        self.play(Create(axes), run_time=0.8)

        bumps = [
            (1.0, 0.55, 1.0, VIOLET),
            (2.0, 0.50, 1.6, BLUE),
            (3.0, 0.45, 2.2, GREEN),
            (4.0, 0.40, 2.8, YELLOW),
        ]
        for c, w, h, col in bumps:
            g = axes.plot(
                lambda x, c=c, w=w, h=h: h * np.sin(np.pi * (x - (c - w)) / (2 * w)) ** 2,
                x_range=[c - w, c + w], color=col, stroke_width=5,
            )
            fill = axes.get_area(g, x_range=[c - w, c + w], color=col, opacity=0.35)
            self.play(Create(g), FadeIn(fill), run_time=0.65)
        g5 = axes.plot(
            lambda x: 3.2 * np.sin(np.pi * (x - 5.3) / 1.0) ** 2,
            x_range=[5.3, 6.3], color=RED, stroke_width=5,
        )
        fill5 = axes.get_area(g5, x_range=[5.3, 6.3], color=RED, opacity=0.35)
        ell = self.zh("……", font_size=32, color=MUTED).move_to(axes.c2p(4.85, 0.2))
        self.play(Write(ell), run_time=0.4)
        self.play(Create(g5), FadeIn(fill5), run_time=0.7)

        defline = self.mixed(
            ("text", "第 n 块：", VIOLET),
            ("math", r"f(x)=n\sin^2\big(\pi n^3(x-n)\big)", VIOLET),
            ("text", "，", INK),
            ("math", r"x\in\Big[n,\ n+\frac{1}{n^3}\Big]", INK),
            ("text", "，其余为 0", INK),
        )
        self.fit(defline, width=config.frame_width - 1.2)
        defline.to_edge(DOWN, buff=0.28)
        self.write_formula(defline, run_time=1.1)
        self.wait(1.5)
        self.clear_scene()

        # 计算
        bar2 = self.title_bar("sin² 凸起：同样奏效", color=VIOLET)
        self.play(Write(bar2), run_time=0.8)
        k1 = VGroup(
            self.mt(r"\int f\,dx=\sum_{n=1}^{\infty}n\cdot\frac{1}{n^3}\cdot\frac{1}{2}=\frac{1}{2}\sum_{n=1}^{\infty}\frac{1}{n^2}=\frac{\pi^2}{12}", 44, GREEN),
            self.zh("收敛", font_size=38, color=GREEN, weight=BOLD),
        ).arrange(RIGHT, buff=0.25)
        k2 = VGroup(
            self.mt(r"\int f^2\,dx=\sum_{n=1}^{\infty}n^2\cdot\frac{1}{n^3}\cdot\frac{3}{8}=\frac{3}{8}\sum_{n=1}^{\infty}\frac{1}{n}=+\infty", 44, RED),
            self.zh("发散", font_size=38, color=RED, weight=BOLD),
        ).arrange(RIGHT, buff=0.25)
        k3 = self.mixed(
            ("text", "用到（降幂公式）：", MUTED),
            ("math", r"\int_0^{\pi}\sin^2u\,du=\frac{\pi}{2},\qquad \int_0^{\pi}\sin^4u\,du=\frac{3\pi}{8}", MUTED),
        text_size=34, math_size=42)
        content = self.layout_below(bar2, k1, k2, k3)
        self.write_formula(k1, run_time=1.2)
        self.write_formula(k2, run_time=1.2)
        self.write_text(k3)
        self.wait(2.0)
        self.clear_scene()

    # ---------- 两种方法对比 ----------
    def compare(self):
        bar = self.title_bar("两种构造，各有千秋")
        self.play(Write(bar), run_time=0.8)

        h1 = self.zh("三角形 + 辛普森（本讲）", font_size=40, color=YELLOW, weight=BOLD)
        c1a = self.zh("几何直观，一图看懂", font_size=36, color=INK)
        c1b = self.zh("数值公式变身精确武器，极巧", font_size=36, color=YELLOW)
        c1c = self.mixed(("text", "只要求连续 ", INK), ("math", r"C^{0}", INK), text_size=36)
        col1 = VGroup(h1, c1a, c1b, c1c).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        col1.next_to(bar, DOWN, buff=0.8).to_edge(LEFT, buff=1.1)

        h2 = self.zh("sin² 光滑凸起", font_size=40, color=VIOLET, weight=BOLD)
        c2a = self.zh("初等三角积分，不借外力", font_size=36, color=INK)
        c2b = self.mixed(("text", "函数无穷光滑 ", INK), ("math", r"C^{\infty}", INK),
                         ("text", "，更强", INK), text_size=36)
        c2c = self.zh("计算稍繁：降幂公式", font_size=36, color=INK)
        col2 = VGroup(h2, c2a, c2b, c2c).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        col2.next_to(bar, DOWN, buff=0.8).to_edge(RIGHT, buff=1.1)

        divider = Line([0, bar.get_bottom()[1] - 0.3, 0], [0, -3.1, 0], color=MUTED, stroke_width=1.5)
        self.play(FadeIn(col1), FadeIn(col2), Create(divider), run_time=1.0)

        bottom = self.zh("灵魂相同：又高又窄的尖峰 —— 线性积分“省着花”，平方积分守不住",
                         font_size=38, color=ORANGE, weight=BOLD)
        self.fit(bottom, width=config.frame_width - 1.2)
        bottom.to_edge(DOWN, buff=0.55)
        self.write_text(bottom, run_time=0.9)
        self.wait(2.0)
        self.clear_scene()

    # ---------- 原理透视 ----------
    def principle(self):
        bar = self.title_bar("原理透视：这类反例为什么一定能找到？", color=RED)
        self.play(Write(bar), run_time=0.8)

        p1 = self.mixed(
            ("text", "① 有限区间 [0,1]：", BLUE),
            ("math", r"f^2\le\max|f|\cdot f\ \Rightarrow\ \int_0^1 f^2\,dx\le \max|f|\int_0^1 f\,dx", BLUE),
            ("text", "，造不出反例", BLUE),
        text_size=36, math_size=40)
        p2 = self.mixed(
            ("text", "② 若 ", GREEN),
            ("math", r"f(x)\to 0", GREEN),
            ("text", "：终有 ", GREEN),
            ("math", r"f\le 1\ \Rightarrow\ f^2\le f", GREEN),
            ("text", "，平方积分必收敛 —— 峰不能落地！", GREEN),
        text_size=36, math_size=40)
        p3 = self.mixed(
            ("text", "③ 若 f 单调：", ORANGE),
            ("math", r"\int f\,dx<\infty\ \Rightarrow\ f\to 0", ORANGE),
            ("text", "，回到 ② —— 单调函数出局", ORANGE),
        text_size=36, math_size=40)
        p4 = self.zh("④ 反例只能：峰不落地 ＋ 宽度狂缩 —— 尖峰是唯一形态（两种方法皆是！）",
                     font_size=38, color=VIOLET, weight=BOLD)
        content = self.layout_below(bar, p1, p2, p3, p4)
        for p in [p1, p2, p3, p4]:
            self.play(Write(p), run_time=1.0)
            self.wait(1.0)
        self.wait(2.0)
        self.clear_scene()

    # ---------- 总结 ----------
    def summary(self):
        bar = self.title_bar("总结", color=GREEN)
        self.play(Write(bar), run_time=0.8)

        r1 = VGroup(
            self.mt(r"\int_0^{+\infty}f\,dx=1+\sqrt{2}", 50, GREEN),
            self.zh("收敛", font_size=36, color=GREEN, weight=BOLD),
            self.mt(r"\int_0^{+\infty}f^2\,dx=+\infty", 50, RED),
            self.zh("发散", font_size=36, color=RED, weight=BOLD),
        ).arrange(RIGHT, buff=0.3)
        r2 = self.zh("巧：辛普森公式对二次函数 100% 精确 —— 数值方法变身精确武器", font_size=38, color=INK)
        r3 = self.mixed(
            ("text", "根：", INK),
            ("math", r"L^{1}", BLUE),
            ("text", " 管“质量”，", INK),
            ("math", r"L^{2}", RED),
            ("text", " 管“能量” —— 无穷区间上互不包含", INK),
        )
        r4 = self.zh("反例的本质：把质量塞进越来越窄的尖峰里", font_size=34, color=MUTED)
        content = self.layout_below(bar, r1, r2, r3, r4)
        self.write_formula(r1, run_time=1.1)
        self.write_text(r2)
        self.write_text(r3)
        self.write_text(r4)
        box = SurroundingRectangle(r1, color=YELLOW, buff=0.2)
        self.play(Create(box), run_time=0.7)
        self.wait(2.5)
