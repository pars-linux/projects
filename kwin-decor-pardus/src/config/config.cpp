/* PARDUS KWin window decoration
  Copyright (C) 2005 Gerd Fleischer <gerdfleischer@web.de>

  based on the window decoration "Plastik"
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

#include <kdebug.h>

#include <qbuttongroup.h>
#include <qcheckbox.h>
#include <qradiobutton.h>
#include <qslider.h>
#include <qspinbox.h>
#include <qwhatsthis.h>
#include <qimage.h>
#include <qlabel.h>
#include <qcombobox.h>

#include <kdeversion.h>
#include <kconfig.h>
#include <klocale.h>
#include <kglobal.h>
#include <kurlrequester.h>
#include <kstandarddirs.h>
#include <kurl.h>
#include <kfiledialog.h>
#include <knuminput.h>
#include <kfileitem.h>

#include "config.h"
#include "configdialog.h"

PARDUSConfig::PARDUSConfig(KConfig* config, QWidget* parent)
    : QObject(parent), m_config(0), m_dialog(0)
{
    m_parent = parent;
    // create the configuration object
    m_config = new KConfig("kwinPARDUSrc");
    KGlobal::locale()->insertCatalogue("kwin_clients");
    KGlobal::locale()->insertCatalogue("kwin_PARDUS");

    // create and show the configuration dialog
    m_dialog = new ConfigDialog(parent);

    m_dialog->show();

    // load the configuration
    load(config);


    // setup the connections
    connect(m_dialog->titleAlign, SIGNAL(clicked(int)),
            this, SIGNAL(changed()));
    connect(m_dialog->roundCorners, SIGNAL(clicked(int)),
            this, SIGNAL(changed()));
    connect(m_dialog->animateButtons, SIGNAL(toggled(bool)),
            this, SIGNAL(changed()));
    connect(m_dialog->menuClose, SIGNAL(toggled(bool)),
            this, SIGNAL(changed()));
    connect(m_dialog->titleShadow, SIGNAL(toggled(bool)),
            this, SIGNAL(changed()));
    connect(m_dialog->titleBarLogo, SIGNAL(toggled(bool)),
            this, SIGNAL(changed()));
    connect(m_dialog->titleBarLogoOffset, SIGNAL(valueChanged(int)),
            this, SIGNAL(changed()));
    connect(m_dialog->selectButton, SIGNAL(clicked()),
            this, SLOT(selectImage()));
    connect(m_dialog->buttonType, SIGNAL(activated(int)),
            this, SIGNAL(changed()));
}

PARDUSConfig::~PARDUSConfig()
{
    if (m_dialog) delete m_dialog;
    if (m_config) delete m_config;
}

void PARDUSConfig::load(KConfig*)
{
    m_config->setGroup("General");


    QString alignValue = m_config->readEntry("TitleAlignment", "AlignLeft");
    QRadioButton *alignButton = (QRadioButton*)m_dialog->titleAlign->child(alignValue.latin1());
    if (alignButton) alignButton->setChecked(true);
    QString roundValue = m_config->readEntry("RoundCorners", "NotMaximized");
    QRadioButton *roundButton = (QRadioButton*)m_dialog->roundCorners->child(roundValue.latin1());
    if (roundButton) roundButton->setChecked(true);
    bool animateButtons = m_config->readBoolEntry("AnimateButtons", true);
    m_dialog->animateButtons->setChecked(animateButtons);
    bool menuClose = m_config->readBoolEntry("CloseOnMenuDoubleClick", true);
    m_dialog->menuClose->setChecked(menuClose);
    bool titleShadow = m_config->readBoolEntry("TitleShadow", true);
    m_dialog->titleShadow->setChecked(titleShadow);
    bool titleBarLogo = m_config->readBoolEntry("TitleBarLogo", false);
    m_dialog->titleBarLogo->setChecked(titleBarLogo);
    int titleBarLogoOffset = m_config->readNumEntry("TitleBarLogoOffset", 5);
    m_dialog->titleBarLogoOffset->setValue(titleBarLogoOffset);
    QString titleBarImage = locate("data", "kwin/pics/titlebar_decor.png");
    titlebarLogoURL = m_config->readEntry("TitleBarLogoURL", titleBarImage);
    QImage tmpLogo = QImage::QImage(titlebarLogoURL);
    m_dialog->logoImage->setPixmap(QPixmap(tmpLogo.smoothScale(120, 20, QImage::ScaleMin)));
    int titleButtonType = m_config->readNumEntry("TitleBarButtonType", 4);
    m_dialog->buttonType->setCurrentItem(titleButtonType);
}

void PARDUSConfig::save(KConfig*)
{
    m_config->setGroup("General");

    QRadioButton *alignButton = (QRadioButton*)m_dialog->titleAlign->selected();
    if (alignButton) m_config->writeEntry("TitleAlignment", QString(alignButton->name()));
    QRadioButton *roundButton = (QRadioButton*)m_dialog->roundCorners->selected();
    if (roundButton) m_config->writeEntry("RoundCorners", QString(roundButton->name()));
    m_config->writeEntry("AnimateButtons", m_dialog->animateButtons->isChecked() );
    m_config->writeEntry("CloseOnMenuDoubleClick", m_dialog->menuClose->isChecked());
    m_config->writeEntry("TitleShadow", m_dialog->titleShadow->isChecked());
    m_config->writeEntry("TitleBarLogo", m_dialog->titleBarLogo->isChecked());
    m_config->writeEntry("TitleBarLogoOffset", m_dialog->titleBarLogoOffset->value());
    m_config->writeEntry("TitleBarLogoURL", QString(titlebarLogoURL));
    m_config->writeEntry("TitleBarButtonType", m_dialog->buttonType->currentItem());
    m_config->sync();
}

void PARDUSConfig::defaults()
{
    QRadioButton *alignButton = (QRadioButton*)m_dialog->titleAlign->child("AlignHCenter");
    if (alignButton) alignButton->setChecked(true);
    QRadioButton *roundButton = (QRadioButton*)m_dialog->roundCorners->child("NotMaximized");
    if (roundButton) roundButton->setChecked(true);
    m_dialog->animateButtons->setChecked(true);
    m_dialog->menuClose->setChecked(false);
    m_dialog->titleShadow->setChecked(true);
    m_dialog->titleBarLogo->setChecked(true);
    m_dialog->titleBarLogoOffset->setValue(3);
    titlebarLogoURL = locate("data", "kwin/pics/titlebar_decor.png");
    QImage tmpLogo = QImage::QImage(titlebarLogoURL);
    m_dialog->logoImage->setPixmap(QPixmap(tmpLogo.smoothScale(120, 20, QImage::ScaleMin)));
    m_dialog->buttonType->setCurrentItem(0);
}

void PARDUSConfig::selectImage()
{
    KURL logoURL = KFileDialog::getImageOpenURL(titlebarLogoURL, m_parent, i18n("Select Logo Image"));
    KFileItem tmpFileItem = KFileItem(KFileItem::Unknown, KFileItem::Unknown, logoURL);
    if (!logoURL.isEmpty() && tmpFileItem.isFile() && tmpFileItem.isReadable()) {
        titlebarLogoURL = logoURL.path();
        QImage tmpLogo = QImage::QImage(titlebarLogoURL);
        m_dialog->logoImage->setPixmap(QPixmap(tmpLogo.smoothScale(120, 20, QImage::ScaleMin)));
        emit changed();
    }
}
//////////////////////////////////////////////////////////////////////////////
// Plugin Stuff                                                             //
//////////////////////////////////////////////////////////////////////////////

extern "C"
{
#if KDE_IS_VERSION(3, 3, 2)
    KDE_EXPORT QObject* allocate_config(KConfig* config, QWidget* parent) {
#else
    QObject* allocate_config(KConfig* config, QWidget* parent) {
#endif
        return (new PARDUSConfig(config, parent));
    }
}

#include "config.moc"
