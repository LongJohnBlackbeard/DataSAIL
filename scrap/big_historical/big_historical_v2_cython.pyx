# author: Alexander DeForge
# date: 03/06/2021
# purpose: helper functions in cython for wsbData_posts_tickers_digest_v2.py
# organization: Lewis University DataSAIL, Dr. Szczurek, Spring 2021
# version: 2


cpdef str aggregate_bodies(list bodies):
    cdef str result = ""
    cdef str delimiter = " "

    cdef int i
    cdef int bodies_length = len(bodies)
    for i in range(bodies_length):
        result = result + delimiter + bodies[i]
    return result

cpdef list process_pos_tokens(list pos_tokens, list target_pos_tags):
    cdef list result = []

    cdef int i
    cdef int pos_tokens_length = len(pos_tokens)
    for i in range(pos_tokens_length):
        if pos_tokens[i][1] in target_pos_tags:
            result.append(pos_tokens[i])
    return result

cpdef object parse_tickers(list corpus, list tickers):
    cdef int occurrences = 0
    result = {}

    cdef int i
    cdef int j
    cdef int tickers_length = len(tickers)
    cdef int corpus_length = len(corpus)
    for i in range(tickers_length):
        occurrences = 0
        token = tickers[i]
        for j in range(corpus_length):
            if token.lower() in corpus[j]:
                occurrences = occurrences + 1
        result[token] = occurrences
    return result

cpdef object parse_pos_tokens(list corpus, list target_pos_tokens):
    cdef int occurrences = 0
    result = {}
    cdef str delimiter = " "

    cdef int i
    cdef int j
    cdef int k = 0
    cdef int l
    cdef int corpus_length = len(corpus)
    cdef int target_pos_tokens_length = len(target_pos_tokens)
    cdef list pos_tokens = []
    cdef int pos_tokens_length = 0

    # for each company name, iterate over corpus looking for occurrences
    for i in range(target_pos_tokens_length):
        occurrences = 0
        pos_tokens = target_pos_tokens[i]
        pos_tokens_length = len(target_pos_tokens[i])
        for j in range(corpus_length):
            # if the tags match and the values match, we have a match
            if corpus[j][1] == pos_tokens[k][1] and corpus[j][0].lower() == pos_tokens[k][0].lower():
                k = k + 1
                # if we have matched the whole company name, we have an occurrence
                if k >= pos_tokens_length:
                    occurrences = occurrences + 1
                    k = 0  # reset for another match
            else:
                if k > 0:
                    j = j - 1  # stay put in corpus on partial mismatch
                    k = 0  # reset for another match
        result[pos_tokens[0][0]] = occurrences
    return result
