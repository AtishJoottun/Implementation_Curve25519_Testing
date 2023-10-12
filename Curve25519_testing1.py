import random as rand

def montgomery_ladder(base_point, scalar):
    # Initialize two points
    R0 = (0, 1)  # Point at infinity
    R1 = base_point  # The base point

    # Bit length of the scalar
    bit_length = scalar.bit_length()

    for i in range(bit_length - 1, -1, -1):
        bit_i = (scalar >> i) & 1  # Get the i-th bit of the scalar

        # Select point based on the bit
        if bit_i == 0:
            R1 = add_points(R0, R1)
            R0 = double_point(R0)
        else:
            R0 = add_points(R0, R1)
            R1 = double_point(R1)

    # Resulting point is R0
    return R0

def double_point(point):
    # Elliptic curve point doubling
    if point == (0, 1):  # Point at infinity
        return (0, 1)

    x, y = point
    m = (3 * x**2 + 2*A*x + 1) * pow(2 * B * y, -1, P) % P
    x3 = (m**2 - 2 * x - A) % P
    y3 = (m * (x - x3) - y) % P

    return (x3, y3)

def add_points(point1, point2):
    # Elliptic curve point addition
    if point1 == (0, 1):  # Point at infinity
        return point2
    if point2 == (0, 1):  # Point at infinity
        return point1

    x1, y1 = point1
    x2, y2 = point2

    m = (y2 - y1) * pow(x2 - x1, -1, P) % P
    x3 = (m**2 - x1 - x2 - A) % P
    y3 = (m * (x1 - x3) - y1) % P

    return (x3, y3)

def encode_curve25519_public_key(public_key_x):
    encoded_public_key = bytes([0x40]) + public_key_x.to_bytes(32, byteorder='little')
    return encoded_public_key

P = 2**255 - 19
B = 1
A = 486662

# print(P, "\n")  # Prime field characteristic for Curve25519
base_point = (9, 14781619447589544791020593568409986887264606134616475288964881837755586237401)

# Random scalar for testing
# private_key = 12345678901234567890123456789012345678
private_key = rand.randint(1, 2^252 + 27742317777372353535851937790883648493)
print("Private Key:", private_key)
print("Encoded Private Key:", private_key.to_bytes(length=32, byteorder='little').hex())
print("\n")

resulting_point = montgomery_ladder(base_point, private_key)
print("Public Key:", resulting_point)

encoded_publicKey = encode_curve25519_public_key(resulting_point[0])
print("Encoded public key: ", encoded_publicKey.hex())


"""
OUTPUT
Private Key: 9910320097326844428298982393541014008
Encoded Private Key: f8b1cbe137b73da36766ff5381a8740700000000000000000000000000000000


Public Key: (49004429370549013129841224372446743908881098679645987423033937445411341868858, 699852680548864298996139262478235041123164475407390262673302344350666711624)
Encoded public key:  3a1f9ef491ec1baa3aeb2c6a3fb9eff10b181daf6c21d0140e7059522c86576c

"""
