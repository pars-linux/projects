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

#include <kdebug.h>

#include <kconfig.h>
#include <klocale.h>
#include <kglobal.h>
#include <kstandarddirs.h>

#include "misc.h"
#include "PARDUS.h"
#include "PARDUS.moc"
#include "PARDUSclient.h"

namespace KWinPARDUS
{

// static bool pixmaps_created = false;

bool PARDUSHandler::m_initialized    = false;
int  PARDUSHandler::m_buttonType     = 0;
bool PARDUSHandler::m_animateButtons = true;
bool PARDUSHandler::m_titleLogo      = true;
bool PARDUSHandler::m_titleShadow    = true;
bool PARDUSHandler::m_shrinkBorders  = true;
bool PARDUSHandler::m_menuClose      = false;
bool PARDUSHandler::m_reverse        = false;
int  PARDUSHandler::m_borderSize     = 4;
int  PARDUSHandler::m_titleHeight    = 19;
int  PARDUSHandler::m_titleHeightTool= 12;
QFont PARDUSHandler::m_titleFont = QFont();
QFont PARDUSHandler::m_titleFontTool = QFont();
Qt::AlignmentFlags PARDUSHandler::m_titleAlign = Qt::AlignLeft;
int PARDUSHandler::m_roundCorners    = 2;
int PARDUSHandler::m_titleLogoOffset = 3;
QString PARDUSHandler::m_titleLogoURL = locate("data", "kwin/pics/titlebar_decor.png");

PARDUSHandler::PARDUSHandler()
{
    KGlobal::locale()->insertCatalogue("kwin_clients");
    KGlobal::locale()->insertCatalogue("kwin_PARDUS");
    reset(0);
}

PARDUSHandler::~PARDUSHandler()
{
    m_initialized = false;
}

bool PARDUSHandler::reset(unsigned long changed)
{
    // we assume the active font to be the same as the inactive font since the control
    // center doesn't offer different settings anyways.
    m_titleFont = KDecoration::options()->font(true, false); // not small
    m_titleFontTool = KDecoration::options()->font(true, true); // small

    switch(KDecoration::options()->preferredBorderSize( this )) {
        case BorderTiny:
            m_borderSize = 3;
            break;
        case BorderLarge:
            m_borderSize = 8;
            break;
        case BorderVeryLarge:
            m_borderSize = 12;
            break;
        case BorderHuge:
            m_borderSize = 18;
            break;
        case BorderVeryHuge:
            m_borderSize = 27;
            break;
        case BorderOversized:
            m_borderSize = 40;
            break;
        case BorderNormal:
        default:
            m_borderSize = 4;
    }

    // check if we are in reverse layout mode
    m_reverse = QApplication::reverseLayout();

    // read in the configuration
    readConfig();

    m_initialized = true;

    // Do we need to "hit the wooden hammer" ?
    bool needHardReset = true;
    // TODO: besides the Color and Font settings I can maybe handle more changes
    //       without a hard reset. I will do this later...
    if (changed & SettingColors || changed & SettingFont)
    {
        needHardReset = false;
    }

    if (needHardReset) {
        return true;
    } else {
        resetDecorations(changed);
        return false;
    }
}

KDecoration* PARDUSHandler::createDecoration( KDecorationBridge* bridge )
{
        return new PARDUSClient( bridge, this );
}

#if KDE_IS_VERSION(3, 4, 0)
bool PARDUSHandler::supports( Ability ability )
{
    switch( ability )
    {
        case AbilityAnnounceButtons:
        case AbilityButtonMenu:
        case AbilityButtonOnAllDesktops:
        case AbilityButtonSpacer:
        case AbilityButtonHelp:
        case AbilityButtonMinimize:
        case AbilityButtonMaximize:
        case AbilityButtonClose:
        case AbilityButtonAboveOthers:
        case AbilityButtonBelowOthers:
        case AbilityButtonShade:
            return true;
        default:
            return false;
    };
}
#endif

void PARDUSHandler::readConfig()
{
    // create a config object
    KConfig config("kwinPARDUSrc");
    config.setGroup("General");

    // grab settings
    m_titleLogo      = config.readBoolEntry("TitleBarLogo", true);
    m_titleLogoOffset = config.readNumEntry("TitleBarLogoOffset", 3);
    m_titleLogoURL   = config.readEntry("TitleBarLogoURL", locate("data", "kwin/pics/titlebar_decor.png"));
    m_titleShadow    = config.readBoolEntry("TitleShadow", true);

    QFontMetrics fm(m_titleFont);  // active font = inactive font
    int titleHeightMin = config.readNumEntry("MinTitleHeight", 16);
    // The title should strech with bigger font sizes!
    m_titleHeight = QMAX(titleHeightMin, fm.height() + 4); // 4 px for the shadow etc.

    fm = QFontMetrics(m_titleFontTool);  // active font = inactive font
    int titleHeightToolMin = config.readNumEntry("MinTitleHeightTool", 13);
    // The title should strech with bigger font sizes!
    m_titleHeightTool = QMAX(titleHeightToolMin, fm.height() ); // don't care about the shadow etc.

    QString alignValue = config.readEntry("TitleAlignment", "AlignLeft");
    if (alignValue == "AlignLeft")         m_titleAlign = Qt::AlignLeft;
    else if (alignValue == "AlignHCenter") m_titleAlign = Qt::AlignHCenter;
    else if (alignValue == "AlignRight")   m_titleAlign = Qt::AlignRight;

    QString roundValue = config.readEntry("RoundCorners", "NotMaximized");
    if (roundValue == "RoundAlways")       m_roundCorners = 1;
    else if (roundValue == "NotMaximized") m_roundCorners = 2;
    else if (roundValue == "RoundNever")   m_roundCorners = 3;

    m_buttonType = config.readNumEntry("TitleBarButtonType", 4);
    m_animateButtons = config.readBoolEntry("AnimateButtons", true);
    m_menuClose = config.readBoolEntry("CloseOnMenuDoubleClick", true);
}

QColor PARDUSHandler::getColor(KWinPARDUS::ColorType type, const bool active)
{
    switch (type) {
        case TitleGradientFrom:
            return KDecoration::options()->color(ColorTitleBar, active);
            break;
        case TitleGradientTo:
            return KDecoration::options()->color(ColorTitleBlend, active);
            break;
        case WindowContour:
        case Border:
            return KDecoration::options()->color(ColorFrame, active);
            break;
        case TitleFont:
            return KDecoration::options()->color(ColorFont, active);
            break;
        case BtnBg:
            return KDecoration::options()->color(ColorButtonBg, active);
            break;
        default:
            return Qt::black;
    }
}

QValueList< PARDUSHandler::BorderSize >
PARDUSHandler::borderSizes() const
{
    // the list must be sorted
    return QValueList< BorderSize >() << BorderTiny << BorderNormal <<
	BorderLarge << BorderVeryLarge <<  BorderHuge <<
	BorderVeryHuge << BorderOversized;
}

} // KWinPARDUS

//////////////////////////////////////////////////////////////////////////////
// Plugin Stuff                                                             //
//////////////////////////////////////////////////////////////////////////////

static KWinPARDUS::PARDUSHandler *handler = 0;

extern "C"
{
#if KDE_IS_VERSION(3, 3, 2)
    KDE_EXPORT KDecorationFactory *create_factory()
#else
    KDecorationFactory *create_factory()
#endif
    {
        handler = new KWinPARDUS::PARDUSHandler();
        return handler;
    }
}
