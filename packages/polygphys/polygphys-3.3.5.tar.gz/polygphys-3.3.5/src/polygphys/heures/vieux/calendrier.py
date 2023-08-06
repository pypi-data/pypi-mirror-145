#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Lecture et écriture de calendriers pour iCal sur MacOS.

Created on Tue Oct  5 10:33:10 2021

@author: ejetzer
"""

import configparser
import datetime

from pathlib import Path

import ics  # https://pypi.org/project/ics/
import plistop  # https://pypi.org/project/plistop/


def trouver_x(titre: str,
              racine: Path,
              suffixe: str) -> tuple[Path, plistop.parse]:
    """
    Trouver les informations sur un calendrier sur MacOS.

    Parameters
    ----------
    titre : str
        DESCRIPTION.
    racine : Path
        DESCRIPTION.
    suffixe : str
        DESCRIPTION.

    Returns
    -------
    chemin : TYPE
        DESCRIPTION.
    infos : TYPE
        DESCRIPTION.

    """
    for chemin in racine.iterdir():
        if chemin.name.endswith(suffixe):
            infos = chemin / 'Info.plist'
            with infos.open() as f:
                infos = plistop.parse(f)

            if infos['Title'] == titre:
                return chemin, infos


class Calendrier:
    """Objet de calendrier MacOS."""

    def __init__(self, compte: str, titre: str, racine: Path):
        """
        Objet de calendrier.

        Parameters
        ----------
        compte : str
            DESCRIPTION.
        titre : str
            DESCRIPTION.
        racine : Path
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.compte = trouver_x(compte, racine, 'caldav')
        self.calendrier = trouver_x(titre, self.compte[0], 'calendar')

    def événements(self,
                   calendrier: trouver_x = None,
                   filtre: callable = lambda x: True) -> iter:
        """
        Liste des événements du calendrier.

        Parameters
        ----------
        calendrier : trouver_x, optional
            DESCRIPTION. The default is None.
        filtre : callable, optional
            DESCRIPTION. The default is lambda x: True.

        Yields
        ------
        iter
            DESCRIPTION.

        """
        if calendrier is None:
            calendrier = self.calendrier

        for chemin in (calendrier[0] / 'Events').iterdir():
            with chemin.open() as f:
                événements = ics.Calendar(f.read())

            yield from filter(filtre, événements)

    def créer_événement(self,
                        titre: str,
                        début: datetime.datetime,
                        durée: datetime.timedelta,
                        desc: str = ''):
        """
        Créer un nouvel événement.

        Parameters
        ----------
        titre : str
            DESCRIPTION.
        début : datetime.datetime
            DESCRIPTION.
        durée : datetime.timedelta
            DESCRIPTION.
        desc : str, optional
            DESCRIPTION. The default is ''.

        Returns
        -------
        calendrier_temporaire : TYPE
            DESCRIPTION.

        """
        calendrier_temporaire = ics.Calendar()
        événement = ics.Event(name=titre,
                              begin=début,
                              duration=durée,
                              uid=hex(hash(début)),
                              created=datetime.datetime.now())
        calendrier_temporaire.events.add(événement)

        return calendrier_temporaire


if __name__ == '__main__':
    cfg = configparser.ConfigParser()
    cfg.read('Configuration.txt')
    cal_cfg = cfg['Calendrier']

    répertoire = Path(cal_cfg['ics']).expanduser()
    cal = Calendrier(cal_cfg['compte'], cal_cfg['cal'], répertoire)

    année = datetime.date.today().year
    HAE_début = datetime.date(année, 3, 8)
    HAE_fin = datetime.date(année, 11, 1)
    if HAE_début <= datetime.date.today() < HAE_fin:
        tz = datetime.timezone(datetime.timedelta(hours=-4), name='HAE')
    else:
        tz = datetime.timezone(datetime.timedelta(hours=-5), name='HSE')

    print(cal.créer_événement('Test', datetime.datetime.now(
        tz), datetime.timedelta(hours=1)))
