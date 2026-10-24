def clean_win_path(p):
    p = p.replace("\\\\", "\\")
    return p

def get_flag(cc):
    if not cc or len(cc) != 2:
        return "🏳️"
    b = 127397
    return "".join(
        chr(b + ord(c))
        for c in cc.upper()
    )
