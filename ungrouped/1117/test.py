def reverse(s: str) -> bool:
    s = s.lower()
    s = "".join(list(filter(lambda x: ord('a') <= ord(x) and ord(x) <= ord('z'), [a for a in s])))
    return s[::-1] == s

print(reverse("hello"))  # Fal
print(reverse("A man, a plan, ac anal: Panama"))
