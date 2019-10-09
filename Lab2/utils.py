# helper functions
def vector_add(v1, v2):
    assert(len(v1) == len(v2))
    sum = len(v1)*[0]
    for i in range(len(v1)):
        sum[i] = v1[i]+v2[i]
    return sum

def vector_sub(v1, v2):
    assert(len(v1) == len(v2))
    sum = len(v1)*[0]
    for i in range(len(v1)):
        sum[i] = v1[i]-v2[i]
    return sum

def vector_dot(v1, v2):
    assert(len(v1) == 2 & len(v2) == 2)
    # a · b = ax × bx + ay × by
    return v1[0]*v2[0] + v1[1]*v2[1]

def vector_mag_sq(v):
    mag_sq = 0
    for p in v:
        mag_sq+=(p*p)
    return mag_sq

def vector_scalar_mul(v, sc):
    mul = len(v)*[0]
    for i in range(len(v)):
        mul[i] = sc*v[i]
    return mul

def vector_scalar_div(v, sc):
    assert(sc != 0)
    for i in range(len(v)):
        v[i] = v[i]/sc
    return v

def vector_vector_mul(v1,v2):
    assert(len(v1) == len(v2))
    res = len(v1)*[0]
    for i in range(len(v1)):
        res[i] = v1[i]*v2[i]
    return res

def vector_del(delv, delr):
    assert(len(delv) == len(delr))
    neg_r = vector_scalar_mul(delr, -1)
    dot_rv = vector_dot(delr, delv)
    num = vector_scalar_mul(neg_r, dot_rv)
    den = vector_mag_sq(delr)
    return vector_scalar_div(num, den)


   