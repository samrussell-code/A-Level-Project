import random
class MergeSort:
    '''
    Class for handling list sorting using the merge algorithmn.
    Methods: CreateList(size), Sort(array), PrintList(array)
    '''
    def CreateList(self,size): #subroutine that creates a list to use as test data
        '''         
        CreateList(size):
       Returns a list of random integers in range 1-100 using size, as debug test data.
        '''
        dataList=[random.randint(1,100) for x in range(size)]
        return dataList

    def Sort(self,arr): #subroutine that merge sorts the array defined as a parameter
        '''         
        Sort(array):
       Returns the parameter {array} in ascending order using the merge sort method.
        '''
        if len(arr)>1:
            listMiddle=len(arr)//2 #finds the centre of the list
            leftSide=arr[:listMiddle] #splits it into two seperate lists of left and right side
            rightSide=arr[listMiddle:]
            self.Sort(leftSide);self.Sort(rightSide) #redoes merge sort for each side
            x=y=z=0
            while x<len(leftSide) and y<len(rightSide): #counts up x, y, and z - x if the right side is bigger, y if the left side is bigger, z always
               if leftSide[x]<rightSide[y]: #the loop ends once the iterator reaches the size of its array
                   arr[z]=leftSide[x] #arr is the temporary list used to store the newly arranged data, z is the current overall iteration
                   x+=1
               else:
                   arr[z]=rightSide[y]
                   y+=1
               z+=1              
            while x<len(leftSide): #fills in the remaining locations of all values that haven't been put back into arr on either side
                arr[z]=leftSide[x]
                x+=1
                z+=1
            while y<len(rightSide):
                arr[z]=rightSide[y]
                y+=1
                z+=1
            return arr

    def PrintList(self,arr): #outputs the list in a readable format into the debug log by printing each element without a new line inbetween
        '''         
        PrintList(array):
        Outputs a debug readable format of the {array} argument
        '''
        for x in range(len(arr)):
            print(arr[x], end=" ")
        print()