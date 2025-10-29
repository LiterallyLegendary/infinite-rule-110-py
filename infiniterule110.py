class Rule110Position:
    bits: bin
    llength: int #how many leftward bits repeat infinitely to the left
    rlength: int #how many rightward bits repeat infinitely to the right

def infinitestep(bits: bin, llength: int, rlength:int) -> bin:
    #initialize output
    length:int = bits.bit_length() - 1
    if rlength <1 or llength <1:
        raise ValueError("don't set the length of the looping strings to less than 1.")
    #apply Rule 110 to the position
    newbits: bin = finitestep(((((((bits>>length-llength) % 4) - 1)*(1+2*(llength==1)) <<
                                     length) + bits) << 2) +
                              ((bits >> (rlength - 2)) % 4  if rlength>1 else bits%2*3)) >> 1

    #we need to simplify the position if bits are found in the middle string that repeat the leftmost or rightmost strings
    cutl:int = ~(newbits>>(length - llength) ^ newbits>>length) & 2+(length>llength+1) 
    cutr:int = ~(newbits>>rlength ^ newbits) & 1+2*(length>rlength+1)
    #the logic after the & is to make sure we're not overcutting when llength/rlength is close to length
    leading1: int = length+2- cutl//2*(1+cutl%2) - cutr%2 * (1 - cutr//2)

    #cutting the new position and returning it (this program does not do it to the fullest extent possible)
    return (newbits >> (cutr%2 * (1 + cutr//2))) % (1<<leading1) + (1<<leading1)

def finitestep(x: bin) -> bin:
    return (~x>>1)&x|x^(x<<1)

def main() -> None:
    pos = Rule110Position()
    pos.bits = int('1'+input("Please enter a string of binary digits to simulate"),2)
    pos.llength = int(input("How many digits on the left infinitely repeat?"))
    pos.rlength = int(input("How many digits on the right infinitely repeat?"))
    j: int = int(input("How many steps would you like to simulate this for?"))
    for i in range(j):
        pos.bits = infinitestep(pos.bits, pos.llength, pos.rlength)
        print(bin(pos.bits)[3:])
    input("Simulation finished, press enter to continue")

if __name__ == "__main__":
    main()

#maybe i improve this with (~x)>>1&x|x^(x<<1)

