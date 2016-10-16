#정렬하는 문제에서 해결방법 http://pyengine.blogspot.kr/2016/07/blog-post_2.html
#멀티맵에 대한 문제 해결방법 http://stackoverflow.com/questions/6813564/python-have-dictionary-with-same-name-keys
gDrawSortDictionary = []

#데이터 그리기 함수
def draw():
    global gDrawSortDictionary
    for i in sorted(gDrawSortDictionary):
        for j in gDrawSortDictionary[i]:
            j.draw()

#데이터 넣기 함수
def addObject(_object):
    global gDrawSortDictionary
    gDrawSortDictionary[_object.Y].append(_object)

#데이터 전부 삭제 함수(실객체를 지우면 큰일난다!)
def reset():
    global gDrawSortDictionary
    for i in sorted(gDrawSortDictionary):
        gDrawSortDictionary[i].clear()