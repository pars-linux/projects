/* Pardus KWin window decoration
  Copyright (C) 2005 Adrian Schroeter <adrian@suse.de>

  based on the window decoration "Plastik" and "Web":
  Copyright (C) 2003 Sandro Giessl <ceebx@users.sourceforge.net>
  Copyright (C) 2001 Rik Hemsley (rikkus) <rik@kde.org>

  This program is free software; you can redistribute it and/or
  modify it under the terms of the GNU General Public
  License as published by the Free Software Foundation; either
  version 2 of the License, or (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
  General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program; see the file COPYING.  If not, write to
  the Free Software Foundation, Inc., 59 Temple Place - Suite 330,
  Boston, MA 02111-1307, USA.
 */

// #include <kwin/options.h>

#include <math.h>

#include <kdebug.h>
#include <qbitmap.h>
#include <qcursor.h>
#include <qimage.h>
#include <qpainter.h>
#include <qpixmap.h>
#include <kpixmap.h>
#include <kpixmapeffect.h>
#include <kdecoration.h>
#include <qtooltip.h>
#include <qtimer.h>

#include "PARDUSbutton.h"
#include "PARDUSbutton.moc"
#include "PARDUSclient.h"
#include "misc.h"
#include "shadow.h"

#define PLASTIK_FLAT 0
#define LIPSTIK_FLAT 1
#define PLASTIK_3D 2
#define LIPSTIK_3D 3
#define LIPSTIK_BRIGHT 4

namespace KWinPARDUS
{

static const uint TIMERINTERVAL = 50; // msec
static const uint ANIMATIONSTEPS = 4;

PARDUSButton::PARDUSButton(PARDUSClient *parent, const char *name,
                             const QString& tip, ButtonType type,
                             int size, bool toggle, int btns)
    : QButton(parent->widget(), name),
    m_client(parent),
    m_lastMouse(NoButton),
    m_realizeButtons(btns),
    m_size(size),
    m_type(type),
    hover(false)
{
    QToolTip::add( this, tip );
    setCursor(ArrowCursor);

    setBackgroundMode(NoBackground);

    setToggleButton(toggle);

    if(m_size < 10) { m_size = 10; }

    setFixedSize(m_size, m_size);

    setDeco();

    animTmr = new QTimer(this);
    connect(animTmr, SIGNAL(timeout() ), this, SLOT(animate() ) );
    animProgress = 0;
}

PARDUSButton::~PARDUSButton()
{
}

QSize PARDUSButton::sizeHint() const
{
    return QSize(m_size, m_size);
}

void PARDUSButton::setSize(int s)
{
    m_size = s;
    if(m_size < 10) { m_size = 10; }
    setFixedSize(m_size, m_size);
    setDeco();
}

void PARDUSButton::setOn(bool on)
{
    QButton::setOn(on);
    setDeco();
}

void PARDUSButton::setDeco()
{
    switch (m_type) {
        case CloseButton:
            btnType = CloseIcon;
            break;
        case HelpButton:
            btnType = HelpIcon;
            break;
        case MinButton:
            btnType = MinIcon;
            break;
        case MaxButton:
            if (isOn()) {
                btnType = MaxRestoreIcon;
            } else {
                btnType = MaxIcon;
            }
            break;
        case OnAllDesktopsButton:
            if (isOn()) {
                btnType = NotOnAllDesktopsIcon;
            } else {
                btnType = OnAllDesktopsIcon;
            }
            break;
        case ShadeButton:
            if (isOn()) {
                btnType = UnShadeIcon;
            } else {
                btnType = ShadeIcon;
            }
            break;
        case AboveButton:
            if (isOn()) {
                btnType = NoKeepAboveIcon;
            } else {
                btnType = KeepAboveIcon;
            }
            break;
        case BelowButton:
            if (isOn()) {
                btnType = NoKeepBelowIcon;
            } else {
                btnType = KeepBelowIcon;
            }
            break;
        default:
            btnType = NumButtonIcons;
            break;
    }

    this->update();
}

void PARDUSButton::setTipText(const QString &tip) {
    QToolTip::remove(this );
    QToolTip::add(this, tip );
}

void PARDUSButton::animate()
{
    animTmr->stop();

    if(hover) {
        if(animProgress < ANIMATIONSTEPS) {
            if (Handler()->animateButtons() ) {
                animProgress++;
            } else {
                animProgress = ANIMATIONSTEPS;
            }
            animTmr->start(TIMERINTERVAL, true); // single-shot
        }
    } else {
        if(animProgress > 0) {
            if (Handler()->animateButtons() ) {
                animProgress--;
            } else {
                animProgress = 0;
            }
            animTmr->start(TIMERINTERVAL, true); // single-shot
        }
    }

    repaint(false);
}

void PARDUSButton::enterEvent(QEvent *e)
{
    QButton::enterEvent(e);

    hover = true;
    animate();
//     repaint(false);
}

void PARDUSButton::leaveEvent(QEvent *e)
{
    QButton::leaveEvent(e);

    hover = false;
    animate();
//     repaint(false);
}

void PARDUSButton::mousePressEvent(QMouseEvent* e)
{
    m_lastMouse = e->button();
    // pass on event after changing button to LeftButton
    QMouseEvent me(e->type(), e->pos(), e->globalPos(),
                   (e->button()&m_realizeButtons)?LeftButton:NoButton, e->state());

    QButton::mousePressEvent(&me);
}

void PARDUSButton::mouseReleaseEvent(QMouseEvent* e)
{
    m_lastMouse = e->button();
    // pass on event after changing button to LeftButton
    QMouseEvent me(e->type(), e->pos(), e->globalPos(),
                    (e->button()&m_realizeButtons)?LeftButton:NoButton, e->state());

    QButton::mouseReleaseEvent(&me);
}

void PARDUSButton::drawButton(QPainter *painter)
{
    if (!Handler()->initialized())
        return;

    int type = Handler()->buttonType();

    switch (type) {
        case PLASTIK_FLAT:
        case LIPSTIK_FLAT:
	case LIPSTIK_BRIGHT:
            drawPlastikBtn(painter);
            break;
        case PLASTIK_3D:
        case LIPSTIK_3D:
            drawLipstikBtn(painter);
            break;
        default:
            drawPlastikBtn(painter);
            break;
    }
}

void PARDUSButton::drawPlastikBtn(QPainter *painter)
{
    QRect r(0,0,width(),height());

    bool active = m_client->isActive();
    QPixmap backgroundTile = m_client->getTitleBarTile(active);
    KPixmap tempKPixmap;

    QColor highlightColor;
    if(m_type == CloseButton) {
        highlightColor = QColor(255,64,0);
    } else {
        highlightColor = Qt::white;
    }

    QColor contourTop = alphaBlendColors(Handler()->getColor(TitleGradientFrom, active),
            Qt::black, 220);
    QColor contourBottom = alphaBlendColors(Handler()->getColor(TitleGradientTo, active),
            Qt::black, 220);
    QColor surfaceTop = alphaBlendColors(Handler()->getColor(TitleGradientFrom, active),
            Qt::white, 220);
    QColor surfaceBottom = alphaBlendColors(Handler()->getColor(TitleGradientTo, active),
            Qt::white, 220);

    int highlightAlpha = static_cast<int>(255-((60/static_cast<double>(ANIMATIONSTEPS))*
                                          static_cast<double>(animProgress) ) );
    contourTop = alphaBlendColors(contourTop, highlightColor, highlightAlpha );
    contourBottom = alphaBlendColors(contourBottom, highlightColor, highlightAlpha);
    surfaceTop = alphaBlendColors(surfaceTop, highlightColor, highlightAlpha);
    surfaceBottom = alphaBlendColors(surfaceBottom, highlightColor, highlightAlpha);

    if (isDown() ) {
        contourTop = alphaBlendColors(contourTop, Qt::black, 200);
        contourBottom = alphaBlendColors(contourBottom, Qt::black, 200);
        surfaceTop = alphaBlendColors(surfaceTop, Qt::black, 200);
        surfaceBottom = alphaBlendColors(surfaceBottom, Qt::black, 200);
    }

    QPixmap buffer;
    buffer.resize(width(), height());
    QPainter bP(&buffer);

    // fill with the titlebar background
    bP.drawTiledPixmap(0, 0, width(), width(), backgroundTile, 0, TOPMARGIN );

    if (m_type != MenuButton || hover || animProgress != 0) {
        // contour
        bP.setPen(contourTop);
        bP.drawLine(r.x()+2, r.y(), r.right()-2, r.y() );
        bP.drawPoint(r.x()+1, r.y()+1);
        bP.drawPoint(r.right()-1, r.y()+1);
        bP.setPen(contourBottom);
        bP.drawLine(r.x()+2, r.bottom(), r.right()-2, r.bottom() );
        bP.drawPoint(r.x()+1, r.bottom()-1);
        bP.drawPoint(r.right()-1, r.bottom()-1);
        // sides of the contour
        tempKPixmap.resize(1, r.height()-2*2);
        KPixmapEffect::gradient(tempKPixmap,
                                contourTop,
                                contourBottom,
                                KPixmapEffect::VerticalGradient);
        bP.drawPixmap(r.x(), r.y()+2, tempKPixmap);
        bP.drawPixmap(r.right(), r.y()+2, tempKPixmap);
        // sort of anti-alias for the contour
        bP.setPen(alphaBlendColors(Handler()->getColor(TitleGradientFrom, active),
                contourTop, 150) );
        bP.drawPoint(r.x()+1, r.y());
        bP.drawPoint(r.right()-1, r.y());
        bP.drawPoint(r.x(), r.y()+1);
        bP.drawPoint(r.right(), r.y()+1);
        bP.setPen(alphaBlendColors(Handler()->getColor(TitleGradientTo, active),
                contourBottom, 150) );
        bP.drawPoint(r.x()+1, r.bottom());
        bP.drawPoint(r.right()-1, r.bottom());
        bP.drawPoint(r.x(), r.bottom()-1);
        bP.drawPoint(r.right(), r.bottom()-1);

        // surface
        // fill top and bottom
        if (Handler()->buttonType() == PLASTIK_FLAT) {
		bP.setPen(surfaceTop);
		bP.drawLine(r.x()+2, r.y()+1, r.right()-2, r.y()+1 );
		bP.setPen(surfaceBottom);
		bP.drawLine(r.x()+2, r.bottom()-1, r.right()-2, r.bottom()-1 );
        } else if (Handler()->buttonType() == LIPSTIK_FLAT || isDown()) {
		bP.setPen(surfaceBottom);
		bP.drawLine(r.x()+2, r.y()+1, r.right()-2, r.y()+1 );
		bP.setPen(surfaceTop);
		bP.drawLine(r.x()+2, r.bottom()-1, r.right()-2, r.bottom()-1 );
        } else {
		bP.setPen(surfaceBottom.light(117));
		bP.drawLine(r.x()+2, r.y()+1, r.right()-2, r.y()+1 );
		bP.setPen(surfaceTop.dark(122));
		bP.drawLine(r.x()+2, r.bottom()-1, r.right()-2, r.bottom()-1 );
	}

        // fill the rest! :)
        tempKPixmap.resize(1, r.height()-2*2);
        if (Handler()->buttonType() == PLASTIK_FLAT) {
		KPixmapEffect::gradient(tempKPixmap,
					surfaceTop,
					surfaceBottom,
					KPixmapEffect::VerticalGradient);
        } else {
		KPixmapEffect::gradient(tempKPixmap,
					surfaceBottom,
					surfaceTop,
					KPixmapEffect::VerticalGradient);
        }
        bP.drawTiledPixmap(r.x()+1, r.y()+2, r.width()-2, r.height()-4, tempKPixmap);
    }

    if (m_type == MenuButton)
    {
        QPixmap menuIcon(m_client->icon().pixmap( QIconSet::Small, QIconSet::Normal));
        if (width() < menuIcon.width() || height() < menuIcon.height() ) {
            menuIcon.convertFromImage( menuIcon.convertToImage().smoothScale(width(), height()));
        }
	if (isDown()) {
        	bP.drawPixmap((width()-menuIcon.width())/2, ((height()-menuIcon.height())/2)+1, menuIcon);
	} else {
        	bP.drawPixmap((width()-menuIcon.width())/2, (height()-menuIcon.height())/2, menuIcon);
	}
    }
    else
    {
        int dX,dY;
        QPixmap deco;
        int s = lroundf(r.height()*Handler()->iconSize());
        if ((s + r.height())%2 != 0) --s;

        if (isDown()) {
            deco = active ? Handler()->buttonPixmap(btnType, s, A_FG_LIGHT) : Handler()->buttonPixmap(btnType, s, I_FG_LIGHT);
        } else {
            deco = active ? Handler()->buttonPixmap(btnType, s, A_FG_DARK) : Handler()->buttonPixmap(btnType, s, I_FG_DARK);
        }
        dX = r.x()+(r.width()-deco.width())/2;
        dY = r.y()+(r.height()-deco.height())/2;
        if (isDown() ) {
            dY++;
        }
        if(active && !isDown() && Handler()->useTitleProps() && Handler()->titleShadow() ) {
            bP.drawPixmap(dX+1, dY+1, Handler()->buttonPixmap(btnType, s, SHADOW));
        }
        bP.drawPixmap(dX, dY, deco);
    }

    bP.end();
    painter->drawPixmap(0, 0, buffer);
}

void PARDUSButton::drawLipstikBtn(QPainter *painter)
{
    QRect r(0,0,width(),height());

    pixmapCache = new QIntCache<CacheEntry>(150000, 499);
    pixmapCache->setAutoDelete(true);

    bool active = m_client->isActive();
    QPixmap backgroundTile = m_client->getTitleBarTile(active);

    QPixmap buffer;
    buffer.resize(width(), height());
    QPainter bP(&buffer);

    // fill with the titlebar background
    bP.drawTiledPixmap(0, 0, width(), width(), backgroundTile, 0, TOPMARGIN );

    if (m_type == MenuButton)
    {
        KPixmap menuIcon(m_client->icon().pixmap( QIconSet::Small, QIconSet::Normal));
        if (width() < menuIcon.width() || height() < menuIcon.height() ) {
            menuIcon.convertFromImage( menuIcon.convertToImage().smoothScale(width(), height()));
        }
        double fade = animProgress * 0.09;
        KPixmapEffect::fade(menuIcon, fade, QColor(240, 240, 240));
        bP.drawPixmap((width()-menuIcon.width())/2, (height()-menuIcon.height())/2, menuIcon);
    } else {
        renderBtnContour(&bP, r);
        if (isDown()) {
            QColor downColor = Handler()->getColor(BtnBg, active).dark(115);
            bP.fillRect(r.left()+1, r.top()+2, r.width()-2, r.height()-4, downColor);
            bP.setPen(downColor);
            // top line
            bP.drawLine(r.left()+2, r.top()+1, r.right()-2, r.top()+1);
            // bottom and right lines
            bP.setPen(downColor.light(106));
            bP.drawLine(r.left()+2, r.bottom()-1, r.right()-2, r.bottom()-1);
            bP.drawLine(r.right()-1, r.top()+2, r.right()-1, r.bottom()-2);
        } else {
            renderBtnSurface(&bP, QRect(r.left()+1, r.top()+1, r.width()-2, r.height()-2));
        }

        int dX,dY;
        QPixmap deco;
        int s = lroundf(r.height()*Handler()->iconSize());
        if ((s + r.height())%2 != 0) --s;

        deco = active ? Handler()->buttonPixmap(btnType, s, A_FG_DARK) : Handler()->buttonPixmap(btnType, s, I_FG_DARK);
        dX = r.x()+(r.width()-deco.width())/2;
        dY = r.y()+(r.height()-deco.height())/2;
        if (isDown() ) {
            dX++;
            dY++;
        }
        if(active && !isDown() && Handler()->useTitleProps() && Handler()->titleShadow() ) {
            bP.drawPixmap(dX+1, dY+1, Handler()->buttonPixmap(btnType, s, SHADOW));
        }
        bP.drawPixmap(dX, dY, deco);
    }

    bP.end();
    painter->drawPixmap(0, 0, buffer);
}

void PARDUSButton::renderBtnContour(QPainter *p, const QRect &r)
{
    if((r.width() <= 0)||(r.height() <= 0))
        return;

    bool active = m_client->isActive();

    QColor backgroundColor = Handler()->getColor(BtnBg, active);
    QColor contourColor = Handler()->getColor(BtnBg, active).dark(135);

// sides
    p->setPen(contourColor);
    p->drawLine(r.left(), r.top()+2, r.left(), r.bottom()-2);
    p->drawLine(r.right(), r.top()+2, r.right(), r.bottom()-2);
    p->drawLine(r.left()+2, r.top(), r.right()-2, r.top());
    p->drawLine(r.left()+2, r.bottom(), r.right()-2, r.bottom());

// edges
    const int alphaAA = 110; // the alpha value for anti-aliasing...

    // first part...
    p->setPen(contourColor);
    p->drawPoint(r.left()+1, r.top()+1);
    p->drawPoint(r.left()+1, r.bottom()-1);
    p->drawPoint(r.right()-1, r.top()+1);
    p->drawPoint(r.right()-1, r.bottom()-1);

    // second part... fill edges in case we don't paint alpha-blended
    p->setPen( backgroundColor );

    // third part... anti-aliasing...
    renderPixel(p,QPoint(r.left()+1,r.top()),alphaAA,contourColor);
    renderPixel(p,QPoint(r.left(),r.top()+1),alphaAA,contourColor);
    renderPixel(p,QPoint(r.left()+1,r.bottom()),alphaAA,contourColor);
    renderPixel(p,QPoint(r.left(),r.bottom()-1),alphaAA,contourColor);
    renderPixel(p,QPoint(r.right()-1,r.top()),alphaAA,contourColor);
    renderPixel(p,QPoint(r.right(),r.top()+1),alphaAA,contourColor);
    renderPixel(p,QPoint(r.right()-1,r.bottom()),alphaAA,contourColor);
    renderPixel(p,QPoint(r.right(),r.bottom()-1),alphaAA,contourColor);
}

void PARDUSButton::renderBtnSurface(QPainter *p, const QRect &r) const
{
    if((r.width() <= 0)||(r.height() <= 0))
        return;

    bool active = m_client->isActive();

    QColor backgroundColor = Handler()->getColor(BtnBg, active);
    QColor baseColor = Handler()->getColor(TitleGradientFrom, active);
    QColor highlightColor;
    if(m_type == CloseButton) {
        highlightColor = QColor(255,0,0);
    } else {
        highlightColor = Qt::white;
    }

    int highlightAlpha = static_cast<int>(255-((60/static_cast<double>(ANIMATIONSTEPS))*
                                          static_cast<double>(animProgress) ) );

    QColor buttonColor, bottomColor, topLineColor, bottomLineColor;

    if (Handler()->buttonType() == LIPSTIK_3D) { // Lipstik
        buttonColor = Handler()->getColor(BtnBg, active);
        bottomColor = buttonColor.light(112);
        topLineColor = buttonColor.light(112);
        bottomLineColor = buttonColor.dark(102);
    } else { // Plastik
        bottomColor = Handler()->getColor(BtnBg, active);
        buttonColor = bottomColor.light(130);
        topLineColor = buttonColor.light(108);
        bottomLineColor = bottomColor.dark(108);
    }

    buttonColor = alphaBlendColors(buttonColor, highlightColor, highlightAlpha);
    bottomColor = alphaBlendColors(bottomColor, highlightColor, highlightAlpha);
    topLineColor = alphaBlendColors(topLineColor, highlightColor, highlightAlpha);
    bottomLineColor = alphaBlendColors(bottomLineColor, highlightColor, highlightAlpha);

// sides,left
    int height = r.height() - 2;
    renderGradient(p, QRect(r.left(), r.top()+1, 1, height), bottomColor, buttonColor);
//right
    renderGradient(p, QRect(r.right(), r.top()+1, 1, height), bottomColor, buttonColor);
//top
    p->setPen(topLineColor);
    p->drawLine(r.left()+1, r.top(), r.right()-1, r.top() );
//bottom
    p->setPen(bottomLineColor);
    p->drawLine(r.left()+1, r.bottom(), r.right()-1, r.bottom() );

// button area...
    int width = r.width();
    height = r.height();
    width-=2;
    height-=2;
    renderGradient(p, QRect(r.left()+1, r.top()+1, width, height),  bottomColor, buttonColor);
}

void PARDUSButton::renderPixel(QPainter *p,
        		       const QPoint &pos,
        		       const int alpha,
        		       const QColor &color) const
{
        QRgb rgb = color.rgb();
        // generate a quite unique key -- use the unused width field to store the alpha value.
        CacheEntry search(cAlphaDot, alpha, 0, rgb);
        int key = search.key();

        CacheEntry *cacheEntry;
        if( (cacheEntry = pixmapCache->find(key)) ) {
            if( search == *cacheEntry ) { // match! we can draw now...
                if(cacheEntry->pixmap)
                    p->drawPixmap(pos, *(cacheEntry->pixmap) );
                return;
            } else { //Remove old entry in case of a conflict!
                pixmapCache->remove( key );
            }
        }

        QImage aImg(1,1,32); // 1x1
        aImg.setAlphaBuffer(true);
        aImg.setPixel(0,0,qRgba(qRed(rgb),qGreen(rgb),qBlue(rgb),alpha));
        QPixmap *result = new QPixmap(aImg);

        p->drawPixmap(pos, *result);

        // add to the cache...
        CacheEntry *toAdd = new CacheEntry(search);
        toAdd->pixmap = result;
        bool insertOk = pixmapCache->insert( key, toAdd, result->depth()/8);
        if(!insertOk)
            delete result;
}

void PARDUSButton::renderGradient(QPainter *painter,
                                  const QRect &rect,
                                  const QColor &c1,
                                  const QColor &c2) const
{
   if((rect.width() <= 0)||(rect.height() <= 0))
        return;

    // generate a quite unique key for this surface.
    CacheEntry search(cGradientTile, 0, rect.height(), c2.rgb(), c1.rgb());
    int key = search.key();

    CacheEntry *cacheEntry;
    if( (cacheEntry = pixmapCache->find(key)) ) {
        if( search == *cacheEntry ) { // match! we can draw now...
            if(cacheEntry->pixmap) {
                painter->drawTiledPixmap(rect, *(cacheEntry->pixmap) );
            }
            return;
        } else {
            // Remove old entry in case of a conflict!
            // This shouldn't happen very often, see comment in CacheEntry.
            pixmapCache->remove(key);
        }
    }

    // there wasn't anything matching in the cache, create the pixmap now...
    QPixmap *result = new QPixmap(10, rect.height());
    QPainter p(result);

//    int r_w = result->rect().width();
    int r_h = result->rect().height();
    int r_x, r_y, r_x2, r_y2;
    result->rect().coords(&r_x, &r_y, &r_x2, &r_y2);

    int rDiff, gDiff, bDiff;
    int rc, gc, bc;

    register int y;


    rDiff = ( c1.red())   - (rc = c2.red());
    gDiff = ( c1.green()) - (gc = c2.green());
    bDiff = ( c1.blue())  - (bc = c2.blue());

    register int rl = rc << 16;
    register int gl = gc << 16;
    register int bl = bc << 16;

    int rdelta = ((1<<16) / r_h) * rDiff;
    int gdelta = ((1<<16) / r_h) * gDiff;
    int bdelta = ((1<<16) / r_h) * bDiff;

    // these for-loops could be merged, but the if's in the inner loop
    // would make it slow
    for ( y = 0; y < r_h; y++ ) {
        rl += rdelta;
        gl += gdelta;
        bl += bdelta;

        p.setPen(QColor(rl>>16, gl>>16, bl>>16));
        p.drawLine(r_x, r_y+y, r_x2, r_y+y);
    }

    p.end();

    // draw the result...
    painter->drawTiledPixmap(rect, *result);

    // insert into cache using the previously created key.
    CacheEntry *toAdd = new CacheEntry(search);
    toAdd->pixmap = result;
    bool insertOk = pixmapCache->insert( key, toAdd, result->width()*result->height()*result->depth()/8 );

    if(!insertOk)
        delete result;
}

QBitmap IconEngine::icon(ButtonIcon icon, int size)
{
    QBitmap bitmap(size,size);
    bitmap.fill(Qt::color0);
    QPainter p(&bitmap);

    p.setPen(Qt::color1);

    QRect r = bitmap.rect();

    // line widths
    int lwTitleBar = 1;
    if (r.width() > 16) {
        lwTitleBar = 4;
    } else if (r.width() > 4) {
        lwTitleBar = 2;
    }
    int lwArrow = 1;
    if (r.width() > 16) {
        lwArrow = 4;
    } else if (r.width() > 7) {
        lwArrow = 2;
    }

    switch(icon) {
        case CloseIcon:
        {
            int lineWidth = 1;
            if (r.width() > 16) {
                lineWidth = 3;
            } else if (r.width() > 4) {
                lineWidth = 2;
            }

            drawObject(p, DiagonalLine, r.x(), r.y(), r.width(), lineWidth);
            drawObject(p, CrossDiagonalLine, r.x(), r.bottom(), r.width(), lineWidth);

            break;
        }

        case MaxIcon:
        {
            int lineWidth2 = 1; // frame
            if (r.width() > 16) {
                lineWidth2 = 2;
            } else if (r.width() > 4) {
                lineWidth2 = 1;
            }

            drawObject(p, HorizontalLine, r.x(), r.top(), r.width(), lwTitleBar);
            drawObject(p, HorizontalLine, r.x(), r.bottom()-(lineWidth2-1), r.width(), lineWidth2);
            drawObject(p, VerticalLine, r.x(), r.top(), r.height(), lineWidth2);
            drawObject(p, VerticalLine, r.right()-(lineWidth2-1), r.top(), r.height(), lineWidth2);

            break;
        }

        case MaxRestoreIcon:
        {
            int lineWidth2 = 1; // frame
            if (r.width() > 16) {
                lineWidth2 = 2;
            } else if (r.width() > 4) {
                lineWidth2 = 1;
            }

            int margin1, margin2;
            margin1 = margin2 = lineWidth2*2;
            if (r.width() < 8)
                margin1 = 1;

            // background window
            drawObject(p, HorizontalLine, r.x()+margin1, r.top(), r.width()-margin1, lineWidth2);
            drawObject(p, HorizontalLine, r.right()-margin2, r.bottom()-(lineWidth2-1)-margin1, margin2, lineWidth2);
            drawObject(p, VerticalLine, r.x()+margin1, r.top(), margin2, lineWidth2);
            drawObject(p, VerticalLine, r.right()-(lineWidth2-1), r.top(), r.height()-margin1, lineWidth2);

            // foreground window
            drawObject(p, HorizontalLine, r.x(), r.top()+margin2, r.width()-margin2, lwTitleBar);
            drawObject(p, HorizontalLine, r.x(), r.bottom()-(lineWidth2-1), r.width()-margin2, lineWidth2);
            drawObject(p, VerticalLine, r.x(), r.top()+margin2, r.height(), lineWidth2);
            drawObject(p, VerticalLine, r.right()-(lineWidth2-1)-margin2, r.top()+margin2, r.height(), lineWidth2);

            break;
        }

        case MinIcon:
        {
            drawObject(p, HorizontalLine, r.x(), r.bottom()-(lwTitleBar-1), r.width(), lwTitleBar);

            break;
        }

        case HelpIcon:
        {
            int center = r.x()+r.width()/2 -1;
            int side = r.width()/4;

            // paint a question mark... code is quite messy, to be cleaned up later...! :o

            if (r.width() > 16) {
                int lineWidth = 3;

                // top bar
                drawObject(p, HorizontalLine, center-side+3, r.y(), 2*side-3-1, lineWidth);
                // top bar rounding
                drawObject(p, CrossDiagonalLine, center-side-1, r.y()+5, 6, lineWidth);
                drawObject(p, DiagonalLine, center+side-3, r.y(), 5, lineWidth);
                // right bar
                drawObject(p, VerticalLine, center+side+2-lineWidth, r.y()+3, r.height()-(2*lineWidth+side+2+1), lineWidth);
                // bottom bar
                drawObject(p, CrossDiagonalLine, center, r.bottom()-2*lineWidth, side+2, lineWidth);
                drawObject(p, HorizontalLine, center, r.bottom()-3*lineWidth+2, lineWidth, lineWidth);
                // the dot
                drawObject(p, HorizontalLine, center, r.bottom()-(lineWidth-1), lineWidth, lineWidth);
            } else if (r.width() > 8) {
                int lineWidth = 2;

                // top bar
                drawObject(p, HorizontalLine, center-(side-1), r.y(), 2*side-1, lineWidth);
                // top bar rounding
                if (r.width() > 9) {
                    drawObject(p, CrossDiagonalLine, center-side-1, r.y()+3, 3, lineWidth);
                } else {
                    drawObject(p, CrossDiagonalLine, center-side-1, r.y()+2, 3, lineWidth);
                }
                drawObject(p, DiagonalLine, center+side-1, r.y(), 3, lineWidth);
                // right bar
                drawObject(p, VerticalLine, center+side+2-lineWidth, r.y()+2, r.height()-(2*lineWidth+side+1), lineWidth);
                // bottom bar
                drawObject(p, CrossDiagonalLine, center, r.bottom()-2*lineWidth+1, side+2, lineWidth);
                // the dot
                drawObject(p, HorizontalLine, center, r.bottom()-(lineWidth-1), lineWidth, lineWidth);
            } else {
                int lineWidth = 1;

                // top bar
                drawObject(p, HorizontalLine, center-(side-1), r.y(), 2*side, lineWidth);
                // top bar rounding
                drawObject(p, CrossDiagonalLine, center-side-1, r.y()+1, 2, lineWidth);
                // right bar
                drawObject(p, VerticalLine, center+side+1, r.y(), r.height()-(side+2+1), lineWidth);
                // bottom bar
                drawObject(p, CrossDiagonalLine, center, r.bottom()-2, side+2, lineWidth);
                // the dot
                drawObject(p, HorizontalLine, center, r.bottom(), 1, 1);
            }

            break;
        }

        case NotOnAllDesktopsIcon:
        {
            int lwMark = r.width()-lwTitleBar*2-2;
            if (lwMark < 1)
                lwMark = 3;

            drawObject(p, HorizontalLine, r.x()+(r.width()-lwMark)/2, r.y()+(r.height()-lwMark)/2, lwMark, lwMark);

            // Fall through to OnAllDesktopsIcon intended!
        }
        case OnAllDesktopsIcon:
        {
            // horizontal bars
            drawObject(p, HorizontalLine, r.x()+lwTitleBar, r.y(), r.width()-2*lwTitleBar, lwTitleBar);
            drawObject(p, HorizontalLine, r.x()+lwTitleBar, r.bottom()-(lwTitleBar-1), r.width()-2*lwTitleBar, lwTitleBar);
            // vertical bars
            drawObject(p, VerticalLine, r.x(), r.y()+lwTitleBar, r.height()-2*lwTitleBar, lwTitleBar);
            drawObject(p, VerticalLine, r.right()-(lwTitleBar-1), r.y()+lwTitleBar, r.height()-2*lwTitleBar, lwTitleBar);


            break;
        }

        case NoKeepAboveIcon:
        {
            int center = r.x()+r.width()/2;

            // arrow
            drawObject(p, CrossDiagonalLine, r.x(), center+2*lwArrow, center-r.x(), lwArrow);
            drawObject(p, DiagonalLine, r.x()+center, r.y()+1+2*lwArrow, center-r.x(), lwArrow);
            if (lwArrow>1)
                drawObject(p, HorizontalLine, center-(lwArrow-2), r.y()+2*lwArrow, (lwArrow-2)*2, lwArrow);

            // Fall through to KeepAboveIcon intended!
        }
        case KeepAboveIcon:
        {
            int center = r.x()+r.width()/2;

            // arrow
            drawObject(p, CrossDiagonalLine, r.x(), center, center-r.x(), lwArrow);
            drawObject(p, DiagonalLine, r.x()+center, r.y()+1, center-r.x(), lwArrow);
            if (lwArrow>1)
                drawObject(p, HorizontalLine, center-(lwArrow-2), r.y(), (lwArrow-2)*2, lwArrow);

            break;
        }

        case NoKeepBelowIcon:
        {
            int center = r.x()+r.width()/2;

            // arrow
            drawObject(p, DiagonalLine, r.x(), center-2*lwArrow, center-r.x(), lwArrow);
            drawObject(p, CrossDiagonalLine, r.x()+center, r.bottom()-1-2*lwArrow, center-r.x(), lwArrow);
            if (lwArrow>1)
                drawObject(p, HorizontalLine, center-(lwArrow-2), r.bottom()-(lwArrow-1)-2*lwArrow, (lwArrow-2)*2, lwArrow);

            // Fall through to KeepBelowIcon intended!
        }
        case KeepBelowIcon:
        {
            int center = r.x()+r.width()/2;

            // arrow
            drawObject(p, DiagonalLine, r.x(), center, center-r.x(), lwArrow);
            drawObject(p, CrossDiagonalLine, r.x()+center, r.bottom()-1, center-r.x(), lwArrow);
            if (lwArrow>1)
                drawObject(p, HorizontalLine, center-(lwArrow-2), r.bottom()-(lwArrow-1), (lwArrow-2)*2, lwArrow);

            break;
        }

        case ShadeIcon:
        {
            drawObject(p, HorizontalLine, r.x(), r.y(), r.width(), lwTitleBar);

            break;
        }

        case UnShadeIcon:
        {
            int lw1 = 1;
            int lw2 = 1;
            if (r.width() > 16) {
                lw1 = 4;
                lw2 = 2;
            } else if (r.width() > 7) {
                lw1 = 2;
                lw2 = 1;
            }

            int h = QMAX( (r.width()/2), (lw1+2*lw2) );

            // horizontal bars
            drawObject(p, HorizontalLine, r.x(), r.y(), r.width(), lw1);
            drawObject(p, HorizontalLine, r.x(), r.x()+h-(lw2-1), r.width(), lw2);
            // vertical bars
            drawObject(p, VerticalLine, r.x(), r.y(), h, lw2);
            drawObject(p, VerticalLine, r.right()-(lw2-1), r.y(), h, lw2);

            break;
        }

        default:
            break;
    }

    p.end();

    bitmap.setMask(bitmap);

    return bitmap;
}

void IconEngine::drawObject(QPainter &p, Object object, int x, int y, int length, int lineWidth)
{
    switch(object) {
        case DiagonalLine:
            if (lineWidth <= 1) {
                for (int i = 0; i < length; ++i) {
                    p.drawPoint(x+i,y+i);
                }
            } else if (lineWidth <= 2) {
                for (int i = 0; i < length; ++i) {
                    p.drawPoint(x+i,y+i);
                }
                for (int i = 0; i < (length-1); ++i) {
                    p.drawPoint(x+1+i,y+i);
                    p.drawPoint(x+i,y+1+i);
                }
            } else {
                for (int i = 1; i < (length-1); ++i) {
                    p.drawPoint(x+i,y+i);
                }
                for (int i = 0; i < (length-1); ++i) {
                    p.drawPoint(x+1+i,y+i);
                    p.drawPoint(x+i,y+1+i);
                }
                for (int i = 0; i < (length-2); ++i) {
                    p.drawPoint(x+2+i,y+i);
                    p.drawPoint(x+i,y+2+i);
                }
            }
            break;
        case CrossDiagonalLine:
            if (lineWidth <= 1) {
                for (int i = 0; i < length; ++i) {
                    p.drawPoint(x+i,y-i);
                }
            } else if (lineWidth <= 2) {
                for (int i = 0; i < length; ++i) {
                    p.drawPoint(x+i,y-i);
                }
                for (int i = 0; i < (length-1); ++i) {
                    p.drawPoint(x+1+i,y-i);
                    p.drawPoint(x+i,y-1-i);
                }
            } else {
                for (int i = 1; i < (length-1); ++i) {
                    p.drawPoint(x+i,y-i);
                }
                for (int i = 0; i < (length-1); ++i) {
                    p.drawPoint(x+1+i,y-i);
                    p.drawPoint(x+i,y-1-i);
                }
                for (int i = 0; i < (length-2); ++i) {
                    p.drawPoint(x+2+i,y-i);
                    p.drawPoint(x+i,y-2-i);
                }
            }
            break;
        case HorizontalLine:
            for (int i = 0; i < lineWidth; ++i) {
                p.drawLine(x,y+i, x+length-1, y+i);
            }
            break;
        case VerticalLine:
            for (int i = 0; i < lineWidth; ++i) {
                p.drawLine(x+i,y, x+i, y+length-1);
            }
            break;
        default:
            break;
    }
}

} // KWinPARDUS
