#!/usr/bin/env python3
"""
generate_lesson_plan.py - 专业级教案Word文档生成器
整合人教版《教师教学用书》和昌明师友《教学设计与指导》内容
用法: python3 generate_lesson_plan.py <json_file> [output_path]
"""
import json, sys, os
from docx import Document
from docx.shared import Pt, Cm, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement


def _set_cell_shading(cell, color):
    """设置单元格背景色"""
    shading = OxmlElement('w:shd')
    shading.set(qn('w:fill'), color)
    shading.set(qn('w:val'), 'clear')
    cell._tc.get_or_add_tcPr().append(shading)


def _add_border_para(doc, text, bold=False, size=12, indent=0, align=None, color=None, font_name='宋体'):
    """添加带格式的段落"""
    p = doc.add_paragraph()
    if align:
        p.alignment = align
    if indent:
        p.paragraph_format.left_indent = Cm(indent)
    run = p.add_run(text)
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.name = font_name
    run.element.rPr.rFonts.set(qn('w:eastAsia'), font_name)
    if color:
        run.font.color.rgb = color
    return p


def _add_rich_para(doc, segments, indent=0):
    """添加富文本段落 segments: [(text, bold, size, color, font), ...]"""
    p = doc.add_paragraph()
    if indent:
        p.paragraph_format.left_indent = Cm(indent)
    for seg in segments:
        text = seg[0]
        bold = seg[1] if len(seg) > 1 else False
        size = seg[2] if len(seg) > 2 else 12
        color = seg[3] if len(seg) > 3 else None
        font = seg[4] if len(seg) > 4 else '宋体'
        run = p.add_run(text)
        run.font.size = Pt(size)
        run.font.bold = bold
        run.font.name = font
        run.element.rPr.rFonts.set(qn('w:eastAsia'), font)
        if color:
            run.font.color.rgb = color
    return p


def create_lesson_plan(data: dict, output_path: str):
    """生成专业级教案Word文档"""
    doc = Document()

    # === 页面设置 A4 ===
    section = doc.sections[0]
    section.page_width = Cm(21)
    section.page_height = Cm(29.7)
    section.left_margin = Cm(2.5)
    section.right_margin = Cm(2.5)
    section.top_margin = Cm(2)
    section.bottom_margin = Cm(2)

    # 默认样式
    style = doc.styles['Normal']
    style.font.name = '宋体'
    style.font.size = Pt(12)
    style.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
    style.paragraph_format.line_spacing = 1.5

    grade = data.get('grade', '___')
    semester = data.get('semester', '___')
    subject = data.get('subject', '___')
    edition = data.get('edition', '人教版')
    unit = data.get('unit', '___')
    lesson = data.get('lesson', '')
    topic = data.get('topic', '___')
    unit_name = data.get('unit_name', '')
    textbook_page = data.get('textbook_page', '')

    # ==================== 大标题 ====================
    title = doc.add_heading('', level=0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run(f'教    案')
    run.font.size = Pt(26)
    run.font.bold = True
    run.font.name = '黑体'
    run.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')

    _add_border_para(doc, f'—— {grade}年级{semester} {subject} {edition}', size=14, align=WD_ALIGN_PARAGRAPH.CENTER, color=RGBColor(100, 100, 100), font_name='楷体')

    # ==================== 基本信息表格 ====================
    doc.add_paragraph()
    info_table = doc.add_table(rows=4, cols=4)
    info_table.style = 'Table Grid'
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER

    info_data = [
        ('年    级', f'{grade}年级'),
        ('学    期', semester),
        ('学    科', subject),
        ('教材版本', edition),
        ('单    元', f'第{unit}单元' + (f'  {unit_name}' if unit_name else '')),
        ('课    题', topic),
        ('课    时', f'第{lesson}课时' if lesson else '共___课时'),
        ('教材页码', f'第{textbook_page}页' if textbook_page else '第___页'),
    ]

    idx = 0
    for r in range(4):
        for c in range(0, 4, 2):
            if idx < len(info_data):
                label_cell = info_table.cell(r, c)
                value_cell = info_table.cell(r, c + 1)
                _set_cell_shading(label_cell, 'F0F0F0')
                label_cell.text = info_data[idx][0]
                value_cell.text = info_data[idx][1]
                for cell in [label_cell, value_cell]:
                    for p in cell.paragraphs:
                        for run in p.runs:
                            run.font.size = Pt(11)
                            run.font.name = '宋体'
                            run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
                for run in label_cell.paragraphs[0].runs:
                    run.font.bold = True
                idx += 1

    doc.add_paragraph()

    # ==================== 一、教材分析 ====================
    _add_heading(doc, '一、教材分析', level=1)

    textbook_analysis = data.get('textbook_analysis', '')
    if textbook_analysis:
        doc.add_paragraph(textbook_analysis)
    else:
        # 提供结构化模板
        sections = [
            ('1. 本课地位', '本课是___年级___册第___单元的第___课，在本单元中承担___的教学任务。'
             '前承___（前一课/前一单元的知识），后启___（后续课/后续单元的知识），'
             '在学生的___学习中起着承上启下的作用。'),
            ('2. 教材内容', '本课教材主要包含以下内容：\n'
             '（1）___\n（2）___\n（3）___\n'
             '教材通过___的方式呈现，注重___能力的培养。'),
            ('3. 编写意图', '教材编者将本课安排在此处，意图在于：\n'
             '①___\n②___\n③___\n'
             '体现了___的课程理念。'),
            ('4. 知识体系', '本课涉及的核心知识点：\n'
             '├── ___\n├── ___\n└── ___\n'
             '知识点之间的逻辑关系为___。'),
        ]
        for sec_title, sec_content in sections:
            _add_rich_para(doc, [(sec_title + '：', True, 12)])
            doc.add_paragraph(sec_content)
    doc.add_paragraph()

    # ==================== 二、学情分析 ====================
    _add_heading(doc, '二、学情分析', level=1)

    student_analysis = data.get('student_analysis', '')
    if student_analysis:
        doc.add_paragraph(student_analysis)
    else:
        items = [
            '1. 知识基础：学生已经学习了___，掌握了___，具备了___的基础。',
            '2. 认知特点：___年级学生正处于___阶段，思维方式以___为主，对___较为敏感。',
            '3. 学习习惯：学生已初步形成___的学习习惯，但在___方面仍需加强。',
            '4. 困难预判：学生在学习本课时可能遇到的困难：\n'
            '   ①___\n   ②___',
        ]
        for item in items:
            doc.add_paragraph(item)
    doc.add_paragraph()

    # ==================== 三、教学目标 ====================
    _add_heading(doc, '三、教学目标', level=1)

    objectives = data.get('objectives', {})
    if objectives:
        # 三维目标
        dims = [
            ('（一）知识与技能目标', 'knowledge', '识记、理解、运用'),
            ('（二）过程与方法目标', 'process', '观察、分析、探究、合作'),
            ('（三）情感态度与价值观目标', 'emotion', '兴趣、态度、价值观'),
        ]
        for dim_title, dim_key, dim_hint in dims:
            _add_rich_para(doc, [(dim_title, True, 12)])
            items = objectives.get(dim_key, [])
            if items:
                for i, item in enumerate(items, 1):
                    doc.add_paragraph(f'  {i}. {item}')
            else:
                doc.add_paragraph(f'  （待填写，关键词：{dim_hint}）')
    else:
        doc.add_paragraph('（待根据教材分析和学情分析确定具体教学目标）')
    doc.add_paragraph()

    # ==================== 四、教学重点 ====================
    _add_heading(doc, '四、教学重点', level=1)
    key_points = data.get('key_points', [])
    if key_points:
        for i, kp in enumerate(key_points, 1):
            _add_rich_para(doc, [
                (f'{i}. {kp}', False, 12),
            ])
            strategy = data.get('key_point_strategies', [''] * len(key_points))
            if i - 1 < len(strategy) and strategy[i - 1]:
                _add_rich_para(doc, [('   突破策略：', True, 11, RGBColor(0, 100, 0)), (strategy[i - 1], False, 11)])
    else:
        doc.add_paragraph('（待填写）')
    doc.add_paragraph()

    # ==================== 五、教学难点 ====================
    _add_heading(doc, '五、教学难点', level=1)
    difficulties = data.get('difficulties', [])
    if difficulties:
        for i, d in enumerate(difficulties, 1):
            _add_rich_para(doc, [(f'{i}. {d}', False, 12)])
            method = data.get('difficulty_methods', [''] * len(difficulties))
            if i - 1 < len(method) and method[i - 1]:
                _add_rich_para(doc, [('   化解方法：', True, 11, RGBColor(0, 100, 0)), (method[i - 1], False, 11)])
    else:
        doc.add_paragraph('（待填写）')
    doc.add_paragraph()

    # ==================== 六、教学方法 ====================
    _add_heading(doc, '六、教学方法', level=1)
    methods = data.get('teaching_methods', {})
    if methods:
        _add_rich_para(doc, [('（一）教法', True, 12)])
        for m in methods.get('teaching', []):
            doc.add_paragraph(f'  • {m}')
        _add_rich_para(doc, [('（二）学法', True, 12)])
        for m in methods.get('learning', []):
            doc.add_paragraph(f'  • {m}')
    else:
        doc.add_paragraph('  教法：情境教学法、启发式教学法、直观演示法')
        doc.add_paragraph('  学法：自主探究、合作学习、实践操作')
    doc.add_paragraph()

    # ==================== 七、教学准备 ====================
    _add_heading(doc, '七、教学准备', level=1)
    preps = data.get('preparations', {})
    if isinstance(preps, dict):
        _add_rich_para(doc, [('教师准备：', True, 12)])
        for p in preps.get('teacher', []):
            doc.add_paragraph(f'  • {p}', style='List Bullet')
        _add_rich_para(doc, [('学生准备：', True, 12)])
        for p in preps.get('student', []):
            doc.add_paragraph(f'  • {p}', style='List Bullet')
    elif isinstance(preps, list):
        for p in preps:
            doc.add_paragraph(f'  • {p}', style='List Bullet')
    else:
        doc.add_paragraph('  • 多媒体课件')
        doc.add_paragraph('  • 相关教具')
    doc.add_paragraph()

    # ==================== 八、教学过程 ====================
    _add_heading(doc, '八、教学过程', level=1)

    process = data.get('teaching_process', [])
    if process:
        for step_idx, step in enumerate(process, 1):
            step_title = step.get('title', f'环节{step_idx}')
            step_time = step.get('time', '')
            step_content = step.get('content', '')
            teacher_act = step.get('teacher_activity', '')
            student_act = step.get('student_activity', '')
            design_intent = step.get('design_intent', '')
            preset_gen = step.get('preset_generation', '')
            transition = step.get('transition', '')

            # 环节标题
            _add_rich_para(doc, [
                (f'环节{step_idx}：{step_title}', True, 14, RGBColor(0, 51, 102), '黑体'),
                (f'  [{step_time}]', False, 11, RGBColor(150, 150, 150)),
            ])

            if step_content:
                _add_rich_para(doc, [('【教学内容】', True, 11, RGBColor(100, 100, 100))])
                doc.add_paragraph(step_content)

            # 师生活动表格
            if teacher_act or student_act:
                t = doc.add_table(rows=2, cols=2)
                t.style = 'Table Grid'
                t.alignment = WD_TABLE_ALIGNMENT.CENTER

                # 表头
                _set_cell_shading(t.cell(0, 0), 'D9E2F3')
                _set_cell_shading(t.cell(0, 1), 'D9E2F3')
                t.cell(0, 0).text = '教师活动'
                t.cell(0, 1).text = '学生活动'
                t.cell(1, 0).text = teacher_act
                t.cell(1, 1).text = student_act

                for row in t.rows:
                    for cell in row.cells:
                        for p in cell.paragraphs:
                            for run in p.runs:
                                run.font.size = Pt(11)
                                run.font.name = '宋体'
                                run.element.rPr.rFonts.set(qn('w:eastAsia'), '宋体')
                for run in t.cell(0, 0).paragraphs[0].runs:
                    run.font.bold = True
                for run in t.cell(0, 1).paragraphs[0].runs:
                    run.font.bold = True

            if design_intent:
                _add_rich_para(doc, [('【设计意图】', True, 11, RGBColor(0, 128, 0))])
                doc.add_paragraph(design_intent)

            if preset_gen:
                _add_rich_para(doc, [('【预设与生成】', True, 11, RGBColor(200, 100, 0))])
                doc.add_paragraph(preset_gen)

            if transition:
                _add_rich_para(doc, [('【过渡语】', True, 11, RGBColor(100, 0, 150)),
                                      (f' "{transition}"', False, 11, RGBColor(100, 0, 150))])

            doc.add_paragraph()  # 环节间空行
    else:
        # 默认详细模板
        default_steps = [
            ('情境导入', '5分钟',
             '教师创设与课题相关的生活情境，引发学生思考和兴趣',
             '① 展示情境素材（图片/视频/实物）\n② 提出驱动性问题：___？\n③ 引导学生初步思考，鼓励自由发言\n④ 过渡到新课学习',
             '① 观察情境素材，产生好奇心\n② 尝试回答教师问题\n③ 产生学习新知的欲望',
             '从学生已有的生活经验出发，建立新旧知识的联系，激发学习兴趣和探究欲望。',
             '预设：学生可能从___角度回答；\n生成：若学生回答偏离，可追问___引导回正。'),
            ('新知探究', '18分钟',
             '教师引导学生逐步探究本课核心知识',
             '① 出示学习任务/探究问题\n② 组织学生自主阅读/观察/操作\n③ 引导发现规律/总结方法\n④ 板书核心知识点\n⑤ 进行示范或讲解',
             '① 阅读教材/观察材料\n② 动手操作/实验探究\n③ 记录发现/标注重点\n④ 举手发言/小组讨论',
             '遵循"感知→理解→掌握"的认知规律，让学生在亲身经历中建构知识。',
             '预设：学生可能发现___\n生成：若学生未能发现关键点，可提示___'),
            ('合作交流', '7分钟',
             '组织小组合作，深化理解',
             '① 布置合作学习任务\n② 巡视各组，参与讨论\n③ 选取典型汇报\n④ 点评提升',
             '① 小组内分工讨论\n② 汇总观点形成结论\n③ 派代表汇报\n④ 聆听他组汇报并补充',
             '通过合作学习培养团队协作能力，在交流中完善思维，实现思维的碰撞与提升。',
             '预设：各组结论可能有___差异\n生成：利用差异引导深入讨论___'),
            ('巩固练习', '8分钟',
             '分层练习，巩固所学',
             '① 出示基础练习题\n② 出示提高练习题\n③ 巡视指导，收集典型错误\n④ 集体讲评纠错',
             '① 独立完成基础练习\n② 挑战提高题\n③ 对照答案自查\n④ 订正错误并记录',
             '遵循"由易到难"的练习梯度，及时反馈巩固，查漏补缺。',
             '预设：学生在___处可能出错\n生成：收集错误案例进行对比分析'),
            ('课堂总结', '3分钟',
             '梳理知识体系，升华提升',
             '① 引导学生回顾本课所学\n② 师生共同梳理知识框架\n③ 总结方法/规律/道理\n④ 布置下节课预告（可选）',
             '① 回忆本课学习内容\n② 口述或填写知识框架\n③ 分享学习收获',
             '通过系统梳理帮助学生形成完整的知识体系，加深理解和记忆。',
             '预设：学生总结可能不够全面\n生成：追问"还有补充吗？"查漏补缺'),
            ('布置作业', '2分钟',
             '分层布置，拓展延伸',
             '① 说明作业要求\n② 强调注意事项\n③ 鼓励拓展探究',
             '① 记录作业内容\n② 明确完成要求',
             '分层作业设计满足不同水平学生的需求，拓展作业激发学有余力学生的探究欲望。',
             ''),
        ]
        for title, time, content, teacher, student, intent, preset in default_steps:
            _add_rich_para(doc, [
                (f'环节：{title}', True, 14, RGBColor(0, 51, 102), '黑体'),
                (f'  [{time}]', False, 11, RGBColor(150, 150, 150)),
            ])
            _add_rich_para(doc, [('【教学内容】', True, 11, RGBColor(100, 100, 100))])
            doc.add_paragraph(content)

            t = doc.add_table(rows=2, cols=2)
            t.style = 'Table Grid'
            _set_cell_shading(t.cell(0, 0), 'D9E2F3')
            _set_cell_shading(t.cell(0, 1), 'D9E2F3')
            t.cell(0, 0).text = '教师活动'
            t.cell(0, 1).text = '学生活动'
            t.cell(1, 0).text = teacher
            t.cell(1, 1).text = student
            for run in t.cell(0, 0).paragraphs[0].runs:
                run.font.bold = True
            for run in t.cell(0, 1).paragraphs[0].runs:
                run.font.bold = True

            _add_rich_para(doc, [('【设计意图】', True, 11, RGBColor(0, 128, 0))])
            doc.add_paragraph(intent)
            if preset:
                _add_rich_para(doc, [('【预设与生成】', True, 11, RGBColor(200, 100, 0))])
                doc.add_paragraph(preset)
            doc.add_paragraph()

    # ==================== 九、板书设计 ====================
    _add_heading(doc, '九、板书设计', level=1)
    board = data.get('board_design', '')
    if board:
        p = doc.add_paragraph()
        run = p.add_run(board)
        run.font.size = Pt(12)
        run.font.name = 'Courier New'
        p.paragraph_format.left_indent = Cm(1)
    else:
        doc.add_paragraph('（用文字+框线设计结构化板书，体现知识体系）')
    doc.add_paragraph()

    # ==================== 十、作业设计 ====================
    _add_heading(doc, '十、作业设计', level=1)
    homework = data.get('homework', {})
    if homework:
        for level, items in homework.items():
            _add_rich_para(doc, [(level, True, 12)])
            if isinstance(items, list):
                for item in items:
                    doc.add_paragraph(f'  • {item}')
            else:
                doc.add_paragraph(f'  • {items}')
    else:
        levels = [
            ('★ 基础作业（必做）', ['抄写/背诵本课核心内容', '完成课后练习第___题']),
            ('★★ 提高作业（选做）', ['完成配套练习册相关习题', '用本课所学解释生活中的___现象']),
            ('★★★ 拓展作业（挑战）', ['查阅相关资料，了解___', '制作___小报/完成___实践']),
        ]
        for level, items in levels:
            _add_rich_para(doc, [(level, True, 12)])
            for item in items:
                doc.add_paragraph(f'  • {item}')
    doc.add_paragraph()

    # ==================== 十一、教学反思 ====================
    _add_heading(doc, '十一、教学反思', level=1)

    reflection = data.get('reflection', {})
    if reflection:
        for key, val in reflection.items():
            _add_rich_para(doc, [(key, True, 12)])
            doc.add_paragraph(val if val else '（课后填写）')
    else:
        reflection_items = [
            ('1. 预设成功点：', '本课设计中预计最有效的环节是___，因为___'),
            ('2. 可能改进点：', '___环节可能需要根据课堂实际情况灵活调整'),
            ('3. 课后实际反思：', ''),
        ]
        for title, content in reflection_items:
            _add_rich_para(doc, [(title, True, 12)])
            if content:
                doc.add_paragraph(content)
            else:
                for _ in range(4):
                    doc.add_paragraph('_' * 60)

    # ==================== 资料来源说明 ====================
    doc.add_page_break()
    _add_heading(doc, '附：资料来源说明', level=1)
    sources = data.get('sources_used', [
        '1. 人民教育出版社《教师教学用书》（电子版）',
        '2. 昌明师友·华东师范大学出版社《教学设计与指导》（电子版）',
        '3. 教材原文及相关教参',
    ])
    for s in sources:
        doc.add_paragraph(s)
    doc.add_paragraph()
    doc.add_paragraph('本教案由备课系统自动生成，仅供参考，请根据实际教学情况调整使用。')

    doc.save(output_path)
    return output_path


def _add_heading(doc, text, level=1):
    heading = doc.add_heading(text, level=level)
    for run in heading.runs:
        run.font.name = '黑体'
        run.element.rPr.rFonts.set(qn('w:eastAsia'), '黑体')
    return heading


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python3 generate_lesson_plan.py <json_file> [output_path]")
        sys.exit(1)
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        data = json.load(f)
    output = sys.argv[2] if len(sys.argv) > 2 else sys.argv[1].replace('.json', '_教案.docx')
    print(f"教案已生成: {create_lesson_plan(data, output)}")
