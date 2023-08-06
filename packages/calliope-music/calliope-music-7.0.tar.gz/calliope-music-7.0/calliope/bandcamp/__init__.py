# Calliope
# Copyright (C) 2021 Sam Thursfield <sam@afuera.me.uk>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


"""Access data from `Bandcamp <https://bandcamp.com/>`_.

This module wraps a local fork of the
`bandcamp_api <https://github.com/Virusmater/bandcamp_api>`_ library.
Additionally, some information is scraped from the Bandcamp website using
BeautifulSoup4.

Authentication
--------------

All the APIs used by this module can be accessed without authentication.

Caching
-------

FIXME: some requests are cached now.

HTTP requests are not cached. At time of writing, ``api.bandcamp.com`` requests
send the HTTP header ``Cache-Control: no-cache, no-store``.

Web pages that are scraped for data will get cached, see function documentation
for more details.
"""

from bs4 import BeautifulSoup
import requests

from datetime import timedelta
from functools import partial
import json
import logging
import pathlib
import re
import sys
import urllib

import calliope.cache
import calliope.config
import calliope.playlist
import calliope.subprojects.bandcamp_api as bandcamp_api

log = logging.getLogger(__name__)


class ScrapeError(RuntimeError):
    pass


class BandcampContext():
    def __init__(self, config: calliope.config.Configuration, user: str=None):
        """Context for accessing Bandcamp API.

        Args:
            user: Default user for requests

        """
        self.config = config

        if not user:
            user = self.config.get('bandcamp', 'user')

        self.user = user
        log.debug("Bandcamp user: {}".format(user))

        self.api = bandcamp_api.bandcamp.Bandcamp(self.user)

        self.cache = calliope.cache.open(namespace='bandcamp')

    def get_fan_id(self):
        return self.api.get_fan_id()


def _get_album_and_band_name_from_paragraph(paragraph_tag,
                                            band_or_label_name):
    try:
        album_name = list(paragraph_tag.children)[0].text.strip()
        band_name_tag = paragraph_tag.find('span', class_='artist-override')
        if band_name_tag:
            band_name = band_name_tag.text.strip()
        else:
            band_name = band_or_label_name
        return (album_name, band_name)
    except (KeyError, ValueError) as e:
        raise ScrapeError(
            f"Could not get album and band name from <p> tag {paragraph_tag}: {e}"
        ) from e


_ART_ID_FROM_IMAGE_URL = re.compile(r'https://f4.bcbits.com/img/a([\d]+)_2.jpg')
def _get_art_id_from_img_tag(img_tag):
    try:
        art_url = img_tag.attrs.get('src')
        match = _ART_ID_FROM_IMAGE_URL.match(art_url)
        if match:
            return int(match.group(1))
        else:
            log.warning("No match for %s in %s", _ART_ID_FROM_IMAGE_URL, art_url)
            return None
    except (KeyError, ValueError) as e:
        raise ScrapeError(
            f"Could not get art ID from img tag {img_tag}: {e}"
        ) from e


def _read_html(url):
    if url.startswith('file://'):
        path = urllib.parse.urlparse(url).path
        return pathlib.Path(path).read_text()
    return requests.get(url).data.text


def _band_url_from_album_url(album_url):
    s = urllib.parse.urlsplit(album_url)
    return urllib.parse.urlunsplit(s[0:2] + ('','',''))

# We could return bandcamp_api.bandcamp.Band, bandcamp_api.bandcamp.Album here,
# but they are not JSON serializable so they wouldn't store in the cache.
def _scrape_albums_from_band_page(band_url):
    html = _read_html(band_url)
    soup = BeautifulSoup(html, features='lxml')

    meta_page_type_tag = soup.find('meta', property='og:type')
    if not meta_page_type_tag:
        log.warning("No og:type property")
    elif meta_page_type_tag.attrs['content'] != "band":
        raise ScrapeError(f"Expected og:type=band, got: {meta_page_type_tag}")

    meta_title_tag = soup.find('meta', property='og:title')
    if meta_title_tag:
        band_or_label_name = meta_title_tag.attrs['content']
    else:
        raise ScrapeError("No og:title tag, could not get band/label name")

    grid_items = soup.find_all(class_='music-grid-item')
    result = []
    for item in grid_items:
        band_id = item.attrs.get('data-band-id')
        album_id = item.attrs.get('data-item-id')
        if album_id.startswith('album-'):
            album_id = album_id[6:]

        album_name, band_name = _get_album_and_band_name_from_paragraph(
            item.find('p', class_='title'), band_or_label_name
        )

        album_link_tag = item.find('a')
        if album_link_tag:
            album_url = album_link_tag.attrs['href']
            if not album_url.startswith('http'):
                album_url = urllib.parse.urljoin(band_url, album_url)
        else:
            raise ScrapeError("No album link found")

        art_id = _get_art_id_from_img_tag(item.find('img'))

        data = {
            'band_name': band_name,
            'band_id': band_id,
            'band_url': _band_url_from_album_url(album_url),
            'album_id': album_id,
            'album_name': album_name,
            'album_url': album_url,
            'art_id': art_id,
        }
        result.append(data)
    return result


def _scrape_album_id_from_album_page(album_url):
    html = _read_html(album_url)
    soup = BeautifulSoup(html, features='lxml')

    meta_page_type_tag = soup.find('meta', property='og:type')
    if not meta_page_type_tag:
        log.warning("No og:type property")
    elif meta_page_type_tag.attrs['content'] != "album":
        raise ScrapeError(f"Expected og:type=album, got: {meta_page_type_tag}")

    meta_bc_page_properties_tag = soup.find(
        'meta',
        attrs={'name': 'bc-page-properties'},
    )
    if not meta_bc_page_properties_tag:
        raise ScrapeError("Missing bc-page-properties, unable to get album ID")

    try:
        content = json.loads(meta_bc_page_properties_tag.attrs['content'])
    except json.decoder.JSONDecodeError as e:
        raise ScrapeError(f"Error decoding bc-page-properties: {e}. Value: {content}") from e

    try:
        return int(content['item_id'])
    except (KeyError, ValueError) as e:
        raise ScrapeError(f"Error getting item_id from bc-page-properties: {e}. Value: {content}") from e


def export_band(context: BandcampContext,
                band_url,
                expand_albums=False,
                cache_expiry: timedelta=None) -> calliope.playlist.Playlist:
    """Export all albums for a Bandcamp artist or label.

    This uses web scraping as I am not aware of an API that provides the info.
    It may provide incomplete data and may stop working based on changes to the
    Bandcamp site.

    The remote page is cached, and by default is only refreshed if older than 1
    week.  Use ``cache_expiry`` to set a different expiry interval.

    """

    cache_expiry = cache_expiry or timedelta(days=7)
    albums = context.cache.wrap(
        band_url,
        partial(
            _scrape_albums_from_band_page, band_url=band_url,
        ),
        expiry=cache_expiry,
    )
    for album in albums:
        album_info = {
            'album': album['album_name'],
            'bandcamp.album_id': album['album_id'],
            'bandcamp.album_url': album['album_url'],
            'bandcamp.artist_url': album['band_url'],
            'creator': album['band_name'],
            'location': album['album_url'],
        }

        if expand_albums:
            try:
                yield from export_album(context, album_id=album['album_id'])
            except bandcamp_api.bandcamp.EmbeddedPlayerUnavailable as e:
                album_info['bandcamp.errors'] = str(e)
                yield album_info
        else:
            yield album_info


def export_album(context: BandcampContext,
                 album_url=None,
                 album_id=None,
                 cache_expiry=None) -> calliope.playlist.Playlist:
    """Export all tracks in an album

    The remote page is cached, and by default is never refreshed.
    Use ``cache_expiry`` to set an expiry interval if needed.

    """
    assert album_url or album_id

    if not album_id:
        pathlib.Path(album_url)
        album_id = context.cache.wrap(
            album_url,
            partial(
                _scrape_album_id_from_album_page, album_url=album_url,
            ),
            expiry=cache_expiry,
        )

    log.debug("Using album ID: %s", album_id)
    album, track_list = context.api.get_album(album_id)

    for track in track_list:
        track_info = {
            'title': track.track_name,
            'trackNum': track.number,
            'album': album.album_name,
            'bandcamp.album_id': album.album_id,
            'bandcamp.album_url': album.album_url,
            'location': album.album_url,
            'creator': album.band_name,
            'bandcamp.artist_url': album.band_url
        }
        if track.duration is not None:
            track_info['duration'] = int(track.duration * 1000)
        yield track_info


def collection(bandcamp: BandcampContext,
               count=1000) -> calliope.playlist.Playlist:
    """Export all albums in Bandcamp collection."""
    bands = bandcamp.api.get_collection(bandcamp.get_fan_id(), count=count)

    for band in bands:
        for album in bands[band]:
            yield {
                'album': album.album_name,
                'bandcamp.album_id': album.album_id,
                'location': album.album_url,
                'creator': band.band_name,
                'bandcamp.artist_id': band.band_id
            }


def wishlist(bandcamp: BandcampContext,
             count=1000) -> calliope.playlist.Playlist:
    """Export all albums in Bandcamp wishlist."""
    bands = bandcamp.api.get_wishlist(bandcamp.get_fan_id(), count=count)

    for band in bands:
        for album in bands[band]:
            yield {
                'album': album.album_name,
                'bandcamp.album_id': album.album_id,
                'location': album.album_url,
                'creator': band.band_name,
                'bandcamp.artist_id': band.band_id
            }
