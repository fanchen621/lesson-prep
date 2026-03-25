#!/usr/bin/env python3
"""
generate_exercises.py - A4双面打印优化分层练习题PDF生成器 v3.0
严格三级分层（基础50-60% / 提高25-35% / 拓展5-15%）
紧凑个人信息栏、无分数、全知识点覆盖
用法: python3 generate_exercises.py <json_file> [output_path]
"""
import json, sys, os
from fpdf import FPDF

FONT_DIR = '/usr/share/fonts'
FONT_REG = os.path.join(FONT_DIR, 'truetype/wqy/wqy-microhei.ttc')
FONT_BOLD = os.path.join(FONT_DIR, 'opentype/noto/NotoSansCJK-Bold.ttc')
if not os.path.exists(FONT_REG):
    FONT_REG = os.path.join(FONT_DIR, 'opentype/noto/NotoSansCJK-Regular.ttc')


class ExercisePDF(FPDF):
    """A4分层练习题PDF - 双面打印优化"""

    def __init__(self, info: dict):
        super().__init__('P', 'mm', 'A4')
        self.info = info
        self.set_auto_page_break(True, margin=18)
        self.add_font('zh', '', FONT_REG)
        self.add_font('zh', 'B', FONT_BOLD if os.path.exists(FONT_BOLD) else FONT_REG)
        self.page_num = 0
        self.q_sub = 0
        self.difficulty_tier = ''  # 当前难度层级标记

    def header(self):
        self.page_num += 1
        if self.page_num == 1:
            return
        self.set_font('zh', '', 7)
        self.set_text_color(180, 180, 180)
        h = f"{self.info.get('subject','')}·{self.info.get('topic','')}·分层练习题"
        self.cell(0, 5, h, align='C', new_x='LMARGIN', new_y='NEXT')
        self.set_draw_color(200, 200, 200)
        self.line(15, 8, 195, 8)
        self.ln(2)

    def footer(self):
        self.set_y(-12)
        self.set_font('zh', '', 7)
        self.set_text_color(180, 180, 180)
        pg = f'{self.page_num}'
        self.cell(0, 5, f'第 {pg} 页 · 请保持卷面整洁', align='C')

    def add_title_page(self):
        """紧凑首页 - 个人信息仅占2行"""
        self.add_page()
        self.ln(8)

        grade = self.info.get('grade', '')
        semester = self.info.get('semester', '')
        subject = self.info.get('subject', '')
        topic = self.info.get('topic', '')
        edition = self.info.get('edition', '人教版')

        # 标题
        self.set_font('zh', 'B', 18)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, f'{grade}年级{semester} {subject} 分层练习题', align='C', new_x='LMARGIN', new_y='NEXT')

        self.set_font('zh', '', 11)
        self.set_text_color(100, 100, 100)
        self.cell(0, 6, f'《{topic}》· {edition}', align='C', new_x='LMARGIN', new_y='NEXT')

        # 分层说明
        self.ln(2)
        self.set_font('zh', '', 9)
        self.set_text_color(120, 120, 120)
        self.cell(0, 5, '★ 基础题（必做）  ★★ 提高题（选做）  ★★★ 拓展题（挑战）',
                  align='C', new_x='LMARGIN', new_y='NEXT')
        self.ln(4)

        # 紧凑个人信息栏 - 仅2行，无分数
        self.set_draw_color(0, 0, 0)
        self.set_text_color(0, 0, 0)
        self.set_font('zh', '', 10)

        y = self.get_y()
        labels1 = ['姓名', '班级', '日期']
        x_starts = [15, 75, 135]
        widths = [55, 55, 55]
        row_h = 7

        for i, label in enumerate(labels1):
            self.rect(x_starts[i], y, widths[i], row_h)
            self.set_xy(x_starts[i] + 1, y + 1)
            self.cell(12, 5, label)
            self.line(x_starts[i] + 13, y + 5, x_starts[i] + widths[i] - 2, y + 5)

        self.set_y(y + row_h + 6)

        # 分隔线
        self.set_draw_color(150, 150, 150)
        self.line(15, self.get_y(), 195, self.get_y())
        self.ln(4)

        self.set_text_color(0, 0, 0)

    def section_title(self, title: str, count: str = '', tier: str = ''):
        """大题标题 - 含难度层级标记"""
        if self.get_y() > 262:
            self.add_page()
        self.ln(2)

        # 难度层级标记
        tier_colors = {
            '基础': (46, 139, 87),    # 绿色
            '提高': (230, 126, 34),    # 橙色
            '拓展': (180, 0, 0),       # 红色
        }

        self.set_font('zh', 'B', 12)
        label = f'  {title}'
        if count:
            label += f'（共{count}）'

        # 如果有层级标记，用颜色区分
        if tier in tier_colors:
            r, g, b = tier_colors[tier]
            self.set_fill_color(r, g, b)
            self.set_text_color(255, 255, 255)
            self.cell(0, 7, label, fill=True, new_x='LMARGIN', new_y='NEXT')
            self.set_text_color(0, 0, 0)
        else:
            self.set_fill_color(245, 245, 245)
            self.cell(0, 7, label, fill=True, new_x='LMARGIN', new_y='NEXT')

        self.ln(3)
        self.q_sub = 0

    def fill_blank(self, content: str, difficulty: str = '基础'):
        """填空题"""
        if self.get_y() > 268:
            self.add_page()
        self.q_sub += 1

        # 难度标记
        diff_mark = {'基础': '★', '提高': '★★', '拓展': '★★★'}
        mark = diff_mark.get(difficulty, '')

        self.set_font('zh', '', 11)
        text = f'{self.q_sub}. {content.replace("___", "________")}'
        if mark:
            self.set_font('zh', '', 8)
            self.set_text_color(150, 150, 150)
            # 不在题目旁显示星级（避免学生分心），通过大题标题区分
            self.set_text_color(0, 0, 0)
            self.set_font('zh', '', 11)
        self.multi_cell(175, 6.5, text, new_x='LMARGIN', new_y='NEXT')
        self.ln(2)

    def choice(self, content: str, options: list, difficulty: str = '基础'):
        """选择题"""
        if self.get_y() > 258:
            self.add_page()
        self.q_sub += 1
        self.set_font('zh', '', 11)

        self.multi_cell(175, 6.5, f'{self.q_sub}. {content}', new_x='LMARGIN', new_y='NEXT')

        labels = 'ABCDEFGH'
        self.set_x(20)
        for i, opt in enumerate(options):
            if i >= len(labels):
                break
            txt = f'{labels[i]}. {opt}   '
            w = self.get_string_width(txt) + 4
            if self.get_x() + w > 190:
                self.ln(6)
                self.set_x(20)
            self.cell(w, 6, txt)
        self.ln(8)

    def true_false(self, content: str, difficulty: str = '基础'):
        """判断题"""
        if self.get_y() > 268:
            self.add_page()
        self.q_sub += 1
        self.set_font('zh', '', 11)
        self.multi_cell(175, 6.5, f'{self.q_sub}. {content}    （    ）', new_x='LMARGIN', new_y='NEXT')
        self.ln(2)

    def answer_q(self, content: str, lines: int = 5, difficulty: str = '基础'):
        """解答题 - 带答题横线"""
        if self.get_y() > 245:
            self.add_page()
        self.q_sub += 1
        self.set_font('zh', '', 11)
        self.multi_cell(175, 6.5, f'{self.q_sub}. {content}', new_x='LMARGIN', new_y='NEXT')
        self.ln(1)
        y = self.get_y()
        for i in range(lines):
            line_y = y + i * 7
            if line_y > 275:
                break
            self.set_draw_color(200, 200, 200)
            self.line(20, line_y, 190, line_y)
        self.set_draw_color(0, 0, 0)
        self.set_y(y + lines * 7 + 3)

    def calc_q(self, content: str, lines: int = 8, difficulty: str = '基础'):
        """计算题 - 大面积答题区"""
        if self.get_y() > 230:
            self.add_page()
        self.q_sub += 1
        self.set_font('zh', '', 11)
        self.multi_cell(175, 6.5, f'{self.q_sub}. {content}', new_x='LMARGIN', new_y='NEXT')
        self.ln(1)
        y = self.get_y()
        for i in range(lines):
            line_y = y + i * 7
            if line_y > 275:
                self.add_page()
                y = self.get_y()
            self.set_draw_color(200, 200, 200)
            self.line(20, y + i * 7, 190, y + i * 7)
        self.set_draw_color(0, 0, 0)
        self.set_y(y + lines * 7 + 3)

    def reading_comprehension(self, passage: str, questions: list, difficulty: str = '基础'):
        """阅读理解题"""
        if self.get_y() > 220:
            self.add_page()

        self.set_font('zh', 'B', 11)
        self.cell(0, 7, '阅读短文，完成练习。', new_x='LMARGIN', new_y='NEXT')
        self.ln(2)

        self.set_font('zh', '', 11)
        self.multi_cell(175, 6.5, passage, new_x='LMARGIN', new_y='NEXT')
        self.ln(3)

        for q in questions:
            q_type = q.get('type', 'answer')
            q_content = q.get('content', '')
            q_diff = q.get('difficulty', difficulty)
            if q_type == 'fill_blank':
                self.fill_blank(q_content, q_diff)
            elif q_type == 'choice':
                self.choice(q_content, q.get('options', []), q_diff)
            elif q_type == 'true_false':
                self.true_false(q_content, q_diff)
            else:
                lines = q.get('lines', 5)
                self.answer_q(q_content, lines, q_diff)

    def add_difficulty_divider(self, from_tier: str, to_tier: str):
        """难度层级分隔线"""
        if self.get_y() > 260:
            self.add_page()
        self.ln(3)
        self.set_draw_color(150, 150, 150)
        self.set_font('zh', '', 9)
        self.set_text_color(150, 150, 150)
        y = self.get_y()
        self.line(15, y, 80, y)
        self.set_xy(82, y - 3)
        self.cell(30, 6, f'↑ {from_tier}  ↓ {to_tier}', align='C')
        self.line(115, y, 195, y)
        self.set_y(y + 6)
        self.set_text_color(0, 0, 0)

    def add_answer_section(self, answers: dict):
        """答案页 - 含详细解析"""
        # 如果当前是奇数页，插入空白页确保双面打印对齐
        if self.pages_count % 2 == 1:
            self.add_page()

        self.add_page()
        self.ln(3)
        self.set_font('zh', 'B', 16)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, '参 考 答 案 与 解 析', align='C', new_x='LMARGIN', new_y='NEXT')
        self.set_draw_color(150, 150, 150)
        self.line(55, self.get_y(), 155, self.get_y())
        self.ln(5)

        for section_title, section_answers in answers.items():
            if self.get_y() > 260:
                self.add_page()
            self.set_font('zh', 'B', 10)
            self.set_text_color(0, 51, 102)
            self.cell(0, 6, section_title, new_x='LMARGIN', new_y='NEXT')
            self.set_text_color(0, 0, 0)
            self.ln(1)

            self.set_font('zh', '', 10)
            if isinstance(section_answers, list):
                for i, ans in enumerate(section_answers):
                    if self.get_y() > 270:
                        self.add_page()
                    if isinstance(ans, dict):
                        ans_text = f'{i+1}. {ans.get("answer","")}'
                        if ans.get('explanation'):
                            ans_text += f'  →解析：{ans["explanation"]}'
                        if ans.get('error_tip'):
                            ans_text += f'  易错：易错提醒：{ans["error_tip"]}'
                    else:
                        ans_text = f'{i+1}. {ans}'
                    self.multi_cell(175, 5.5, ans_text, new_x='LMARGIN', new_y='NEXT')
                    self.ln(0.5)
            elif isinstance(section_answers, str):
                self.multi_cell(175, 5.5, section_answers, new_x='LMARGIN', new_y='NEXT')
            self.ln(3)


def generate_exercise_pdf(data: dict, output_path: str):
    """生成分层练习题PDF"""
    info = {
        'grade': data.get('grade', ''),
        'semester': data.get('semester', ''),
        'subject': data.get('subject', ''),
        'edition': data.get('edition', '人教版'),
        'topic': data.get('topic', ''),
    }

    pdf = ExercisePDF(info)
    pdf.add_title_page()

    sections = data.get('exercise_sections', [])
    if sections:
        current_tier = ''
        for sec in sections:
            title = sec.get('title', '')
            count = sec.get('count', '')
            sec_type = sec.get('type', '')
            tier = sec.get('tier', '')  # 基础/提高/拓展
            questions = sec.get('questions', [])

            # 如果难度层级变化，添加分隔线
            if tier and tier != current_tier and current_tier:
                pdf.add_difficulty_divider(current_tier, tier)
            current_tier = tier or current_tier

            pdf.section_title(title, count, tier)

            for q in questions:
                q_type = q.get('type', sec_type)
                q_content = q.get('content', '')
                q_diff = q.get('difficulty', tier or '基础')

                if q_type == 'choice':
                    pdf.choice(q_content, q.get('options', []), q_diff)
                elif q_type == 'true_false':
                    pdf.true_false(q_content, q_diff)
                elif q_type == 'fill_blank':
                    pdf.fill_blank(q_content, q_diff)
                elif q_type == 'answer':
                    pdf.answer_q(q_content, q.get('lines', 5), q_diff)
                elif q_type == 'calc':
                    pdf.calc_q(q_content, q.get('lines', 8), q_diff)
                elif q_type == 'reading':
                    pdf.reading_comprehension(q.get('passage', ''), q.get('questions', []), q_diff)
                else:
                    pdf.answer_q(q_content, q.get('lines', 5), q_diff)
    else:
        # 三级分层默认模板
        # ★ 基础题（50-60%）
        pdf.section_title('一、填空题', '10题', '基础')
        for _ in range(5):
            pdf.fill_blank('（基础题·题目内容待填写）_______________', '基础')

        pdf.section_title('二、选择题', '5题', '基础')
        for _ in range(3):
            pdf.choice('（基础题·题目内容待填写）', ['A选项', 'B选项', 'C选项', 'D选项'], '基础')

        # ★★ 提高题（25-35%）
        pdf.section_title('三、判断题', '5题', '提高')
        for _ in range(3):
            pdf.true_false('（提高题·题目内容待填写）', '提高')

        pdf.section_title('四、解答题', '4题', '提高')
        for _ in range(3):
            pdf.answer_q('（提高题·题目内容待填写）', 5, '提高')

        # ★★★ 拓展题（5-15%）
        pdf.section_title('五、综合运用', '2题', '拓展')
        for _ in range(2):
            pdf.answer_q('（拓展题·题目内容待填写）', 8, '拓展')

    answers = data.get('answers', {})
    if answers:
        pdf.add_answer_section(answers)

    pdf.output(output_path)
    return output_path


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python3 generate_exercises.py <json_file> [output_path]")
        sys.exit(1)
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        data = json.load(f)
    output = sys.argv[2] if len(sys.argv) > 2 else sys.argv[1].replace('.json', '_练习题.pdf')
    print(f"练习题PDF已生成: {generate_exercise_pdf(data, output)}")
