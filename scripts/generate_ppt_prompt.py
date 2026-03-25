#!/usr/bin/env python3
"""
generate_ppt_prompt.py - TOP专业设计师级PPT制作提示词生成器 v3.0
含完整设计系统、栅格布局、动效叙事、信息层级、可访问性
专业设计师拿到这份提示词可以直接做出成品课件
用法: python3 generate_ppt_prompt.py <json_file> [output_path]
"""
import json, sys


def generate_ppt_prompt(data: dict) -> str:
    grade = data.get('grade', 'X')
    semester = data.get('semester', '')
    subject = data.get('subject', '')
    edition = data.get('edition', '人教版')
    topic = data.get('topic', '课题')
    unit = data.get('unit', '')
    lesson = data.get('lesson', '')
    unit_name = data.get('unit_name', '')

    objectives = data.get('objectives', {})
    key_points = data.get('key_points', [])
    difficulties = data.get('difficulties', [])
    process = data.get('teaching_process', [])
    board_design = data.get('board_design', '')

    # ===== 科目专属设计系统 =====
    design_systems = {
        '语文': {
            'primary': '#B22222', 'primary_rgb': '178,34,34', 'primary_name': '朱砂红',
            'secondary': '#FFF5E1', 'secondary_rgb': '255,245,225', 'secondary_name': '暖宣纸',
            'accent': '#D4A017', 'accent_rgb': '212,160,23', 'accent_name': '琥珀金',
            'bg': '#FFFAF0', 'bg_rgb': '255,250,240', 'bg_name': '米白',
            'text': '#2C1810', 'text_rgb': '44,24,16', 'text_name': '墨色',
            'highlight': '#E74C3C', 'highlight_rgb': '231,76,60',
            'muted': '#8B7355', 'muted_rgb': '139,115,85',
            'success': '#27AE60', 'warning': '#F39C12',
            'style': '新中式水墨风', 'mood': '典雅、温润、有文化底蕴',
            'font_title': '思源宋体 Heavy / 方正小标宋',
            'font_body': '思源宋体 Regular / 宋体',
            'font_accent': '思源黑体 Medium',
            'font_en': 'Playfair Display / Cormorant Garamond',
            'decoration': '水墨晕染、宣纸纹理、印章元素、竹简/卷轴装饰线',
            'icon_style': '线性水墨风图标',
            'pattern': '淡雅水墨山水/花鸟纹样做背景水印',
        },
        '数学': {
            'primary': '#1A365D', 'primary_rgb': '26,54,93', 'primary_name': '深邃蓝',
            'secondary': '#EBF5FB', 'secondary_rgb': '235,245,251', 'secondary_name': '天空蓝',
            'accent': '#E67E22', 'accent_rgb': '230,126,34', 'accent_name': '活力橙',
            'bg': '#F8FAFC', 'bg_rgb': '248,250,252', 'bg_name': '极简白',
            'text': '#1A202C', 'text_rgb': '26,32,44', 'text_name': '深空黑',
            'highlight': '#3182CE', 'highlight_rgb': '49,130,206',
            'muted': '#718096', 'muted_rgb': '113,128,150',
            'success': '#38A169', 'warning': '#DD6B20',
            'style': '极简几何风', 'mood': '理性、清晰、逻辑感强',
            'font_title': '思源黑体 Heavy / Montserrat Bold',
            'font_body': '思源黑体 Regular / Noto Sans',
            'font_accent': '思源黑体 Medium',
            'font_en': 'Montserrat / Roboto',
            'decoration': '几何图形、网格线、坐标系元素、渐变色块',
            'icon_style': '双色面性图标',
            'pattern': '淡色几何网格/点阵做背景',
        },
        '英语': {
            'primary': '#2B6CB0', 'primary_rgb': '43,108,176', 'primary_name': '天际蓝',
            'secondary': '#EBF8FF', 'secondary_rgb': '235,248,255', 'secondary_name': '晴空蓝',
            'accent': '#E53E3E', 'accent_rgb': '229,62,62', 'accent_name': '活力红',
            'bg': '#FAFCFF', 'bg_rgb': '250,252,255', 'bg_name': '云白',
            'text': '#1A365D', 'text_rgb': '26,54,93', 'text_name': '铅字蓝',
            'highlight': '#48BB78', 'highlight_rgb': '72,187,120',
            'muted': '#A0AEC0', 'muted_rgb': '160,174,192',
            'success': '#48BB78', 'warning': '#ECC94B',
            'style': '活泼国际化风', 'mood': '明快、开放、充满活力',
            'font_title': 'Poppins Bold / 思源黑体 Bold',
            'font_body': 'Open Sans / 思源黑体 Regular',
            'font_accent': 'Nunito SemiBold',
            'font_en': 'Poppins / Nunito',
            'decoration': '气泡对话框、世界地图元素、多彩气球/星星',
            'icon_style': '多彩扁平图标',
            'pattern': '淡色波点/气泡做背景',
        },
        '科学': {
            'primary': '#22543D', 'primary_rgb': '34,84,61', 'primary_name': '森林绿',
            'secondary': '#F0FFF4', 'secondary_rgb': '240,255,244', 'secondary_name': '薄荷绿',
            'accent': '#D69E2E', 'accent_rgb': '214,158,46', 'accent_name': '大地金',
            'bg': '#FFFFF0', 'bg_rgb': '255,255,240', 'bg_name': '嫩叶白',
            'text': '#1A2E1A', 'text_rgb': '30,46,30', 'text_name': '松墨绿',
            'highlight': '#48BB78', 'highlight_rgb': '72,187,120',
            'muted': '#68D391', 'muted_rgb': '104,211,145',
            'success': '#38A169', 'warning': '#DD6B20',
            'style': '自然探索风', 'mood': '生机、好奇、探索感',
            'font_title': '思源黑体 Heavy / Nunito Bold',
            'font_body': '思源黑体 Regular / Nunito',
            'font_accent': '思源黑体 Medium',
            'font_en': 'Nunito / Quicksand',
            'decoration': '叶片、放大镜、DNA双螺旋、星球元素',
            'icon_style': '自然元素线性图标',
            'pattern': '叶脉纹理/细胞结构做背景水印',
        },
    }

    ds = design_systems.get(subject, design_systems['语文'])

    L = []

    def add(text=''):
        L.append(text)

    def section(title, level=2):
        add()
        add('---')
        add(f'{"#" * level} {title}')
        add()

    # ================================================================
    #  文件头
    # ================================================================
    add(f'# PPT制作提示词 — TOP专业设计师级')
    add(f'# {grade}年级{semester} {subject} {edition}')
    add(f'# {unit_name or f"第{unit}单元"} · {topic}')
    add()
    add('> **📌 使用说明**')
    add('> 本提示词为专业课件设计师编写的完整制作指令。每页幻灯片包含精确的栅格布局、')
    add('> 完整文字内容（含字号字重）、配图详细要求、动画时间线、教师备注。')
    add('> 请严格按照下方描述生成每一页幻灯片。设计师可直接据此制作成品。')
    add()

    # ================================================================
    #  第一部分：设计系统 Design System
    # ================================================================
    section('第一部分：设计系统（Design System）')

    add('### 1.1 项目信息')
    add(f'- **学段学科**：小学{grade}年级{semester} {subject}')
    add(f'- **教材版本**：{edition}')
    add(f'- **课题名称**：{topic}')
    add(f'- **设计风格**：{ds["style"]}')
    add(f'- **设计调性**：{ds["mood"]}')
    add(f'- **预计总页数**：{20 + len(process) * 3}页')
    add(f'- **目标受众**：{grade}年级小学生（6-12岁）+ 授课教师')
    add(f'- **使用场景**：教室投影/一体机（1920×1080），可能放大到幕布')
    add()

    add('### 1.2 品牌配色系统（严格遵守）')
    add()
    add('| 角色 | HEX | RGB | 名称 | 用途 | 使用频率 |')
    add('|------|-----|-----|------|------|----------|')
    add(f'| **主色** | `{ds["primary"]}` | rgb({ds["primary_rgb"]}) | {ds["primary_name"]} | 标题文字、主装饰线、关键图标 | 高 |')
    add(f'| **辅色** | `{ds["secondary"]}` | rgb({ds["secondary_rgb"]}) | {ds["secondary_name"]} | 卡片背景、信息框、表格底色 | 高 |')
    add(f'| **强调色** | `{ds["accent"]}` | rgb({ds["accent_rgb"]}) | {ds["accent_name"]} | 关键词高亮、互动标记、按钮 | 中 |')
    add(f'| **背景色** | `{ds["bg"]}` | rgb({ds["bg_rgb"]}) | {ds["bg_name"]} | 页面默认背景 | 高 |')
    add(f'| **文字色** | `{ds["text"]}` | rgb({ds["text_rgb"]}) | {ds["text_name"]} | 所有正文文字 | 高 |')
    add(f'| **高亮色** | `{ds["highlight"]}` | rgb({ds["highlight_rgb"]}) | — | 重点标注、正确反馈 | 低 |')
    add(f'| **静音色** | `{ds["muted"]}` | rgb({ds["muted_rgb"]}) | — | 辅助文字、时间标签、注释 | 中 |')
    add()
    add('**配色原则**：')
    add(f'- 页面背景统一使用 `{ds["bg"]}`，不使用纯白色（#FFFFFF）以免刺眼')
    add(f'- 文字与背景对比度必须 ≥ 4.5:1（WCAG AA标准）')
    add(f'- 每页使用不超过3种颜色（背景色不计）')
    add(f'- 强调色使用面积 ≤ 页面总面积的 10%')
    add()

    add('### 1.3 字体系统')
    add()
    add('| 层级 | 中文字体 | 英文字体 | 字号 | 字重 | 行高 | 字间距 | 颜色 |')
    add('|------|----------|----------|------|------|------|--------|------|')
    add(f'| **H1 大标题** | {ds["font_title"]} | {ds["font_en"]} | 40-48pt | Bold/Heavy | 1.3x | 0.02em | `{ds["primary"]}` |')
    add(f'| **H2 页面标题** | {ds["font_title"]} | {ds["font_en"]} | 28-32pt | Bold | 1.4x | 0.01em | `{ds["text"]}` |')
    add(f'| **H3 小标题** | {ds["font_accent"]} | {ds["font_en"]} | 22-24pt | Medium | 1.5x | normal | `{ds["text"]}` |')
    add(f'| **正文** | {ds["font_body"]} | {ds["font_en"]} | 18-22pt | Regular | 1.6x | normal | `{ds["text"]}` |')
    add(f'| **注释/标注** | {ds["font_body"]} | — | 14-16pt | Light | 1.5x | normal | `{ds["muted"]}` |')
    add(f'| **强调文字** | {ds["font_accent"]} | — | 同正文 | Medium | 同正文 | normal | `{ds["accent"]}` |')
    add()
    add('**字体原则**：')
    add('- 正文字号 ≥ 18pt（确保教室后排学生能看清）')
    add('- 英文/数字使用配套西文字体，不使用中文字体显示英文')
    add('- 每页最多使用2种字体族（标题1种 + 正文1种）')
    add('- 行高至少1.5倍，给小学生眼睛足够的"呼吸空间"')
    add()

    add('### 1.4 栅格系统与安全区域')
    add()
    add('```')
    add('┌─────────────────────────────────────────────────┐')
    add('│  安全区域（80px padding）                        │')
    add('│  ┌───────────────────────────────────────────┐  │')
    add('│  │ 标题区（顶部120px）                        │  │')
    add('│  │                                           │  │')
    add('│  │ 内容区（12列栅格，间距24px）               │  │')
    add('│  │ ████████ ████████ ████████                │  │')
    add('│  │ ████████ ████████ ████████                │  │')
    add('│  │                                           │  │')
    add('│  │ 底部装饰区（60px）                         │  │')
    add('│  └───────────────────────────────────────────┘  │')
    add('└─────────────────────────────────────────────────┘')
    add('```')
    add()
    add('- **页面尺寸**：16:9（1920×1080px）')
    add('- **安全区域**：距边缘80px以内不放重要文字')
    add('- **栅格**：12列，列宽128px，间距24px')
    add('- **标题区**：顶部120px，用于页面标题')
    add('- **底部装饰**：60px高，可放置页码/装饰线/标签')
    add('- **内容密度**：每页核心信息不超过7±2条（米勒定律）')
    add()

    add('### 1.5 视觉语言规范')
    add()
    add(f'**装饰风格**：{ds["decoration"]}')
    add(f'**图标风格**：{ds["icon_style"]}，统一使用一套图标库')
    add(f'**背景纹理**：{ds["pattern"]}')
    add()
    add('**阴影规范**：')
    add('- 卡片阴影：`box-shadow: 0 2px 8px rgba(0,0,0,0.08)`')
    add('- 悬浮阴影：`box-shadow: 0 8px 24px rgba(0,0,0,0.12)`')
    add('- 阴影颜色使用主色的10%透明度，不使用纯黑阴影')
    add()
    add('**圆角规范**：')
    add('- 卡片：8-12px')
    add('- 按钮/标签：20px（胶囊形）')
    add('- 图片：8px 或圆形（头像类）')
    add()

    add('### 1.6 动效规范')
    add()
    add('| 动效类型 | 缓动曲线 | 默认时长 | 触发方式 |')
    add('|----------|----------|----------|----------|')
    add('| 淡入 | ease-out | 0.5s | 自动/点击 |')
    add('| 滑入（左→右）| ease-out | 0.6s | 自动 |')
    add('| 滑入（下→上）| ease-out | 0.5s | 自动 |')
    add('| 弹入 | cubic-bezier(0.68,-0.55,0.27,1.55) | 0.6s | 点击 |')
    add('| 缩放强调 | ease-in-out | 0.3s | 自动 |')
    add('| 逐字显示 | linear | 0.08s/字 | 自动 |')
    add('| 旋转出现 | ease-out | 0.5s | 自动 |')
    add()
    add('**动效原则**：')
    add('- 动效服务于理解，不花哨')
    add('- 同一页面最多3种动画类型')
    add('- 所有动画总时长 ≤ 3秒')
    add('- 避免全页元素同时飞入（杂乱）')
    add('- 重点内容使用弹入/缩放强调')
    add()

    # ================================================================
    #  第二部分：逐页详细设计
    # ================================================================
    section('第二部分：逐页详细设计')

    page_num = 0

    def add_page(title, layout_desc, content_lines, image_desc=None,
                 animation=None, transition=None, interactive=None,
                 teacher_note=None, a11y_note=None, density_note=None):
        nonlocal page_num
        page_num += 1
        add(f'### 第{page_num}页 — {title}')
        add()

        add(f'**【栅格布局】**')
        for ld in layout_desc:
            add(f'- {ld}')
        add()

        add(f'**【文字内容】**')
        for cl in content_lines:
            add(cl)
        add()

        if image_desc:
            add(f'**【配图要求】**')
            for img in image_desc:
                add(f'- {img}')
            add()

        if animation:
            add(f'**【动画时间线】**')
            for i, anim in enumerate(animation, 1):
                add(f'{i}. {anim}')
            add()

        if transition:
            add(f'**【页面切换】** {transition}')
            add()

        if interactive:
            add(f'**【互动设计】**')
            for inter in interactive:
                add(f'- {inter}')
            add()

        if teacher_note:
            add(f'**【教师备注】** {teacher_note}')
            add()

        if a11y_note:
            add(f'**【可访问性】** {a11y_note}')
            add()

        if density_note:
            add(f'**【信息密度】** {density_note}')
            add()

        add('---')
        add()

    # ===== 第1页：封面 =====
    add_page('封面',
             [
                 f'背景：`{ds["bg"]}`纯色 + `{ds["pattern"]}`（透明度15%）',
                 f'底部装饰条：高60px，`{ds["primary"]}`色，距底边0px，全宽',
                 f'标题：栅格2-11列，垂直居中偏上1/3（Y: 320px）',
                 f'配图：栅格8-12列，垂直居中（Y: 400px）',
             ],
             [
                 f'- 大标题（H1）：`{topic}` — 48pt，`{ds["primary"]}`，{ds["font_title"]}，居中',
                 f'- 副标题：`{grade}年级{semester} {subject} {edition}` — 24pt，`{ds["text"]}`，不加粗，标题下方30px',
                 f'- 单元标签：`{unit_name or f"第{unit}单元"}`' + (f' · 第{lesson}课' if lesson else '') + f' — 16pt，白色，底部装饰条内居中',
                 f'- 右下角小字：`人民教育出版社` — 12pt，`{ds["muted"]}`',
             ],
             [
                 f'内容：与"{topic}"课题高度相关的主题插图',
                 f'位置：页面右侧2/5区域，垂直居中',
                 f'尺寸：600×500px（约占页面30%面积）',
                 f'风格：{ds["style"]}风格的高质量插画/照片',
                 f'处理：轻微投影（模拟纸张浮起效果）',
                 f'来源建议：教材原图 > Unsplash搜索"{topic} illustration" > 稿定设计',
                 f'备选方案：找不到合适图时，使用课题名的艺术字设计（大字+装饰纹样）替代',
             ],
             [
                 f'底部装饰条：从左到右展开（0.6s, ease-out）',
                 f'标题：从底部向上淡入+轻微放大（scale 0.95→1.0, opacity 0→1, 0.8s, ease-out），装饰条完成后0.2s开始',
                 f'副标题：标题完成后0.3s，从底部滑入（0.5s）',
                 f'配图：与标题同时从右侧淡入+右移30px（1s, ease-out）',
                 f'单元标签：最后从底部浮出（0.4s）',
             ],
             '平滑过渡（第一页无切换）',
             None,
             '这是学生看到的第一印象。标题字必须大（48pt），确保教室最后一排也能看清。整体留白充足，不要拥挤。',
             '标题与背景对比度 ≥ 7:1（大字标准）',
             '信息密度：低。核心信息仅3条（标题+副标题+配图），留白 ≥ 40%。')

    # ===== 第2页：课堂导入 =====
    add_page('课堂导入 — 悬念/兴趣激发',
             [
                 f'背景：全屏模糊化主题图片（透明度15-20%）叠加`{ds["bg"]}`半透明蒙版',
                 f'标题：栅格1-4列（左上角），Y: 100px',
                 f'悬念文字：栅格2-11列，垂直居中（Y: 420px）',
                 f'引导语：栅格4-9列，底部（Y: 880px）',
                 f'右下角小图：栅格10-12列，底部（Y: 800px）',
             ],
             [
                 f'- 页面标题（H2）：`🔍 猜猜看！` 或 `❓ 你知道吗？` — 28pt，`{ds["primary"]}`',
                 f'- 悬念大字（H1）：与课题相关的趣味问题或惊人事实 — 36pt，`{ds["text"]}`',
                 f'  示例：`"一万年前的一只苍蝇和一只蜘蛛，被永远定格在了一起……这是怎么发生的？"`',
                 f'- 引导语：`"让我们翻开课本，一起寻找答案吧！"` — 20pt，`{ds["accent"]}`，斜体',
             ],
             [
                 f'背景图：与课题相关的氛围图（模糊处理），搜索关键词："{topic} atmosphere"',
                 f'右下角小图：清晰的焦点特写，150×150px，圆角12px，轻微阴影',
                 f'来源：教材原图放大版 或 搜索"amber macro insect"',
             ],
             [
                 f'背景图：先淡入（1s, ease-out）',
                 f'标题"猜猜看"：从上方弹入（0.5s, 弹性缓动），附音效提示标记',
                 f'悬念大字：逐字显示（打字机效果），每字0.08s，全句显示约3-4s',
                 f'引导语：大字全部显示后1s，从底部浮出（0.5s）',
             ],
             '从封面推入（从右到左，0.7s, ease-out）',
             [
                 '在显示大字前，先保持安静3-5秒，让学生自己阅读，制造悬念',
                 '等学生开始小声议论时，再开口引导',
                 '可以走动到教室中间，用期待的眼神扫视全班',
             ],
             '导入环节的关键是抓住注意力。悬念要足够有趣，让学生"想知道答案"。不要急着给答案。',
             '大字与背景蒙版对比度 ≥ 4.5:1',
             '信息密度：极低。仅2条核心信息（悬念+引导），大量留白制造呼吸感。')

    # ===== 第3页：学习目标 =====
    add_page('学习目标 — 目标可视化',
             [
                 f'背景：`{ds["bg"]}` + `{ds["secondary"]}`色卡片区域',
                 f'标题：栅格1-6列（左上角）',
                 f'目标卡片：栅格2-11列，垂直排列，卡片间距16px',
                 f'底部激励语：栅格3-10列，底部居中',
             ],
             [
                 f'- 页面标题（H2）：`📋 今天我们要学什么？` — 28pt，`{ds["primary"]}`',
                 f'- 目标卡片内容：',
             ] + (
                 [f'  - 📖 卡片1：{objectives.get("knowledge", ["掌握本课核心知识"])[0]} — 20pt']
                 if objectives.get('knowledge') else
                 [f'  - 📖 卡片1：掌握本课核心知识 — 20pt']
             ) + (
                 [f'  - 🔍 卡片2：{objectives.get("process", ["学会探究方法"])[0]} — 20pt']
                 if objectives.get('process') else
                 [f'  - 🔍 卡片2：学会探究方法 — 20pt']
             ) + (
                 [f'  - 💡 卡片3：{objectives.get("emotion", ["感受学习的乐趣"])[0]} — 20pt']
                 if objectives.get('emotion') else
                 [f'  - 💡 卡片3：感受学习的乐趣 — 20pt']
             ) + [
                 f'- 底部激励语：`"准备好了吗？出发！🚀"` — 18pt，`{ds["accent"]}`',
             ],
             [
                 f'每个目标卡片左侧放一个圆形图标（48×48px），底色为`{ds["primary"]}`，图标白色',
                 f'卡片样式：`{ds["secondary"]}`背景，`{ds["primary"]}`色左边框（4px宽），圆角8px',
                 f'推荐图标：📖（知识）🔍（探究）💡（感悟）— 扁平风格',
             ],
             [
                 f'目标卡片：从上到下依次弹入，每张间隔0.3s（弹性缓动）',
                 f'图标：弹入时带轻微旋转（-15°→0°, 0.4s）',
                 f'底部激励语：所有卡片完成后，从底部浮出（0.5s）',
             ],
             '从导入页推入（从右到左，0.6s）',
             None,
             '逐一朗读学习目标，每读一条稍作停顿。让学生明确"这节课我要学会什么"。',
             '图标+文字的双重编码，帮助不同学习风格的学生理解目标。',
             '信息密度：中低。3条目标 + 1条激励语，视觉节奏清晰。')

    # ===== 教学过程各环节 =====
    if process:
        for step_idx, step in enumerate(process, 1):
            step_title = step.get('title', f'环节{step_idx}')
            step_time = step.get('time', '')
            step_content = step.get('content', '')
            teacher_act = step.get('teacher_activity', '')
            student_act = step.get('student_activity', '')

            # --- 环节标题过渡页 ---
            add_page(f'{step_title} — 环节过渡',
                     [
                         f'左侧竖条：全高，宽80px，`{ds["primary"]}`色',
                         f'章节编号：左侧竖条内居中，白色大字',
                         f'标题：栅格3-10列，垂直居中偏上',
                         f'时间标签：标题下方20px',
                         f'环节描述：栅格3-10列，标题下方60px',
                         f'装饰图标：栅格10-12列，底部',
                     ],
                     [
                         f'- 章节编号（大字）：`{step_idx}` — 72pt，白色，`{ds["font_title"]}`',
                         f'- 章节标题（H1）：`{step_title}` — 40pt，`{ds["primary"]}`',
                         f'- 时间标签：`⏱ {step_time}` — 18pt，`{ds["muted"]}`，灰色胶囊标签（`{ds["secondary"]}`背景，圆角20px）',
                         f'- 环节描述：`{step_content[:60] if step_content else "（根据教案内容填充）"}` — 20pt，`{ds["text"]}`',
                     ],
                     [
                         f'内容：与"{step_title}"相关的主题图标',
                         f'尺寸：200×200px',
                         f'风格：{ds["icon_style"]}',
                         f'来源：IconPark / Flaticon 搜索对应中文关键词',
                         f'推荐图标映射：导入→放大镜 / 探究→灯泡 / 合作→握手 / 练习→铅笔 / 总结→书本',
                     ],
                     [
                         f'左侧竖条：从底部向上展开（0.5s, ease-out）',
                         f'章节编号：竖条展开完成后在竖条内放大出现（scale 0→1, 0.4s, 弹性）',
                         f'标题：编号出现后从左侧滑入（0.5s）',
                         f'时间标签+描述：标题到位后依次从右侧淡入（各0.3s）',
                         f'装饰图标：最后从右下角浮出（0.4s）',
                     ],
                     '从上一页平滑过渡（淡入, 0.5s）',
                     None,
                     '本页为过渡页，停留2-3秒即可进入详细内容。快速建立"环节切换"的心理预期。',
                     None,
                     '信息密度：极低。仅过渡信息，不承载教学内容。')

            # --- 教师活动详细页 ---
            if teacher_act:
                teacher_lines = [l.strip() for l in teacher_act.split('\n') if l.strip()]
                page_num += 1
                add(f'### 第{page_num}页 — {step_title} — 教师引导')
                add()
                add(f'**【栅格布局】**')
                add(f'- 标题：栅格1-6列（左上角），Y: 100px')
                add(f'- 活动列表：栅格1-11列，标题下方，每行间距24px')
                add(f'- 配图：栅格9-12列，右侧区域')
                add()
                add(f'**【文字内容】**')
                add(f'- 页面标题（H2）：`👨‍🏫 教师引导` — 28pt，`{ds["primary"]}`')
                for i, line in enumerate(teacher_lines[:8]):
                    add(f'- 步骤{i+1}：`{line}` — 20pt，`{ds["text"]}`')
                add()
                add(f'**【配图要求】**')
                add(f'- 内容：教师教学场景插画（教师在黑板前/手持教具）')
                add(f'- 位置：页面右侧，垂直居中')
                add(f'- 尺寸：350×300px')
                add(f'- 风格：{ds["style"]}风格温馨卡通')
                add(f'- 来源：搜索"小学课堂教师教学 卡通插画"或使用教材配套插图')
                add()
                add(f'**【动画时间线】**')
                add(f'1. 标题：从上方滑入（0.5s）')
                add(f'2. 步骤编号圆圈：从左到右依次弹入，间隔0.2s')
                add(f'3. 步骤文字：编号到位后0.1s从右侧滑入（0.3s）')
                add(f'4. 配图：与第一个编号同时从右侧淡入（0.8s）')
                add()
                add(f'**【页面切换】** 从环节过渡页推入（从右到左，0.6s）')
                add()
                add(f'**【教师备注】** 这是教师的行动指南。每个编号步骤对应课堂上的一个具体动作。')
                add(f'重点步骤（提问/板书）建议用`{ds["accent"]}`色在PPT中高亮。')
                add()
                add('---')
                add()

            # --- 学生活动详细页 ---
            if student_act:
                student_lines = [l.strip() for l in student_act.split('\n') if l.strip()]
                page_num += 1
                add(f'### 第{page_num}页 — {step_title} — 学生活动')
                add()
                add(f'**【栅格布局】**')
                add(f'- 标题：栅格1-6列（左上角），Y: 100px')
                add(f'- 活动列表：栅格1-11列，标题下方')
                add(f'- 场景图：栅格1-12列，页面底部横幅')
                add()
                add(f'**【文字内容】**')
                add(f'- 页面标题（H2）：`👦👧 学生行动` — 28pt，`{ds["primary"]}`')
                for i, line in enumerate(student_lines[:8]):
                    add(f'- 活动{i+1}：✏️ `{line}` — 20pt，`{ds["text"]}`')
                add()
                add(f'**【配图要求】**')
                add(f'- 内容：小学生围坐讨论/举手发言/动手操作的场景插画')
                add(f'- 位置：页面底部，横幅式')
                add(f'- 尺寸：1200×200px')
                add(f'- 风格：活泼可爱的{ds["style"]}风格')
                add(f'- 来源：搜索"小学生课堂讨论 插画"或"children classroom cartoon"')
                add()
                add(f'**【动画时间线】**')
                add(f'1. 标题：从上方滑入（0.5s）')
                add(f'2. 活动列表：从左侧依次滑入，间隔0.3s')
                add(f'3. 底部场景图：从底部浮出，最后显示（0.6s）')
                add()
                add(f'**【页面切换】** 从教师活动页推入（从右到左，0.6s）')
                add()
                add(f'**【教师备注】** 学生活动与教师活动交替展示，形成"教-学"互动的视觉节奏。')
                add(f'此页可停留稍长（30-45秒），让学生明确自己要做什么。')
                add()
                add('---')
                add()

    else:
        # 默认环节页面
        default_steps = [
            ('情境导入', '5分钟',
             '展示图片，提问引入',
             '① 展示实物/图片\n② 提问：你们知道这是什么吗？\n③ 引导：它是怎么来的呢？\n④ 过渡：让我们一起走进课文',
             '① 观察图片\n② 自由回答\n③ 产生好奇\n④ 进入学习状态'),
            ('新知探究', '18分钟',
             '逐步分析核心内容',
             '① 布置自读任务\n② 检查基础知识\n③ 分段精读/逐步推导\n④ 板书关键节点',
             '① 自由朗读/思考\n② 标注重点\n③ 回答提问\n④ 完成填空'),
            ('合作交流', '7分钟',
             '小组讨论，深化理解',
             '① 布置讨论任务\n② 巡视指导\n③ 组织汇报\n④ 点评总结',
             '① 小组分工讨论\n② 记录结果\n③ 代表汇报\n④ 聆听补充'),
            ('巩固练习', '8分钟',
             '分层练习，巩固所学',
             '① 出示基础题\n② 出示提高题\n③ 巡视收集\n④ 集体讲评',
             '① 独立完成\n② 挑战提高\n③ 自查订正\n④ 记录错题'),
            ('课堂总结', '3分钟',
             '梳理知识，升华提升',
             '① 引导回顾\n② 梳理板书\n③ 总结升华',
             '① 回忆所学\n② 口述总结\n③ 分享收获'),
            ('布置作业', '2分钟',
             '分层布置，拓展延伸',
             '① 说明作业\n② 强调重点\n③ 鼓励探究',
             '① 记录作业\n② 明确要求'),
        ]

        for st_title, st_time, st_content, st_teacher, st_student in default_steps:
            page_num += 1
            add(f'### 第{page_num}页 — {st_title}')
            add()
            add(f'**【栅格布局】**')
            add(f'- 标题：栅格1-6列（左上角）')
            add(f'- 内容区：栅格1-11列，标题下方')
            add()
            add(f'**【文字内容】**')
            add(f'- 页面标题（H2）：`{st_title}` — 32pt，`{ds["primary"]}`')
            add(f'- 时间标签：`⏱ {st_time}` — 18pt，`{ds["muted"]}`')
            add(f'- 内容：`{st_content}` — 20pt')
            add()
            add(f'**【动画时间线】**')
            add(f'1. 标题：从左侧滑入（0.5s）')
            add(f'2. 时间标签+内容：标题到位后淡入（0.4s）')
            add()
            add(f'**【页面切换】** 从上一页推入（从右到左，0.6s）')
            add()
            add('---')
            add()

    # ===== 练习互动页 =====
    add_page('课堂练习 — 互动题',
             [
                 f'背景：`{ds["bg"]}`',
                 f'标题：栅格1-6列（左上角）',
                 f'题目卡片：栅格1-10列，标题下方，每题一个独立卡片',
                 f'计时器：栅格10-12列，右上角圆形',
                 f'鼓励插图：栅格10-12列，右下角',
             ],
             [
                 f'- 页面标题（H2）：`✍️ 试一试！` — 28pt，`{ds["primary"]}`',
                 f'- 题目内容：（根据实际题目填充，以下为示例格式）',
                 f'  - 题目1（基础）：白色卡片，`{ds["secondary"]}`色左边框 — 20pt',
                 f'  - 题目2（提高）：白色卡片，`{ds["accent"]}`色左边框 — 20pt',
             ],
             [
                 f'计时器：圆形进度条（直径120px），`{ds["primary"]}`色描边',
                 f'插图：卡通人物认真做作业，180×180px，圆角12px',
                 f'来源：搜索"小学生做作业 卡通插画"',
             ],
             [
                 f'标题：从左侧滑入（0.5s）',
                 f'题目卡片：从底部依次浮出，间隔0.5s',
                 f'计时器：所有题目显示后，在右上角弹入（弹性缓动）',
                 f'计时结束提示：全屏闪烁一次`{ds["accent"]}`色（0.3s）',
             ],
             '从上一页推入（0.6s）',
             [
                 '给学生2-3分钟独立完成时间',
                 'PPT内置倒计时或口头倒计时',
                 '鼓励举手回答，不急着公布答案',
             ],
             '练习环节要给足时间。先让学生独立思考，再请人回答。答案在下一页揭晓。',
             '基础题用`{ds["secondary"]}`边框，提高题用`{ds["accent"]}`边框 — 色盲友好，同时用文字标注难度。',
             '信息密度：中。2-3道练习题 + 计时器，卡片式布局保持整洁。')

    # ===== 答案揭晓页 =====
    add_page('练习答案 — 答案揭晓',
             [
                 f'标题：栅格1-6列',
                 f'答案区：栅格1-11列，标题下方',
                 f'正确率标签：栅格10-12列，右上角',
             ],
             [
                 f'- 页面标题（H2）：`✅ 答案揭晓` — 28pt，`{ds["primary"]}`',
                 f'- 答案内容：（根据实际答案填充）',
                 f'  - ✓ 题目1答案 + 解析 — 20pt，`{ds["highlight"]}`色',
                 f'  - ✓ 题目2答案 + 解析 — 20pt',
             ],
             None,
             [
                 f'答案：每题从左到右依次擦除显现（0.5s间隔）',
                 f'正确图标 ✓：答案显现时弹入 + 缩放强调（0.8→1.1→1.0, 0.3s）',
             ],
             '从练习页平滑过渡（淡入, 0.5s）',
             None,
             '逐题讲解，重点讲易错题。对答错的学生不批评，分析错误原因。',
             None,
             '信息密度：中。答案+解析，视觉层级清晰。')

    # ===== 课堂总结页 =====
    add_page('课堂总结 — 知识回顾',
             [
                 f'背景：`{ds["bg"]}`',
                 f'标题：顶部居中',
                 f'思维导图：页面中央，以课题为根节点',
                 f'金句区：底部居中',
             ],
             [
                 f'- 页面标题（H2）：`📝 今天我们学到了什么？` — 28pt，`{ds["primary"]}`',
                 f'- 思维导图中心：`{topic}` — 24pt，`{ds["primary"]}`色圆角矩形',
                 f'- 分支1-3：核心知识点 — 18pt，`{ds["secondary"]}`色圆角矩形',
                 f'- 金句/收获：底部，20pt，楷体，`{ds["accent"]}`',
             ],
             [
                 f'思维导图中心图标：课题核心概念图标，60×60px，扁平化',
                 f'风格：简约放射状思维导图',
             ],
             [
                 f'中心节点：先出现（0.5s, 弹性缓动）',
                 f'分支：中心到位后依次展开（每支0.3s, ease-out）',
                 f'金句：导图全部展开后从底部浮出（0.5s）',
             ],
             '从上一页推入（0.6s）',
             [
                 '引导学生一起回顾：今天我们学了什么？',
                 '请2-3位学生口述收获',
                 '用思维导图帮学生建立知识框架',
             ],
             '总结环节很重要，不能草草结束。要让学生自己说出学到了什么。',
             None,
             '信息密度：中。思维导图可视化信息结构，金句提供情感升华。')

    # ===== 作业页 =====
    add_page('课后作业 — 分层布置',
             [
                 f'标题：栅格1-6列',
                 f'作业卡片：栅格2-11列，三级纵向排列，间距16px',
                 f'装饰图标：栅格11-12列，右上角',
             ],
             [
                 f'- 页面标题（H2）：`📚 课后小任务` — 28pt，`{ds["primary"]}`',
                 f'- ⭐ 基础作业（必做）：`{ds["primary"]}`色边框卡片 — 20pt',
                 f'- ⭐⭐ 提高作业（选做）：虚线边框卡片 — 20pt',
                 f'- ⭐⭐⭐ 拓展作业（挑战）：虚线边框卡片 — 20pt',
                 f'- 底部提示：`"按时完成，明天检查哦！"` — 16pt，`{ds["muted"]}`',
             ],
             [
                 f'书本+铅笔图标组合，120×120px，简约线条风格',
                 f'来源：IconPark搜索"书本"或"作业"',
             ],
             [
                 f'作业卡片：从上到下依次滑入，间隔0.4s',
                 f'星级图标：滑入时带弹性动画（scale 0.8→1.1→1.0, 0.4s）',
             ],
             '从总结页推入（0.6s）',
             None,
             '强调必做作业要求，选做/挑战作业简要介绍激发兴趣即可。',
             None,
             '信息密度：中低。3条作业 + 1条提示，层级分明。')

    # ===== 结束页 =====
    add_page('结束页 — 温馨收尾',
             [
                 f'背景：与封面呼应的`{ds["bg"]}` + 淡装饰',
                 f'大字：页面正中',
                 f'预告：大字下方',
             ],
             [
                 f'- 中央大字（H1）：`下节课再见 👋` — 48pt，`{ds["primary"]}`，居中',
                 f'- 下节预告：`下节课预告：___` — 18pt，`{ds["muted"]}`',
                 f'- 教师信息：右下角小字 — 14pt，`{ds["muted"]}`',
             ],
             [
                 f'两侧装饰：可爱的挥手/比心卡通人物，各150×150px',
                 f'风格：与整体风格一致的{ds["style"]}插画',
             ],
             [
                 f'大字：从中心放大出现（scale 0.5→1.0, 0.6s, 弹性缓动）',
                 f'两侧图片：同时从两侧滑入（0.5s）',
                 f'预告：图片到位后从底部浮出（0.4s）',
             ],
             '从作业页淡入（0.7s）',
             None,
             '温馨收尾，给学生留下好印象。',
             None,
             '信息密度：极低。仅告别信息+预告，大面积留白。')

    # ===== 板书参考页（教师用） =====
    if board_design:
        page_num += 1
        add(f'### 第{page_num}页 — 板书设计参考（仅教师用/备注页）')
        add()
        add(f'**【栅格布局】** 整页居中展示板书结构')
        add()
        add(f'**【文字内容】**')
        add('```')
        add(board_design)
        add('```')
        add()
        add(f'**【备注】** 此页在PPT中设置为备注页或隐藏页，不展示给学生。仅供教师板书参考。')
        add()
        add('---')
        add()

    # ================================================================
    #  第三部分：设计备忘与检查清单
    # ================================================================
    section('第三部分：设计备忘')

    add('### 3.1 核心设计原则')
    add('1. **简洁优先**：每页文字不超过50字（标题不算），宁可多分页')
    add('2. **图片说话**：能用图表达的不用文字，小学生的注意力靠视觉刺激')
    add('3. **互动驱动**：每3-4页至少一个互动环节（提问/讨论/练习）')
    add('4. **动画适度**：动画增强理解，不花哨。避免全页元素同时飞入')
    add('5. **字体够大**：正文 ≥ 18pt，标题 ≥ 28pt，确保后排学生看清')
    add('6. **色彩克制**：每页最多3种颜色，强调色面积 ≤ 10%')
    add('7. **留白呼吸**：内容面积 ≤ 页面面积的60%，留白 ≥ 40%')
    add()

    add('### 3.2 配图资源库')
    add(f'- **教材原图**：{edition}教材电子版（优先级最高）')
    add('- **国际图库**：Unsplash / Pexels / Pixabay（搜索英文关键词）')
    add('- **中文图库**：觅元素 / 千图网 / 稿定设计 / 创客贴')
    add('- **图标库**：IconPark（字节跳动）/ Flaticon / Iconfont / Heroicons')
    add('- **插画库**：undraw.co / drawkit.io / blush.design')
    add('- **AI生成**：Midjourney / DALL·E（搜索"children illustration {topic}"）')
    add()

    add('### 3.3 设计自查清单')
    add(f'- [ ] 所有标题使用 `{ds["primary"]}` 或 `{ds["text"]}`')
    add(f'- [ ] 所有高亮/强调使用 `{ds["accent"]}`')
    add(f'- [ ] 所有卡片背景使用 `{ds["secondary"]}`')
    add(f'- [ ] 所有正文使用 `{ds["text"]}`')
    add(f'- [ ] 页面背景统一为 `{ds["bg"]}`')
    add('- [ ] 正文字号 ≥ 18pt')
    add('- [ ] 文字与背景对比度 ≥ 4.5:1')
    add('- [ ] 每页动画总数 ≤ 5个')
    add('- [ ] 每页颜色数 ≤ 3种')
    add('- [ ] 留白面积 ≥ 页面40%')
    add('- [ ] 所有配图有来源标注和备选方案')
    add('- [ ] 互动环节每3-4页出现一次')
    add('- [ ] 教师备注填写完整')
    add()

    add('### 3.4 可访问性检查')
    add('- [ ] 色盲友好：不依赖单一颜色传达信息，同时使用形状/文字')
    add('- [ ] 对比度：所有文字与背景对比度 ≥ 4.5:1（WCAG AA）')
    add('- [ ] 字号：最小字号 ≥ 14pt（标注），正文 ≥ 18pt')
    add('- [ ] 动画：提供无动画备选方案（关闭动画后仍可阅读）')
    add()

    add('---')
    add(f'*本提示词由备课系统v3.0生成 | TOP专业设计师级 | {grade}年级{semester} {subject} {edition} | {topic}*')

    return '\n'.join(L)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("用法: python3 generate_ppt_prompt.py <json_file> [output_path]")
        sys.exit(1)
    with open(sys.argv[1], 'r', encoding='utf-8') as f:
        data = json.load(f)
    output = sys.argv[2] if len(sys.argv) > 2 else sys.argv[1].replace('.json', '_PPT提示词.txt')
    content = generate_ppt_prompt(data)
    with open(output, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"PPT提示词已生成: {output} ({len(content)} 字符)")
