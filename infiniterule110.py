class Rule110Position:
    bits: bin
    llength: int #how many leftward bits repeat infinitely to the left
    rlength: int #how many rightward bits repeat infinitely to the right
    xpos: int

def infinitestep(pos1: Rule110Position) -> None:
    #initialize output
    length:int = pos1.bits.bit_length() - 1
    if pos1.rlength <1 or pos1.llength <1:
        raise ValueError("don't set the length of the looping strings to less than 1.")
    #apply Rule 110 to the position
    newbits: bin = finitestep(((((((pos1.bits>>length-pos1.llength) % 4) - 1)*(1+2*(pos1.llength==1)) <<
                                     length) + pos1.bits) << 2) +
                              ((pos1.bits >> (pos1.rlength - 2)) % 4  if pos1.rlength>1 else pos1.bits%2*3)) >> 1

    #we need to simplify the position if bits are found in the middle string that repeat the leftmost or rightmost strings
    cutl:int = ~(newbits>>(length - pos1.llength) ^ newbits>>length) & 2+(length>pos1.llength+1) 
    cutr:int = ~(newbits>>pos1.rlength ^ newbits) & 1+2*(length>pos1.rlength+1)
    #the logic after the & is to make sure we're not overcutting when llength/rlength is close to length
    leading1: int = length+2- cutl//2*(1+cutl%2) - cutr%2 * (1 - cutr//2)

    #simplifying the new position (this program does not simplify to the fullest extent possible)
    pos1.bits = (newbits >> (cutr%2 * (1 + cutr//2))) % (1<<leading1) + (1<<leading1)
    pos1.xpos += cutl//2*(1+cutl%2)-1

def finitestep(x: bin) -> bin:
    return (~x>>1)&x|x^(x<<1)

def main() -> None:
    pos = Rule110Position()
    pos.bits = int('1'+input("Please enter a string of binary digits to simulate"),2)
    pos.llength = int(input("How many digits on the left infinitely repeat?"))
    pos.rlength = int(input("How many digits on the right infinitely repeat?"))
    pos.xpos = 0
    j: int = int(input("How many steps would you like to simulate this for?"))
    for i in range(j):
        infinitestep(pos)
        print(bin(pos.bits)[3:])
    print(f'Relative xpos of leftmost non-repeating bit: {pos.xpos}')
    input("Simulation finished, press enter to continue")

if __name__ == "__main__":
    main()

#maybe i improve this with (~x)>>1&x|x^(x<<1)
