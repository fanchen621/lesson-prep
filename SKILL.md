# 备课 Skill v4.0 — 零占位符版

## 核心理念

**AI 即知识源，脚本只管排版。**

v3.0 问题：要求 web 搜索 → 填 JSON → 传脚本。搜索失败 = 全是 `___` 占位符。
v4.0 方案：AI 直接用自身知识生成完整内容 → 输出 JSON → 脚本纯排版。零依赖外部搜索，零占位符。

## 工作流程（3步，不可跳步）

### 第一步：解析用户指令

运行 `scripts/parse_input.py` 提取参数：
```bash
python3 scripts/parse_input.py "帮我备课，小学四年级下册语文人教版第三单元短诗三首"
```

检查 `missing` 字段，缺失项**必须追问用户**，不可假设。

### 第二步：AI 生成完整 JSON 数据（最关键的一步）

**这是整个流程的核心。AI 必须用自己的知识生成完整、详细的教学内容。**

将生成的 JSON 写入临时文件：`/tmp/lesson_data.json`

#### JSON 数据要求（必须全部填写，禁止任何 `___` 占位符）

```json
{
  "grade": 4,
  "semester": "下册",
  "subject": "语文",
  "edition": "人教版",
  "unit": 3,
  "unit_name": "自然之韵",
  "lesson": "2-3",
  "topic": "短诗三首",
  "textbook_page": "",

  "textbook_analysis": "完整的教材分析（800-1500字）...",
  "student_analysis": "完整的学情分析（300-500字）...",

  "objectives": {
    "knowledge": ["目标1", "目标2", "目标3"],
    "process": ["目标1", "目标2", "目标3"],
    "emotion": ["目标1", "目标2", "目标3"]
  },

  "key_points": ["重点1", "重点2"],
  "key_point_strategies": ["突破策略1", "突破策略2"],
  "difficulties": ["难点1"],
  "difficulty_methods": ["化解方法1"],

  "teaching_methods": {
    "teaching": ["情境教学法", "启发式教学法"],
    "learning": ["自主探究", "合作学习"]
  },

  "preparations": {
    "teacher": ["多媒体课件（含配乐朗读音频）", "板书预设卡片"],
    "student": ["预习课文，标注生字词"]
  },

  "teaching_process": [
    {
      "title": "情境导入",
      "time": "5分钟",
      "content": "本环节教学内容概述",
      "teacher_activity": "① 教师话术：\"同学们...\"\n② 展示教具...\n③ 提问：\"...\"",
      "student_activity": "① 预设A：学生回答...→教师跟进\n② 预设B：学生沉默→教师引导",
      "design_intent": "为什么这样设计",
      "preset_generation": "预设与生成的具体描述",
      "transition": "下一环节的过渡语",
      "classroom_management": "课堂调控策略"
    }
  ],

  "board_design": "板书的文本布局描述",

  "homework": {
    "★ 基础作业（必做）": ["具体作业内容1", "具体作业内容2"],
    "★★ 提高作业（选做）": ["具体作业内容"],
    "★★★ 拓展作业（挑战）": ["具体作业内容"]
  },

  "reflection": {
    "预设成功点": "具体内容",
    "需改进处": "具体内容"
  },

  "exercise_sections": [
    {
      "title": "一、填空题",
      "count": "10题",
      "type": "fill_blank",
      "tier": "基础",
      "questions": [
        {"type": "fill_blank", "content": "题目内容", "difficulty": "基础"}
      ]
    }
  ],

  "answers": {
    "一、填空题": [
      {"answer": "答案", "explanation": "解析", "error_tip": "易错提醒"}
    ]
  }
}
```

#### 生成质量标准

**教材分析（必须是实际内容，不是模板）：**
- 说明本课在本单元的地位和作用
- 分析与前后知识的衔接
- 说明教材编写意图
- 列出核心知识点体系

**学情分析（必须针对本课）：**
- 学生已有的相关知识基础（具体到哪些课/哪些知识点）
- 本年龄段认知特点
- 本课可能遇到的具体困难

**教学目标（必须具体可测量）：**
- 知识目标：具体到字词、概念、技能
- 过程目标：具体到方法和能力
- 情感目标：具体到体验和态度

**教学过程（详案级，核心中的核心）：**
- teacher_activity: 教师的逐句话术，包括导入语、每个问题的精确表述、追问话术、板书动作
- student_activity: 学生的预判回答（至少2种可能），以及教师的应对策略
- 设计意图、预设与生成、过渡语、课堂调控，都必须填写

**练习题：**
- 严格三级分层：基础50-60% / 提高25-35% / 拓展5-15%
- 题目内容必须是本课实际知识点
- 每题附答案+解析+易错提醒

### 第三步：调用脚本生成文件

```bash
# 生成教案 Word 文档
python3 scripts/generate_lesson_plan.py /tmp/lesson_data.json "/path/to/output_教案.docx"

# 生成 PPT 提示词
python3 scripts/generate_ppt_prompt.py /tmp/lesson_data.json "/path/to/output_PPT提示词.txt"

# 生成练习题 PDF（需要中文字体）
python3 scripts/generate_exercises.py /tmp/lesson_data.json "/path/to/output_练习题.pdf"
```

## 输出文件命名规则

```
{年级}年级{学期}_{科目}_{版本}_{课题}_教案.docx
{年级}年级{学期}_{科目}_{版本}_{课题}_PPT提示词.txt
{年级}年级{学期}_{科目}_{版本}_{课题}_练习题.pdf
```

## 脚本路径

- `scripts/parse_input.py` — 自然语言解析
- `scripts/generate_lesson_plan.py` — Word 教案生成
- `scripts/generate_ppt_prompt.py` — PPT 提示词生成
- `scripts/generate_exercises.py` — 练习题 PDF 生成

## 环境依赖

```bash
pip install python-docx fpdf2
# 系统中文字体（任一）：
# wqy-microhei (apt install fonts-wqy-microhei)
# NotoSansCJK (apt install fonts-noto-cjk)
```

## 使用示例

用户输入：
```
帮我备课，小学四年级下册语文人教版第三单元短诗三首
```

AI 执行流程：
1. 运行 parse_input.py → 提取参数
2. 用自己的知识生成完整 JSON（禁止 `___`）
3. 写入 /tmp/lesson_data.json
4. 调用三个生成脚本
5. 输出文件路径给用户

## 质量自检（生成后必须检查）

- [ ] JSON 中是否有任何 `___` 占位符？（零容忍）
- [ ] 教材分析是否 ≥ 800 字？
- [ ] 教学过程是否包含逐句话术？
- [ ] 每个教学环节是否有预设与生成？
- [ ] 练习题是否有具体题目内容（非模板）？
- [ ] 答案解析是否完整？
- [ ] 教案 docx 是否可以正常打开？
