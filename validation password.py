def password_validation(a: str) -> bool:
    contain_chr = []
    for i in a:
        if not contain_chr.count(i):
            contain_chr.append(i)
    if len(contain_chr) >= 3:
        if not a.count('password') and not a.count('PASSWORD'):
            if 6 < len(a) <= 9:
                return any(map(str.isdigit, a)) and any(map(str.isalpha, a))
            else:
                return len(a) > 9
        else:
            return False
    else:
        return False