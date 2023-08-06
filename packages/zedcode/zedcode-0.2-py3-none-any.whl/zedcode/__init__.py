
def substring(s):
    '''
    Author: Kishan Mishra
    Returns a list containing all the substrings of inputted string
    :param s: String whose substrings you need
    :return: a list containing all the substrings of a list
    '''
    res=[] #Empty list
    n=len(s)
    #logic
    for i in range(n):
        for j in range(i + 1, n + 1):
            res.append(s[i:j])

    return res #returns a list of all substrings


def subarray(arr):
    '''
    Author: Kishan Mishra
    Print subarrays of an array.
    :param arr: Array whose subarrays you need to print
    :return: It prints all the subarrays of the array
    '''
    n=len(arr)
    for i in range(0, n):

        # Pick ending point
        for j in range(i, n):

            # Print subarray between
            # current starting
            # and ending points
            for k in range(i, j + 1):
                print(arr[k], end=" ")

            print("\n", end="")


def fibonacci(n,k):
    '''
    Author: Kishan Mishra
     Returns a list of fibonacci series till nth term.
     Returns nth term of fibonacci series.

    :param n: till which term series should continue.
    :param k: the kth term of fibonacci series .
    :return: returns a list of fibonacci series if k is not mentioned
    else return nth term of fibonaccci series.
    '''

    lis=[0,1]
    for i in range(2,n):
        lis.append(lis[i-2]+lis[i-1])
    if k>0:
        return (lis[0:n])[k]
    else:
        return(lis[0:n])


def nthfibo(n):
    '''
    Author: Kishan Mishra
    Function to calculate nth term of fibonacci series.
    :param n: nth term to retrieve (based on 0-indexing list )
    :return: value at nth term
    '''
    v1, v2, v3 = 1, 1, 0
    for rec in bin(n)[3:]:
        calc = v2*v2
        v1, v2, v3 = v1*v1+calc, (v1+v3)*v2, calc+v3*v3
        if rec == '1':
            v1, v2, v3 = v1+v2, v1, v2
    return v2



def longestPalSubstring(s):
    """
    Author: Kishan Mishra
    Returns the longest palindromic substring from a given string
    :param s: String whose longest palindromic substring you want to find
    :return: Return longest palindromic substring
    """

    def printSubstring(str, left, right):
        st = ""
        for i in range(left, right + 1):
            st += str[i]
        return st

    strLen = 2 * len(s) + 3
    sChars = [0]*strLen
    sChars[0] = '@'
    sChars[strLen - 1] = '$'
    t = 1
    for i in s:
        sChars[t] = '#'
        t += 1
        sChars[t] = i
        t += 1

    sChars[t] = '#'

    maxLen = int(0)
    start = int(0)
    maxRight = int(0)
    center = int(0)
    p = [0] * strLen
    for i in range(1, strLen - 1):
        if i < maxRight:
            p[i] = min(maxRight - i, p[2 * center - i])
        while sChars[i + p[i] + 1] == sChars[i - p[i] - 1]:
            p[i] += 1
        if i + p[i] > maxRight:
            center = i
            maxRight = i + p[i]
        if p[i] > maxLen:
            start = int((i - p[i] - 1) / 2)
            maxLen = p[i]
    return printSubstring(s, start, start + maxLen - 1)


def spermutations(word):
    '''
    Author:Kishan Mishra
    :param word: String whose permutation you want to find.
    :return: list of string permutation
    '''
    if len(word) == 1:
        return word
    perms = spermutations(word[1:])
    char = word[0]
    res = []
    for perm in perms:
        for i in range(len(perm) + 1):
            res.append(perm[:i] + char + perm[i:])
    return res

#---------- BINARY OPERATIONS -------------------
def powx(a,b):
    """
    Author: Kishan Mishra
    To computer power of a and b
    :param a: base
    :param b: power
    :return: return a raised to the power b
    """
    m = int(1000000007)
    a=a%m
    b=b%m
    res=int(1)
    while b>0:
        if (b%2==1):
            res=res*a%m
        b=int(b/2)
        a=a*a%m
    return res

def reversedBits(X):
    """
    Author: Kishan Mishra
    Reverses a binary string into decimal value
    :param X: Binary string of length 32
    :return: Integer value of reversed bits
    """
    b = bin(X)[2:]
    if len(b) < 32:
        x = 32 - len(b)
        b = ("0" * x) + b
        b = b[::-1]
        return int(b, 2)
    else:
        b = b[::-1]
        return int(b, 2)
def countsetbits(N):
    """
    Author:Kishan Mishra
    Count number of set bits
    :param N: Positive integer N
    :return: returns number of set bits
    """
    return bin(N)[2:].count("1")

def countBitsFlip(a, b):
    """
    Author: Kishan Mishra

    :param a: Decimal Number
    :param b: Decimal Number
    :return: Returns number of bits needed to be flipped to convert A to B.
    """
    res = a ^ b
    count = 0
    while res:
        if res & 1:
            count += 1
        res >>= 1
    return count

def searchRange(nums, target):
    '''
    A sorted array arr containing n elements with possibly duplicate elements,
    the task is to find indexes of first and last occurrences of an element target in the given array.
    :param nums:a sorted array arr
    :param target: element
    :return: indexes of first and last occurrences of an element x
    '''

    def startIndexBinarySearch(start, end):
        if (start < end):
            mid = start + (end - start) // 2
            # print(mid)
            if (nums[mid] == target):
                if (mid > 0 and nums[mid - 1] == target):
                    return startIndexBinarySearch(start, mid)
                return mid

            if (nums[mid] > target):
                return startIndexBinarySearch(start, mid)
            return startIndexBinarySearch(mid + 1, end)
        return -1

    def endIndexBinarySearch(start, end):
        if (start < end):
            mid = start + (end - start) // 2
            # print(mid)
            if (nums[mid] == target):
                if (mid + 1 < len(nums) and nums[mid + 1] == target):
                    return endIndexBinarySearch(mid + 1, end)
                return mid

            if (nums[mid] > target):
                return endIndexBinarySearch(start, mid)
            return endIndexBinarySearch(mid + 1, end)
        return -1

    startIndex = startIndexBinarySearch(0, len(nums))
    if startIndex == -1:
        return [-1, -1]

    endIndex = endIndexBinarySearch(0, len(nums))

    return [startIndex, endIndex]


def StringSearch(pat, txt):
    """
    Returns the strating index of the pattern in the string ,
    :param pat: pattern
    :param txt: string
    :return: firt occurance of pattern
    """

    def computeLPSArray(pat, M, lps):
        len = 0
        # lps[0]
        i = 1
        while i < M:
            if pat[i] == pat[len]:
                len += 1
                lps[i] = len
                i += 1
            else:
                if len != 0:
                    len = lps[len - 1]
                else:
                    lps[i] = 0

                    i += 1
    M = len(pat)
    N = len(txt)
    lps = [0] * M
    j = 0
    computeLPSArray(pat, M, lps)
    i = 0
    while i < N:
        if pat[j] == txt[i]:
            i += 1
            j += 1

        if j == M:
            k=str(i-j)
            j = lps[j - 1]
            return k
        elif i < N and pat[j] != txt[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1


def nprimes(n):
    '''
    Author: Kishan Mishra
    Find prime numbers from 1 to n
    :param n: Nth term
    :return: List containing prime numbers from 1 to n
    '''
    primes = []
    prime_bool = [True for i in range(n + 1)]
    p = 2
    while (p * p <= n):
        if (prime_bool[p] == True):
            for i in range(p * p, n+1, p):
                prime_bool[i] = False
        p += 1
    for p in range(2, n+1):
        if prime_bool[p]:
            primes.append(p)
    return primes


def printalgos():
    """
    Author:Kishan Mishra
    Some mostly used data structure and algorithms frames.
    :return:
    """
    print("1.Binary Search")
    print("2.Stack")
    print("3.Queue")
    print("4.Linked-list")
    print("5.Bubble sort")
    print("6.Insertion sort")
    print("7.Selection sort")
    print("8.Merge sort")
    print("9.Binary Search in martrix")
    print("10.Longest common subsequence")
    print("11.Compute Permutations")
    print("12.Compute Combinations")
    print("13.Generate Prime Numbers in 1-N")
    print("14.Largest Palindromic String")
    print("15. LCM and HCF")

    bsr = '''def binary_search(arr, x):
        low = 0
        high = len(arr) - 1
        mid = 0

        while low <= high:

            mid = (high + low) // 2

            if arr[mid] < x:
                low = mid + 1

            elif arr[mid] > x:
                high = mid - 1
            else:
                return mid
        return -1'''
    st = '''class Stack:
        def __init__(self, max_size):
            self.__max_size = max_size
            self.__elements = [None] * self.__max_size
            self.__top = -1

        def get_max_size(self):
            return self.__max_size

        def is_full(self):
            if (self.__top == self.__max_size - 1):
                return True
            return False

        def is_empty(self):
            if (self.__top == -1):
                return True
            return False

        def push(self, data):
            if (self.is_full()):
                print("The stack is full!!")
            else:
                self.__top += 1
                self.__elements[self.__top] = data

        def pop(self):
            if (self.is_empty()):
                print("The stack is empty!!")
            else:
                data = self.__elements[self.__top]
                self.__top -= 1
                return data

        def display(self):
            if (self.is_empty()):
                print("The stack is empty")
            else:
                index = self.__top
                while (index >= 0):
                    print(self.__elements[index])
                    index -= 1

        # You can use the below __str__() to print the elements of the DS object while debugging
        def __str__(self):
            msg = []
            index = self.__top
            while (index >= 0):
                msg.append((str)(self.__elements[index]))
                index -= 1
            msg = " ".join(msg)
            msg = "Stack data(Top to Bottom): " + msg
            return msg'''
    qu = """class Queue:
    def __init__(self,max_size):
        self.__max_size=max_size
        self.__elements=[None]*self.__max_size
        self.__rear=-1
        self.__front=0

    def is_full(self):
        if(self.__rear==self.__max_size-1):
                return True
        return False

    def is_empty(self):
        if(self.__front>self.__rear):
            return True
        return False

    def enqueue(self,data):
        if(self.is_full()):
            print("Queue is full!!!")
        else:
            self.__rear+=1
            self.__elements[self.__rear]=data

    def dequeue(self):
        if(self.is_empty()):
            print("Queue is empty!!!")
        else:
            data=self.__elements[self.__front]
            self.__front+=1
            return data

    def display(self):
        for index in range(self.__front, self.__rear+1):
            print(self.__elements[index])

    def get_max_size(self):
        return self.__max_size

    #You can use the below __str__() to print the elements of the DS object while debugging
    def __str__(self):
        msg=[]
        index=self.__front
        while(index<=self.__rear):
            msg.append((str)(self.__elements[index]))
            index+=1
        msg=" ".join(msg)
        msg="Queue data(Front to Rear): "+msg
        return """
    ll = """class Node:
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next

    class LinkedList:
    def __init__(self):
        self.head = None

    def print(self):
        if self.head is None:
            print("Linked list is empty")
            return
        itr = self.head
        llstr = ''
        while itr:
            llstr += str(itr.data)+' --> ' if itr.next else str(itr.data)
            itr = itr.next
        print(llstr)

    def get_length(self):
        count = 0
        itr = self.head
        while itr:
            count+=1
            itr = itr.next

        return count

    def insert_at_begining(self, data):
        node = Node(data, self.head)
        self.head = node

    def insert_at_end(self, data):
        if self.head is None:
            self.head = Node(data, None)
            return

        itr = self.head

        while itr.next:
            itr = itr.next

        itr.next = Node(data, None)

    def insert_after_value(self, data_after, data_to_insert):
        if self.head is None:
            return

        if self.head.data == data_after:
            self.head.next = Node(data_to_insert, self.head.next)
            return

        itr = self.head
        while itr:
            if itr.data == data_after:
                itr.next = Node(data_to_insert, itr.next)
                break

            itr = itr.next

    def insert_at(self, index, data):
        if index<0 or index>self.get_length():
            raise Exception("Invalid Index")

        if index==0:
            self.insert_at_begining(data)
            return

        count = 0
        itr = self.head
        while itr:
            if count == index - 1:
                node = Node(data, itr.next)
                itr.next = node
                break

            itr = itr.next
            count += 1

    def remove_at(self, index):
        if index<0 or index>=self.get_length():
            raise Exception("Invalid Index")

        if index==0:
            self.head = self.head.next
            return

        count = 0
        itr = self.head
        while itr:
            if count == index - 1:
                itr.next = itr.next.next
                break

            itr = itr.next
            count+=1

    def insert_values(self, data_list):
        self.head = None
        for data in data_list:
            self.insert_at_end(data)"""
    bs = """for i in range(len(arr)-1):
    swapped=False
    for j in range(len(arr)-1-i):
        if arr[j]>arr[j+1]:
            arr[j],arr[j+1]=arr[j+1],arr[j]
            swapped=True
    if not swapped :
        break"""
    ins = """def insertionSort(arr):
      # Start from 1 as arr[0] is always sorted
      for i in range(1, len(arr)): 
        currentElement = arr[i]
        # Move elements of arr[0..i-1], that are greater than key, 
        # to one position ahead of their current position
        j = i-1
        while j >= 0 and arr[j] > currentElement :
            arr[j + 1] = arr[j]
            j -= 1
         # Finally place the Current element at its correct position.
        arr[j + 1] = currentElement"""
    ss = """def selectionSort(arr):

   # loop to iterate over the array elements
   for i in range(len(arr)):

       # set min_index equal to the first unsorted element
       min_index = i

       # iterate over unsorted sublist
       for j in range(i+1, len(arr)):

    #helps in finding the minimum element
           if arr[min_index] > arr[j]:
               min_index = j

       # swapping the minimum element with the element at min_index to place it at its correct position

       arr[i], arr[min_index] = arr[min_index], arr[i]"""
    ms = """def mergesort(arr):
    if len(arr)<=1:
        return
    mid=(len(arr))//2
    left=arr[:mid]
    right=arr[mid:]
    mergesort(left)
    mergesort(right)
    merge(left,right,arr)
    return arr

    def merge(a,b,arr):
    len_a=len(a)
    len_b=len(b)
    i,j,k=0,0,0
    while i<len_a and j<len_b:
        if a[i]<=b[j]:
            arr[k]=a[i]
            i+=1
        else:
            arr[k]=b[j]
            j+=1
        k+=1
    while(i<len_a):
        arr[k]=a[i]
        i+=1
        k+=1
    while j< len_b:
        arr[k] =b[j]
        j+=1
        k+=1"""
    bsm = """def searchMatrix(matrix, target):

        left, right = 0, len(matrix)-1
        while left < right: 
            mid = left + math.ceil((right - left) / 2)

            if matrix[mid][0] == target:
                return True

            if matrix[mid][0] > target:
                right = mid - 1
            else:
                left = mid

        target_row = right

        left, right = 0, len(matrix[0])
        while left < right:
            mid = left + ((right - left) >> 1)

            if matrix[target_row][mid] == target:
                return True

            if matrix[target_row][mid] < target:
                left = mid + 1
            else:
                right = mid

        return False"""
    lcs = """def longestCommonSubsequence(text1, text2):
        n1 = len(text1)
        n2 = len(text2)
        def sub(text1, text2, n1, n2):
            dp = [0] * (n2 + 1)
            for i in range(n1):
                newdp = [0] * (n2 + 1)
                for j in range(n2):
                    if text1[i] == text2[j]:
                        newdp[j + 1] = 1 + dp[j]
                    else:
                        newdp[j + 1] = max(dp[j + 1], newdp[j])
                dp = newdp
            return dp[n2]
        if n1 > n2:
            return sub(text1, text2, n1, n2)
        else:
            return sub(text2, text1, n2, n1)"""
    perm = """def permute(nums):
        n = len(nums)
        if n==0:
            return [[]]
        if n==1:
            return [nums]
        ret_list = [None]*math.factorial(n)
        i=0
        for perm in permutations:
            for x in range(n):
                # Store 'All values before the excluded digit' + 'excluded digit' + 'All values after the excluded digit'
                ret_list[i] = perm[:x] + [nums[n-1]] + perm[x:]
                i += 1
        return ret_list"""
    cmb = """def n_length_combo(lst, n):

    if n == 0:
        return [[]]

    l =[]
    for i in range(0, len(lst)):

        m = lst[i]
        remLst = lst[i + 1:]

        for p in n_length_combo(remLst, n-1):
            l.append([m]+p)

    return l"""
    prime = """def nprimes(n):
    primes = []
    prime_bool = [True for i in range(n + 1)]
    p = 2
    while (p * p <= n):
        if (prime_bool[p] == True):
            for i in range(p * p, n+1, p):
                prime_bool[i] = False
        p += 1
    for p in range(2, n+1):
        if prime_bool[p]:
            primes.append(p)
    return primes"""
    lps = """def printSubstring(str, left, right):
    st=""
    for i in range(left, right + 1):
        st+=str[i]
    return st

    def longestPalSubstring(s):
        strLen = 2 * len(s) + 3
        sChars = [0]*strLen
        sChars[0] = '@'
        sChars[strLen - 1] = '$'
        t = 1
        for i in s:
            sChars[t] = '#'
            t += 1
            sChars[t] = i
            t += 1

        sChars[t] = '#'

        maxLen = int(0)
        start = int(0)
        maxRight = int(0)
        center = int(0)
        p = [0] * strLen
        for i in range(1, strLen - 1):
            if i < maxRight:
                p[i] = min(maxRight - i, p[2 * center - i])
            while sChars[i + p[i] + 1] == sChars[i - p[i] - 1]:
                p[i] += 1
            if i + p[i] > maxRight:
                center = i
                maxRight = i + p[i]
            if p[i] > maxLen:
                start = int((i - p[i] - 1) / 2)
                maxLen = p[i]
        return printSubstring(s, start, start + maxLen - 1)"""

    lcmhcf = """def compute_hcf(x, y):
    while(y):
        x, y = y, x % y
    return x
    def compute_lcm(x, y):
        lcm = (x*y)//compute_gcd(x,y)
        return lcm"""

    k = int(input("Enter your need : "))
    if k == 1:
        print(bsr)
    elif k == 2:
        print(st)
    elif k == 3:
        print(qu)
    elif k == 4:
        print(ll)
    elif k == 5:
        print(bs)
    elif k == 6:
        print(ins)
    elif k == 7:
        print(ss)
    elif k == 8:
        print(ms)
    elif k == 9:
        print(bsm)
    elif k == 10:
        print(lcs)
    elif k == 11:
        print(perm)
    elif k == 12:
        print(cmb)
    elif k == 13:
        print(prime)
    elif k == 14:
        print(lps)
    elif k == 15:
        print(lcmhcf)
    else:
        print("Invalid Option")


