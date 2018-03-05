class SStack(object):
    def __init__(self):
        self.__element = []

    def top(self):
        if not self.__element:
            raise ValueError('stack is empty')
        return self.__element[-1]

    def pop(self):
        return self.__element.pop()

    def has(self, item):
        # todo
        return item in self.__element

    def push(self, item):
        self.__element.append(item)

    def is_empty(self):
        return self.__element == []

    def items(self):
        return "".join(self.__element)


class Solution(object):
    def removeDuplicateLetters(self, s):
        """
        :type s: str
        :rtype: str
        """
        if not s:
            return s
        stack = SStack()
        stack.push(s[0])
        for index, c in enumerate(s[1:]):
            # 已经在栈中，直接丢弃
            if stack.has(c):
                continue

            if c == stack.top():
                continue
            # c 大于top
            elif c > stack.top():
                stack.push(c)
            # c 小于top
            else:
                while not stack.is_empty() and c < stack.top() and stack.top() in s[1+index:]:
                    stack.pop()
                stack.push(c)
        return stack.items()


def main():
    s = 'cbacdcbc'
    # s = 'bbcaac'
    # s = 'bcabc'

    print(Solution().removeDuplicateLetters2(s))
    pass

if __name__ == '__main__':
    main()
