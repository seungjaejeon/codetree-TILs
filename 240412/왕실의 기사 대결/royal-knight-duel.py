# 1, 1 시작 L, L마지막
# r, c의 초기위치, h w크기의 직사각형

# 상하좌우 한칸 이동
# 이동하려는 위치에 다른 기사가 있다면?
# 그 기사도 연쇄적으로 한칸 밀려남
# 또 있다면? 또 밀려남
# 하지만 이동하려는 방향의 끝에 벽이 있다면?
# 그 기사들은 모두 다 이동하지 않게 됨 -> 먼저 끝까지 확인하고 이동해야할 듯

# 대결 대미지
# 기사를 밀치면 밀려난 기사들은 피해를 입는다.
# 함정의 수만큼 피해를 입게 되는 것임
# 현재 체력 이상의 대미지를 입으면 체스판에서 사라짐 pop O
# 명령을 받은 기사는 피해 x 밀려난 기사들만 피해
# 밀렸더라도 함정이 없다면 피해를 입지 않음 O

# Q번의 왕의 명령
# Q번의 대결 이후에 생존한 기사들이 총 받은 대미지의 합을 출력 O

from collections import defaultdict
L, N, Q = map(int, input().split())
pan = []
knight = [[0 for i in range(L)] for j in range(L)]
dic = defaultdict(list)
dx = [-1,0,1,0] # 상 우 하 좌
dy = [0,1,0,-1]
firstk = []
for i in range(L):
    line = list(map(int, input().split()))
    pan.append(line)

for i in range(1, N+1):
    r, c, h, w, k = map(int,input().split())
    dic[i] = [r-1, c-1, h, w, k]
    firstk.append(k)
    for x in range(r-1, r-1+h):
        for y in range(c-1, c-1+w):
            knight[x][y] = i

def canmove(i, d):#i번 기사를 d로 이동
    # i번 기사와 맞닿아 있는 기사 확인
    global wall
    nx = set()
    r, c, h, w, k = dic[i]
    nr, nc = r+dx[d], c+dy[d]
    for x in range(nr, nr+h):
        for y in range(nc, nc+w):
            if x < 0 or y < 0 or x >= L or y >= L or pan[x][y] == 2: # 확인하는 과정에서 벽이 있다면
                wall = True
                return
            if knight[x][y] != i and knight[x][y] != 0:
                nextmove.add(knight[x][y])
                nx.add(knight[x][y])
    for k in nx:
        canmove(k, d)
    return

# knight를 빼고 움직였을 때 맞닿는 애를 알 방법..

def realmove(i, d): # 바꿔줘야 할 것 = knight, dic
    r, c, h, w, k = dic[i]
    nr = r + dx[d]
    nc = c + dy[d]
    dic[i] = [nr, nc, h, w, k]
    
def damage(i): #대미지
    r,c,h,w,k = dic[i]
    hurt = 0
    for x in range(r, r+h):
        for y in range(c, c+w):
            if pan[x][y] == 1:
                hurt += 1
    return hurt

for _ in range(Q):
    i ,d = map(int, input().split())
    if i not in dic: # 명령에 없는 기사면 실행하지 않음
        continue
    nextmove = set() # 밀려난 기사
    wall = False
    canmove(i, d) # 밀려난 기사 set 넣기
    if wall: #움직임에 벽이 있었다면 아무일도 일어나지 않음
        continue
    # 벽이 없었다면 실제로 움직여야함
    for nxmv in nextmove: # 밀려난 기사 이동시키기
        realmove(nxmv, d)

    r,c,h,w,k = dic[i] # 움직인 원흉도 해주기
    nr = r + dx[d]
    nc = c + dy[d]
    dic[i] = [nr, nc, h, w, k]

    for nxmv in nextmove: #움직인 놈들에 대해서 대미지 확인
        r,c,h,w,k = dic[nxmv]
        hurt = damage(nxmv)
        if k-hurt <= 0:
            dic.pop(nxmv)
        else:
            dic[nxmv] = [r,c,h,w,k-hurt]
    knight = [[0 for i in range(L)] for j in range(L)]
    for liveknight in dic.keys():
        r, c, h, w, k = dic[liveknight]
        for x in range(r, r+h):
            for y in  range(c, c+w):
                knight[x][y] = liveknight
sum_k = 0
for i in dic.keys():
    sum_k += firstk[i-1]-dic[i][4]
print(sum_k)