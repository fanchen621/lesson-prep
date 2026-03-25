#!/usr/bin/env python3
"""测试脚本 - 验证所有生成器正常工作"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from parse_input import parse_input

# 测试1: 解析输入
print("=" * 60)
print("测试1: 输入解析")
print("=" * 60)

test_inputs = [
    "帮我琥珀备课，小学四年级下册语文人教版第二单元第五课琥珀",
    "备课，三年级数学上册，人教版，第3单元，测量",
    "帮我准备一下六年级科学科教版第一单元的教案",
    "五年级英语下册外研社版第4单元",
]

for text in test_inputs:
    result = parse_input(text)
    print(f"\n输入: {text}")
    print(f"解析: 年级={result['grade']}, 学期={result['semester']}, "
          f"科目={result['subject']}, 版本={result['edition']}, "
          f"单元={result['unit']}, 课={result['lesson']}, "
          f"课题={result['topic']}")
    if result['missing']:
        print(f"缺失: {', '.join(result['missing'])}")

# 测试2: 生成教案Word
print("\n" + "=" * 60)
print("测试2: 教案Word生成")
print("=" * 60)

test_lesson_data = {
    "grade": "四",
    "semester": "下册",
    "subject": "语文",
    "edition": "人教版",
    "unit": 2,
    "lesson": 5,
    "topic": "琥珀",
    "objectives": {
        "knowledge": [
            "认识本课生字词，会写课后生字",
            "理解课文内容，了解琥珀的形成过程",
        ],
        "process": [
            "通过朗读、讨论，理解课文的叙述顺序",
            "学习作者按时间顺序描写事物的方法",
        ],
        "emotion": [
            "激发学生对自然科学的兴趣",
            "培养学生探索自然奥秘的意识",
        ]
    },
    "key_points": [
        "理解琥珀的形成过程",
        "体会作者用词的准确性和生动性",
    ],
    "difficulties": [
        "理解琥珀形成的科学原理",
        "体会课文合理想象与科学依据的结合",
    ],
    "preparations": [
        "多媒体课件（含琥珀图片、形成过程动画）",
        "生字卡片",
        "学生预习课文",
    ],
    "teaching_process": [
        {
            "title": "导入新课",
            "time": "5分钟",
            "content": "出示琥珀实物或图片，激发学生兴趣，引出课题",
            "teacher_activity": "展示琥珀图片，提问：你们知道这是什么吗？它是怎么形成的？",
            "student_activity": "观察图片，自由发言，产生好奇心",
        },
        {
            "title": "初读课文",
            "time": "8分钟",
            "content": "学生自由朗读课文，标注生字词，初步了解课文大意",
            "teacher_activity": "布置朗读任务，巡视指导，纠正读音",
            "student_activity": "自由朗读，圈画生字词，同桌互读",
        },
        {
            "title": "精读理解",
            "time": "15分钟",
            "content": "分析琥珀形成的四个阶段，理解课文叙述顺序",
            "teacher_activity": "引导学生逐段分析，板书形成过程的关键词",
            "student_activity": "分组讨论，汇报学习成果，完成填空练习",
        },
        {
            "title": "品味语言",
            "time": "7分钟",
            "content": "体会课文中准确、生动的用词",
            "teacher_activity": "找出关键语句，引导品味用词的精妙",
            "student_activity": "朗读精彩语句，交流感受",
        },
        {
            "title": "课堂总结",
            "time": "3分钟",
            "content": "回顾本课所学，梳理琥珀形成过程",
            "teacher_activity": "引导学生回顾板书，总结本课重点",
            "student_activity": "复述琥珀形成过程",
        },
        {
            "title": "布置作业",
            "time": "2分钟",
            "content": "抄写生字词；用自己的话复述琥珀的形成过程",
            "teacher_activity": "布置作业，提出要求",
            "student_activity": "记录作业",
        },
    ],
    "board_design": "                琥珀\n    ┌─────────────────────┐\n    │ 一万年前（松脂球）    │\n    │ 松树 → 松脂 → 包裹   │\n    │ ↓                    │\n    │ 沉入海底 → 变成琥珀   │\n    │ ↓                    │\n    │ 被发现（渔民父子）    │\n    └─────────────────────┘",
}

test_dir = os.path.dirname(__file__)
json_path = os.path.join(test_dir, 'test_data.json')
with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(test_lesson_data, f, ensure_ascii=False, indent=2)

from generate_lesson_plan import create_lesson_plan
docx_path = os.path.join(test_dir, 'test_教案.docx')
result = create_lesson_plan(test_lesson_data, docx_path)
print(f"✅ {result}")

# 测试3: PPT提示词
print("\n" + "=" * 60)
print("测试3: PPT提示词生成")
print("=" * 60)

from generate_ppt_prompt import generate_ppt_prompt
txt_path = os.path.join(test_dir, 'test_PPT提示词.txt')
content = generate_ppt_prompt(test_lesson_data)
with open(txt_path, 'w', encoding='utf-8') as f:
    f.write(content)
print(f"✅ {txt_path} ({len(content)} 字符)")

# 测试4: 练习题PDF
print("\n" + "=" * 60)
print("测试4: 练习题PDF生成")
print("=" * 60)

test_exercise_data = {
    **test_lesson_data,
    "exercise_sections": [
        {
            "title": "一、看拼音，写词语",
            "score": "每词2分，共10分",
            "type": "fill_blank",
            "questions": [
                {"content": "nù hǒu (        )", "type": "fill_blank"},
                {"content": "sōng zhī (        )", "type": "fill_blank"},
                {"content": "fú shì (        )", "type": "fill_blank"},
                {"content": "měi cān (        )", "type": "fill_blank"},
                {"content": "shèn chū (        )", "type": "fill_blank"},
            ]
        },
        {
            "title": "二、选择题",
            "score": "每题3分，共15分",
            "type": "choice",
            "questions": [
                {
                    "content": "下列加点字读音完全正确的一项是（  ）",
                    "type": "choice",
                    "options": ["琥珀(pō)  澎湃(bài)", "掸翅膀(dǎn)  拂拭(shì)", "渗出(shèn)  埋在(lǐ)", "挣扎(zhēng)  冲刷(shuā)"]
                },
                {
                    "content": "琥珀形成的正确顺序是（  ）",
                    "type": "choice",
                    "options": ["松脂→包裹→沉入海底→变成琥珀", "包裹→松脂→变成琥珀→沉入海底", "沉入海底→松脂→包裹→变成琥珀", "变成琥珀→松脂→包裹→沉入海底"]
                },
            ]
        },
        {
            "title": "三、按课文内容填空",
            "score": "每空2分，共20分",
            "type": "fill_blank",
            "questions": [
                {"content": "这个故事发生在___年前，那时候这里是一片___。", "type": "fill_blank"},
                {"content": "蜘蛛刚扑过去，突然发生了一件___的事情。一大滴松脂从树上滴下来，刚好落在树干上，把苍蝇和蜘蛛一齐包在里头。", "type": "fill_blank"},
            ]
        },
        {
            "title": "四、阅读理解",
            "score": "共25分",
            "type": "answer",
            "questions": [
                {"content": "用自己的话简述琥珀的形成过程。（10分）", "type": "answer", "blank_lines": 6},
                {"content": '课文最后说"从那块琥珀，我们可以推测发生在一万年前的故事的详细经过"，你认为作者的推测合理吗？请结合课文内容说明理由。（15分）', "type": "answer", "blank_lines": 8},
            ]
        },
        {
            "title": "五、拓展题",
            "score": "共10分",
            "type": "answer",
            "questions": [
                {"content": '除了琥珀，你还知道哪些可以保存远古生物的天然"时间胶囊"？请举出至少两个例子，并简单介绍。（10分）', "type": "answer", "blank_lines": 6},
            ]
        },
    ],
    "answers": {
        "一、看拼音，写词语": ["怒吼", "松脂", "拂拭", "美餐", "渗出"],
        "二、选择题": ["B", "A"],
        "三、按课文内容填空": ["一万 / 松树林", "可怕"],
        "四、阅读理解": [
            "松树滴下松脂，包裹住苍蝇和蜘蛛 → 松脂继续滴落形成松脂球 → 地壳变化，松脂球沉入海底 → 经过漫长岁月变成化石（琥珀）",
            "合理。依据：1.琥珀中有苍蝇和蜘蛛；2.琥珀的形成需要特定条件；3.课文对形成过程的推断符合科学常识。",
        ],
        "五、拓展题": [
            "示例：1.冻土（如西伯利亚猛犸象，冰冻保存完整）；2.沥青坑（如洛杉矶拉布雷亚沥青坑，保存了大量史前动物骨骼）；3.火山灰（如庞贝古城，保存了古罗马人的生活场景）",
        ],
    },
}

from generate_exercises import generate_exercise_pdf
pdf_path = os.path.join(test_dir, 'test_练习题.pdf')
result = generate_exercise_pdf(test_exercise_data, pdf_path)
print(f"✅ {result}")

# 清理
os.remove(json_path)

print("\n" + "=" * 60)
print("🎉 所有测试通过！")
print("=" * 60)
print(f"生成文件：")
print(f"  📄 {docx_path}")
print(f"  📝 {txt_path}")
print(f"  📋 {pdf_path}")
