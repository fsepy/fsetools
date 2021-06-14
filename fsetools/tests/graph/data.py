import io

vertices_csv = io.StringIO("""NAME,TYPE,CAPACITY
Room01,Room,120
Room02,Room,100
Room01Door,Door,250
Room02Door,Door,40
Corridor,Corridor,1000
FinalExit01,FinalExit,450""")

edges_csv = io.StringIO("""DOOR,FROM,TO,BIDIRECTIONAL
Room01Door,Room01,Corridor,FALSE
Room02Door,Room02,Corridor,FALSE
FinalExit01,Corridor,-,FALSE""")
