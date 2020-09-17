# Author: Xinyu Ma

dx = [-1, -1, -1, 0, 0, 1, 1, 1]
dy = [-1, 0, 1, 1, -1, -1, 0, 1]

# Problem 1
def longest_oscillation(alist):
    '''
    input: A list
    output: length of longest oscillation and longest oscillation
    time complexity: O(n)
    space complexity: O(n)
    optimal implementation:
    assume we have known all the oscillations for list [1, 5, 7] ([1], [5], [7], [1, 5], [1, 7], [5, 7])
    if we want to know the longest oscillation of list [1, 5, 7, 4], we only need to find the longest sub-list among [1], [5], [7], [1, 5], [1, 7], [5, 7], [1, 4], [5, 4], [7, 4], [1, 5, 4], [1, 7, 4], [5, 7, 4]
    so the problem of solving [1, 5, 7, 4] is equal to the problem of solving [1, 5, 7]
    and we can further optimize it:
    we do not need to store all the oscillations for list [1, 5, 7]
    [1], [5], [7], their length is the shortest, so there is no need to store them
    we can define an array, the length of oscillation is the index of our array plus one, the value in our array should include the last digit of the length under the oscillation and the expected value of next digit
    for example:
    when we reach 1 in list [1, 5, 7, 4], our current array is [1], and the next expected value is either greater than or less than 1
    when we reach 5, because 5 is greater than 1, so we add 5 into out array [1,5]
    then we hope next digit is less than 5, because from 1 to 5 is up
    when we reach 7, 7 is greater than 5, not the digit we expected, so we replace 5 with 7
    our array is now [1,7] and we hope next digit is less than 7
    so we can just use [1,7] to represent all the oscillations for list [1, 5, 7]
    every time we traverse one digit in out list, we change the last digit in our array
    '''
    if len(alist) <= 1:
        return (len(alist), [i for i in range(len(alist))])
    ans = [0]
    pos = 0
    for pos in range(1, len(alist)):
        if alist[pos] != alist[0]:
            ans.append(pos)
            break
    for i in range(pos+1, len(alist)):
        if alist[ans[-2]] - alist[ans[-1]] > 0:   # down
            if alist[ans[-1]] - alist[i] > 0:     # to down
                ans[-1] = i
            elif alist[ans[-1]] - alist[i] < 0:   # to up
                ans.append(i)
        elif alist[ans[-2]] - alist[ans[-1]] < 0: # up
            if alist[ans[-1]] - alist[i] > 0:     # to down
                ans.append(i)
            elif alist[ans[-1]] - alist[i] < 0:   # to up
                ans[-1] = i
    return (len(ans), ans)


# Problem 2
def length(M, step_len, i, j):
    '''
    input: M: a matrix
    i, j: row and column of each location
    step_len: record the longest walk with M[i][j] as the end point at each location
    implementation:
    if the step length has not been solved at this location (record as -1)
    when determining the walk, we traverse the 8 surrounding locations and record it as nx, ny
    if M[nx][ny] at this location is smaller than M[i][j], pass
    the maximum value of step_len[nx][ny] + 1 is the step_len[i][j]
    '''
    if step_len[i][j] != -1:
        return step_len[i][j]
    
    maxstep = -1
    for direction in range(8):
        nx = i + dx[direction]
        ny = j + dy[direction]
        if 0 <= nx < len(M) and 0 <= ny < len(M[0]):
            if M[nx][ny] < M[i][j]:
                maxstep = max(maxstep, length(M, step_len, nx, ny))
    if maxstep == -1:
        step_len[i][j] = 1
        return step_len[i][j]
    else:
        step_len[i][j] = maxstep + 1
        return step_len[i][j]


def nextxy(step_len, x, y):
    '''
    step_len: longest walk recorded for each location
    x, y: current location
    iterating through the walk of 8 locations around our current location
    if its walk is the walk of original location - 1, then the location of nx, ny can be used as the previous step of x, y
    so we return nx, ny
    '''
    for direction in range(8):
        nx = x + dx[direction]
        ny = y + dy[direction]
        if 0 <= nx < len(step_len) and 0 <= ny < len(step_len[0]):
            if step_len[nx][ny] == step_len[x][y] - 1:
                return nx, ny


def longest_walk(M):
    '''
    input: M: a matrix
    output: a sequence of values of M
    time complexity: O(n*m)
    space complexity: O(n*m)
    optimal implementation:
    we define step_len to record the longest walk at each location
    for example:
    [[1,2,3],
    [4,5,6],
    [7,8,9]]
    the walk of 5 can be obtained by the longest walk of 1, 2, 3, 4 plus one
    we see 2,4,5 around 1 are larger than 1, so the longest walk of 1 is 1
    only 1 around 2 is smaller than it, so the walk of 2 is 1+1 = 2 (the longest walk of 1 plus one)
    similarly, the walk of 3 is also the longest walk of 2 plus one, so 2+1 = 3
    the walk of 4 can be obtained by the longest walk of 1, 2 plus one, so 2+1 = 3
    the walk of 5 can be obtained by the longest walk of 1, 2, 3, 4 plus one, so 3+1 = 4
    and so on, the walk of 9 can be obtained by the walk of 8 plus one, so 6+1 = 7
    therefore, the longest walk of each location can be obtained by comparing up to 7 times (because we have at most 8 numbers)
    we can produce a step matrix:
    [[1,2,3],
    [3,4,5],
    [5,6,7]]
    through the maximum value 7 in the step matrix back to the location of 6, the location of 5, and the location of 4 , finally reach the location of 1, the path can be obtained.
    time complexity of this part is also O(n*m)
    space complexity of this part is also O(n*m)
    '''
    step_len = [[-1 for j in range(len(M[0]))] for i in range(len(M))]
    maxstep = -1
    maxposx = -1
    maxposy = -1
    for i in range(len(M)):
        for j in range(len(M[0])):
            tl = length(M, step_len, i, j)   # length() is used to determine the walk of M[i][j]
            if tl > maxstep:
                maxstep = tl
                maxposx = i 
                maxposy = j
    # backtracking path:
    ans = []
    nowstepsize = maxstep
    nowx = maxposx
    nowy = maxposy
    ans.append((nowx, nowy))
    while True:
        nowx, nowy = nextxy(step_len, nowx, nowy)
        ans.append((nowx, nowy))
        nowstepsize = step_len[nowx][nowy]
        if nowstepsize == 1:
            break
    return (len(ans), ans[::-1])

    
def main():
    alist = [ [1, 5, 7, 4, 6, 8, 6, 7, 1],
            [1, 5, 7, 8, 7, 1],
            [1, 1, 1, 1, 1],
            [1, 2, 3],
            [1, 2, 0, 3, 5],
            [1, 1, 3, 1, 2] ]
    for l in alist:
        print("list:", l, '\nlongest oscillation:', longest_oscillation(l))

    Ms = [
        [[1,2,3],
        [4,5,6],
        [7,8,9]],

        [[9,8,7],
         [2,1,6],
         [3,4,5]],

        [[1,2,3],
        [1,2,1],
        [2,1,3]],

        [[4,6],
        [7,2]],

        [[1, 2],
         [2, 3],
         [3, 4]]
        ]
    for M in Ms:
        print(longest_walk(M))

if __name__ == '__main__':
    main()
