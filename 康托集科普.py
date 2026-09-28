# -*- coding: utf-8 -*-
"""任务4：康托集科普 —— 测度为 0 却与实数「一样多」
要点：
  构造：逐次挖去中间三分之一
  测度：去掉总长 = 1/3·Σ(2/3)^n = 1  ⇒  勒贝格测度 0
  基数：三进制仅含 0/2 的数 ↔ 二进制 ⇒ 与 [0,1] 等势（连续统）
  维数：ln2/ln3 ≈ 0.6309
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from skill_base import *


class CantorSet(SkillScene):

    def construct(self):
        self.camera.background_color = BG
        self.opening()
        self.construction_page()
        self.measure_page()
        self.limit_history_page()
        self.cardinality_ternary()
        self.cardinality_bijection()
        self.endpoints_page()
        self.paradox_summary()
        self.quadrant_page()
        self.fractal_dim_page()
        self.more_results_page()
        self.ending()

    # ───────────── S0 开场 ─────────────
    def opening(self):
        title = self.zh("康托集", font_size=66, weight=BOLD)
        title.to_edge(UP, buff=0.55)
        sub = self.mixed(
            ("text", "长度为零，却有和整条实数轴一样多的点 —— 数学中最安静的悖论", YELLOW),
            text_size=36, math_size=40)
        sub.next_to(title, DOWN, buff=0.3)
        self.play(Write(title), run_time=1.0)
        self.play(FadeIn(sub), run_time=0.8)

        # 逐步构造动画预览
        y = -1.0
        seg = Line([-6.4, y, 0], [6.4, y, 0], color=INK, stroke_width=7)
        self.play(Create(seg), run_time=0.8)
        cur = [(-6.4, 6.4)]
        cols = [BLUE, GREEN, ORANGE, RED, VIOLET]
        for it in range(5):
            nxt = []
            for a, b in cur:
                w = (b - a) / 3
                nxt += [(a, a + w), (b - w, b)]
            col = cols[it]
            segs = VGroup(*[Line([a, y - 0.55 * (it + 1), 0], [b, y - 0.55 * (it + 1), 0],
                                 color=col, stroke_width=6) for a, b in nxt])
            self.play(Create(segs), run_time=0.6)
            cur = nxt
        cap = self.zh("无穷次挖去之后，还剩下什么？", font_size=32, color=MUTED)
        cap.to_edge(DOWN, buff=0.45)
        self.play(FadeIn(cap), run_time=0.8)
        self.wait(2.2)
        self.clear_scene()

    # ───────────── S1 构造全过程 ─────────────
    def construction_page(self):
        bar = self.title_bar("构造：每次挖去每段的中间三分之一")
        self.play(Write(bar), run_time=0.8)

        L, R = -7.0, 7.0
        y0 = 2.35
        seg0 = Line([L, y0, 0], [R, y0, 0], color=INK, stroke_width=8)
        lab0 = self.mixed(("math", r"C_0=[0,\,1]", INK), text_size=28, math_size=34)
        lab0.move_to([L + 0.05, y0 + 0.36, 0], aligned_edge=LEFT)
        self.play(Create(seg0), FadeIn(lab0), run_time=0.9)

        cur = [(0.0, 1.0)]
        cols = [BLUE, GREEN, ORANGE, RED, VIOLET, TEAL]
        prev_segs = VGroup(seg0)
        y = y0
        for it in range(6):
            nxt = []
            for a, b in cur:
                w = (b - a) / 3
                nxt += [(a, a + w), (b - w, b)]
            col = cols[it]
            y -= 0.92
            new_segs = VGroup()
            for a, b in nxt:
                s = Line([L + a * (R - L), y, 0], [L + b * (R - L), y, 0],
                         color=col, stroke_width=7)
                new_segs.add(s)
            lbl = self.mixed(("math", r"C_{%d}" % (it + 1), col),
                             ("text", "  剩 ", MUTED),
                             ("math", r"2^{%d}" % (it + 1), col),
                             ("text", " 段，总长 ", MUTED),
                             ("math", r"\left(\tfrac{2}{3}\right)^{%d}" % (it + 1), col),
                             text_size=26, math_size=32)
            lbl.move_to([L + 0.05, y + 0.34, 0], aligned_edge=LEFT)
            self.play(Create(new_segs), FadeIn(lbl), run_time=0.9)
            self.wait(0.8)
            cur = nxt
            prev_segs.add(new_segs)
        note = self.mixed(
            ("text", "挖去的部分永不归还，剩下的点组成康托集 C —— 「体无完肤」却始终非空", MUTED),
            text_size=32, math_size=38)
        note.to_edge(DOWN, buff=0.3)
        self.play(FadeIn(note), run_time=0.8)
        self.wait(2.2)
        self.clear_scene()

    # ───────────── S2 测度为 0 ─────────────
    def measure_page(self):
        bar = self.title_bar("性质一 · 长度去哪儿了？（勒贝格测度 0）", color=RED)
        self.play(Write(bar), run_time=0.8)
        l1 = self.mixed(
            ("text", "第 n 步挖去 ", INK),
            ("math", r"2^{\,n-1}", INK),
            ("text", " 段，每段长 ", INK),
            ("math", r"3^{-n}", INK),
            ("text", "，故第 n 步共挖去 ", INK),
            ("math", r"\left(\tfrac{2}{3}\right)^{n-1}\cdot\tfrac{1}{3}", RED),
            text_size=34, math_size=42)
        l2 = self.mixed(
            ("text", "挖去的总长度：", INK),
            ("math", r"\sum_{n=1}^{\infty}\frac{1}{3}\left(\frac{2}{3}\right)^{n-1}=\frac{1/3}{1-2/3}=1", YELLOW),
            text_size=36, math_size=46)
        l3 = self.mixed(
            ("text", "从总长 1 的区间里恰好挖掉了 1 ⇒ 康托集的勒贝格测度为 ", INK),
            ("math", r"m(C)=0", RED),
            text_size=36, math_size=44)
        l4 = self.mixed(
            ("text", "通俗版：随机往 [0,1] 扔一个点，扎中 C 的概率是 0 —— 它「几乎没有」任何长度", MUTED),
            text_size=32, math_size=38)
        content = self.layout_below(bar, l1, l2, l3, l4)
        for line in (l1, l2, l3, l4):
            self.write_formula(line, run_time=1.1)
        self.wait(2.4)
        self.clear_scene()

    # ───────────── S3 三进制刻画 ─────────────
    def cardinality_ternary(self):
        bar = self.title_bar("性质二 · 给剩点登记户口：三进制", color=BLUE)
        self.play(Write(bar), run_time=0.8)
        l1 = self.mixed(
            ("text", "三进制里，「挖中三分之一」意味着该位发生进位：", INK),
            ("math", r"0.1_3=0.0222\cdots_3", MUTED),
            text_size=34, math_size=42)
        l2 = self.mixed(
            ("text", "于是：", INK),
            ("math", r"x\in C", GREEN),
            ("text", " 当且仅当 x 存在一个", INK),
            ("text", "只用数字 0 和 2", GREEN),
            ("text", " 的三进制展开", INK),
            text_size=34, math_size=42)
        l3 = self.mixed(
            ("math", r"x=0.\varepsilon_1\varepsilon_2\varepsilon_3\cdots_3,\quad \varepsilon_k\in\{0,\,2\}", YELLOW),
            text_size=36, math_size=46)
        l4 = self.mixed(
            ("text", "例子：", INK),
            ("math", r"\tfrac{1}{3}=0.1_3=0.0222\cdots_3\in C", GREEN),
            ("text", "（端点全部幸存）", MUTED),
            text_size=34, math_size=42)
        content = self.layout_below(bar, l1, l2, l3, l4)
        for line in (l1, l2, l3, l4):
            self.write_formula(line, run_time=1.1)
        self.wait(2.4)
        self.clear_scene()

    # ───────────── S4 双射：与 [0,1] 等势 ─────────────
    def cardinality_bijection(self):
        bar = self.title_bar("性质三 · 点数竟与整段实数一样多", color=GREEN)
        self.play(Write(bar), run_time=0.8)
        l1 = self.mixed(
            ("text", "把三进制数字做替换：", INK),
            ("math", r"0\mapsto 0,\quad 2\mapsto 1", YELLOW),
            ("text", "，就把 C 的元素读成一个二进制数", INK),
            text_size=34, math_size=42)
        l2 = self.mixed(
            ("math", r"f:\ C\ \longrightarrow\ [0,\,1],\quad 0.\varepsilon_1\varepsilon_2\cdots_3\ \longmapsto\ 0.\eta_1\eta_2\cdots_2", INK),
            text_size=34, math_size=42)
        l3 = self.mixed(
            ("text", "f 是满射（每个二进制展开都有来源），而康托在 1874 年证明这样的对应可做成双射", INK),
            text_size=32, math_size=40)
        l4 = self.mixed(
            ("math", r"\mathrm{card}(C)=\mathrm{card}([0,1])=2^{\aleph_0}", GREEN),
            ("text", " —— 连续统！", YELLOW),
            text_size=40, math_size=48)
        content = self.layout_below(bar, l1, l2, l3, l4)
        for line in (l1, l2, l3, l4):
            self.write_formula(line, run_time=1.15)
        self.wait(2.4)
        self.clear_scene()

    # ───────────── S2.5 极限与历史 ─────────────
    def limit_history_page(self):
        bar = self.title_bar("挖去过程的「极限」是什么？", color=GREEN)
        self.play(Write(bar), run_time=0.8)
        l1 = self.mixed(
            ("text", "康托集是无穷次挖去后剩下的点：", INK),
            ("math", r"C=\bigcap_{n\ge0}C_{n}", YELLOW),
            text_size=36, math_size=44)
        l2 = self.mixed(
            ("text", "每一层 ", INK),
            ("math", r"C_{n}", INK),
            ("text", " 都是有限个闭区间的并，且层层收缩 ⇒ 又见「套」的身影：", INK),
            ("text", "嵌套闭集的交非空", GREEN),
            text_size=34, math_size=40)
        l3 = self.mixed(
            ("text", "C 同时是", INK),
            ("text", "闭集", BLUE),
            ("text", "（含全部极限点）与", INK),
            ("text", "无处稠密集", RED),
            ("text", "（不含任何区间）—— 两种身份并存", INK),
            text_size=34, math_size=40)
        l4 = self.mixed(
            ("text", "历史注脚：康托研究三角级数的唯一性问题时，被迫造出这些怪集合（1874）", MUTED),
            text_size=32, math_size=38)
        content = self.layout_below(bar, l1, l2, l3, l4)
        for line in (l1, l2, l3, l4):
            self.write_formula(line, run_time=1.1)
        self.wait(2.4)
        self.clear_scene()

    # ───────────── S4.5 端点的命运 ─────────────
    def endpoints_page(self):
        bar = self.title_bar("追问 · 谁在康托集里？先看端点", color=ORANGE)
        self.play(Write(bar), run_time=0.8)

        y = 1.6
        seg = Line([-6.6, y, 0], [6.6, y, 0], color=INK, stroke_width=6)
        pts = VGroup()
        for t in (-6.6 + 12 * v for v in (0, 1)):
            pts.add(Dot([t, y, 0], color=RED, radius=0.08))
        self.play(Create(seg), FadeIn(pts), run_time=0.8)
        row1 = self.mixed(
            ("text", "第一层端点 ", MUTED),
            ("math", r"0,\ 1,\ \tfrac{1}{3},\ \tfrac{2}{3}", YELLOW),
            ("text", " —— 三进制里是 0.222…_3、0.2_3 这类「双写」形式，永不被挖去", INK),
            text_size=30, math_size=36)
        row1.next_to(seg, DOWN, buff=0.5)
        self.fit(row1)
        self.play(FadeIn(row1), run_time=1.0)

        y2 = y - 1.35
        cur = [(0.0, 1.0)]
        for _ in range(2):
            nxt = []
            for a, b in cur:
                w = (b - a) / 3
                nxt += [(a, a + w), (b - w, b)]
            cur = nxt
        seg2 = VGroup(*[Line([-6.6 + 12 * a, y2, 0], [-6.6 + 12 * b, y2, 0],
                             color=BLUE, stroke_width=6) for a, b in cur])
        pts2 = VGroup()
        for a, b in cur:
            for t in (a, b):
                pts2.add(Dot([-6.6 + 12 * t, y2, 0], color=RED, radius=0.07))
        self.play(Create(seg2), FadeIn(pts2), run_time=0.9)
        row2 = self.mixed(
            ("text", "第 n 层共有 ", MUTED),
            ("math", r"2\times 2^{n}", YELLOW),
            ("text", " 个端点，全部幸存 —— 但总数仍是", MUTED),
            ("text", "可数的", GREEN),
            text_size=30, math_size=36)
        row2.next_to(seg2, DOWN, buff=0.5)
        self.fit(row2)
        self.play(FadeIn(row2), run_time=1.0)

        row3 = self.mixed(
            ("text", "而 C 是不可数的：", MUTED),
            ("text", "端点只占康托集的「沧海一粟」", RED),
            ("text", "，绝大多数点深藏于层层聚点之中", INK),
            text_size=32, math_size=36)
        row3.to_edge(DOWN, buff=0.55)
        self.fit(row3)
        self.play(FadeIn(row3), run_time=1.0)
        self.wait(2.2)
        self.clear_scene()

    # ───────────── S5 悖论总览表 ─────────────
    def paradox_summary(self):
        bar = self.title_bar("把两个事实放在一起看", color=RED)
        self.play(Write(bar), run_time=0.8)
        # 对比卡片
        card1 = RoundedRectangle(corner_radius=0.25, width=6.6, height=3.3,
                                 color=RED, stroke_width=2.5)
        t1a = self.zh("长度（勒贝格测度）", font_size=36, color=RED, weight=BOLD)
        t1b = self.mixed(("math", r"m(C)=0", RED), text_size=36, math_size=48)
        t1c = self.zh("「几乎处处没有点」", font_size=28, color=MUTED)
        card1.add(VGroup(t1a, t1b, t1c).arrange(DOWN, buff=0.4).move_to(card1))
        card1[1:].move_to(card1.get_center())

        card2 = RoundedRectangle(corner_radius=0.25, width=6.6, height=3.3,
                                 color=GREEN, stroke_width=2.5)
        t2a = self.zh("点的个数（基数）", font_size=36, color=GREEN, weight=BOLD)
        t2b = self.mixed(("math", r"\mathrm{card}(C)=2^{\aleph_0}", GREEN),
                         text_size=36, math_size=44)
        t2c = self.zh("与全体实数一样多", font_size=28, color=MUTED)
        card2.add(VGroup(t2a, t2b, t2c).arrange(DOWN, buff=0.4).move_to(card2))
        card2[1:].move_to(card2.get_center())

        cards = VGroup(card1, card2).arrange(RIGHT, buff=1.1).move_to([0, 0.2, 0])
        self.play(Create(card1), Create(card2), run_time=1.0)
        bottom = self.mixed(
            ("text", "没有长度的集合，却装下了连续统 —— 「多少」与「多长」是两个独立的问题", YELLOW),
            text_size=34, math_size=38)
        bottom.to_edge(DOWN, buff=0.55)
        self.fit(bottom)
        self.play(FadeIn(bottom), run_time=0.9)
        self.wait(2.4)
        self.clear_scene()

    # ───────────── S5.5 测度 × 基数四象限 ─────────────
    def quadrant_page(self):
        bar = self.title_bar("测度 × 基数：一张表看懂「另类」", color=TEAL)
        self.play(Write(bar), run_time=0.8)

        def header(text, color):
            return self.zh(text, font_size=32, color=color, weight=BOLD)

        def cell(sym, desc, col):
            box = RoundedRectangle(corner_radius=0.16, width=4.7, height=1.6,
                                   color=col, stroke_width=2.2)
            txt = VGroup(self.mt(sym, font_size=32, color=INK),
                         self.zh(desc, font_size=23, color=MUTED))
            txt.arrange(DOWN, buff=0.1)
            txt.move_to(box.get_center())
            return VGroup(box, txt)

        corner = Rectangle(width=2.7, height=0.9, stroke_width=0, fill_opacity=0)
        head_row = VGroup(corner, header("可数", YELLOW), header("不可数", YELLOW)
                          ).arrange(RIGHT, buff=0.55)
        row1 = VGroup(header("测度为 0", BLUE),
                      cell(r"\mathbb{Q}\cap[0,1]", "有理数：稠密却零长", INK),
                      cell(r"C", "康托集：本片主角", YELLOW)
                      ).arrange(RIGHT, buff=0.55)
        row2 = VGroup(header("测度 > 0", BLUE),
                      cell(r"\varnothing", "可数集测度必为 0\n此格永远空缺", RED),
                      cell(r"[0,1]", "无理数贡献了全部长度", GREEN)
                      ).arrange(RIGHT, buff=0.55)
        allg = VGroup(head_row, row1, row2).arrange(DOWN, buff=0.55)
        allg.move_to([0, 0.35, 0])
        for m in (head_row[1], head_row[2], row1[0], row2[0],
                  row1[1], row1[2], row2[1], row2[2]):
            self.play(FadeIn(m, scale=0.9), run_time=0.38)
        bottom = self.mixed(
            ("text", "测度与基数互不决定 —— 这正是实变函数论的第一课", YELLOW),
            text_size=34, math_size=38)
        bottom.to_edge(DOWN, buff=0.45)
        self.fit(bottom)
        self.play(FadeIn(bottom), run_time=0.9)
        self.wait(2.4)
        self.clear_scene()

    # ───────────── S6 分形维数 ─────────────
    def fractal_dim_page(self):
        bar = self.title_bar("再进一步 · 它是几维的？", color=VIOLET)
        self.play(Write(bar), run_time=0.8)
        l1 = self.mixed(
            ("text", "每步把线段缩为 1/3、保留 2 份，自相似维数：", INK),
            ("math", r"d=\frac{\ln 2}{\ln 3}\approx 0.6309", YELLOW),
            text_size=36, math_size=46)
        l2 = self.mixed(
            ("text", "介于 0（一个点）与 1（一条线段）之间 —— 一个「尘埃状」的分形维度", INK),
            text_size=34, math_size=40)
        l3 = self.mixed(
            ("text", "C 还是完备集（闭 + 每点都是聚点）：没有孤立点，也不含任何区间", INK),
            text_size=34, math_size=40)
        l4 = self.mixed(
            ("text", "自相似：C = (C/3) ∪ ((C+2)/3)，每个角落都装着缩小版的整个 C", TEAL),
            text_size=34, math_size=40)
        content = self.layout_below(bar, l1, l2, l3, l4)
        for line in (l1, l2, l3, l4):
            self.write_formula(line, run_time=1.05)
        self.wait(2.4)
        self.clear_scene()

    # ───────────── S7 衍生小结论 ─────────────
    def more_results_page(self):
        bar = self.title_bar("衍生小结论与思考", color=BLUE)
        self.play(Write(bar), run_time=0.8)
        l1 = self.mixed(
            ("text", "C + C = [0, 2]：两个零长集合相加，居然填满整个区间！", ORANGE),
            text_size=36, math_size=42)
        l2 = self.mixed(
            ("text", "康托函数（魔鬼阶梯）：连续、单调不减，却在 C 上「平台爬升」导数几乎处处为零", GREEN),
            text_size=34, math_size=40)
        l3 = self.mixed(
            ("text", "思考：把挖去的比例从 1/3 改小（如 1/4），测度就不为 0 了 —— 临界正是 1/3", INK),
            text_size=34, math_size=40)
        l4 = self.mixed(
            ("text", "康托集是实变函数论的「试金石」：反例、测度论、分形几何都从它出发", TEAL),
            text_size=34, math_size=40)
        content = self.layout_below(bar, l1, l2, l3, l4)
        for line in (l1, l2, l3, l4):
            self.write_formula(line, run_time=1.05)
        self.wait(2.4)
        self.clear_scene()

    # ───────────── S8 结尾 ─────────────
    def ending(self):
        t1 = self.zh("康托集：无中生有", font_size=58, weight=BOLD)
        t1.move_to([0, 1.6, 0])
        t2 = self.mixed(
            ("math", r"m(C)=0", RED),
            ("text", "　而　", MUTED),
            ("math", r"\mathrm{card}(C)=2^{\aleph_0}", GREEN),
            text_size=40, math_size=50)
        t2.next_to(t1, DOWN, buff=0.5)
        self.play(Write(t1), run_time=1.0)
        self.play(Write(t2), run_time=1.2)

        # 终极形态：8 层细密康托尘
        y = -1.6
        cur = [(0.0, 1.0)]
        seg = Line([-6.0, y, 0], [6.0, y, 0], color=INK, stroke_width=6)
        self.play(Create(seg), run_time=0.7)
        for it in range(8):
            nxt = []
            for a, b in cur:
                w = (b - a) / 3
                nxt += [(a, a + w), (b - w, b)]
            col = [BLUE, GREEN, ORANGE, RED, VIOLET, TEAL, PINK, YELLOW][it]
            segs = VGroup(*[Line([-6.0 + a * 12, y - 0.42 * (it + 1), 0],
                                 [-6.0 + b * 12, y - 0.42 * (it + 1), 0],
                                 color=col, stroke_width=5) for a, b in nxt])
            self.play(Create(segs), run_time=0.45)
            cur = nxt
        self.wait(3.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
        self.wait(0.3)
