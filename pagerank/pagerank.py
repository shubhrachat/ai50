import copy
import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    # dictionary with keys of page
    # values of probability
    # currently set to null
    nextpage_prob = {}

    # length of current dictionary
    # gives us the number of pages
    # in the corpus dictionary
    total_pages = len(corpus)

    # The corpus is a Python dictionary mapping a page name
    # to a set of all pages linked to by that page.
    # As mentioned above accessing page
    # will give us to pages linked to each page
    # in the corpus dictionary
    linked_pages = len(corpus[page])

    # if there are linked pages
    if linked_pages != 0:

        # for every name of page in corpus
        # choose one of all pages
        # if the name of the page is also present
        # in its linked pages
        # add probability of one of the links from page

        for name in corpus.keys():

            # stores probability of choosing page in null dictionary
            # key = name : value = probability
            nextpage_prob[name] = (1 - damping_factor) / total_pages

            if name in corpus[page]:

                # adds probability of choosing link in dictionary
                # key = name : value = probability
                nextpage_prob[name] += damping_factor / linked_pages

    # when no linked pages
    else:

        # choose at random from pages with equal probability

        for name in corpus.keys():

            nextpage_prob[name] = 1 / total_pages

    # return dictionary with name and probaility of page
    return nextpage_prob


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # a Python dictionary which will have
    # one key for each page in the corpus

    pagerank = {}

    # for every page in corpus
    # set it to 0
    for name in corpus:

        pagerank[name] = 0

    # for every page in sample
    for i in range(0, n):

        # for first sample generate by choosing from a page at random
        if i == 0:

            # converting dictionary to an iterable sequence
            # and then using choice to choose randomly from sequence
            page = random.choice(list(corpus))

        pagerank[page] += 1

        # the remaining samples should be generated based on the previous sample’s transition model
        remaining = transition_model(corpus, page, damping_factor)

        # remaining identifier has a dictionary
        # to access the probabilities for the next sample
        # we have to access the values

        # convert to iterable form
        # and access values
        prob_values = list(remaining.values())
        page = random.choices(list(remaining.keys()), weights=prob_values)[0]

    for rank in pagerank:
        # we assume the PageRank of every page is 1 / N
        pagerank[rank] = pagerank[rank] / n

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # original pagerank values
    pagerank = {}

    # stores pagerank values after updation
    pagerank2 = {}

    # setting N
    N = len(corpus)

    # Setting page values
    for name in corpus:
        pagerank[name] = 1 / N

    # setting a flag
    flag = True

    # when delta value is > 0.001
    while flag:

        # for every page in pagerank
        for name in pagerank:
            sum = 0

            # for every page in corpus
            for page in corpus:

                # if in corpus Summation PR(i) / Numlinks(i)
                if name in corpus[page]:
                    ev = pagerank[page] / len(corpus[page])
                    sum += ev

                if not corpus[page]:
                    ev = pagerank[page] / N
                    sum += ev

            # Updating using formula -
            # PR(A) = (1 – d ) + d ( PR(t1) / C(t1) + ... + PR(tn)/C(tn) )
            pagerank2[name] = (1 - damping_factor) / N + sum * damping_factor

        # change in pagerank
        # absolute value
        # then maximum of abs
        delta = max(abs(pagerank[page] - pagerank2[page]) for page in pagerank)

        # if less than 0.001
        # exit while loop
        if delta < 0.001:
            flag = False
            break

        else:
            # else go in with pagerank2 values and continue
            flag = True
            pagerank = pagerank2.copy()

    return pagerank


if __name__ == "__main__":
    main()
