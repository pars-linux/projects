/* Plastik KWin window decoration
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

#ifndef CONFIG_H
#define CONFIG_H

#include <qobject.h>

class QButtonGroup;
class QGroupBox;
class KConfig;
class ConfigDialog;

class PARDUSConfig : public QObject
{
    Q_OBJECT
public:
    PARDUSConfig(KConfig* config, QWidget* parent);
    ~PARDUSConfig();

signals:
    void changed();

public slots:
    void load(KConfig *config);
    void save(KConfig *config);
    void defaults();

private:
    QWidget *m_parent;
    KConfig *m_config;
    ConfigDialog *m_dialog;
    QString titlebarLogoURL;

private slots:
    void selectImage();
};

#endif

