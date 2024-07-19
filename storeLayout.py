#this is a graph
"""
#simple 5 shelf layout. Can be more obviously. 
#( (u, v), e )
layout = [ 
(("01", "2"), 4), 
(("02", "03"), 8),
(("03", "04"), 1),
(("01", "05"), 3),
(("02", "05"), 2),
(("03", "05"), 7),
(("04", "05"), 9)
]
"""

#adjanceny matrix
layout = [ 
    [0, 4, 8, 9, 1], #shelf 1
    [4, 0, 4, 5, 2], #shelf 2 and so on
    [8, 4, 0, 1, 7],
    [9, 5, 4, 0, 9],
    [3, 2, 7, 9, 0]
]
#image of this layout is in github