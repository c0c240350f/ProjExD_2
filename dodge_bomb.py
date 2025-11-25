import os
import sys
import random
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP: (0, -5),
    pg.K_DOWN: (0, +5),
    pg.K_LEFT: (-5, 0),
    pg.K_RIGHT: (+5, 0)
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct:pg.Rect) -> tuple[bool,bool]:
    """
    引数：こうかとんRectかばくだんRect
    戻り値：タプル（横方向判定結果、縦方向判定結果）
    画面内ならTrue、画面外ならFalse
    """
    yoko,tate=True,True
    if rct.left<0 or WIDTH<rct.right: #横方向のはみだしチェック
        yoko=False
    if rct.top<0 or HEIGHT<rct.bottom: #横方向のはみだしチェック
        tate=False
    return yoko,tate

def gameover(screen: pg.Surface) -> None:
    go_img=pg.Surface((1100,650))
    pg.draw.rect(go_img,(0,0,0),(0,0,1100,650))
    go_img.set_alpha(150)
    fonto=pg.font.Font(None,80)
    txt=fonto.render("Game Over",True,(255,255,255))
    txt_rect=txt.get_rect()
    txt_rect.center=WIDTH/2,HEIGHT/2
    screen.blit(txt, txt_rect)
    ck_img=pg.transform.rotozoom(pg.image.load("fig/8.png"),0,0.9)
    ck_rect=ck_img.get_rect()
    ck_rect.center=WIDTH/2-200,HEIGHT/2
    screen.blit(ck_img,ck_rect)
    ck_rect.center=WIDTH/2+200,HEIGHT/2
    screen.blit(ck_img,ck_rect)
    screen.blit(go_img,[0,0])
    pg.display.update()
    time.sleep(5)


def init_bb_imgs() -> tuple[list[pg.Surface],list[int]]:
    bb_imgs=[a for a in range(1,11)]
    bb_accs=[a for a in range(1,11)]
    for r in range(1,11):
        bb_img=pg.Surface((20*r,20*r))
        pg.draw.circle(bb_img,(255,0,0),(10*r,10*r),10*r)
        bb_imgs.append(bb_img)
        return bb_imgs,bb_accs
    avx=vx*bb_accs[min(tmr//500,9)]
    bb_img=bb_imgs[min(tmr//500,9)]
    if bb_imgs>bb_img:
        bb_rct.width=bb_img.get_rect().width


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img=pg.Surface((20,20)) #空のsurface
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)#半径10の赤い円を描画
    bb_img.set_colorkey((0,0,0)) #黒色を透明に
    bb_rct=bb_img.get_rect()#爆弾rect
    bb_rct.center = random.randint(0,WIDTH),random.randint(0,WIDTH) #爆弾の座標
    vx,vy=+5,+5 #爆弾の横速度、縦速度


    clock = pg.time.Clock()
    tmr = 0


    init_bb_imgs()
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        
        if kk_rct.colliderect(bb_rct): #こうかとんと爆弾が衝突したら
            print("ゲームオーバー")
            gameover(screen)
            return 

        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        

        for key,mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0]+=mv[0] #横方向の移動
                sum_mv[1]+=mv[1] #縦方向の移動
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) !=(True,True):#画面外なら
            kk_rct.move_ip(-sum_mv[0],-sum_mv[1])
        screen.blit(kk_img, kk_rct)
        yoko,tate=check_bound(bb_rct)
        if not yoko: #横方向にはみ出していたら
            vx *=-1
        if not tate: #縦方向にはみ出していたら
            vy *=-1
        bb_rct.move_ip(vx,vy)
        screen.blit(bb_img,bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
