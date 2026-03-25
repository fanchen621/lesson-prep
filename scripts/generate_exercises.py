#!/usr/bin/env python3
"""
generate_exercises.py - A4双面打印优化练习题PDF生成器
紧凑个人信息栏、无分数、从江西智慧教育平台等来源整合题目
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
    """A4练习题PDF - 双面打印优化"""

    def __init__(self, info: dict):
        super().__init__('P', 'mm', 'A4')
        self.info = info
        self.set_auto_page_break(True, margin=18)
        self.add_font('zh', '', FONT_REG)
        self.add_font('zh', 'B', FONT_BOLD if os.path.exists(FONT_BOLD) else FONT_REG)
        self.page_num = 0
        self.q_sub = 0

    def header(self):
        self.page_num += 1
        if self.page_num == 1:
            return  # 首页有自己的标题
        self.set_font('zh', '', 7)
        self.set_text_color(180, 180, 180)
        h = f"{self.info.get('subject','')}·{self.info.get('topic','')}·练习题"
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

        # 标题
        self.set_font('zh', 'B', 18)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, f'{grade}年级{semester} {subject} 练习题', align='C', new_x='LMARGIN', new_y='NEXT')

        self.set_font('zh', '', 11)
        self.set_text_color(100, 100, 100)
        self.cell(0, 6, f'《{topic}》', align='C', new_x='LMARGIN', new_y='NEXT')
        self.ln(4)

        # 紧凑个人信息栏 - 仅2行，无分数
        self.set_draw_color(0, 0, 0)
        self.set_text_color(0, 0, 0)
        self.set_font('zh', '', 10)

        y = self.get_y()
        # 第一行：姓名  班级  日期
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

    def section_title(self, title: str, count: str = ''):
        """大题标题 - 简洁版"""
        if self.get_y() > 262:
            self.add_page()
        self.ln(2)
        self.set_font('zh', 'B', 12)
        self.set_fill_color(245, 245, 245)
        label = f'  {title}'
        if count:
            label += f'（共{count}）'
        self.cell(0, 7, label, fill=True, new_x='LMARGIN', new_y='NEXT')
        self.ln(3)
        self.q_sub = 0

    def fill_blank(self, content: str):
        """填空题"""
        if self.get_y() > 268:
            self.add_page()
        self.q_sub += 1
        self.set_font('zh', '', 11)
        text = f'{self.q_sub}. {content.replace("___", "________")}'
        self.multi_cell(175, 6.5, text, new_x='LMARGIN', new_y='NEXT')
        self.ln(2)

    def choice(self, content: str, options: list):
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

    def true_false(self, content: str):
        """判断题"""
        if self.get_y() > 268:
            self.add_page()
        self.q_sub += 1
        self.set_font('zh', '', 11)
        self.multi_cell(175, 6.5, f'{self.q_sub}. {content}    （    ）', new_x='LMARGIN', new_y='NEXT')
        self.ln(2)

    def answer_q(self, content: str, lines: int = 5):
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

    def calc_q(self, content: str, lines: int = 8):
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

    def reading_comprehension(self, passage: str, questions: list):
        """阅读理解题"""
        if self.get_y() > 220:
            self.add_page()

        self.set_font('zh', 'B', 11)
        self.cell(0, 7, '阅读短文，完成练习。', new_x='LMARGIN', new_y='NEXT')
        self.ln(2)

        # 短文内容
        self.set_font('zh', '', 11)
        self.multi_cell(175, 6.5, passage, new_x='LMARGIN', new_y='NEXT')
        self.ln(3)

        # 短文后的题目
        for q in questions:
            q_type = q.get('type', 'answer')
            q_content = q.get('content', '')
            if q_type == 'fill_blank':
                self.fill_blank(q_content)
            elif q_type == 'choice':
                self.choice(q_content, q.get('options', []))
            elif q_type == 'true_false':
                self.true_false(q_content)
            else:
                lines = q.get('lines', 5)
                self.answer_q(q_content, lines)

    def add_answer_section(self, answers: dict):
        """答案页 - 双面打印对齐"""
        # 如果当前是奇数页，插入空白页
        if self.pages_count % 2 == 1:
            self.add_page()

        self.add_page()
        self.ln(3)
        self.set_font('zh', 'B', 16)
        self.set_text_color(0, 0, 0)
        self.cell(0, 10, '参 考 答 案', align='C', new_x='LMARGIN', new_y='NEXT')
        self.set_draw_color(150, 150, 150)
        self.line(60, self.get_y(), 150, self.get_y())
        self.ln(5)

        for section_title, section_answers in answers.items():
            if self.get_y() > 260:
                self.add_page()
            self.set_font('zh', 'B', 10)
            self.cell(0, 6, section_title, new_x='LMARGIN', new_y='NEXT')
            self.ln(1)

            self.set_font('zh', '', 10)
            if isinstance(section_answers, list):
                for i, ans in enumerate(section_answers):
                    if self.get_y() > 270:
                        self.add_page()
                    if isinstance(ans, dict):
                        ans_text = f'{i+1}. {ans.get("answer","")}'
                        if ans.get('explanation'):
                            ans_text += f'  ▸{ans["explanation"]}'
                    else:
                        ans_text = f'{i+1}. {ans}'
                    self.multi_cell(175, 5.5, ans_text, new_x='LMARGIN', new_y='NEXT')
                    self.ln(0.5)
            elif isinstance(section_answers, str):
                self.multi_cell(175, 5.5, section_answers, new_x='LMARGIN', new_y='NEXT')
            self.ln(3)


def generate_exercise_pdf(data: dict, output_path: str):
    """生成练习题PDF"""
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
        for sec in sections:
            title = sec.get('title', '')
            count = sec.get('count', '')
            sec_type = sec.get('type', '')
            questions = sec.get('questions', [])

            pdf.section_title(title, count)

            for q in questions:
                q_type = q.get('type', sec_type)
                q_content = q.get('content', '')

                if q_type == 'choice':
                    pdf.choice(q_content, q.get('options', []))
                elif q_type == 'true_false':
                    pdf.true_false(q_content)
                elif q_type == 'fill_blank':
                    pdf.fill_blank(q_content)
                elif q_type == 'answer':
                    pdf.answer_q(q_content, q.get('lines', 5))
                elif q_type == 'calc':
                    pdf.calc_q(q_content, q.get('lines', 8))
                elif q_type == 'reading':
                    pdf.reading_comprehension(q.get('passage', ''), q.get('questions', []))
                else:
                    pdf.answer_q(q_content, q.get('lines', 5))
    else:
        # 空模板
        pdf.section_title('一、填空题', '10题')
        for _ in range(5):
            pdf.fill_blank('（题目内容待填写）_______________')

        pdf.section_title('二、选择题', '5题')
        for _ in range(3):
            pdf.choice('（题目内容待填写）', ['A选项', 'B选项', 'C选项', 'D选项'])

        pdf.section_title('三、解答题', '4题')
        for _ in range(3):
            pdf.answer_q('（题目内容待填写）', 5)

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
