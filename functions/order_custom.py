import numpy as np
import matplotlib.pyplot as plt

def test_02(Obj):
    
    n_l = np.array(Obj.node_list)
    n_d = np.array(Obj.degrees)
    
    def getSmallest(A):
        counts = np.sum(A, axis=1)
        return np.argwhere(counts == np.min(counts))
    
    corners = getSmallest(Obj.A).ravel().tolist()
    
    unique, counts = np.unique(n_d, return_counts=True)
    stats = dict(zip(unique, counts))
    print (stats)
    print (len(stats), 'unique situations in a perfectly homogenous milieu')
           
    # 1. isolate low degree nodes -> boundaries
    #    make a submatrix
    
    edges_idx = np.argwhere((n_d >= 8) & (n_d <= 14))
    print (edges_idx.shape)

    A_edges = Obj.A[edges_idx.ravel()][:,edges_idx.ravel()]
    n_l2 = n_l[edges_idx.ravel()]
    n_d2 = n_d[edges_idx.ravel()]
    
    print (Obj.A.shape, A_edges.shape)
    print (n_l2.shape, n_d2.shape)
    
    # 2. reconstruct the boundaries    
    sequences = []
       
    for i in range(len(n_l2)):
        
        delta = A_edges - A_edges[i,:]
        delta[i,:] = 1
        delta[:,i] = 1
        identities = np.argwhere(np.sum(np.abs(delta), axis=1) == np.min(np.sum(np.abs(delta), axis=1)))
        
        if len(n_l2[identities.ravel()]) > 1:
            l = [n_l2[identities.ravel()][0], n_l2[i], n_l2[identities.ravel()][1]]
        else:
            l = [n_l2[identities.ravel()][0], n_l2[i]]
        
        sequences.append(l)
        
    def reduce(sequences):
        for s1 in sequences.copy():
            for s2 in sequences.copy():
                if s1!=s2:
                    if s1[-1] == s2[0] and s1[-2] != s2[1]:
                        s3 = s1[:-1] + s2
                        try: sequences.remove(s1)
                        except: pass
                        try: sequences.remove(s2)
                        except: pass
                        if s3 not in sequences: sequences.append(s3) 
                    elif s1[0] == s2[-1] and s1[1] != s2[-2]:
                        s3 = s2 + s1[1:]
                        try: sequences.remove(s1)
                        except: pass
                        try: sequences.remove(s2)
                        except: pass
                        if s3 not in sequences: sequences.append(s3) 
                    elif s1[::-1][-1] == s2[0] and s1[::-1][-2] != s2[1]:
                        s3 = s1[::-1][:-1] + s2
                        try: sequences.remove(s1)
                        except: pass
                        try: sequences.remove(s2)
                        except: pass
                        if s3 not in sequences: sequences.append(s3) 
                    elif s1[::-1][0] == s2[-1] and s1[::-1][1] != s2[-2]:
                        s3 = s2 + s1[::-1][1:]
                        try: sequences.remove(s1)
                        except: pass
                        try: sequences.remove(s2)
                        except: pass
                        if s3 not in sequences: sequences.append(s3)   

        for s1 in sequences.copy():
            for s2 in sequences.copy():
                if s1!=s2:
                    # print (set(s1)-set(s2))
                    if len(set(s1)-set(s2)) == 0:
                        try: sequences.remove(s1)
                        except: pass
                    elif len(set(s2)-set(s1)) == 0:
                        try: sequences.remove(s2)
                        except: pass
                    
        return sequences
    
    print (sequences)
                    
    sequences = reduce(sequences)
    sequences = reduce(sequences)
    
    beginnings = [s[0] for s in sequences] + [s[-1] for s in sequences]
    
    for i in range(len(beginnings)):
        
        idx = np.argwhere(n_l2==beginnings[i]).ravel()
        delta = A_edges - A_edges[idx,:]
     
        delta[idx,:] = 1
        delta[:,idx] = 1
        identities = np.argwhere(np.sum(np.abs(delta), axis=1) == np.min(np.sum(np.abs(delta), axis=1)))
        
        if len(n_l2[identities.ravel()]) > 1:
            l = [n_l2[identities.ravel()][0], n_l2[i], n_l2[identities.ravel()][1]]
        else:
            l = [n_l2[identities.ravel()][0], n_l2[i]]
        
        print (beginnings[i], n_l2[identities.ravel()])
                    
    for s in sequences:
        print (s)

def test_01(Obj, substract=1):    
    
    n_l = np.array(Obj.node_list)
    n_d = np.array(Obj.degrees)
    
    def getSmallest(A):
        counts = np.sum(A, axis=1)
        return np.argwhere(counts == np.min(counts))
    
    corners = getSmallest(Obj.A).ravel().tolist()
    
    visited = []    
    next_idx = corners[0]

    next_item = n_l[next_idx]
    visited.append(next_idx)
    n_d[np.argwhere(Obj.A[next_idx]).ravel()] -= substract
    
    for i in range(len(Obj.node_list)):
        cand_idx = np.argwhere(Obj.A[next_idx]).ravel()
        cand_idx = np.setdiff1d(cand_idx, visited)
        ord_next = cand_idx[np.argsort(n_d[cand_idx])[:1]]
        if len(ord_next)==0:
            break
        n_d[np.argwhere(Obj.A[ord_next]).ravel()] -= substract
        
        next_idx = ord_next.ravel().tolist()
        visited += next_idx

    return n_l[visited]