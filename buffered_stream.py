import sys
class BufferedStream:
    def __init__(self, stream=sys.stdin) -> None:
        self._stream = stream
        self._buffered = []

    def getc(self) -> str:
        if self._buffered:
            return self._buffered.pop(0)
        return self._stream.read(1)

    def ungetc(self, c) -> None:
        self._buffered.insert(0, c)

    def peek(self) -> str:
        if self._buffered:
            return self._buffered[0]
        c = self._stream.read(1)
        self._buffered.append(c)
        return c

    def remove_whitespace(self) -> None:
        c = self.getc()
        while c:
            if c == ' ':
                c = self.getc()
            elif c == '\n':
                c = self.getc()
            elif c == ';':
                c = self.getc()
                while c and c != '\n':
                    c = self.getc()
            else:
                self.ungetc(c)
                break
