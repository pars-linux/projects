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

#ifndef PARDUS_H
#define PARDUS_H

#define A_FG_DARK 0
#define A_FG_LIGHT 1
#define I_FG_DARK 2
#define I_FG_LIGHT 3
#define SHADOW 4

#include <qfont.h>

#include <kdecoration.h>
#include <kdecorationfactory.h>

namespace KWinPARDUS {

enum ButtonIcon {
    CloseIcon = 0,
    MaxIcon,
    MaxRestoreIcon,
    MinIcon,
    HelpIcon,
    OnAllDesktopsIcon,
    NotOnAllDesktopsIcon,
    KeepAboveIcon,
    NoKeepAboveIcon,
    KeepBelowIcon,
    NoKeepBelowIcon,
    ShadeIcon,
    UnShadeIcon,
    NumButtonIcons
};

enum ButtonType {
    HelpButton=0,
    MaxButton,
    MinButton,
    CloseButton,
    MenuButton,
    OnAllDesktopsButton,
    AboveButton,
    BelowButton,
    ShadeButton,
    NumButtons
};

enum ColorType {
    WindowContour=0,
    TitleGradientFrom,
    TitleGradientTo,
    Border,
    TitleFont,
    BtnBg
};

class PARDUSHandler: public QObject, public KDecorationFactory
{
    Q_OBJECT
public:
    PARDUSHandler();
    ~PARDUSHandler();
    virtual bool reset( unsigned long changed );

    virtual KDecoration* createDecoration( KDecorationBridge* );

#if KDE_VERSION > KDE_MAKE_VERSION(3, 3, 90)
    virtual bool supports( Ability ability );
#endif

    const QPixmap &buttonPixmap(ButtonIcon type, int size, int state);

    bool initialized() { return m_initialized; }

    int  titleHeight() { return m_titleHeight; }
    int  titleHeightTool() { return m_titleHeightTool; }
    QFont titleFont() { return m_titleFont; }
    QFont titleFontTool() { return m_titleFontTool; }
    bool titleLogo() { return m_titleLogo; }
    int titleLogoOffset() { return m_titleLogoOffset; }
    QString titleLogoURL() { return m_titleLogoURL; }
    bool titleShadow() { return m_titleShadow; }
    int  borderSize() { return m_borderSize; }
    int buttonType() { return m_buttonType; }
    float iconSize() { return m_iconSize; }
    bool useTitleProps() { return m_useTitleProps; }
    bool animateButtons() { return m_animateButtons; }
    bool menuClose() { return m_menuClose; }
    Qt::AlignmentFlags titleAlign() { return m_titleAlign; }
    int roundCorners() { return m_roundCorners; }
    bool reverseLayout() { return m_reverse; }
    QColor getColor(KWinPARDUS::ColorType type, const bool active = true);
    QValueList< PARDUSHandler::BorderSize >  borderSizes() const;
private:
    void readConfig();

    bool m_titleLogo;
    bool m_titleShadow;
    bool m_shrinkBorders;
    int  m_buttonType;
    float m_iconSize;
    bool m_animateButtons;
    bool m_menuClose;
    bool m_reverse;
    int  m_borderSize;
    int  m_titleHeight;
    int  m_titleHeightTool;
    QFont m_titleFont;
    QFont m_titleFontTool;
    Qt::AlignmentFlags m_titleAlign;
    int m_roundCorners;
    int m_titleLogoOffset;
    QString m_titleLogoURL;
    bool m_useTitleProps;
    bool m_initialized;

    QPixmap *m_pixmaps[5][NumButtonIcons];
};

PARDUSHandler* Handler();

} // KWinPARDUS

#endif
