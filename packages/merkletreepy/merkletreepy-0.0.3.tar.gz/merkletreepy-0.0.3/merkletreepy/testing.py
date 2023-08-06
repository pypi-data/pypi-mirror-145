from web3 import Web3
import hashlib


from merkletreepy import MerkleTree


def web3_solidity_keccak(x):
    return Web3.keccak(x).hex()[2:]


def sha256(x):
    return hashlib.sha256(x).digest()


leaves = [sha256(leaf.encode()) for leaf in "abc"]
tree = MerkleTree(leaves, sha256)
root = tree.get_root()
leaf = sha256("a".encode())
bad_leaf = sha256("x".encode())
proof = tree.get_proof(leaf)
assert tree.verify(proof, leaf, root) == True
assert tree.verify(proof, bad_leaf, root) == False


# leaves = [
#     "0xAC0D2DC707C62C151135149DB9AD83BB29DA7AFE",
#     "0x435731F32287ED87C4B8A3BA842372BDBF192B5C",
#     "0x435731F32287ED8712313241232372BDBF192B5C",
# ]
# hashed_leaves = [web3_solidity_keccak(leaf.encode()) for leaf in leaves]
# tree = MerkleTree(hashed_leaves, web3_solidity_keccak, sort=True)
# root = tree.get_root()
# leaf = web3_solidity_keccak(leaves[1].encode())
# bad_leaf = web3_solidity_keccak(leaves[1].replace("1", "2").encode())
# proof = tree.get_proof(leaf)
# assert tree.verify(proof, leaf, root) == True, "keccak doesnt work"
# assert tree.verify(proof, bad_leaf, root) == False
