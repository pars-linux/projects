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

#include "xpm/close.xpm"
#include "xpm/minimize.xpm"
#include "xpm/maximize.xpm"
#include "xpm/restore.xpm"
#include "xpm/help.xpm"
#include "xpm/sticky.xpm"
#include "xpm/unsticky.xpm"
#include "xpm/shade.xpm"
#include "xpm/unshade.xpm"
#include "xpm/keepabove.xpm"
#include "xpm/notkeepabove.xpm"
#include "xpm/keepbelow.xpm"
#include "xpm/notkeepbelow.xpm"
#include "xpm/empty.xpm"

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
    m_aDecoLight(QImage() ), m_iDecoLight(QImage() ),
    m_aDecoDark(QImage() ), m_iDecoDark(QImage() ),
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
    QColor aDecoFgDark = alphaBlendColors(PARDUSHandler::getColor(TitleGradientTo, true),
            Qt::black, 50);
    QColor aDecoFgLight = alphaBlendColors(PARDUSHandler::getColor(TitleGradientTo, true),
            Qt::white, 50);
    QColor iDecoFgDark = alphaBlendColors(PARDUSHandler::getColor(TitleGradientTo, false),
            Qt::black, 50);
    QColor iDecoFgLight = alphaBlendColors(PARDUSHandler::getColor(TitleGradientTo, false),
            Qt::white, 50);

    int reduceW = 0, reduceH = 0;
    if(width()>12) {
        reduceW = static_cast<int>(2*(width()/3.5) );
    }
    else
        reduceW = 4;
    if(height()>12)
        reduceH = static_cast<int>(2*(height()/3.5) );
    else
        reduceH = 4;

    QImage img;
    switch (m_type) {
        case CloseButton:
            img = QImage(close_xpm);
            break;
        case HelpButton:
            img = QImage(help_xpm);
            break;
        case MinButton:
            img = QImage(minimize_xpm);
            break;
        case MaxButton:
            if (isOn()) {
                img = QImage(restore_xpm);
            } else {
                img = QImage(maximize_xpm);
            }
            break;
        case OnAllDesktopsButton:
            if (isOn()) {
                img = QImage(unsticky_xpm);
            } else {
                img = QImage(sticky_xpm);
            }
            break;
        case ShadeButton:
            if (isOn()) {
                img = QImage(unshade_xpm);
            } else {
                img = QImage(shade_xpm);
            }
            break;
        case AboveButton:
            if (isOn()) {
                img = QImage(notkeepabove_xpm);
            } else {
                img = QImage(keepabove_xpm);
            }
            break;
        case BelowButton:
            if (isOn()) {
                img = QImage(notkeepbelow_xpm);
            } else {
                img = QImage(keepbelow_xpm);
            }
            break;
        default:
            img = QImage(empty_xpm);
            break;
    }

    m_aDecoDark = recolorImage(&img, aDecoFgDark).smoothScale(width()-reduceW, height()-reduceH);
    m_iDecoDark = recolorImage(&img, iDecoFgDark).smoothScale(width()-reduceW, height()-reduceH);
    m_aDecoLight = recolorImage(&img, aDecoFgLight).smoothScale(width()-reduceW, height()-reduceH);
    m_iDecoLight = recolorImage(&img, iDecoFgLight).smoothScale(width()-reduceW, height()-reduceH);

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
            if (PARDUSHandler::animateButtons() ) {
                animProgress++;
            } else {
                animProgress = ANIMATIONSTEPS;
            }
            animTmr->start(TIMERINTERVAL, true); // single-shot
        }
    } else {
        if(animProgress > 0) {
            if (PARDUSHandler::animateButtons() ) {
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
    if (!PARDUSHandler::initialized())
        return;

    int type = PARDUSHandler::buttonType();

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

    QColor contourTop = alphaBlendColors(PARDUSHandler::getColor(TitleGradientFrom, active),
            Qt::black, 220);
    QColor contourBottom = alphaBlendColors(PARDUSHandler::getColor(TitleGradientTo, active),
            Qt::black, 220);
    QColor surfaceTop = alphaBlendColors(PARDUSHandler::getColor(TitleGradientFrom, active),
            Qt::white, 220);
    QColor surfaceBottom = alphaBlendColors(PARDUSHandler::getColor(TitleGradientTo, active),
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
        bP.setPen(alphaBlendColors(PARDUSHandler::getColor(TitleGradientFrom, active),
                contourTop, 150) );
        bP.drawPoint(r.x()+1, r.y());
        bP.drawPoint(r.right()-1, r.y());
        bP.drawPoint(r.x(), r.y()+1);
        bP.drawPoint(r.right(), r.y()+1);
        bP.setPen(alphaBlendColors(PARDUSHandler::getColor(TitleGradientTo, active),
                contourBottom, 150) );
        bP.drawPoint(r.x()+1, r.bottom());
        bP.drawPoint(r.right()-1, r.bottom());
        bP.drawPoint(r.x(), r.bottom()-1);
        bP.drawPoint(r.right(), r.bottom()-1);

        // surface
        // fill top and bottom
        if (PARDUSHandler::buttonType() == PLASTIK_FLAT) {
		bP.setPen(surfaceTop);
		bP.drawLine(r.x()+2, r.y()+1, r.right()-2, r.y()+1 );
		bP.setPen(surfaceBottom);
		bP.drawLine(r.x()+2, r.bottom()-1, r.right()-2, r.bottom()-1 );
        } else if (PARDUSHandler::buttonType() == LIPSTIK_FLAT || isDown()) {
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
        if (PARDUSHandler::buttonType() == PLASTIK_FLAT) {
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
        QImage *deco = 0;
        if (isDown()) {
            deco = active?&m_aDecoLight:&m_iDecoLight;
        } else {
            deco = active?&m_aDecoDark:&m_iDecoDark;
        }
        dX = r.x()+(r.width()-deco->width())/2;
        dY = r.y()+(r.height()-deco->height())/2;
        if (isDown() ) {
            dY++;
        }
        bP.drawImage(dX, dY, *deco);
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
            QColor downColor = PARDUSHandler::getColor(BtnBg, active).dark(115);
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
        QImage *deco = 0;
        deco = active?&m_aDecoDark:&m_iDecoDark;
        dX = r.x()+(r.width()-deco->width())/2;
        dY = r.y()+(r.height()-deco->height())/2;
        if (isDown() ) {
            dX++;
            dY++;
        }
        bP.drawImage(dX, dY, *deco);
    }

    bP.end();
    painter->drawPixmap(0, 0, buffer);
}

void PARDUSButton::renderBtnContour(QPainter *p, const QRect &r)
{
    if((r.width() <= 0)||(r.height() <= 0))
        return;

    bool active = m_client->isActive();

    QColor backgroundColor = PARDUSHandler::getColor(BtnBg, active);
    QColor contourColor = PARDUSHandler::getColor(BtnBg, active).dark(135);

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

    QColor backgroundColor = PARDUSHandler::getColor(BtnBg, active);
    QColor baseColor = PARDUSHandler::getColor(TitleGradientFrom, active);
    QColor highlightColor;
    if(m_type == CloseButton) {
        highlightColor = QColor(255,0,0);
    } else {
        highlightColor = Qt::white;
    }

    int highlightAlpha = static_cast<int>(255-((60/static_cast<double>(ANIMATIONSTEPS))*
                                          static_cast<double>(animProgress) ) );

    QColor buttonColor, bottomColor, topLineColor, bottomLineColor;

    if (PARDUSHandler::buttonType() == LIPSTIK_3D) { // Lipstik
        buttonColor = PARDUSHandler::getColor(BtnBg, active);
        bottomColor = buttonColor.light(112);
        topLineColor = buttonColor.light(112);
        bottomLineColor = buttonColor.dark(102);
    } else { // Plastik
        bottomColor = PARDUSHandler::getColor(BtnBg, active);
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


} // KWinPARDUS
