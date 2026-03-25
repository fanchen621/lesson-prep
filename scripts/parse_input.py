#!/usr/bin/env python3
"""
parse_input.py - 解析用户备课指令，提取结构化信息
输出 JSON 格式的备课参数
"""
import re
import json
import sys

# 年级映射
GRADE_MAP = {
    '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6,
    '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
}

# 科目列表
SUBJECTS = ['语文', '数学', '英语', '科学', '道德与法治', '音乐', '美术', '体育', '信息技术',
            '品德与社会', '品德与生活', '道德与法治']

# 版本映射
EDITION_MAP = {
    '人教版': '人教版', '人民教育出版社': '人教版', 'PEP': '人教版', '部编版': '人教版', '统编版': '人教版',
    '科教版': '科教版', '科学教育出版社': '科教版', '教科版': '科教版',
    '北师大版': '北师大版', '北京师范大学出版社': '北师大版', 'BS版': '北师大版',
    '苏教版': '苏教版', '江苏教育出版社': '苏教版',
    '外研版': '外研社版', '外研社版': '外研社版', '外语教学与研究出版社': '外研社版',
    '冀教版': '冀教版', '河北教育出版社': '冀教版',
    '西师大版': '西师大版', '西南师范大学出版社': '西师大版',
    '青岛版': '青岛版', '青岛出版社': '青岛版',
    '浙教版': '浙教版', '浙江教育出版社': '浙教版',
    '湘教版': '湘教版', '湖南教育出版社': '湘教版',
    '沪教版': '沪教版', '上海教育出版社': '沪教版',
}


def parse_input(text: str) -> dict:
    """从自然语言中提取备课参数"""
    result = {
        'grade': None,          # 年级 (1-6)
        'semester': None,       # 学期: 上册/下册
        'subject': None,        # 科目
        'edition': '人教版',    # 版本，默认人教版
        'unit': None,           # 单元号
        'lesson': None,         # 课时号
        'topic': None,          # 课题名称
        'raw': text,            # 原始输入
        'missing': [],          # 缺失字段
    }

    # 1. 提取年级
    grade_patterns = [
        r'([一二三四五六123456])年级',
        r'小学([一二三四五六123456])',
        r'grade\s*(\d)',
    ]
    for pat in grade_patterns:
        m = re.search(pat, text)
        if m:
            g = m.group(1)
            result['grade'] = GRADE_MAP.get(g, int(g) if g.isdigit() else None)
            break

    # 2. 提取学期
    if '上册' in text or '上学期' in text:
        result['semester'] = '上册'
    elif '下册' in text or '下学期' in text:
        result['semester'] = '下册'

    # 3. 提取科目
    for subj in SUBJECTS:
        if subj in text:
            result['subject'] = subj
            break

    # 4. 提取版本（优先科教版）
    for key, val in EDITION_MAP.items():
        if key in text:
            result['edition'] = val
            break

    # 5. 提取单元号
    unit_m = re.search(r'第([一二三四五六七八九十1234567890]+)\s*单元', text)
    if unit_m:
        unit_str = unit_m.group(1)
        cn_nums = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6,
                   '七': 7, '八': 8, '九': 9, '十': 10}
        if unit_str in cn_nums:
            result['unit'] = cn_nums[unit_str]
        elif unit_str.isdigit():
            result['unit'] = int(unit_str)

    # 6. 提取课时号
    lesson_m = re.search(r'第([一二三四五六七八九十1234567890]+)\s*课', text)
    if lesson_m:
        lesson_str = lesson_m.group(1)
        cn_nums = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6,
                   '七': 7, '八': 8, '九': 9, '十': 10}
        if lesson_str in cn_nums:
            result['lesson'] = cn_nums[lesson_str]
        elif lesson_str.isdigit():
            result['lesson'] = int(lesson_str)

    # 7. 提取课题名称（课名通常在"第X课"后面，或者在年级/科目信息之后的关键词）
    topic = None
    # 模式1: "第X课 课题名"
    topic_m = re.search(r'第[一二三四五六七八九十1234567890]+\s*课\s*([\u4e00-\u9fff《》\w]+)', text)
    if topic_m:
        topic = topic_m.group(1).strip()
    # 模式2: "课XXXX" 直接跟课名 (如 "课琥珀")
    if not topic:
        topic_m2 = re.search(r'课\s*([\u4e00-\u9fff《》]{2,20})', text)
        if topic_m2:
            candidate = topic_m2.group(1).strip()
            # 排除"教案"等通用词
            if candidate not in ['教案', '教学', '设计', '准备', '提示']:
                topic = candidate
    # 模式3: 书名号内容 《课题名》
    if not topic:
        topic_m3 = re.search(r'《([\u4e00-\u9fff\w]+)》', text)
        if topic_m3:
            topic = topic_m3.group(1).strip()

    result['topic'] = topic

    # 标记缺失字段
    if not result['grade']:
        result['missing'].append('年级')
    if not result['semester']:
        result['missing'].append('学期(上册/下册)')
    if not result['subject']:
        result['missing'].append('科目')
    if not result['lesson'] and not result['topic']:
        result['missing'].append('课时号或课题名称')

    return result


if __name__ == '__main__':
    if len(sys.argv) > 1:
        text = ' '.join(sys.argv[1:])
    else:
        text = sys.stdin.read()
    result = parse_input(text)
    print(json.dumps(result, ensure_ascii=False, indent=2))
