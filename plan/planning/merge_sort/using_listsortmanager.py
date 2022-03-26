from planning.merge_sort.ListSortManager import MergeSort
merger=MergeSort()
listExample=merger.CreateList(100)
listExample=merger.Sort(listExample)
merger.PrintList(listExample)