/* SuSE KWin window decoration
  Copyright (C) 2003 Sandro Giessl <ceebx@users.sourceforge.net>

  based on the window decoration "Web":
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

#ifndef PARDUSBUTTON_H
#define PARDUSBUTTON_H

#include <qbutton.h>
#include <qpixmap.h>
#include <qintcache.h>
#include "PARDUS.h"

class QTimer;

namespace KWinPARDUS {

class PARDUSClient;

class PARDUSButton : public QButton
{
    Q_OBJECT
public:
    PARDUSButton(PARDUSClient *parent, const char *name, const QString &tip, ButtonType type, int size, bool toggle = false, int btns = LeftButton);
    ~PARDUSButton();

    QSize sizeHint() const; ///< Return size hint.
    ButtonState lastMousePress() const { return m_lastMouse; }
    void reset() { repaint(false); }
    PARDUSClient * client() { return m_client; }
    virtual void setOn(bool on);
    void setDeco();
    void setTipText(const QString &tip);
    void setSize(const int s);

protected slots:
    void animate();

private:
    void enterEvent(QEvent *e);
    void leaveEvent(QEvent *e);
    void mousePressEvent(QMouseEvent *e);
    void mouseReleaseEvent(QMouseEvent *e);
    void drawButton(QPainter *painter);
    void drawPlastikBtn(QPainter *painter);
    void drawLipstikBtn(QPainter *painter);
    void renderBtnContour(QPainter *p, const QRect &r);
    void renderBtnSurface(QPainter *p, const QRect &r) const;
    void renderPixel(QPainter *p,
        		       const QPoint &pos,
        		       const int alpha,
        		       const QColor &color) const;
    void renderGradient(QPainter *p,
                        const QRect &r,
                        const QColor &c1,
                        const QColor &c2) const;


private:
    PARDUSClient *m_client;
    ButtonState m_lastMouse;
    int m_realizeButtons;

    int m_size;

    ButtonType m_type;
    ButtonIcon btnType;
    bool hover;

    QTimer *animTmr;
    uint animProgress;
    // pixmap cache.
    enum CacheEntryType {
        cSurface,
        cGradientTile,
        cAlphaDot
    };
    struct CacheEntry
    {
        CacheEntryType type;
        int width;
        int height;
        QRgb c1Rgb;
        QRgb c2Rgb;

        QPixmap* pixmap;

        CacheEntry(CacheEntryType t, int w, int h, QRgb c1, QRgb c2 = 0, QPixmap* p = 0 ):
            type(t), width(w), height(h), c1Rgb(c1), c2Rgb(c2), pixmap(p)
        {}

        ~CacheEntry()
        {
            delete pixmap;
        }

        int key()
        {
            // create an int key from the properties which is used to refer to entries in the QIntCache.
            // the result may not be 100% correct as we don't have so much space in one integer -- use
            // == operator after find to make sure we got the right one. :)
            return 1 ^ (type<<1) ^ (width<<5) ^ (height<<10) ^ (c1Rgb<<19) ^ (c2Rgb<<22);
        }

        bool operator == (const CacheEntry& other)
        {
            bool match = (type == other.type) &&
                        (width   == other.width) &&
                        (height == other.height) &&
                        (c1Rgb == other.c1Rgb) &&
                        (c1Rgb == other.c1Rgb);
            return match;
        }
    };
    QIntCache<CacheEntry> *pixmapCache;
};

/**
 * This class creates bitmaps which can be used as icons on buttons. The icons
 * are "hardcoded".
 * Over the previous "Gimp->xpm->QImage->recolor->SmoothScale->QPixmap" solution
 * it has the important advantage that icons are more scalable and at the same
 * time sharp and not blurred.
 */
class IconEngine
{
    public:
        static QBitmap icon(ButtonIcon icon, int size);

    private:
        enum Object {
            HorizontalLine,
            VerticalLine,
            DiagonalLine,
            CrossDiagonalLine
        };

        static void drawObject(QPainter &p, Object object, int x, int y, int length, int lineWidth);
};

} // namespace KWinPARDUS

#endif
