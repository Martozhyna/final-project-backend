from enum import Enum


class RegEx(Enum):
    STATUS = (
        r'^(In work|New|Agree|Disagree|Dubbing)?$',
        'you can specify the status: In work, New, Agree, Disagree, Dubbing or do not specify anything',
    )

    COURSE = (
        r'^(FS|QACX|JCX|JSCX|FE|PCX)?$',
        'you can specify the course: FS, QACX, JCX, JSCX, FE, PCX or do not specify anything'
    )

    COURSE_TYPE = (
        r'^(pro|minimal|premium|incubator|vip)?$',
        'you can specify the course_type: pro, minimal, premium, incubator, vip or do not specify anything'
    )
    COURSE_FORMAT = (
        r'^(static|online)?$',
        'you can specify the course_type: static, online or do not specify anything'
    )

    def __init__(self, pattern: str, msg: str | list[str]):
        self.pattern = pattern
        self.msg = msg
