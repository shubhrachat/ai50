import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """

    # storing parents probability
    parents = {}

    joint_probability = 1

    # for every person in people csv
    for person in people:

        # we should check how many bad genes they have

        # if person in one bad gene set
        if person in one_gene:
            bad_gene = 1

        # if person in two bad gene set
        elif person in two_genes:
            bad_gene = 2

        # if person in neither sets
        # then person has no bad genes
        # so 0 bad genes :)
        else:
            bad_gene = 0

        # unconditional probability for number of bad genes
        # this probabilty is relevant in case of no parent
        # probability is unconditional

        # storing probability calling gene dictionary
        unconditional_probability = PROBS["gene"][bad_gene]

        # checking if the trait is apparent for the person
        # with their number of bad genes

        # accessing nested trait dictionary
        # for bad gene
        # then accessing second nest for trait
        # NESTED

        if person in have_trait:
            trait = True
        else:
            trait = False

        apparency = PROBS["trait"][bad_gene][trait]

        # storing parents
        mother = people[person]["mother"]
        father = people[person]["father"]

        # checking whether parents exist

        # if parents exist probability is conditional
        # else uncondiitonal

        if mother is None and father is None:

            # compute final unconditional probability
            joint_probability *= unconditional_probability * apparency

        # when parents exist
        # conditions exist
        else:

            # computing parents probabilities

            # storing probability for either parent
            for parent in [mother, father]:

                # parent has one bad gene
                if parent in one_gene:

                    # if one bad gene
                    # then one good gene and 1/2 possibility of bad gene
                    parents[parent] = 0.5

                # parent has two bad genes
                elif parent in two_genes:

                    # then getting bad gene probability
                    # unless mutation happens
                    parents[parent] = (1 - PROBS["mutation"])

                # parent has no bad gene
                else:
                    # only possibility of getting bad gene
                    # is mutation
                    parents[parent] = PROBS["mutation"]

            # now that parents probability is stored
            # we can compute joint probability

            if bad_gene == 2:

                # both parents have to have bad genes only
                # Bad AND Bad
                joint_probability *= (parents[mother]) * (parents[father])

            elif bad_gene == 1:

                # one parent has bad gene
                # Either Bad mom AND Good dad
                # or Good mom AND Bad dad
                joint_probability *= (parents[mother]) * (1 - parents[father]) + \
                    (1 - parents[mother]) * (parents[father])

            else:
                # neither have bad genes
                # Good mom AND Good dad
                joint_probability *= (1 - parents[mother]) * (1 - parents[father])

            # conditional probability calculated
            # checking whether trait present or absent
            # multiplying the final probability with apparency
            # and getting the joint probability

            joint_probability *= apparency

    return joint_probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """

    # for every persons' data in probabilities
    for person in probabilities:

        if person in one_gene:

            bad_gene = 1

        elif person in two_genes:

            bad_gene = 2

        else:
            bad_gene = 0

        # Each person gene distrbution being updated
        probabilities[person]["gene"][bad_gene] += p

        # Each person trait distrbution being updated

        # checking whether value is True or False
        if person in have_trait:

            probabilities[person]["trait"][True] += p

        else:

            probabilities[person]["trait"][False] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    sum1 = 0

    # for every person in nested dictionary
    for person in probabilities:

        # each persons has data as either gene or trait
        # accessing both
        for data in ["gene", "trait"]:

            # summing up each value for each person in gene and trait
            sum1 = sum(probabilities[person][data].values())

            # for every value inside person and type of data
            for calculations in probabilities[person][data]:

                # normalize the value
                normal_value = probabilities[person][data][calculations] / sum1

                # after normalizing store the value of the probability
                probabilities[person][data][calculations] = normal_value


if __name__ == "__main__":
    main()
