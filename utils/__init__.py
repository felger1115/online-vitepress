import hashlib
import re

def md5(s):
    h = hashlib.md5(s.encode())
    return h.hexdigest()

# patch a method bind on cls
def binder(foreign_prop_id=None, foreign_prop=None, key_prop='id'):
    def decorator(cls):
        field = cls.__name__.lower()
        _foreign_prop_id = foreign_prop_id or field
        _foreign_prop = foreign_prop or field
        def bind(refs, foreign_prop_id=_foreign_prop_id, foreign_prop=_foreign_prop, key_prop=key_prop):
            if type(refs) is not list:
                return cls.bind([refs], foreign_prop_id, foreign_prop)
            ids = [ ref[foreign_prop_id] for ref in refs ]
            ids = list(set(ids))
            elements = cls.get(ids=ids, exclude_archived=False)
            cache = { getattr(e, key_prop): e for e in elements }
            for ref in refs:
                id = ref[foreign_prop_id]
                ref[foreign_prop] = cache.get(str(id))
            return refs

        cls.bind = bind
        return cls
    return decorator

def text_diff_all_is_punctuation(text1, text2):
    '''
    判断text1和text2之间的差异是否全是标点
    '''
    punctuation_list = [
        ".", ",", ";", ":", "?", "!", "-", "–", "—", "_", "'", "\"", "(", ")", "[", "]", "{", "}", "<", ">", "/", "\\",
        "|", "~", "`", "@", "#", "$", "%", "^", "&", "*", "+", "=", "°", "…", "·", "•", "‖", "‿", "⁀", "⁂", "⁃", "⁄", "⁇",
        "⁈", "⁉", "⁌", "⁍", "⁎", "⁑", "⁓", "⁕", "⁖", "⁗", "⁘", "⁙", "⁛", "⁜", "⁝", "⁞", "⁺", "⁻", "⁼", "⁽", "⁾", "ⁿ",
        "₊", "₋", "₌", "₍", "₎", "₏", "ₐ", "ₑ", "ₒ", "ₓ", "ₔ", "ₕ", "ₖ", "ₗ", "ₘ", "ₙ", "ₚ", "ₛ", "ₜ", "₝","∑", "−", "∓", 
        "∔", "∕", "∖", "∗", "∘", "∙", "√", "∛", "∜", "∝", "∞", "∣", "∤", "∥", "∦", "∧", "∨", "∩", "∪", "⊊", "⊋", "⊌", "⊍",
        "⊎", "⊏", "⊐", "⊑", "⊒", "⊓", "⊔", "⊕", "⊖", "⊗", "⊘", "⊙", "⊚", "⊛", "⊜", "⊝", "⊞", "⊟", "⊠", "⊡", "⊢", "⊣", "⊤", "⊥", "⋁", "⋂", "⋃","⋿",
        "，", "。", "、", "；", "：", "？", "（", "）", "［", "］", "｛", "｝", "《", "》", "〈", "〉", "【", "】", "‘", "’",
        "“", "”", "…", "—", "～", "￥", "·", "「", "」", "『", "』", "﹏", "︴", "｜", "﹁", "﹂", "﹃", "﹄", "︱", "︳", "︴",
        "😁", "😭", "😎", "😞","😌","😠"
    ]
    punctuation = "".join(punctuation_list)  # 包括中文标点
    text1_no_punct = re.sub(f"[{re.escape(punctuation)}]", "", text1)
    text2_no_punct = re.sub(f"[{re.escape(punctuation)}]", "", text2)
    return text1_no_punct == text2_no_punct


def content_diff(content1, content2):
    if isinstance(content1, str) and isinstance(content2, str):
        return text_diff_all_is_punctuation(content1, content2)
    if isinstance(content1, list) and isinstance(content2, list):
        return sorted(content1) == sorted(content2)
    return False
