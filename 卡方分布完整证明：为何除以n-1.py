from manim import *
import numpy as np
import math

# ============ 横屏大字·代数动画 SKILL（老版排版规范，本地化：Kaiti SC） ============
config.pixel_width = 1920
config.pixel_height = 1080
config.frame_width = 16.0
config.frame_height = 9.0

ZH_FONT = "Kaiti SC"     # SKILL 原值 KaiTi 为 Windows 字体，macOS 对应 Kaiti SC
BG     = "#0F1720"
INK    = "#F6F2EA"
MUTED  = "#A9B4C2"
BLUE   = "#5DADEC"
GREEN  = "#66D19E"
YELLOW = "#FFD166"
ORANGE = "#F59E62"
RED    = "#FF6B6B"
VIOLET = "#B79CFF"
READ_PAUSE = 2.5


def chi2_pdf(x, k):
    if x <= 0:
        return 0.0
    return x ** (k / 2 - 1) * np.exp(-x / 2) / (2 ** (k / 2) * math.gamma(k / 2))


class Chi2Proof(Scene):
    # ================= 辅助方法（老 SKILL 模板） =================
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

    def title_bar(self, text, color=BLUE, math_part=None):
        t1 = self.zh(text, font_size=52, color=color, weight=BOLD)
        if math_part is not None:
            t2 = MathTex(math_part, font_size=52, color=color, stroke_width=1)
            title = VGroup(t1, t2).arrange(RIGHT, buff=0.18)
        else:
            title = VGroup(t1)
        title.to_edge(UP, buff=0.38)
        return title

    def layout_below(self, bar, *lines, buff=None):
        n = len(lines)
        for line in lines:
            self.fit(line, width=config.frame_width - 1.2)
        if buff is None:
            buff = 1.1 if n <= 2 else (0.95 if n == 3 else 0.72)
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
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)

    # ================= 主流程 =================
    def construct(self):
        self.camera.background_color = BG
        self.opening()
        self.problem()
        self.strategy()
        self.concept_sample()
        self.concept_chi2()
        self.chi2_demo()
        self.concept_df()
        self.concept_back()
        self.roadmap()
        self.standardize()
        self.expand_one()
        self.expand_two()
        self.intuition_chi1()
        self.qform_intro()
        self.a_matrix()
        self.eigen_review()
        self.orth_diag()
        self.similar_congruent()
        self.isotropy()
        self.decompose()
        self.rank1_eig()
        self.eig_add()
        self.manuscript()
        self.geometry()
        self.diag_a()
        self.substitute()
        self.y_normal()
        self.finale()
        self.summary()
        self.ending()

    # ---------- 1. 开场 ----------
    def opening(self):
        colors = [YELLOW, ORANGE, RED, VIOLET, BLUE, GREEN,
                  YELLOW, ORANGE, RED, VIOLET, BLUE, GREEN, YELLOW, ORANGE, RED, VIOLET, BLUE]
        t = Text("样本方差为何除以 n-1 ？", font=ZH_FONT, font_size=72, weight=BOLD)
        for i, ch in enumerate(t):
            ch.set_color(colors[i % len(colors)])
        t.to_edge(UP, buff=1.1)
        sub = self.zh("—— 样本方差服从卡方分布 χ²(n-1) 的完整证明 ——",
                      font_size=40, color=INK).next_to(t, DOWN, buff=0.8)
        tag = self.zh("零基础 · 概念全铺垫 · 线代补课 · 全程可视化",
                      font_size=30, color=MUTED).next_to(sub, DOWN, buff=0.5)
        self.play(Write(t), run_time=1.2)
        self.play(FadeIn(sub, shift=UP * 0.3), run_time=0.6)
        self.play(FadeIn(tag), run_time=0.4)
        self.wait(3.3)
        self.clear_scene()

    # ---------- 2. 抄题 ----------
    def problem(self):
        bar = self.title_bar("题目", color=BLUE)
        self.play(Write(bar), run_time=0.7)
        given = self.mixed(
            ("text", "已知：", BLUE),
            ("math", r"X_1,\cdots,X_n\ \text{ iid}\ \sim\ N(\mu,\ \sigma^2)", INK),
         text_size=40, math_size=48)
        ask1 = self.mixed(
            ("text", "求证：", GREEN),
            ("math", r"\sum_{i=1}^{n}\frac{(X_i-\bar{X})^2}{\sigma^2}\sim\chi^2(n-1)", GREEN),
         text_size=40, math_size=50)
        ask2 = self.mixed(
            ("text", "即：", ORANGE),
            ("math", r"\frac{(n-1)S^2}{\sigma^2}\sim\chi^2(n-1)", ORANGE),
            ("text", "（样本方差 S² 的分布）", MUTED),
         text_size=38, math_size=48)
        iid_note = self.zh(
            "小注：iid = independent and identically distributed，即“独立同分布”——每个 Xi 同分布且相互独立",
            font_size=30, color=MUTED)
        content = self.layout_below(bar, given, ask1, ask2, iid_note)
        self.write_text(given, run_time=1.0)
        self.write_formula(ask1, run_time=1.0)
        self.write_formula(ask2, run_time=1.0)
        self.write_text(iid_note, run_time=0.8)
        self.wait(1.8)
        self.wait(3.3)
        self.clear_scene()

    # ---------- 3. 思路分析 ----------
    def strategy(self):
        bar = self.title_bar("证明思路分析", color=GREEN)
        self.play(Write(bar), run_time=0.7)
        s1 = self.mixed(
            ("text", "一、标准化：", BLUE),
            ("math", r"Z_i=\frac{X_i-\mu}{\sigma}\sim N(0,1)", BLUE),
            ("text", "，把 σ² 归一，只证 σ²=1", BLUE),
         text_size=36, math_size=44)
        s2 = self.mixed(
            ("text", "二、展开：", ORANGE),
            ("math", r"\sum(Z_i-\bar{Z})^2=\sum Z_i^2-n\bar{Z}^2", ORANGE),
            ("text", "，写成二次型", ORANGE),
         text_size=36, math_size=44)
        s3 = self.mixed(
            ("text", "三、线代补课：", VIOLET),
            ("math", r"z^{\mathsf{T}}Az", VIOLET),
            ("text", "、特征值、实对称矩阵的正交对角化", VIOLET),
         text_size=36, math_size=44)
        s4 = self.mixed(
            ("text", "四、对角化数 1：", GREEN),
            ("math", r"Q^{\mathsf{T}}AQ=\mathrm{diag}(1,\cdots,1,0)", GREEN),
            ("text", "，1 的个数 = 自由度 = n-1", GREEN),
         text_size=36, math_size=44)
        content = self.layout_below(bar, s1, s2, s3, s4)
        for line in [s1, s2, s3, s4]:
            self.play(Write(line), run_time=0.9)
            self.wait(0.5)
        self.wait(3.3)
        self.clear_scene()

    # ---------- 4. 概念：样本均值与样本方差 ----------
    def concept_sample(self):
        bar = self.title_bar("概念铺垫：主角登场", color=BLUE)
        self.play(Write(bar), run_time=0.7)
        d1 = self.mixed(
            ("text", "样本均值 ", INK),
            ("math", r"\bar{X}=\frac{1}{n}\sum_{i=1}^{n}X_i", YELLOW),
            ("text", "，样本方差 ", INK),
            ("math", r"S^2=\frac{1}{n-1}\sum_{i=1}^{n}(X_i-\bar{X})^2", GREEN),
         text_size=36, math_size=44)
        content = self.layout_below(bar, d1)
        self.write_formula(d1, run_time=1.1)

        # 数轴可视化：n=5 个样本点与均值
        line = Line(LEFT * 6.2, RIGHT * 6.2, color=MUTED, stroke_width=3)
        line.shift(DOWN * 1.4)
        vals = [1.1, 2.3, 2.9, 3.6, 5.1]
        mean = float(np.mean(vals))
        dots = VGroup()
        for v in vals:
            dots.add(Dot(line.get_left() + RIGHT * (v / 6.0) * 6.2 * 2 + UP * 0.0,
                         radius=0.09, color=BLUE))
        # 均值虚线
        xbar_x = line.get_left()[0] + (mean / 6.0) * 12.4
        dline = DashedLine([xbar_x, line.get_y() - 0.45, 0], [xbar_x, line.get_y() + 1.6, 0],
                           color=YELLOW, stroke_width=3)
        mlab = self.mt(r"\bar{X}", font_size=40, color=YELLOW).next_to(dline, UP, buff=0.1)
        segs = VGroup()
        for d in dots:
            segs.add(Line(d.get_center(), [xbar_x, d.get_y(), 0],
                          color=RED, stroke_width=3))
        lab = self.zh("样本点（蓝）、样本均值（黄）、偏差（红）",
                      font_size=30, color=MUTED).next_to(line, DOWN, buff=0.5)
        self.play(Create(line), run_time=0.5)
        self.play(FadeIn(dots, lag_ratio=0.1), Create(dline), Write(mlab), run_time=0.7)
        self.play(Create(segs), run_time=0.7)
        self.play(Write(lab), run_time=0.6)
        self.wait(2.3)
        self.clear_scene()

    # ---------- 5. 概念：卡方分布 ----------
    def concept_chi2(self):
        bar = self.title_bar("概念铺垫：什么是卡方分布", color=BLUE, math_part=r"\chi^2(k)")
        self.play(Write(bar), run_time=0.7)
        d1 = self.mixed(
            ("text", "定义：", GREEN),
            ("math", r"Z_1,\cdots,Z_k\ \text{iid}\sim N(0,1)\ \Longrightarrow\ Z_1^2+\cdots+Z_k^2\sim\chi^2(k)", INK),
         text_size=36, math_size=42)
        d2 = self.zh("k 个独立标准正态的平方和，参数 k 叫做自由度",
                     font_size=34, color=MUTED)
        content = self.layout_below(bar, d1, d2)
        self.write_formula(d1, run_time=1.1)
        self.write_text(d2)

        # PDF 曲线族
        axes = Axes(x_range=[0, 13, 1], y_range=[0, 1.75, 0.5],
                    x_length=11.5, y_length=3.3,
                    axis_config={"color": MUTED, "stroke_width": 2, "include_ticks": False})
        axes.move_to(DOWN * 1.15)
        curves = VGroup()
        labs = VGroup()
        for k, col in [(1, BLUE), (3, GREEN), (6, RED)]:
            cv = axes.plot(lambda x, k=k: chi2_pdf(x, k),
                           x_range=[0.05 if k == 1 else 0.001, 13],
                           color=col, stroke_width=4)
            curves.add(cv)
            labs.add(MathTex(r"\chi^2(%d)" % k, font_size=32, color=col)
                     .move_to(axes.c2p(0.7 if k == 1 else (1.8 if k == 3 else 6.2),
                                       chi2_pdf(0.7 if k == 1 else (1.8 if k == 3 else 6.2), k) + 0.28)))
        self.play(Create(axes), run_time=0.5)
        self.play(Create(curves[0]), FadeIn(labs[0]), run_time=0.6)
        self.play(Create(curves[1]), FadeIn(labs[1]), run_time=0.5)
        self.play(Create(curves[2]), FadeIn(labs[2]), run_time=0.5)
        cap = self.zh("自由度越大，分布越靠右、越宽、越对称", font_size=28, color=MUTED)
        cap.next_to(axes, DOWN, buff=0.35)
        self.play(Write(cap), run_time=0.5)
        self.wait(2.3)
        self.clear_scene()


    # ---------- 2.5 卡方举个例子：蒙特卡洛 ----------
    def chi2_demo(self):
        bar = self.title_bar("举个例子：亲手造一个卡方", color=BLUE, math_part=r"n=3")
        self.play(Write(bar), run_time=0.7)
        l1 = self.mixed(
            ("text", "每次抽 ", INK),
            ("math", "3", YELLOW),
            ("text", " 个独立标准正态，平方求和 —— 重复 400 次：", INK),
         text_size=36, math_size=44)
        content = self.layout_below(bar, l1)
        self.write_formula(l1, run_time=0.9)

        axes = Axes(x_range=[0, 12, 1], y_range=[0, 0.62, 0.2],
                    x_length=11.5, y_length=3.4,
                    axis_config={"color": MUTED, "stroke_width": 2, "include_ticks": False})
        axes.move_to(DOWN * 1.15)
        rng = np.random.default_rng(5)
        sums = (rng.normal(0, 1, (400, 3)) ** 2).sum(axis=1)
        edges = np.linspace(0, 12, 25)
        freqs, _ = np.histogram(sums, bins=edges)
        dens = freqs / 400 / (edges[1] - edges[0])
        bars = VGroup()
        for i in range(24):
            if dens[i] <= 0.002:
                continue
            x0, x1, h = edges[i], edges[i + 1], dens[i]
            bars.add(Polygon(axes.c2p(x0, 0), axes.c2p(x0, h), axes.c2p(x1, h),
                             axes.c2p(x1, 0), fill_color=BLUE, fill_opacity=0.55,
                             stroke_width=0))
        cv = axes.plot(lambda x: chi2_pdf(x, 3), x_range=[0.01, 12],
                       color=YELLOW, stroke_width=5)
        lab = MathTex(r"\chi^2(3)", font_size=34, color=YELLOW).move_to(axes.c2p(5.4, 0.4))
        self.play(Create(axes), run_time=0.4)
        self.play(FadeIn(bars, lag_ratio=0.05), run_time=1.5)
        self.play(Create(cv), FadeIn(lab), run_time=0.7)
        cap = self.zh("400 根柱子的直方图，与 χ²(3) 理论曲线完美贴合",
                      font_size=30, color=MUTED).next_to(axes, DOWN, buff=0.35)
        self.play(Write(cap), run_time=0.5)
        self.wait(2.9)
        self.clear_scene()

    # ---------- 6. 概念：自由度（锁死动画） ----------
    def concept_df(self):
        bar = self.title_bar("概念铺垫：自由度是什么", color=BLUE)
        self.play(Write(bar), run_time=0.7)
        d1 = self.zh("三个数之和必须是 30 —— 你能自由填几个？",
                     font_size=40, color=INK)
        d1.move_to(UP * 2.2)
        self.write_text(d1)

        boxes = VGroup()
        nums = VGroup()
        for i in range(3):
            bx = Square(side_length=1.5, color=MUTED, stroke_width=3)
            bx.move_to(LEFT * 3.2 + RIGHT * i * 2.4 + DOWN * 0.4)
            boxes.add(bx)
        self.play(Create(boxes), run_time=0.6)
        n1 = self.mt("12", font_size=56, color=GREEN).move_to(boxes[0])
        n2 = self.mt("11", font_size=56, color=GREEN).move_to(boxes[1])
        self.play(Write(n1), run_time=0.4)
        self.wait(0.4)
        self.play(Write(n2), run_time=0.4)
        n3 = self.mt("7", font_size=56, color=RED).move_to(boxes[2])
        lock = self.zh("被锁死！", font_size=30, color=RED, weight=BOLD)
        lock.next_to(boxes[2], DOWN, buff=0.25)
        self.play(Write(n3), FadeIn(lock, shift=UP * 0.2), run_time=0.6)
        box3 = SurroundingRectangle(boxes[2], color=RED, buff=0.08)
        self.play(Create(box3), run_time=0.4)
        self.wait(1.0)

        d2 = self.mixed(
            ("text", "约束一出现，自由就少一个：", INK),
            ("math", r"n\ \text{numbers}\ \xrightarrow{\ 1\ \text{constraint}\ }\ n-1\ \text{free}", YELLOW),
         text_size=36, math_size=44)
        d2.move_to(DOWN * 2.3)
        self.fit(d2)
        self.write_formula(d2, run_time=1.0)
        self.wait(3.3)
        self.clear_scene()

    # ---------- 7. 概念：回到样本 ----------
    def concept_back(self):
        bar = self.title_bar("回到样本：自由度 n-1 从哪来", color=BLUE)
        self.play(Write(bar), run_time=0.7)
        l1 = self.mixed(
            ("text", "样本均值 ", INK),
            ("math", r"\bar{X}", YELLOW),
            ("text", " 把 ", INK),
            ("math", r"\sum_{i=1}^{n}(X_i-\bar{X})=0", INK),
            ("text", " 这个约束焊死在偏差上", INK),
         text_size=36, math_size=44)
        l2 = self.mixed(
            ("text", "n 个偏差 ", INK),
            ("math", r"X_1-\bar{X},\cdots,X_n-\bar{X}", INK),
            ("text", " 中只有 ", RED),
            ("math", r"n-1", RED),
            ("text", " 个能自由变化", RED),
         text_size=36, math_size=44)
        l3 = self.mixed(
            ("text", "所以样本方差除以 ", INK),
            ("math", r"n-1", GREEN),
            ("text", "：这样 ", INK),
            ("math", r"E(S^2)=\sigma^2", GREEN),
            ("text", "（无偏）", INK),
         text_size=36, math_size=44)
        l4 = self.zh("今天的任务：证明这个 n-1 也决定了卡方分布的自由度",
                     font_size=34, color=ORANGE, weight=BOLD)
        content = self.layout_below(bar, l1, l2, l3, l4)
        for line in [l1, l2, l3, l4]:
            self.write_formula(line, run_time=0.9)
        self.wait(3.3)
        self.clear_scene()

    # ---------- 8. 路线图 ----------
    def roadmap(self):
        bar = self.title_bar("证明路线图", color=ORANGE)
        self.play(Write(bar), run_time=0.7)
        r1 = self.mixed(("text", "① 标准化：", BLUE),
                        ("math", r"\frac{\sum(X_i-\bar{X})^2}{\sigma^2}=\sum(Z_i-\bar{Z})^2", BLUE),
                         text_size=36, math_size=42)
        r2 = self.mixed(("text", "② 展开成二次型：", VIOLET),
                        ("math", r"\sum Z_i^2-n\bar{Z}^2=z^{\mathsf{T}}Az,\ \ A=I-\frac{1}{n}J", VIOLET),
                         text_size=36, math_size=42)
        r3 = self.mixed(("text", "③ 正交对角化：", ORANGE),
                        ("math", r"Q^{\mathsf{T}}AQ=\mathrm{diag}(1,\cdots,1,0)", ORANGE),
                         text_size=36, math_size=42)
        r4 = self.mixed(("text", "④ 数一数：", GREEN),
                        ("math", r"\sum y_i^2\ (n-1\ \text{terms})\sim\chi^2(n-1)", GREEN),
                         text_size=36, math_size=42)
        content = self.layout_below(bar, r1, r2, r3, r4)
        for line in [r1, r2, r3, r4]:
            self.write_formula(line, run_time=0.9)
        self.wait(3.3)
        self.clear_scene()

    # ---------- 9. 标准化 ----------
    def standardize(self):
        bar = self.title_bar("第一步：标准化", color=ORANGE, math_part=r"\sigma^2=1")
        self.play(Write(bar), run_time=0.7)
        l1 = self.mixed(("text", "令 ", INK),
                        ("math", r"Z_i=\frac{X_i-\mu}{\sigma}\sim N(0,1)", YELLOW),
                        ("text", "（独立同分布）", INK), text_size=36, math_size=46)
        l2 = self.mt(r"\bar{X}=\mu+\sigma\bar{Z}\ \Longrightarrow\ X_i-\bar{X}=\sigma(Z_i-\bar{Z})",
                     font_size=48)
        l3 = self.mt(r"\Longrightarrow\ \sum_{i=1}^{n}\frac{(X_i-\bar{X})^2}{\sigma^2}=\sum_{i=1}^{n}(Z_i-\bar{Z})^2",
                     font_size=46, color=GREEN)
        l4 = self.zh("σ² 被彻底消化 —— 下面只证 σ²=1 的情形",
                     font_size=34, color=MUTED)
        content = self.layout_below(bar, l1, l2, l3, l4)
        self.write_formula(l1, run_time=0.9)
        self.write_formula(l2, run_time=1.1)
        self.write_formula(l3, run_time=1.1)
        self.write_text(l4)
        self.wait(1.6)
        self.clear_scene()

    # ---------- 10. 展开一 ----------
    def expand_one(self):
        bar = self.title_bar("第二步：展开平方和", color=ORANGE)
        self.play(Write(bar), run_time=0.7)
        l1 = self.mt(r"\sum_{i=1}^{n}(Z_i-\bar{Z})^2=\sum_{i=1}^{n}\left(Z_i^2-2Z_i\bar{Z}+\bar{Z}^2\right)",
                     font_size=48)
        l2 = self.mt(r"=\sum_{i=1}^{n}Z_i^2\ -\ 2\bar{Z}\sum_{i=1}^{n}Z_i\ +\ n\bar{Z}^2",
                     font_size=48)
        l3 = self.mixed(("text", "记住这个恒等式：", INK),
                        ("math", r"\sum_{i=1}^{n}Z_i=n\bar{Z}", YELLOW),
                        ("text", "（均值的定义）", INK), text_size=36, math_size=46)
        content = self.layout_below(bar, l1, l2, l3)
        self.write_formula(l1, run_time=1.1)
        self.write_formula(l2, run_time=1.1)
        self.write_formula(l3, run_time=0.9)
        self.wait(1.6)
        self.clear_scene()

    # ---------- 11. 展开二 ----------
    def expand_two(self):
        bar = self.title_bar("第二步：收拢成一个减一个", color=ORANGE)
        self.play(Write(bar), run_time=0.7)
        l1 = self.mt(r"\sum_{i=1}^{n}(Z_i-\bar{Z})^2=\sum_{i=1}^{n}Z_i^2-n\bar{Z}^2",
                     font_size=54, color=YELLOW)
        l2 = self.mixed(("text", "本来 ", INK),
                        ("math", r"\sum Z_i^2\sim\chi^2(n)", GREEN),
                        ("text", "（n 个独立平方和）", INK), text_size=36, math_size=44)
        l3 = self.mixed(("text", "减去 ", INK),
                        ("math", r"n\bar{Z}^2=\left(\frac{\sum Z_i}{\sqrt{n}}\right)^2", RED),
                        ("text", "，恰好吃掉 1 个自由度", INK), text_size=36, math_size=44)
        l4 = self.zh("but 这只是直觉 —— 要把它变成定理，得请出线性代数",
                     font_size=34, color=ORANGE, weight=BOLD)
        content = self.layout_below(bar, l1, l2, l3, l4)
        self.write_formula(l1, run_time=1.1)
        self.write_formula(l2, run_time=0.9)
        self.write_formula(l3, run_time=0.9)
        self.write_text(l4)
        self.wait(1.6)
        self.clear_scene()


    # ---------- 10.5 直觉版：nZ̄² 也是卡方 ----------
    def intuition_chi1(self):
        bar = self.title_bar("直觉版：被减去的恰是一个卡方", color=ORANGE)
        self.play(Write(bar), run_time=0.7)
        l1 = self.mixed(
            ("text", "独立正态之和仍正态：", INK),
            ("math", r"\sqrt{n}\,\bar{Z}=\frac{Z_1+\cdots+Z_n}{\sqrt{n}}\sim N(0,1)", YELLOW),
             text_size=36, math_size=46)
        l2 = self.mixed(
            ("text", "于是被减去的 ", INK),
            ("math", r"n\bar{Z}^2=\left(\sqrt{n}\,\bar{Z}\right)^2\sim\chi^2(1)", GREEN),
            ("text", "，也是卡方！", INK),
             text_size=36, math_size=46)
        l3 = self.mixed(
            ("text", "直觉：", ORANGE),
            ("math", r"\chi^2(n)-\chi^2(1)=\chi^2(n-1)", ORANGE),
            ("text", "？—— 相减要有资格：两块必须独立", INK),
             text_size=36, math_size=46)
        l4 = self.zh("ΣZ² 与 Z̄ 独立吗？直觉不够 —— 二次型路线来严格化",
                     font_size=34, color=VIOLET, weight=BOLD)
        content = self.layout_below(bar, l1, l2, l3, l4)
        self.write_formula(l1, run_time=1.0)
        self.write_formula(l2, run_time=1.0)
        self.write_formula(l3, run_time=1.0)
        self.write_text(l4)
        self.wait(2.7)
        self.clear_scene()

    # ---------- 12. 线代补课：二次型 ----------
    def qform_intro(self):
        bar = self.title_bar("线代补课①：二次型", color=VIOLET, math_part=r"z^{\mathsf{T}}Az")
        self.play(Write(bar), run_time=0.7)
        l1 = self.mixed(("text", "对称矩阵 ", INK),
                        ("math", r"A", VIOLET),
                        ("text", " 的二次型：", INK),
                        ("math", r"z^{\mathsf{T}}Az=\sum_{i,j}a_{ij}z_iz_j", YELLOW),
                         text_size=36, math_size=44)
        content = self.layout_below(bar, l1)
        self.write_formula(l1, run_time=1.0)

        # 三个水平集曲线
        trio = VGroup()
        mats = [
            (np.array([[1.0, 0.0], [0.0, 1.0]]), r"z_1^2+z_2^2", BLUE, "圆"),
            (np.array([[1.0, 0.0], [0.0, 4.0]]), r"z_1^2+4z_2^2", GREEN, "正椭圆"),
            (np.array([[1.0, 1.0], [1.0, 2.0]]), r"z_1^2+2z_1z_2+2z_2^2", RED, "斜椭圆"),
        ]
        for A2, tex, col, tag in mats:
            vals, vecs = np.linalg.eigh(A2)
            pts = []
            for t in np.linspace(0, 2 * np.pi, 120):
                z = vecs @ np.array([np.cos(t) / np.sqrt(vals[0]),
                                     np.sin(t) / np.sqrt(vals[1])])
                pts.append([z[0] * 1.1, z[1] * 1.1, 0.0])
            arr = np.array(pts)
            curve = ParametricFunction(
                lambda tt, arr=arr: arr[min(int(tt / (2 * np.pi) * 119), 119)],
                t_range=[0, 2 * np.pi], color=col, stroke_width=4)
            lab = MathTex(tex, font_size=34, color=col)
            tagt = self.zh(tag, font_size=26, color=MUTED)
            grp = VGroup(curve, lab, tagt).arrange(DOWN, buff=0.25)
            trio.add(grp)
        trio.arrange(RIGHT, buff=1.2).move_to(DOWN * 1.3)
        self.play(FadeIn(trio[0]), run_time=0.5)
        self.play(FadeIn(trio[1]), run_time=0.5)
        self.play(FadeIn(trio[2]), run_time=0.5)
        cap = self.zh("矩阵决定形状；交叉项让椭圆歪头 —— 矩阵的非对角元",
                      font_size=30, color=MUTED).next_to(trio, DOWN, buff=0.4)
        self.play(Write(cap), run_time=0.6)
        self.wait(1.6)
        self.clear_scene()

    # ---------- 13. 我们的二次型矩阵 ----------
    def a_matrix(self):
        bar = self.title_bar("写出我们的二次型矩阵", color=ORANGE)
        self.play(Write(bar), run_time=0.7)
        l1 = self.mt(r"\sum_{i=1}^{n}Z_i^2-n\bar{Z}^2=\sum_{i=1}^{n}Z_i^2-\frac{1}{n}\Big(\sum_{i=1}^{n}Z_i\Big)^2",
                     font_size=44)
        l2 = self.mixed(("text", "由于 ", INK),
                        ("math", r"\bar{Z}^2=\frac{1}{n^2}\big(\sum Z_i\big)^2=\frac{1}{n}\cdot\frac{1}{n}\big(\sum Z_i\big)^2", MUTED),
                         text_size=34, math_size=42)
        l3 = self.mt(r"=z^{\mathsf{T}}Az,\qquad A=I-\frac{1}{n}J,\quad J=\begin{bmatrix}1&\cdots&1\\ \vdots&\ddots&\vdots\\ 1&\cdots&1\end{bmatrix}",
                     font_size=42, color=YELLOW)
        l4 = self.zh("J：全 1 矩阵；I：单位阵 —— 全场主角登场",
                     font_size=32, color=MUTED)
        content = self.layout_below(bar, l1, l2, l3, l4)
        self.write_formula(l1, run_time=1.1)
        self.write_formula(l2, run_time=0.8)
        self.write_formula(l3, run_time=1.3)
        self.write_text(l4)
        self.wait(1.6)
        self.clear_scene()

    # ---------- 14. 线代补课：特征值 ----------
    def eigen_review(self):
        bar = self.title_bar("线代补课②：特征值与特征向量", color=VIOLET, math_part=r"Av=\lambda v")
        self.play(Write(bar), run_time=0.7)
        l1 = self.mixed(("text", "几何意义：", INK),
                        ("math", r"v", GREEN),
                        ("text", " 方向只被拉伸 ", INK),
                        ("math", r"\lambda", RED),
                        ("text", " 倍，方向不变", INK), text_size=36, math_size=46)
        content = self.layout_below(bar, l1)
        self.write_formula(l1, run_time=0.9)

        # 单位圆 → 椭圆（A=diag(2,1)）
        circ = ParametricFunction(
            lambda t: np.array([np.cos(t), np.sin(t), 0]), t_range=[0, TAU],
            color=INK, stroke_width=3)
        ell = ParametricFunction(
            lambda t: np.array([2 * np.cos(t), np.sin(t), 0]), t_range=[0, TAU],
            color=YELLOW, stroke_width=5)
        v1 = Arrow(ORIGIN, RIGHT * 2, color=RED, buff=0)
        v2 = Arrow(ORIGIN, UP * 1, color=GREEN, buff=0)
        l1t = MathTex(r"\lambda_1=2", font_size=30, color=RED).next_to(v1, DOWN, buff=0.15)
        l2t = MathTex(r"\lambda_2=1", font_size=30, color=GREEN).next_to(v2, RIGHT, buff=0.15)
        grp = VGroup(circ, ell, v1, v2, l1t, l2t).move_to(DOWN * 1.5)
        self.play(Create(circ), run_time=0.6)
        self.play(Transform(circ, ell), FadeIn(v1), FadeIn(v2), FadeIn(l1t), FadeIn(l2t),
                  run_time=1.0)
        cap = self.zh("A = diag(2,1)：圆变椭圆，只有特征方向毫不动摇",
                      font_size=30, color=MUTED).next_to(grp, DOWN, buff=0.35)
        self.play(Write(cap), run_time=0.6)
        self.wait(1.6)
        self.clear_scene()

    # ---------- 15. 线代补课：实对称正交对角化 ----------
    def orth_diag(self):
        bar = self.title_bar("线代补课③：实对称必可正交对角化", color=VIOLET)
        self.play(Write(bar), run_time=0.7)
        l1 = self.mt(r"A=A^{\mathsf{T}}\ \Longrightarrow\ \exists\ Q^{\mathsf{T}}Q=E:\ Q^{\mathsf{T}}AQ=\Lambda",
                     font_size=46, color=YELLOW)
        l2 = self.zh("几何翻译：旋转坐标系，歪椭圆总能摆正",
                     font_size=36, color=INK)
        content = self.layout_below(bar, l1, l2)
        self.write_formula(l1, run_time=1.1)
        self.write_text(l2)

        # 斜椭圆摆正动画
        A2 = np.array([[1.0, 1.0], [1.0, 2.0]])
        vals, vecs = np.linalg.eigh(A2)
        angle = float(np.arctan2(vecs[1, 1], vecs[0, 1]))
        pts = np.array([[*(vecs @ np.array([np.cos(t) / np.sqrt(vals[0]),
                                            np.sin(t) / np.sqrt(vals[1])])) * 1.15, 0.0]
                        for t in np.linspace(0, 2 * np.pi, 120)])
        tilted = ParametricFunction(
            lambda t: pts[min(int(t / (2 * np.pi) * 119), 119)],
            t_range=[0, 2 * np.pi], color=RED, stroke_width=5)
        ax1 = Arrow(ORIGIN, np.array([*(vecs[:, 1] * np.sqrt(vals[1]) * 1.3), 0.0]),
                    color=GREEN, buff=0)
        ax2 = Arrow(ORIGIN, np.array([*(vecs[:, 0] * np.sqrt(vals[0]) * 1.3), 0]),
                    color=BLUE, buff=0)
        grp = VGroup(tilted, ax1, ax2).move_to(DOWN * 1.6)
        self.play(Create(tilted), FadeIn(ax1), FadeIn(ax2), run_time=0.8)
        self.play(Rotate(grp, -angle), run_time=1.2)
        cap = self.zh("转正之后：两个坐标轴正好就是特征向量方向",
                      font_size=30, color=MUTED).next_to(grp, DOWN, buff=0.35)
        self.play(Write(cap), run_time=0.6)
        self.wait(1.6)
        self.clear_scene()

    # ---------- 16. 相似与合同 ----------
    def similar_congruent(self):
        bar = self.title_bar("线代补课④：相似 = 合同", color=VIOLET)
        self.play(Write(bar), run_time=0.7)
        l1 = self.mixed(("text", "正交矩阵满足 ", INK),
                        ("math", r"Q^{\mathsf{T}}Q=E\ \Longrightarrow\ Q^{\mathsf{T}}=Q^{-1}", YELLOW),
                         text_size=36, math_size=46)
        l2 = self.mt(r"\Longrightarrow\ Q^{\mathsf{T}}AQ=Q^{-1}AQ=\Lambda", font_size=50, color=GREEN)
        l3 = self.zh("同一个变换，既是相似（保特征值），又是合同（保二次型）",
                     font_size=34, color=INK)
        l4 = self.zh("这就是为什么对角化能同时服务特征值与二次型",
                     font_size=30, color=MUTED)
        content = self.layout_below(bar, l1, l2, l3, l4)
        self.write_formula(l1, run_time=0.9)
        self.write_formula(l2, run_time=1.0)
        self.write_text(l3)
        self.write_text(l4)
        self.wait(1.6)
        self.clear_scene()

    # ---------- 17. 各向同性：云旋转不变 ----------
    def isotropy(self):
        bar = self.title_bar("关键性质：标准正态云各向同性", color=VIOLET)
        self.play(Write(bar), run_time=0.7)
        l1 = self.mixed(("text", "密度只看距离：", INK),
                        ("math", r"f_Z(z)=\frac{1}{(2\pi)^{n/2}}e^{-\|z\|^2/2}", YELLOW),
                         text_size=36, math_size=46)
        content = self.layout_below(bar, l1)
        self.write_formula(l1, run_time=1.0)

        rng = np.random.default_rng(3)
        pts = rng.normal(0, 1, (90, 2)) * 0.95
        cloud = VGroup(*[Dot(np.array([p[0] * 0.62, p[1] * 0.62, 0.0]), radius=0.05, color=BLUE).set_opacity(0.85) for p in pts])
        ghost = cloud.copy().set_opacity(0.18)
        grp = VGroup(ghost, cloud).move_to(DOWN * 1.5)
        self.play(FadeIn(cloud, lag_ratio=0.05), run_time=0.7)
        self.add(ghost)
        self.play(Rotate(cloud, 1.05), run_time=1.4)
        cap = self.zh("旋转 60° 后与影子重合 —— 每个方向都长得一样",
                      font_size=30, color=MUTED).next_to(grp, DOWN, buff=0.35)
        self.play(Write(cap), run_time=0.6)
        self.wait(2.3)
        self.clear_scene()

    # ---------- 18. 分解 A ----------
    def decompose(self):
        bar = self.title_bar("第三步：分解二次型矩阵", color=ORANGE)
        self.play(Write(bar), run_time=0.7)
        l1 = self.mt(r"A=I-\frac{1}{n}J", font_size=54, color=YELLOW)
        l2 = self.mt(r"J=\begin{bmatrix}1&\cdots&1\\ \vdots&\ddots&\vdots\\ 1&\cdots&1\end{bmatrix},\qquad \frac{1}{n}J=\begin{bmatrix}\frac1n&\cdots&\frac1n\\ \vdots&\ddots&\vdots\\ \frac1n&\cdots&\frac1n\end{bmatrix}",
                     font_size=40)
        l3 = self.mixed(("text", "秩 1 矩阵：", RED),
                        ("math", r"\frac1n J=u u^{\mathsf{T}},\ u=\frac{1}{\sqrt{n}}(1,\cdots,1)^{\mathsf{T}}", RED),
                        ("text", "，每一行完全相同", INK),
                         text_size=36, math_size=44)
        content = self.layout_below(bar, l1, l2, l3)
        self.write_formula(l1, run_time=0.9)
        self.write_formula(l2, run_time=1.2)
        self.write_formula(l3, run_time=1.0)
        self.wait(1.6)
        self.clear_scene()

    # ---------- 19. 秩 1 矩阵的特征值 ----------
    def rank1_eig(self):
        bar = self.title_bar("秩 1 矩阵的特征值", color=ORANGE, math_part=r"J\mathbf{1}=n\mathbf{1}")
        self.play(Write(bar), run_time=0.7)
        l1 = self.mixed(("text", "全 1 向量 ", INK),
                        ("math", r"\mathbf{1}=(1,\cdots,1)^{\mathsf{T}}", GREEN),
                        ("text", " 是特征向量：", INK),
                        ("math", r"J\mathbf{1}=n\mathbf{1}", YELLOW),
                        ("text", "（每行求和都是 n）", INK),
                         text_size=34, math_size=44)
        l2 = self.mixed(("text", "J 对称且秩为 1 ⟹ 特征值：", INK),
                        ("math", r"n,\ 0,\ \cdots,\ 0", YELLOW),
                         text_size=36, math_size=46)
        l3 = self.mixed(("text", "于是 ", INK),
                        ("math", r"B=-\frac1nJ", ORANGE),
                        ("text", " 的特征值：", INK),
                        ("math", r"-1,\ 0,\ \cdots,\ 0", RED),
                        ("text", "（迹 = -1 交叉验证）", MUTED),
                         text_size=34, math_size=46)
        content = self.layout_below(bar, l1, l2, l3)
        self.write_formula(l1, run_time=1.1)
        self.write_formula(l2, run_time=0.9)
        self.write_formula(l3, run_time=1.0)
        self.wait(1.6)
        self.clear_scene()

    # ---------- 20. 特征值相加 ----------
    def eig_add(self):
        bar = self.title_bar("手稿的关键一步：特征值怎么相加", color=ORANGE)
        self.play(Write(bar), run_time=0.7)
        l1 = self.mixed(("text", "【关键补充】", RED),
                        ("text", "两个矩阵的特征值能直接相加，当且仅当它们", INK),
                        ("text", "可同时对角化", RED, ),
                         text_size=34, math_size=42)
        l2 = self.mixed(("text", "好消息：", GREEN),
                        ("math", r"BE=EB", GREEN),
                        ("text", " 自动成立（E 乘谁都等于谁），且都对称", GREEN),
                         text_size=34, math_size=44)
        l3 = self.mixed(("text", "⟹ 可同时对角化 ⟹ A 的特征值逐个相加：", INK),
                         text_size=34, math_size=42)
        l4 = self.mt(r"\underbrace{(-1)+1}_{\mathbf{1}\ \text{dir.}}=0,\qquad \underbrace{0+1}_{\perp\ \mathbf{1}}=1,\cdots,\ 1",
                     font_size=48, color=YELLOW)
        l5 = self.mixed(("text", "交叉验证：", MUTED),
                        ("math", r"\mathrm{tr}(A)=n-\frac{n}{n}=n-1", MUTED),
                        ("text", "，与特征值之和完全一致", MUTED),
                         text_size=32, math_size=42)
        content = self.layout_below(bar, l1, l2, l3, l4, l5, buff=0.6)
        self.play(Write(l1), run_time=1.0)
        self.write_formula(l2, run_time=0.9)
        self.write_text(l3)
        self.write_formula(l4, run_time=1.1)
        self.write_formula(l5, run_time=0.9)
        self.wait(1.6)
        self.clear_scene()


    # ---------- 21.5 几何透视：偏差住在 n-1 维子空间 ----------
    def geometry(self):
        bar = self.title_bar("几何透视：偏差向量住在 n-1 维子空间", color=ORANGE)
        self.play(Write(bar), run_time=0.7)
        l1 = self.mixed(
            ("text", "以 n=2 为例：偏差 ", INK),
            ("math", r"(Z_1-\bar{Z},\ Z_2-\bar{Z})=\Big(\frac{Z_1-Z_2}{2},\ -\frac{Z_1-Z_2}{2}\Big)", YELLOW),
            ("text", "，恒在直线 ", INK),
            ("math", r"Z_1+Z_2=0", GREEN),
            ("text", " 上", INK),
             text_size=34, math_size=42)
        content = self.layout_below(bar, l1)
        self.write_formula(l1, run_time=1.1)

        axes = Axes(x_range=[-3, 3, 1], y_range=[-3, 3, 1],
                    x_length=4.6, y_length=4.6,
                    axis_config={"color": MUTED, "stroke_width": 2, "include_ticks": False})
        axes.move_to(DOWN * 1.35).shift(LEFT * 3.4)
        ln = Line(axes.c2p(-2.3, 2.3), axes.c2p(2.3, -2.3), color=GREEN, stroke_width=4)
        zpt = Dot(axes.c2p(1.3, 0.55), radius=0.07, color=BLUE)
        zlab = MathTex(r"z", font_size=30, color=BLUE).next_to(zpt, UR, buff=0.1)
        foot = axes.c2p(0.375, -0.375)
        perp = DashedLine(axes.c2p(1.3, 0.55), foot, color=MUTED, stroke_width=2)
        dev = Arrow(axes.c2p(0, 0), foot, color=RED, buff=0)
        devlab = MathTex(r"\text{dev}", font_size=28, color=RED).next_to(dev, DOWN, buff=0.15)
        o酸的 = MathTex(r"O", font_size=26, color=MUTED).next_to(axes.c2p(0, 0), DL, buff=0.1)
        self.play(Create(axes), Create(ln), run_time=0.6)
        self.play(FadeIn(zpt), FadeIn(zlab), run_time=0.4)
        self.play(Create(perp), Create(dev), FadeIn(devlab), FadeIn(o酸的), run_time=0.7)
        # 右侧文字
        r1 = self.zh("偏差向量 = z 在直线上的投影", font_size=32, color=INK)
        r2 = self.mixed(
            ("text", "直线的维数 1 = n-1：", GREEN),
            ("math", r"\text{dev}\perp\mathbf{1}", GREEN),
            ("text", " 永远成立", GREEN),
             text_size=32, math_size=42)
        r3 = self.zh("Σ(偏差)² = 投影长度的平方 —— 1 的个数由此而来",
                     font_size=32, color=ORANGE, weight=BOLD)
        right = VGroup(r1, r2, r3).arrange(DOWN, buff=0.55, aligned_edge=LEFT)
        right.next_to(axes, RIGHT, buff=0.9)
        self.play(Write(r1), run_time=0.7)
        self.play(Write(r2), run_time=0.8)
        self.play(Write(r3), run_time=0.7)
        self.wait(2.7)
        self.clear_scene()


    # ---------- 20.5 对照手稿 ----------
    def manuscript(self):
        bar = self.title_bar("对照手稿：这次证明补在哪里", color=GREEN)
        self.play(Write(bar), run_time=0.7)
        m1 = self.zh("一、A = B + E 的分解、J 的特征值 —— 手稿正确", font_size=38, color=GREEN)
        m2 = self.zh("二、E 的特征值全为 1 —— 手稿正确", font_size=38, color=GREEN)
        m3 = self.zh("三、特征值直接相加 —— 手稿跳步，补：可同时对角化", font_size=38, color=RED)
        m4 = self.zh("四、迹检验 tr(A) = n-1 —— 双保险，证明完整", font_size=38, color=GREEN)
        content = self.layout_below(bar, m1, m2, m3, m4)
        for line in [m1, m2, m3, m4]:
            self.play(Write(line), run_time=0.85)
            self.wait(0.5)
        self.wait(2.7)
        self.clear_scene()

    # ---------- 21. 正交对角化 A ----------
    def diag_a(self):
        bar = self.title_bar("第四步：正交对角化", color=ORANGE)
        self.play(Write(bar), run_time=0.7)
        l1 = self.mixed(("text", "A 实对称 ⟹ 存在正交矩阵 ", INK),
                        ("math", r"Q", YELLOW),
                        ("text", "：", INK), text_size=36, math_size=44)
        l2 = self.mt(r"Q^{\mathsf{T}}AQ=\Lambda=\mathrm{diag}\big(\underbrace{1,\cdots,1}_{n-1},\ 0\big)",
                     font_size=50, color=YELLOW)
        l3 = self.zh("（Q 的列 = A 的单位正交特征向量）", font_size=30, color=MUTED)
        content = self.layout_below(bar, l1, l2, l3)
        self.write_formula(l1, run_time=0.8)
        self.write_formula(l2, run_time=1.2)
        self.write_text(l3)
        self.wait(1.6)
        self.clear_scene()

    # ---------- 22. 换元 ----------
    def substitute(self):
        bar = self.title_bar("第五步：正交换元", color=ORANGE, math_part=r"Z=QY")
        self.play(Write(bar), run_time=0.7)
        l1 = self.mt(r"Z^{\mathsf{T}}AZ=(QY)^{\mathsf{T}}A(QY)=Y^{\mathsf{T}}\Lambda Y=\sum_{i=1}^{n-1}y_i^2",
                     font_size=46, color=GREEN)
        l2 = self.zh("n 个平方只剩 n-1 个 —— 最后那个平方被特征值 0 抹掉了",
                     font_size=34, color=INK)
        l3 = self.mixed(("text", "自由度 = ", RED),
                        ("math", r"1", RED),
                        ("text", " 的个数 = ", RED),
                        ("math", r"n-1", RED),
                        ("text", "，与偏差的约束完美呼应！", RED),
                         text_size=34, math_size=46)
        content = self.layout_below(bar, l1, l2, l3)
        self.write_formula(l1, run_time=1.2)
        self.write_text(l2)
        self.write_formula(l3, run_time=1.0)
        self.wait(1.6)
        self.clear_scene()

    # ---------- 23. y 的分布 ----------
    def y_normal(self):
        bar = self.title_bar("最后一块拼图：y 还是标准正态吗", color=ORANGE)
        self.play(Write(bar), run_time=0.7)
        l1 = self.mixed(("text", "密度只依赖 ", INK),
                        ("math", r"\|z\|", YELLOW),
                        ("text", "，而正交变换保长度：", INK),
                        ("math", r"\|Qy\|=\|y\|", YELLOW),
                         text_size=36, math_size=46)
        l2 = self.mt(r"f_Y(y)=f_Z(Qy)=\frac{1}{(2\pi)^{n/2}}e^{-\|y\|^2/2}",
                     font_size=46, color=GREEN)
        l3 = self.mixed(("text", "⟹ ", INK),
                        ("math", r"Y=Q^{\mathsf{T}}Z\sim N(0,I)", GREEN),
                        ("text", "：各分量仍是独立标准正态", INK),
                         text_size=36, math_size=46)
        l4 = self.zh("（各向同性云随便转 —— 就是刚才那页动画）",
                     font_size=30, color=MUTED)
        content = self.layout_below(bar, l1, l2, l3, l4)
        self.write_formula(l1, run_time=0.9)
        self.write_formula(l2, run_time=1.1)
        self.write_formula(l3, run_time=1.0)
        self.write_text(l4)
        self.wait(1.6)
        self.clear_scene()

    # ---------- 24. 大结局 ----------
    def finale(self):
        bar = self.title_bar("大结局：完整链路", color=GREEN)
        self.play(Write(bar), run_time=0.7)
        c1 = self.mixed(("text", "① 标准化：", BLUE),
                        ("math", r"\frac{\sum(X_i-\bar{X})^2}{\sigma^2}=\sum(Z_i-\bar{Z})^2", BLUE),
                         text_size=34, math_size=42)
        c2 = self.mixed(("text", "② 二次型：", VIOLET),
                        ("math", r"=z^{\mathsf{T}}(I-\tfrac{1}{n}J)z", VIOLET),
                         text_size=34, math_size=42)
        c3 = self.mixed(("text", "③ 正交对角化：", ORANGE),
                        ("math", r"=y_1^2+\cdots+y_{n-1}^2", ORANGE),
                         text_size=34, math_size=42)
        c4 = self.mixed(("text", "④ 独立标准正态平方和：", GREEN),
                        ("math", r"\sim\chi^2(n-1)", GREEN),
                         text_size=34, math_size=46)
        final = self.mt(r"\sum_{i=1}^{n}\frac{(X_i-\bar{X})^2}{\sigma^2}=\frac{(n-1)S^2}{\sigma^2}\sim\chi^2(n-1)",
                        font_size=50, color=YELLOW)
        final.move_to(DOWN * 3.35)
        content = self.layout_below(bar, c1, c2, c3, c4, buff=0.55)
        for line in [c1, c2, c3, c4]:
            self.write_formula(line, run_time=0.85)
        self.play(Write(final), run_time=1.2)
        box = SurroundingRectangle(final, color=YELLOW, buff=0.18)
        self.play(Create(box), run_time=0.6)
        qed = self.mt(r"\blacksquare", font_size=44, color=GREEN)
        qed.next_to(box, RIGHT, buff=0.3)
        self.play(FadeIn(qed), run_time=0.3)
        self.wait(4.2)
        self.clear_scene()

    # ---------- 25. 总结与彩蛋 ----------
    def summary(self):
        bar = self.title_bar("回顾与彩蛋", color=GREEN)
        self.play(Write(bar), run_time=0.7)
        s1 = self.zh("自由度：约束吃掉一个，平方和就少一项", font_size=38, color=INK)
        s2 = self.mixed(("text", "工具链：", INK),
                        ("math", r"\text{standardize}\to\text{quadratic form}\to\text{orthogonal diag.}", YELLOW),
                         text_size=34, math_size=40)
        s3 = self.mixed(("text", "彩蛋：同款套路立刻得到 ", INK),
                        ("math", r"\bar{X}\ \perp\ S^2", RED),
                        ("text", "（样本均值与样本方差独立）", INK),
                         text_size=34, math_size=44)
        s4 = self.mixed(("text", "而 ", INK),
                        ("math", r"\frac{\bar{X}-\mu}{S/\sqrt{n}}\sim t(n-1)", BLUE),
                        ("text", "、F 分布，全都站在这块基石上", INK),
                         text_size=34, math_size=44)
        content = self.layout_below(bar, s1, s2, s3, s4)
        for line in [s1, s2, s3, s4]:
            self.play(Write(line), run_time=0.85)
            self.wait(0.4)
        self.wait(3.3)
        self.clear_scene()

    # ---------- 26. 结尾 ----------
    def ending(self):
        t = Text("点赞 · 收藏 · 关注", font=ZH_FONT, font_size=64, weight=BOLD)
        t.set_color_by_gradient("#FFD166", "#F59E62")
        t.move_to(UP * 0.8)
        s = self.zh("统计学的地基，就是这样一砖一瓦垒起来的", font_size=36, color=INK)
        s.next_to(t, DOWN, buff=0.7)
        self.play(Write(t), run_time=0.9)
        self.play(FadeIn(s, shift=UP * 0.3), run_time=0.6)
        self.wait(2.2)
