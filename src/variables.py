import os
from api import *

CONFIG_PATH = os.getenv("EDCM_CONFIG_PATH", "/config/config.ini")
EDCM_DEBUG = os.getenv("EDCM_DEBUG", False)
DEBUG = True if EDCM_DEBUG != False else False
EMBY_ADDRESS = os.getenv("EMBY_ADDRESS")
EMBY_PORT = int(os.getenv("EMBY_PORT", 8096))
EMBY_TOKEN = os.getenv("EMBY_TOKEN")
SCAN_INTERVAL = int(os.getenv("EDCM_SCAN_INTERVAL", 600))  # seconds
USE_SSL = os.getenv("EDCM_USE_SSL", False)
HTTPS = "https" if USE_SSL != False else "http"

emby_api = api(base_url=f"{HTTPS}://{EMBY_ADDRESS}:{EMBY_PORT}", api_token=EMBY_TOKEN)

items_param_rules = [
    "AdjacentTo",
    "AiredDuringSeason",
    "Albums",
    "Artists",
    "ArtistType",
    "AudioCodecs",
    "Containers",
    "ExcludeLocationTypes",
    "HasImdbId",
    "HasOfficialRating",
    "HasOverview",
    "HasParentalRating",
    "HasSpecialFeature",
    "HasSubtitles",
    "HasThemeSong",
    "HasThemeVideo",
    "HasTmdbId",
    "HasTrailer",
    "HasTvdbId",
    "Is3D",
    "IsFavorite",
    "IsHD",
    "IsLocked",
    "IsMissing",
    "IsPlaceHolder",
    "IsPlayed",
    "IsUnaired",
    "LocationTypes",
    "MaxOfficialRating",
    "MaxPlayers",
    "MaxPremiereDate",
    "MinCommunityRating",
    "MinCriticRating",
    "MinDateLastSaved",
    "MinDateLastSavedForUser",
    "MinIndexNumber",
    "MinOfficialRating",
    "MinPlayers",
    "MinPremiereDate",
    "OfficialRatings",
    "ParentIndexNumber",
    "Path",
    "SeriesStatus",
    "SubtitleCodecs",
    "Tags",
    "VideoCodecs",
    "VideoTypes",
    "Years",
]
