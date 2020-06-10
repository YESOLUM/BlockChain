import hashlib
import datetime


class Block:
    """
    lash_hash : 마지막 생성된 블록의 해시
    next_index : 마지막 생성된 블럭의 갯수
    """
    __last_hash = None
    __next_index = 0

    def __init__(self, data=None):
        """
        index : 블록이 생성된 순서
        timestamp : 블록이 생성된 시간
        data : 블록이 가지고 있는 이력
        prev_hash : 이전블록의 해시
        hash : 현재 블록의 해시
        :param data:
        """
        self.index = Block.__next_index
        self.timestamp = datetime.datetime.now()
        self.data = data
        self.prev_hash = Block.__last_hash
        self.hash = self.__cal_hash()
        Block.__next_index += 1
        Block.__last_hash = self.hash

    def __cal_hash(self, _hash="hash"):
        encodes = [str(value).encode() for key, value in list(self.__dict__.items()) if key != _hash]
        for encode in encodes:
            encodes[0] += encode
        return hashlib.sha256(encodes[0]+str("hello!").encode()).hexdigest()

    def __check_hash(self):
        return self.hash == self.__cal_hash()

    @classmethod
    def __compare(cls, cur, prev):
        return cur.prev_hash == prev.__cal_hash()

    @classmethod
    def is_valid(cls, blocks):
        for i, block in enumerate(blocks):
            if not block.__check_hash():
                return False
            if i:
                if not cls.__compare(blocks[i], blocks[i-1]):
                    return False
        return True

    def __str__(self):
        return f"{self.__dict__}"


class BlockChain:
    def __init__(self, block):
        self.blocks = list()
        self.__create_genesis(block)

    def __create_genesis(self, block):
        self.add(block)

    def add(self, block):
        self.blocks.append(block)

    def __str__(self):
        return "\n".join(map(str, self.blocks))


bc = BlockChain(Block())
for i in range(5):
    words = input("메세지를 입력하세요\n")
    bc.add(Block(words))
print(bc)
print(Block.is_valid(bc.blocks))
bc.blocks[2].data = 1998
print(bc)
print(Block.is_valid(bc.blocks))