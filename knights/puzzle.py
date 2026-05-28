from logic import *

AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# Puzzle 0
# A says "I am both a knight and a knave."
knowledge0 = And(  # Starting from the "And" logical connective, becasue each proposition represents knowledge that we know to be true.

    # translation of what A says
    Implication(AKnight, And(AKnight, AKnave)),

    # condition1 : can either be a knight or a knave
    Or(AKnight, AKnave),

    # if A claims to be both knight and knave
    # which is not posisble so A is a Knave
    Implication(AKnave, Not(And(AKnight, AKnave))),

)


# Puzzle 1
# A says "We are both knaves."
# B says nothing.
knowledge1 = And(

    # translation of what A says which can only be true if said by a knight
    Implication(AKnight, And(AKnave, BKnave)),

    # 4 combinations are possible


    # either (Knight, Knight)
    #        (Knight, Knave)
    #        (Knave, Knight)
    #        (Knave, Knave)

    Or(And(AKnight, BKnight), And(AKnight, BKnave), And(AKnave, BKnight), And(AKnave, BKnave)),

    # if a Knave says A and B are both Knaves
    # then A is a Knave for lying cause Knave would never tell the truth
    # But B is a Knight as A lied about B being a Knave

    Implication(AKnave, Not(And(AKnave, BKnave))),

)


# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
knowledge2 = And(

    # translation of what A says
    # A says we are either both Knight or both Knaves
    Implication(AKnight, Or(And(AKnave, BKnave), And(AKnight, BKnight))),

    # translation of what B says
    # B says we are different
    # which is correct cause one is clearly lying
    # if one is lying and one telling the truth , they are different

    Implication(BKnight, Or(And(AKnave, BKnight), And(AKnight, BKnave))),

    # 4 combinations are possible


    # either (Knight, Knight)
    #        (Knight, Knave)
    #        (Knave, Knight)
    #        (Knave, Knave)

    Or(And(AKnight, BKnight), And(AKnight, BKnave), And(AKnave, BKnight), And(AKnave, BKnave)),

    # if A is a Knave then they are different
    Implication(AKnave, Not(Or(And(AKnave, BKnave), And(AKnight, BKnight)))),


    # if B is a Knave then they are same
    Implication(BKnave, Not(Or(And(AKnave, BKnight), And(AKnight, BKnave)))),

)


# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
knowledge3 = And(

    # translation of what A says
    Implication(AKnight, And(Or(AKnight, AKnave))),

    # transaltion of what B says
    # C is a Knave
    # A supposedly said A is a Knave
    Implication(BKnight, And(CKnave, Or(Implication(
        AKnight, AKnave), Implication(AKnave, Not(AKnave))))),

    # transaltion of what C says
    # according to C , A is a Knight
    Implication(CKnight, AKnight),

    # in case A is a Knave
    # statement becomes false
    Implication(AKnave, Not(And(Or(AKnight, AKnave)))),

    # in case B is a Knave
    # statement becomes false
    # A does not say it is a Knave
    # C is not Knave
    Implication(BKnave, Not(
        And(CKnave, Or(Implication(AKnight, AKnave), Implication(AKnave, Not(AKnave)))))),

    # transaltion of what C says if C is a knave
    Implication(CKnave, Not(AKnight)),

    # What the possible combinations are
    # Each combination is ruled out as the AI deduces it
    # Possible Combinations = n^2-1
    # n = 3
    # Possible Combinations = 8
    Or(And(AKnight, BKnight, CKnight),
        And(AKnight, BKnight, CKnave),
        And(AKnight, BKnave, CKnight),
        And(AKnave,  BKnight, CKnight),
        And(AKnight, BKnave, CKnave),
        And(AKnave, BKnight, CKnave),
        And(AKnave, BKnave, CKnight),
        And(AKnave, BKnave, CKnave),
       )
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
