#!/usr/bin/env python3
"""
parse_input.py - 解析用户备课指令，提取结构化信息 v3.0
输出 JSON 格式的备课参数，支持更多自然语言表达
"""
import re
import json
import sys

# 年级映射
GRADE_MAP = {
    '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6,
    '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6,
}

# 科目列表（去重+排序）
SUBJECTS = [
    '语文', '数学', '英语', '科学', '道德与法治', '音乐', '美术',
    '体育', '信息技术', '品德与社会', '品德与生活',
]

# 版本映射
EDITION_MAP = {
    '人教版': '人教版', '人民教育出版社': '人教版', 'PEP': '人教版',
    '部编版': '人教版', '统编版': '人教版',
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
    '湘少版': '湘少版', '湘少': '湘少版',
    '人音版': '人音版', '人美版': '人美版', '湘美版': '湘美版', '浙美版': '浙美版',
}

# 中文数字映射
CN_NUMS = {
    '零': 0, '一': 1, '二': 2, '三': 3, '四': 4, '五': 5,
    '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
    '十一': 11, '十二': 12,
}


def _parse_cn_num(s: str) -> int:
    """解析中文数字或阿拉伯数字"""
    if s.isdigit():
        return int(s)
    if s in CN_NUMS:
        return CN_NUMS[s]
    # 处理"十一"、"十二"等
    if len(s) == 2 and s[0] == '十':
        return 10 + CN_NUMS.get(s[1], 0)
    if len(s) == 2 and s[1] == '十':
        return CN_NUMS.get(s[0], 0) * 10
    return None


def parse_input(text: str) -> dict:
    """从自然语言中提取备课参数"""
    result = {
        'grade': None,
        'semester': None,
        'subject': None,
        'edition': '人教版',
        'unit': None,
        'lesson': None,
        'topic': None,
        'unit_name': None,
        'raw': text,
        'missing': [],
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

    # 3. 提取科目（优先匹配长名称）
    for subj in sorted(SUBJECTS, key=len, reverse=True):
        if subj in text:
            result['subject'] = subj
            break

    # 4. 提取版本（优先科教版等非人教版）
    edition_candidates = []
    for key, val in EDITION_MAP.items():
        if key in text:
            edition_candidates.append((len(key), val))
    if edition_candidates:
        # 优先选择最长匹配（更精确）
        edition_candidates.sort(reverse=True)
        result['edition'] = edition_candidates[0][1]

    # 5. 提取单元号
    unit_m = re.search(r'第([一二三四五六七八九十\d]+)\s*单元', text)
    if unit_m:
        result['unit'] = _parse_cn_num(unit_m.group(1))

    # 6. 提取课时号
    lesson_m = re.search(r'第([一二三四五六七八九十\d]+)\s*课时?', text)
    if lesson_m:
        result['lesson'] = _parse_cn_num(lesson_m.group(1))

    # 7. 提取课题名称
    topic = None

    # 模式1: "第X课 课题名"
    topic_m = re.search(r'第[一二三四五六七八九十\d]+\s*课\s*([\u4e00-\u9fff《》\w]{2,30})', text)
    if topic_m:
        candidate = topic_m.group(1).strip()
        if candidate not in ['教案', '教学', '设计', '准备', '提示', '练习']:
            topic = candidate

    # 模式2: "课XXXX"（如"课琥珀"）
    if not topic:
        topic_m2 = re.search(r'课\s*([\u4e00-\u9fff《》]{2,20})', text)
        if topic_m2:
            candidate = topic_m2.group(1).strip()
            if candidate not in ['教案', '教学', '设计', '准备', '提示', '练习', '课件']:
                topic = candidate

    # 模式3: 书名号内容 《课题名》
    if not topic:
        topic_m3 = re.search(r'《([\u4e00-\u9fff\w·]{2,30})》', text)
        if topic_m3:
            topic = topic_m3.group(1).strip()

    # 模式4: Module/Unit 后面的英文
    if not topic:
        topic_m4 = re.search(r'(?:Module|Unit)\s*[\d]+(?:\s*[-—]\s*)?([\w\s]{2,30})?', text, re.IGNORECASE)
        if topic_m4 and topic_m4.group(1):
            topic = topic_m4.group(1).strip()

    # 模式5: "备课 XXX" — 尝试提取课题名（在年级/科目信息之后的关键词）
    if not topic:
        # 移除已知的通用词和年级/科目/版本信息后，剩余的可能是课题名
        cleaned = text
        for word in ['帮我备课', '备课', '教案', '教学设计', '上课准备', '课件制作']:
            cleaned = cleaned.replace(word, '')
        for subj in SUBJECTS:
            cleaned = cleaned.replace(subj, '')
        for ed in EDITION_MAP:
            cleaned = cleaned.replace(ed, '')
        cleaned = re.sub(r'[一二三四五六123456]年级', '', cleaned)
        cleaned = re.sub(r'上册|下册|上学期|下学期', '', cleaned)
        cleaned = re.sub(r'第[一二三四五六七八九十\d]+\s*单元', '', cleaned)
        cleaned = re.sub(r'第[一二三四五六七八九十\d]+\s*课时?', '', cleaned)
        cleaned = cleaned.strip(' ,，。、')
        # 剩余有意义的中文词可能是课题名
        remaining = re.findall(r'[\u4e00-\u9fff·]{2,15}', cleaned)
        if remaining:
            # 过滤掉常见无关词
            skip_words = ['小学', '请', '帮我', '给', '准备', '今天', '现在']
            for r_word in remaining:
                if r_word not in skip_words and len(r_word) >= 2:
                    topic = r_word
                    break

    result['topic'] = topic

    # 标记缺失字段
    if not result['grade']:
        result['missing'].append('年级')
    if not result['semester']:
        result['missing'].append('学期(上册/下册)')
    if not result['subject']:
        result['missing'].append('科目')
    if not result['topic'] and not result['lesson']:
        result['missing'].append('课题名称')

    return result


if __name__ == '__main__':
    if len(sys.argv) > 1:
        text = ' '.join(sys.argv[1:])
    else:
        text = sys.stdin.read()
    result = parse_input(text)
    print(json.dumps(result, ensure_ascii=False, indent=2))
