/* SuSE KWin window decoration
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

#include <klocale.h>
#include <kpixmap.h>
#include <kimageeffect.h>
#include <kpixmapeffect.h>
#include <kstandarddirs.h>
#include <kdecoration.h>

#include <qbitmap.h>
#include <qdatetime.h>
#include <qfontmetrics.h>
#include <qimage.h>
#include <qlabel.h>
#include <qlayout.h>
#include <qpainter.h>
#include <qpixmap.h>
#include <qimage.h>

#include "PARDUSclient.h"
#include "PARDUSclient.moc"
#include "PARDUSbutton.h"
#include "misc.h"
#include "shadow.h"

// Default button layout
const char default_left[]  = "M";
const char default_right[] = "HIAX";

namespace KWinPARDUS
{
PARDUSClient::PARDUSClient(KDecorationBridge* bridge, KDecorationFactory* factory)
    : KDecoration(bridge, factory),
    mainLayout_(0),
    topSpacer_(0), titleSpacer_(0), leftTitleSpacer_(0), rightTitleSpacer_(0),
    decoSpacer_(0), leftSpacer_(0), rightSpacer_(0), bottomSpacer_(0),
    aCaptionBuffer(0), iCaptionBuffer(0),
    aTitleBarTile(0), iTitleBarTile(0),
    pixmaps_created(false),
    captionBufferDirty(true),
    closing(false),
    s_titleHeight(0),
    s_titleFont(QFont())
{}

PARDUSClient::~PARDUSClient()
{
    delete_pixmaps();

    delete aCaptionBuffer;
    delete iCaptionBuffer;

    for (int n=0; n<NumButtons; n++) {
        if (m_button[n]) delete m_button[n];
    }
}

void PARDUSClient::init()
{
    connect(this, SIGNAL(keepAboveChanged(bool)), SLOT(keepAboveChange(bool)));
    connect(this, SIGNAL(keepBelowChanged(bool)), SLOT(keepBelowChange(bool)));

    s_titleHeight = isTool() ?
                    Handler()->titleHeightTool()
                    : Handler()->titleHeight();
    s_titleFont = isTool() ?
                  Handler()->titleFontTool()
                  : Handler()->titleFont();

    createMainWidget(WNoAutoErase);

    widget()->installEventFilter(this);

    // for flicker-free redraws
    widget()->setBackgroundMode(NoBackground);

    _resetLayout();

    create_pixmaps();

    aCaptionBuffer = new QPixmap();
    iCaptionBuffer = new QPixmap();
    captionBufferDirty = true;
    widget()->update(titleSpacer_->geometry());
}

const int SUPPORTED_WINDOW_TYPES_MASK = NET::NormalMask | NET::DesktopMask | NET::DockMask
    | NET::ToolbarMask | NET::MenuMask | NET::DialogMask | NET::OverrideMask | NET::TopMenuMask
    | NET::UtilityMask | NET::SplashMask;

bool PARDUSClient::isTool()
{
    NET::WindowType type = windowType(SUPPORTED_WINDOW_TYPES_MASK);
    return ((type==NET::Toolbar)||(type==NET::Utility)||(type==NET::Menu));
}

void PARDUSClient::resizeEvent()
{
    doShape();

    // FIXME: don't update() here! this would result in two paintEvent()s
    // because there is already "something" else triggering the repaint...
    // needed if the corners change
//    if (Handler()->roundCorners() == 2) widget()->update();
}

void PARDUSClient::paintEvent(QPaintEvent*)
{
    if (!Handler()->initialized()) return;

    if (captionBufferDirty) update_captionBuffer();

    bool active = isActive();

    QPainter painter(widget());

    // colors...
    const QColor windowContour = Handler()->getColor(WindowContour, active);
    const QColor innerWindowContour = Handler()->getColor(TitleGradientTo, active);
    const QColor deco = Handler()->getColor(TitleGradientTo, active);
    const QColor aBorder = Handler()->getColor(Border, active);
    const QColor iBorder = innerWindowContour;

    QRect Rtop(topSpacer_->geometry());
    QRect Rtitle(titleSpacer_->geometry());
    QRect Rltitle(leftTitleSpacer_->geometry());
    QRect Rrtitle(rightTitleSpacer_->geometry());
    QRect Rdeco(decoSpacer_->geometry());
    QRect Rleft(leftSpacer_->geometry());
    QRect Rright(rightSpacer_->geometry());
    QRect Rbottom(bottomSpacer_->geometry());
    QRect tempRect;

    // the title background over full width
    painter.drawTiledPixmap(Rleft.left(), Rtitle.top() - TOPMARGIN,
                            Rbottom.width(), Rtitle.height() + Rdeco.height() + TOPMARGIN,
                            active ? *aTitleBarTile : *iTitleBarTile);

    // leftTitleSpacer
    if(Rltitle.width() > 0) {
        painter.setPen(windowContour );
        painter.drawLine(Rltitle.left(), Rltitle.top(),
                         Rltitle.left(), Rdeco.bottom() );

        painter.setPen(innerWindowContour );
        painter.drawLine(Rltitle.left()+1, Rltitle.top()+1,
                         Rltitle.left()+1, Rdeco.bottom() );
    }

    // rightTitleSpacer
    if(Rrtitle.width() > 0) {
        painter.setPen(windowContour );
        painter.drawLine(Rrtitle.right(), Rrtitle.top(),
                         Rrtitle.right(), Rdeco.bottom() );

        painter.setPen(innerWindowContour );
        painter.drawLine(Rrtitle.right()-1, Rrtitle.top()+1,
                         Rrtitle.right()-1, Rdeco.bottom() );
    }

    // titleSpacer
    QPixmap *titleBfrPtr = active ? aCaptionBuffer : iCaptionBuffer;
    if(Rtitle.width() > 0 && titleBfrPtr != 0) {
        const int titleMargin = 5; // 5 px between title and buttons

        int tX, tW;
        switch (Handler()->titleAlign()) {
            // AlignCenter
            case Qt::AlignHCenter:
                tX = (titleBfrPtr->width() > Rtitle.width()-2 * titleMargin) ?
                        (Rtitle.left()+titleMargin)
                        : Rtitle.left()+(Rtitle.width()- titleBfrPtr->width())/2;
                tW = (titleBfrPtr->width() > Rtitle.width()-2 * titleMargin) ?
                        (Rtitle.width()-2 * titleMargin)
                        : titleBfrPtr->width();
                break;
            // AlignRight
            case Qt::AlignRight:
                tX = (titleBfrPtr->width() > Rtitle.width()-2 * titleMargin) ?
                        (Rtitle.left()+titleMargin)
                        : Rtitle.right()-titleMargin-titleBfrPtr->width();
                tW = (titleBfrPtr->width() > Rtitle.width()-2 * titleMargin) ?
                        (Rtitle.width()-2 * titleMargin)
                        : titleBfrPtr->width();
                break;
            // AlignLeft
            default:
                tX = (Rtitle.left()+titleMargin);
                tW = (titleBfrPtr->width() > Rtitle.width()-2 * titleMargin) ?
                        (Rtitle.width()-2 * titleMargin)
                        : titleBfrPtr->width();
        }

        if(tW > 0) {
            painter.drawTiledPixmap(tX, Rtitle.top() - TOPMARGIN,
                                    tW, Rtitle.height() + Rdeco.height() + TOPMARGIN,
                                    *titleBfrPtr);
        }
    }
    titleBfrPtr = 0;

    // title border lines
    painter.setPen(windowContour);
    if (Handler()->roundCorners() == 1 ||
        (Handler()->roundCorners() == 2 && maximizeMode() != MaximizeFull)) {
        // top line
        if (maximizeMode() != MaximizeFull || options()->moveResizeMaximizedWindows()) {
            painter.drawLine(Rtop.left()+5, Rtop.top(), Rtop.right()-5, Rtop.top());
            painter.setPen(iBorder);
            painter.drawLine(Rtop.left()+3, Rtop.top()+1, Rtop.right()-3, Rtop.top()+1);
            painter.setPen(windowContour);
        }

        // left corner - rounded
        painter.drawLine(Rtop.left()+3, Rtop.top()+1, Rtop.left()+4, Rtop.top()+1 );
        painter.drawPoint(Rtop.left()+2, Rtop.top()+2 );
        painter.drawLine(Rtop.left()+1, Rtop.top()+3, Rtop.left()+1, Rtop.top()+4 );
        // right corner - rounded
        painter.drawLine(Rtop.right()-3, Rtop.top()+1, Rtop.right()-4, Rtop.top()+1 );
        painter.drawPoint(Rtop.right()-2, Rtop.top()+2 );
        painter.drawLine(Rtop.right()-1, Rtop.top()+3, Rtop.right()-1, Rtop.top()+4 );
        // left side
        painter.drawLine(Rtop.left(), Rtop.top()+5, Rtop.left(), Rtop.bottom() );
        // right side
        painter.drawLine(Rtop.right(), Rtop.top()+5, Rtop.right(), Rtop.bottom() );

        painter.setPen(iBorder);
        // left inner corner
        painter.drawLine(Rtop.left()+3, Rtop.top()+2, Rtop.left()+4, Rtop.top()+2 );
        painter.drawLine(Rtop.left()+2, Rtop.top()+3, Rtop.left()+2, Rtop.top()+4 );
        // right inner corner
        painter.drawLine(Rtop.right()-3, Rtop.top()+2, Rtop.right()-4, Rtop.top()+2 );
        painter.drawLine(Rtop.right()-2, Rtop.top()+3, Rtop.right()-2, Rtop.top()+4 );
    } else {
        // top line
        if (maximizeMode() != MaximizeFull || options()->moveResizeMaximizedWindows()) {
            painter.drawLine(Rtop.left()+2, Rtop.top(), Rtop.right()-2, Rtop.top() );
            painter.setPen(iBorder);
            painter.drawLine(Rtop.left()+1, Rtop.top()+1, Rtop.right()-1, Rtop.top()+1);
            painter.setPen(windowContour);
        }

        painter.setPen(alphaBlendColors(iBorder, windowContour, 110));
        // left corner
        painter.drawLine(Rtop.left(), Rtop.top(), Rtop.left()+1, Rtop.top());
        painter.drawPoint(Rtop.left(), Rtop.top()+1);
        // right corner
        painter.drawLine(Rtop.right(), Rtop.top(), Rtop.right()-1, Rtop.top());
        painter.drawPoint(Rtop.right(), Rtop.top()+1);

        painter.setPen(windowContour);
        // left side
        painter.drawLine(Rtop.left(), Rtop.top()+2, Rtop.left(), Rtop.bottom());
        // right side
        painter.drawLine(Rtop.right(), Rtop.top()+2, Rtop.right(), Rtop.bottom());

        painter.setPen(iBorder);
        // left inner corner
        painter.drawLine(Rtop.left()+1, Rtop.top()+2, Rtop.left()+1, Rtop.top()+4);
        // right inner corner
        painter.drawLine(Rtop.right()-1, Rtop.top()+2, Rtop.right()-1, Rtop.top()+4);
    }

    // leftSpacer
    if (Rleft.width() > 0 && Rleft.height() > 0) {
        painter.setPen(windowContour);
        painter.drawLine(Rleft.left(), Rleft.top(), Rleft.left(), Rleft.bottom());
        painter.drawLine(Rleft.right(), Rleft.top(), Rleft.right(), Rleft.bottom());

        painter.setPen(iBorder);
        painter.drawLine(Rleft.left()+1, Rleft.top(), Rleft.left()+1, Rleft.bottom());

        if (Rleft.width() > 3) {
            tempRect.setCoords(Rleft.left()+2, Rleft.top(),
                            Rleft.right()-1, Rleft.bottom() );
            painter.fillRect(tempRect, active ? aGradientBottom : iGradientBottom);
        }
    }

    // rightSpacer
    if(Rright.width() > 0 && Rright.height() > 0) {
        painter.setPen(windowContour);
        painter.drawLine(Rright.right(), Rright.top(), Rright.right(), Rright.bottom());
        painter.drawLine(Rright.left(), Rright.top(), Rright.left(), Rright.bottom());

        painter.setPen(iBorder);
        painter.drawLine(Rright.right()-1, Rright.top(), Rright.right()-1, Rright.bottom());

        if(Rright.width() > 3) {
            tempRect.setCoords(Rright.left()+1, Rright.top(), Rright.right()-2, Rright.bottom());
            painter.fillRect(tempRect, active ? aGradientBottom : iGradientBottom);
        }
    }

    // bottomSpacer
    if (Rbottom.height() > 0) {
        // bottom line
        painter.setPen(windowContour);
        painter.drawLine(Rbottom.left()+2, Rbottom.bottom(),
                         Rbottom.right()-2, Rbottom.bottom());

        painter.setPen(iBorder);
        painter.drawLine(Rbottom.left()+2, Rbottom.bottom()-1,
                         Rbottom.right()-2, Rbottom.bottom()-1);


        if (Rleft.width() != 0) {
            painter.setPen(iBorder);
            painter.drawLine(Rleft.left()+1, Rbottom.top(), Rleft.left()+1, Rbottom.bottom()-1);

            painter.setPen(windowContour);
            // rounded left bottom corner - side
            painter.drawLine(Rbottom.left(), Rbottom.top(), Rbottom.left(), Rbottom.bottom()-2);

            // anti-alias for the window contour...
            painter.setPen(alphaBlendColors(iBorder, windowContour, 110) );
            painter.drawLine(Rbottom.left(), Rbottom.bottom()-1, Rbottom.left(), Rbottom.bottom());
            painter.drawPoint(Rbottom.left()+1, Rbottom.bottom());
        }

        if (Rright.width() != 0) {
            painter.setPen(iBorder);
            painter.drawLine(Rright.right()-1, Rbottom.top(), Rright.right()-1, Rbottom.bottom()-1);

            painter.setPen(windowContour);
            // rounded right bottom corner - side
            painter.drawLine(Rbottom.right(), Rbottom.top(), Rbottom.right(), Rbottom.bottom()-2);

            // anti-alias for the window contour...
            painter.setPen(alphaBlendColors(iBorder, windowContour, 110) );
            painter.drawLine(Rbottom.right(), Rbottom.bottom()-1, Rbottom.right(), Rbottom.bottom());
            painter.drawPoint(Rbottom.right()-1, Rbottom.bottom());
        }

        int l;
        if (Rleft.width() != 0)
            l = Rbottom.left()+2;
        else
            l = Rbottom.left();
        int r;
        if (Rright.width() != 0)
            r = Rbottom.right()-2;
        else
            r = Rbottom.right();

        if (Rbottom.height() > 3) {
            tempRect.setCoords(l, Rbottom.bottom()-Handler()->borderSize()+1, r, Rbottom.bottom()-2);
            painter.fillRect(tempRect, active ? aGradientBottom : iGradientBottom);
        }

        painter.setPen(windowContour);
        painter.drawLine(l, Rbottom.bottom(), r, Rbottom.bottom());
        painter.drawLine(Rbottom.left()+Handler()->borderSize()-1, Rbottom.bottom()-Handler()->borderSize()+1,
                         Rbottom.left()+Handler()->borderSize()-1, Rbottom.top() );
        painter.drawLine(Rbottom.right()-Handler()->borderSize()+1, Rbottom.bottom()-Handler()->borderSize()+1,
                         Rbottom.right()-Handler()->borderSize()+1, Rbottom.top() );
        painter.drawLine(Rbottom.left()+Handler()->borderSize(), Rbottom.bottom()-Handler()->borderSize()+1,
                         Rbottom.right()-Handler()->borderSize(), Rbottom.bottom()-Handler()->borderSize()+1 );
    }
}

void PARDUSClient::mouseDoubleClickEvent(QMouseEvent *e)
{
    if (titleSpacer_->geometry().contains(e->pos())) titlebarDblClickOperation();
}

void PARDUSClient::doShape()
{
    int w = widget()->width();
    int h = widget()->height();
    int r(w);
    int b(h);

    QRegion mask(0, 0, w, h);

    if (titleSpacer_->geometry().height() > 0) {
        // Remove top-left corner.
        if (leftTitleSpacer_->geometry().width() > 0 &&
            (Handler()->roundCorners() == 1 ||
            (Handler()->roundCorners() == 2 && maximizeMode() != MaximizeFull))) {
            mask -= QRegion(0, 0, 1, 5);
            mask -= QRegion(0, 0, 2, 3);
            mask -= QRegion(0, 0, 3, 2);
            mask -= QRegion(0, 0, 5, 1);
        } else if (maximizeMode() == MaximizeFull) {
            // don't let the background shine through with sharp corners and maximized
        } else {
            mask -= QRegion(0, 0, 1, 1);
        }
        // Remove top-right corner.
        if (rightTitleSpacer_->geometry().width() > 0 &&
            (Handler()->roundCorners() == 1 ||
            (Handler()->roundCorners() == 2 && maximizeMode() != MaximizeFull))) {
            mask -= QRegion(r-1, 0, 1, 5);
            mask -= QRegion(r-2, 0, 2, 3);
            mask -= QRegion(r-3, 0, 3, 2);
            mask -= QRegion(r-5, 0, 5, 1);
        } else if (maximizeMode() == MaximizeFull) {
            // don't let the background shine through with sharp corners and maximized
        } else {
            mask -= QRegion(r-1, 0, 1, 1);
        }
    }

    // Remove bottom-left corner and bottom-right corner.
    if (bottomSpacer_->geometry().height() > 0 && maximizeMode() != MaximizeFull) {
        mask -= QRegion(0, b-1, 1, 1);
        mask -= QRegion(r-1, b-1, 1, 1);
    }

    setMask(mask);
}

void PARDUSClient::_resetLayout()
{
    // basic layout:
    //  _______________________________________________________________
    // |                         topSpacer                             |
    // |_______________________________________________________________|
    // | leftTitleSpacer | btns | titleSpacer | bts | rightTitleSpacer |
    // |_________________|______|_____________|_____|__________________|
    // |                         decoSpacer                            |
    // |_______________________________________________________________|
    // | |                                                           | |
    // | |                      contentsFake                         | |
    // | |                                                           | |
    // |leftSpacer                                          rightSpacer|
    // |_|___________________________________________________________|_|
    // |                           bottomSpacer                        |
    // |_______________________________________________________________|
    //

    if (!Handler()->initialized()) return;

    delete mainLayout_;

    delete topSpacer_;
    delete titleSpacer_;
    delete leftTitleSpacer_;
    delete rightTitleSpacer_;
    delete decoSpacer_;
    delete leftSpacer_;
    delete rightSpacer_;
    delete bottomSpacer_;

    mainLayout_ = new QVBoxLayout(widget(), 0, 0);

    topSpacer_        = new QSpacerItem(1, TOPMARGIN, QSizePolicy::Expanding, QSizePolicy::Fixed);
    titleSpacer_      = new QSpacerItem(1, s_titleHeight,
                                        QSizePolicy::Expanding, QSizePolicy::Fixed);
    leftTitleSpacer_  = new QSpacerItem(SIDETITLEMARGIN, s_titleHeight,
                                        QSizePolicy::Fixed, QSizePolicy::Fixed);
    rightTitleSpacer_ = new QSpacerItem(SIDETITLEMARGIN, s_titleHeight,
                                        QSizePolicy::Fixed, QSizePolicy::Fixed);
    decoSpacer_       = new QSpacerItem(1, DECOHEIGHT, QSizePolicy::Expanding, QSizePolicy::Fixed);
    leftSpacer_       = new QSpacerItem(Handler()->borderSize(), 1,
                                        QSizePolicy::Fixed, QSizePolicy::Expanding);
    rightSpacer_      = new QSpacerItem(Handler()->borderSize(), 1,
                                        QSizePolicy::Fixed, QSizePolicy::Expanding);
    bottomSpacer_     = new QSpacerItem(1, Handler()->borderSize(),
                                        QSizePolicy::Expanding, QSizePolicy::Fixed);

    // top
    mainLayout_->addItem(topSpacer_);

    // title
    QHBoxLayout *titleLayout_ = new QHBoxLayout(mainLayout_, 0, 0);

    // sizeof(...) is calculated at compile time
    memset(m_button, 0, sizeof(PARDUSButton *) * NumButtons);

    titleLayout_->addItem(Handler()->reverseLayout() ? rightTitleSpacer_ : leftTitleSpacer_);
    addButtons(titleLayout_,
               options()->customButtonPositions() ? options()->titleButtonsLeft() : QString(default_left),
               s_titleHeight-1);
    titleLayout_->addItem(titleSpacer_);
    addButtons(titleLayout_,
               options()->customButtonPositions() ? options()->titleButtonsRight() : QString(default_right),
               s_titleHeight-1);
    titleLayout_->addItem(Handler()->reverseLayout() ? leftTitleSpacer_ : rightTitleSpacer_);

    // deco
    mainLayout_->addItem(decoSpacer_);

    //Mid
    QHBoxLayout *midLayout   = new QHBoxLayout(mainLayout_, 0, 0);
    midLayout->addItem(Handler()->reverseLayout() ? rightSpacer_ : leftSpacer_);

    if( isPreview())
        midLayout->addWidget(new QLabel("<center><b>" + i18n("PARDUS preview (Version 0.3.1)") + "</b></center>", widget()));
    else
        midLayout->addItem(new QSpacerItem(0, 0));

    midLayout->addItem(Handler()->reverseLayout() ? leftSpacer_ : rightSpacer_);

    //Bottom
    mainLayout_->addItem(bottomSpacer_);


}

void PARDUSClient::addButtons(QBoxLayout *layout, const QString &s, int buttonSize)
{
    if (s.length() > 0) {
        for (unsigned n=0; n < s.length(); n++) {
            switch (s[n]) {
                case 'M': // Menu button
                    if (!m_button[MenuButton]){
                        m_button[MenuButton] = new PARDUSButton(this, "menu", i18n("Menu"),
                                                              MenuButton, buttonSize, LeftButton|RightButton);
                        connect(m_button[MenuButton], SIGNAL(pressed()), SLOT(menuButtonPressed()));
                        connect(m_button[MenuButton], SIGNAL(released()), this, SLOT(menuButtonReleased()));
                      layout->addWidget(m_button[MenuButton], 0, Qt::AlignHCenter | Qt::AlignTop);
                    }
                    break;
                case 'S': // OnAllDesktops button
                    if (!m_button[OnAllDesktopsButton]){
                        const bool oad = isOnAllDesktops();
                        m_button[OnAllDesktopsButton] = new PARDUSButton(this, "on_all_desktops",
                                                                       oad ? i18n("Not on all desktops")
                                                                       : i18n("On all desktops"),
                                                                       OnAllDesktopsButton, buttonSize, true);
                        m_button[OnAllDesktopsButton]->setOn(oad);
                        connect(m_button[OnAllDesktopsButton], SIGNAL(clicked()), SLOT(toggleOnAllDesktops()));
                        layout->addWidget(m_button[OnAllDesktopsButton], 0, Qt::AlignHCenter | Qt::AlignTop);
                    }
                    break;
                case 'H': // Help button
                    if ((!m_button[HelpButton]) && providesContextHelp()) {
                        m_button[HelpButton] = new PARDUSButton(this, "help", i18n("Help"), HelpButton, buttonSize);
                       connect(m_button[HelpButton], SIGNAL(clicked()), SLOT(showContextHelp()));
                       layout->addWidget(m_button[HelpButton], 0, Qt::AlignHCenter | Qt::AlignTop);
                    }
                    break;
                case 'I': // Minimize button
                    if ((!m_button[MinButton]) && isMinimizable()) {
                        m_button[MinButton] = new PARDUSButton(this, "minimize", i18n("Minimize"), MinButton, buttonSize);
                        connect(m_button[MinButton], SIGNAL(clicked()), SLOT(minimize()));
                        layout->addWidget(m_button[MinButton], 0, Qt::AlignHCenter | Qt::AlignTop);
                    }
                    break;
                case 'A': // Maximize button
                    if ((!m_button[MaxButton]) && isMaximizable()) {
                        const bool max = maximizeMode()!=MaximizeRestore;
                        m_button[MaxButton] = new PARDUSButton(this, "maximize",
                                                             max ?i18n("Restore") : i18n("Maximize"),
                                                             MaxButton, buttonSize, true,
                                                             LeftButton|MidButton|RightButton);
                        m_button[MaxButton]->setOn(max);
                        connect(m_button[MaxButton], SIGNAL(clicked()), SLOT(slotMaximize()));
                        layout->addWidget(m_button[MaxButton], 0, Qt::AlignHCenter | Qt::AlignTop);
                    }
                    break;
                case 'X': // Close button
                    if ((!m_button[CloseButton]) && isCloseable()) {
                        m_button[CloseButton] = new PARDUSButton(this, "close", i18n("Close"), CloseButton, buttonSize);
                        connect(m_button[CloseButton], SIGNAL(clicked()), SLOT(closeWindow()));
                        layout->addWidget(m_button[CloseButton], 0, Qt::AlignHCenter | Qt::AlignTop);
                    }
                    break;
                case 'F': // AboveButton button
                    if (!m_button[AboveButton]) {
                        bool above = keepAbove();
                        m_button[AboveButton] = new PARDUSButton(this, "above",
                                                               above ? i18n("Do not keep above others")
                                                               : i18n("Keep above others"),
                                                               AboveButton, buttonSize, true);
                        m_button[AboveButton]->setOn(above);
                        connect(m_button[AboveButton], SIGNAL(clicked()), SLOT(slotKeepAbove()));
                        layout->addWidget(m_button[AboveButton], 0, Qt::AlignHCenter | Qt::AlignTop);
                    }
                    break;
                case 'B': // BelowButton button
                    if (!m_button[BelowButton]) {
                        bool below = keepBelow();
                        m_button[BelowButton] = new PARDUSButton(this, "below",
                                                               below ? i18n("Do not keep below others")
                                                               : i18n("Keep below others"),
                                                               BelowButton, buttonSize, true);
                        m_button[BelowButton]->setOn(below);
                        connect(m_button[BelowButton], SIGNAL(clicked()), SLOT(slotKeepBelow()));
                        layout->addWidget(m_button[BelowButton], 0, Qt::AlignHCenter | Qt::AlignTop);
                    }
                    break;
                case 'L': // Shade button
                    if ((!m_button[ShadeButton]) && isShadeable()) {
                        bool shaded = isSetShade();
                        m_button[ShadeButton] = new PARDUSButton(this, "shade",
                                                               shaded ? i18n("Unshade") : i18n("Shade"),
                                                               ShadeButton, buttonSize, true);
                        m_button[ShadeButton]->setOn(shaded);
                        connect(m_button[ShadeButton], SIGNAL(clicked()), SLOT(slotShade()));
                        layout->addWidget(m_button[ShadeButton], 0, Qt::AlignHCenter | Qt::AlignTop);
                    }
                    break;
                case '_': // Spacer item
                    layout->addSpacing(3); // add a 3 px spacing...
            }

            // add 2 px spacing between buttons
            if(n < (s.length()-1) ) // and only between them!
                layout->addSpacing (1);
        }
    }
}

void PARDUSClient::captionChange()
{
    captionBufferDirty = true;
    QRect g = titleSpacer_->geometry();
    g.setHeight(titleSpacer_->geometry().height() + decoSpacer_->geometry().height());
    widget()->update(g);
}

void PARDUSClient::reset(unsigned long changed)
{
    if (changed & SettingColors) {
        // repaint the whole thing
        delete_pixmaps();
        create_pixmaps();
        captionBufferDirty = true;
        widget()->update();
        for (int n=0; n<NumButtons; n++) {
            if (m_button[n]) m_button[n]->update();
        }
    } else if (changed & SettingFont) {
        // font has changed -- update title height and font
        s_titleHeight = isTool() ?
                        Handler()->titleHeightTool()
                        : Handler()->titleHeight();
        s_titleFont = isTool() ?
                      Handler()->titleFontTool()
                      : Handler()->titleFont();
        // update buttons
        for (int n=0; n<NumButtons; n++) {
            if (m_button[n]) m_button[n]->setSize(s_titleHeight-1);
        }
        // update the spacer
        titleSpacer_->changeSize(1, s_titleHeight,
                                 QSizePolicy::Expanding, QSizePolicy::Fixed);
        // then repaint
        delete_pixmaps();
        create_pixmaps();
        captionBufferDirty = true;
        widget()->update();
    }
}

PARDUSClient::Position PARDUSClient::mousePosition(const QPoint &point) const
{
    const int corner = 18+3 * Handler()->borderSize()/2;
    Position pos = PositionCenter;

    // often needed coords..
    QRect topRect(topSpacer_->geometry());
    QRect decoRect(decoSpacer_->geometry());
    QRect leftRect(leftSpacer_->geometry());
    QRect leftTitleRect(leftTitleSpacer_->geometry());
    QRect rightRect(rightSpacer_->geometry());
    QRect rightTitleRect(rightTitleSpacer_->geometry());
    QRect bottomRect(bottomSpacer_->geometry());

    if(bottomRect.contains(point)) {
        if      (point.x() <= bottomRect.left()+corner)  pos = PositionBottomLeft;
        else if (point.x() >= bottomRect.right()-corner) pos = PositionBottomRight;
        else                                             pos = PositionBottom;
    }
    else if(leftRect.contains(point)) {
        if      (point.y() <= topRect.top()+corner)       pos = PositionTopLeft;
        else if (point.y() >= bottomRect.bottom()-corner) pos = PositionBottomLeft;
        else                                              pos = PositionLeft;
    }
    else if(leftTitleRect.contains(point)) {
        if      (point.y() <= topRect.top()+corner)       pos = PositionTopLeft;
        else                                              pos = PositionLeft;
    }
    else if(rightRect.contains(point)) {
        if      (point.y() <= topRect.top()+corner)       pos = PositionTopRight;
        else if (point.y() >= bottomRect.bottom()-corner) pos = PositionBottomRight;
        else                                              pos = PositionRight;
    }
    else if(rightTitleRect.contains(point)) {
        if      (point.y() <= topRect.top()+corner)       pos = PositionTopRight;
        else                                              pos = PositionRight;
    }
    else if(topRect.contains(point)) {
        if      (point.x() <= topRect.left()+corner)      pos = PositionTopLeft;
        else if (point.x() >= topRect.right()-corner)     pos = PositionTopRight;
        else                                              pos = PositionTop;
    }
    else if(decoRect.contains(point)) {
        if(point.x() <= leftTitleRect.right()) {
            if(point.y() <= topRect.top()+corner)         pos = PositionTopLeft;
            else                                          pos = PositionLeft;
        }
        else if(point.x() >= rightTitleRect.left()) {
            if(point.y() <= topRect.top()+corner)         pos = PositionTopRight;
            else                                          pos = PositionRight;
        }
    }

    return pos;
}

void PARDUSClient::iconChange()
{
    if (m_button[MenuButton]) {
        m_button[MenuButton]->update();
    }
}

void PARDUSClient::activeChange()
{
    for (int n=0; n<NumButtons; n++)
        if (m_button[n]) m_button[n]->update();
    widget()->update();
}

void PARDUSClient::maximizeChange()
{
    if (!Handler()->initialized()) return;

    if (m_button[MaxButton]) {
        m_button[MaxButton]->setOn(maximizeMode()==MaximizeFull);
        m_button[MaxButton]->setTipText((maximizeMode()==MaximizeRestore) ?
                                         i18n("Maximize")
                                         : i18n("Restore"));
    }
    if (Handler()->roundCorners() == 2) widget()->update();
}

void PARDUSClient::desktopChange()
{
    if (m_button[OnAllDesktopsButton]) {
        m_button[OnAllDesktopsButton]->setOn(isOnAllDesktops());
        m_button[OnAllDesktopsButton]->setTipText(isOnAllDesktops() ?
                                                  i18n("Not on all desktops")
                                                  : i18n("On all desktops"));
    }
}

void PARDUSClient::shadeChange()
{
    if (m_button[ShadeButton]) {
        bool shaded = isSetShade();
        m_button[ShadeButton]->setOn(shaded);
        m_button[ShadeButton]->setTipText(shaded ?
                                          i18n("Unshade")
                                          : i18n("Shade"));
    }
}

void PARDUSClient::slotMaximize()
{
    if (m_button[MaxButton]) {
        maximize(m_button[MaxButton]->lastMousePress());
        doShape();
    }
}

void PARDUSClient::slotShade()
{
    setShade(!isSetShade());
}

void PARDUSClient::slotKeepAbove()
{
    setKeepAbove(!keepAbove());
}

void PARDUSClient::slotKeepBelow()
{
    setKeepBelow(!keepBelow());
}

void PARDUSClient::keepAboveChange(bool above)
{
    if (m_button[AboveButton]) {
        m_button[AboveButton]->setOn(above);
        m_button[AboveButton]->setTipText(above ? i18n("Do not keep above others") : i18n("Keep above others"));
    }

    if (m_button[BelowButton] && m_button[BelowButton]->isOn()) {
        m_button[BelowButton]->setOn(false);
        m_button[BelowButton]->setTipText(i18n("Keep below others"));
    }
}

void PARDUSClient::keepBelowChange(bool below)
{
    if (m_button[BelowButton]) {
        m_button[BelowButton]->setOn(below);
        m_button[BelowButton]->setTipText(below ? i18n("Do not keep below others") : i18n("Keep below others"));
    }

    if (m_button[AboveButton] && m_button[AboveButton]->isOn()) {
        m_button[AboveButton]->setOn(false);
        m_button[AboveButton]->setTipText(i18n("Keep above others"));
    }
}

void PARDUSClient::menuButtonPressed()
{
    static QTime *t = NULL;
    static PARDUSClient *lastClient = NULL;
    if (t == NULL)
        t = new QTime;
    bool dbl = (lastClient==this && t->elapsed() <= QApplication::doubleClickInterval());
    lastClient = this;
    t->start();
    if (!dbl || !Handler()->menuClose()) {
        QRect menuRect = m_button[MenuButton]->rect();
        QPoint menutop = m_button[MenuButton]->mapToGlobal(menuRect.topLeft());
        QPoint menubottom = m_button[MenuButton]->mapToGlobal(menuRect.bottomRight());
        KDecorationFactory* f = factory();
        showWindowMenu(QRect(menutop, menubottom));
        if( !f->exists(this)) // 'this' was deleted
            return;
        m_button[MenuButton]->setDown(false);
    }
    else
        closing = true;
}

void PARDUSClient::menuButtonReleased()
{
    if(closing)
        closeWindow();
}

void PARDUSClient::create_pixmaps()
{
    if(pixmaps_created)
        return;

    KPixmap tempPixmap;
    QPainter painter;

    // aTitleBarTile
    tempPixmap.resize(1, DECOHEIGHT + TOPMARGIN + s_titleHeight);
    KPixmapEffect::gradient(tempPixmap,
                            Handler()->getColor(TitleGradientFrom, true),
                            Handler()->getColor(TitleGradientTo, true),
                            KPixmapEffect::VerticalGradient);
    aTitleBarTile = new QPixmap(1, DECOHEIGHT + TOPMARGIN + s_titleHeight);
    painter.begin(aTitleBarTile);
    painter.drawPixmap(0, 0, tempPixmap);
    QImage t(1, (DECOHEIGHT + TOPMARGIN + s_titleHeight)/2 + 1, 32 );
    t = KImageEffect::gradient(QSize(1, t.height()),
                               Handler()->getColor(TitleGradientFrom, true).light(150),
                               Handler()->getColor(TitleGradientTo, true).light(110),
                               KImageEffect::VerticalGradient);
    painter.drawImage(0, 2, t, 0, 0, -1, tempPixmap.height()-2);
    t = KImageEffect::gradient(QSize(1, t.height()),
                               Handler()->getColor(TitleGradientTo, true),
                               Handler()->getColor(TitleGradientFrom, true),
                               KImageEffect::VerticalGradient);
    painter.drawImage(0, t.height(), t, 0, 0, -1, t.height());
    painter.end();

    // iTitleBarTile
    tempPixmap.resize(1, DECOHEIGHT + TOPMARGIN + s_titleHeight);
    KPixmapEffect::gradient(tempPixmap,
                            Handler()->getColor(TitleGradientFrom, false),
                            Handler()->getColor(TitleGradientTo, false),
                            KPixmapEffect::VerticalGradient);
    iTitleBarTile = new QPixmap(1, DECOHEIGHT + TOPMARGIN + s_titleHeight);
    painter.begin(iTitleBarTile);
    painter.drawPixmap(0, 0, tempPixmap);
    painter.end();

    QImage aTempImage = aTitleBarTile->convertToImage();
    aGradientBottom = QColor::QColor(aTempImage.pixel(0, aTempImage.height()-1));
    QImage iTempImage = iTitleBarTile->convertToImage();
    iGradientBottom = QColor::QColor(iTempImage.pixel(0, iTempImage.height()-1));

    pixmaps_created = true;
}

void PARDUSClient::delete_pixmaps()
{
    delete aTitleBarTile;
    aTitleBarTile = 0;

    delete iTitleBarTile;
    iTitleBarTile = 0;

    pixmaps_created = false;
}

void PARDUSClient::update_captionBuffer()
{
    if (!Handler()->initialized()) return;

    const uint maxCaptionLength = 300; // truncate captions longer than this!
    QString c(caption());
    if (c.length() > maxCaptionLength) {
        c.truncate(maxCaptionLength);
        c.append(" [...]");
    }

    QImage logo(Handler()->titleLogoURL());
    int logoOffset = Handler()->titleLogoOffset();
    QFontMetrics fm(s_titleFont);
    int captionWidth  = fm.width(c);

    if (Handler()->titleLogo()) {
        captionWidth += logo.width() + logoOffset;
        if (logo.height()+1 > fm.height())
            logo.scaleHeight(fm.height()-1);
    }

    QPixmap textPixmap;
    QPainter painter;
    if(Handler()->titleShadow()) {
        // prepare the shadow
        textPixmap = QPixmap(captionWidth+4, DECOHEIGHT + TOPMARGIN + s_titleHeight); // 4 px shadow space
        textPixmap.fill(QColor(0,0,0));
        textPixmap.setMask(textPixmap.createHeuristicMask(TRUE));
        painter.begin(&textPixmap);
        painter.setFont(s_titleFont);
        painter.setPen(white);
        if (Handler()->titleLogo()) {
            painter.drawText(textPixmap.rect().left(), textPixmap.rect().top()+TOPMARGIN,
                             textPixmap.rect().width()-logo.width() - logoOffset, textPixmap.rect().height()-TOPMARGIN-DECOHEIGHT,
                             AlignCenter, c);
            painter.drawImage(captionWidth - logo.width(), TOPMARGIN, logo);
        } else {
            painter.drawText(textPixmap.rect().left(), textPixmap.rect().top()+TOPMARGIN,
                             textPixmap.rect().width(), textPixmap.rect().height()-TOPMARGIN-DECOHEIGHT,
                             AlignCenter, c);
        }
        painter.end();
    }

    QImage shadow;
    ShadowEngine se;

    // active
    aCaptionBuffer->resize(captionWidth+4, DECOHEIGHT + TOPMARGIN + s_titleHeight); // 4 px shadow
    painter.begin(aCaptionBuffer);
    painter.drawTiledPixmap(aCaptionBuffer->rect(), *aTitleBarTile);
    if(Handler()->titleShadow()) {
        shadow = se.makeShadow(textPixmap, QColor(0, 0, 0));
        painter.drawImage(1, 1, shadow);
    }
    painter.setFont(s_titleFont);
    painter.setPen(Handler()->getColor(TitleFont,true));
    if (Handler()->titleLogo()) {
        painter.drawText(aCaptionBuffer->rect().left(), aCaptionBuffer->rect().top() + TOPMARGIN,
                         aCaptionBuffer->rect().width()-logo.width()-logoOffset, aCaptionBuffer->rect().height() - TOPMARGIN-DECOHEIGHT,
                         AlignCenter, c);

        painter.drawImage(captionWidth - logo.width(), TOPMARGIN, logo);
    } else {
        painter.drawText(aCaptionBuffer->rect().left(), aCaptionBuffer->rect().top() + TOPMARGIN,
                         aCaptionBuffer->rect().width(), aCaptionBuffer->rect().height() - TOPMARGIN - DECOHEIGHT,
                         AlignCenter, c);
    }
    painter.end();


    // inactive -> no shadow
    iCaptionBuffer->resize(captionWidth+4, DECOHEIGHT + TOPMARGIN + s_titleHeight);
    painter.begin(iCaptionBuffer);
    painter.drawTiledPixmap(iCaptionBuffer->rect(), *iTitleBarTile);
    painter.setFont(s_titleFont);
    painter.setPen(Handler()->getColor(TitleFont,false));
    if (Handler()->titleLogo()) {
        painter.drawText(iCaptionBuffer->rect().left(), iCaptionBuffer->rect().top() + TOPMARGIN,
                         iCaptionBuffer->rect().width() - logo.width() - logoOffset, iCaptionBuffer->rect().height() - TOPMARGIN - DECOHEIGHT,
                         AlignCenter, c);
    } else {
        painter.drawText(iCaptionBuffer->rect().left(), iCaptionBuffer->rect().top() + TOPMARGIN,
                         iCaptionBuffer->rect().width(), iCaptionBuffer->rect().height() - TOPMARGIN - DECOHEIGHT,
                         AlignCenter, c);
    }
    painter.end();

    captionBufferDirty = false;
}

void PARDUSClient::borders(int &left, int &right, int &top, int &bottom) const
{
    if ((maximizeMode() == MaximizeFull) && !options()->moveResizeMaximizedWindows()) {
        left = right = bottom = 0;
        top = s_titleHeight;

        // update layout etc.
        topSpacer_->changeSize(1, 0, QSizePolicy::Expanding, QSizePolicy::Fixed);
        decoSpacer_->changeSize(1, 0, QSizePolicy::Expanding, QSizePolicy::Fixed);
        leftSpacer_->changeSize(left, 1, QSizePolicy::Fixed, QSizePolicy::Expanding);
        leftTitleSpacer_->changeSize(left, s_titleHeight, QSizePolicy::Fixed, QSizePolicy::Fixed);
        rightSpacer_->changeSize(right, 1, QSizePolicy::Fixed, QSizePolicy::Expanding);
        rightTitleSpacer_->changeSize(right, s_titleHeight, QSizePolicy::Fixed, QSizePolicy::Fixed);
        bottomSpacer_->changeSize(1, bottom, QSizePolicy::Expanding, QSizePolicy::Fixed);
    } else {
        left = right = bottom = Handler()->borderSize();
        top = s_titleHeight + DECOHEIGHT + TOPMARGIN;

        // update layout etc.
        topSpacer_->changeSize(1, TOPMARGIN, QSizePolicy::Expanding, QSizePolicy::Fixed);
        decoSpacer_->changeSize(1, DECOHEIGHT, QSizePolicy::Expanding, QSizePolicy::Fixed);
        leftSpacer_->changeSize(left, 1, QSizePolicy::Fixed, QSizePolicy::Expanding);
        leftTitleSpacer_->changeSize(SIDETITLEMARGIN, s_titleHeight,
                                     QSizePolicy::Fixed, QSizePolicy::Fixed);
        rightSpacer_->changeSize(right, 1, QSizePolicy::Fixed, QSizePolicy::Expanding);
        rightTitleSpacer_->changeSize(SIDETITLEMARGIN, s_titleHeight,
                                      QSizePolicy::Fixed, QSizePolicy::Fixed);
        bottomSpacer_->changeSize(1, bottom, QSizePolicy::Expanding, QSizePolicy::Fixed);
    }

    // activate updated layout
    widget()->layout()->activate();
}

QSize PARDUSClient::minimumSize() const
{
    return widget()->minimumSize();
}

void PARDUSClient::show()
{
    widget()->show();
}

void PARDUSClient::resize(const QSize &s)
{
    widget()->resize(s);
}

bool PARDUSClient::eventFilter( QObject *o, QEvent *e )
{
    if (o != widget()) return false;

    switch( e->type()) {
        case QEvent::Resize:
            resizeEvent();
            return true;
        case QEvent::Paint:
            paintEvent( static_cast< QPaintEvent* >( e ));
            return true;
        case QEvent::MouseButtonDblClick:
            mouseDoubleClickEvent( static_cast< QMouseEvent* >( e ));
            return true;
        case QEvent::MouseButtonPress:
            processMousePressEvent( static_cast< QMouseEvent* >( e ));
            return true;
        default:
            break;
    }
    return false;
}

} // KWinPARDUS

// kate: space-indent on; indent-width 4; replace-tabs on;

