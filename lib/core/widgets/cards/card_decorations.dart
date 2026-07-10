import 'package:flutter/material.dart';
import '../../models/content_type.dart';

part './card_decoration_builders.dart';
part './card_decoration_primitives.dart';

Widget buildCardDecoration(ContentType type) {
  switch (type) {
    // --- Modèle Stars : cercles + icônes étoiles ---
    case ContentType.anecdote:
      return _anecdoteDecoration();
    case ContentType.space:
    case ContentType.exoplanet:
      return _stars(count: 3);

    // --- Modèle Rects : rectangles pivotés + icône ---
    case ContentType.chuckNorris:
      return _rects(Icons.bolt);
    case ContentType.history:
      return _historyDecoration();

    // --- Modèle Bubbles : bulles + icône (quote) ---
    case ContentType.celebrityQuote:
      return _bubbles(Icons.format_quote);

    // --- Modèle DoubleIcon : 2 cercles + 2 icônes ---
    case ContentType.animals:
      return _doubleIcon(Icons.eco, Icons.eco);
    case ContentType.country:
      return _doubleIcon(Icons.public, Icons.location_on);
    case ContentType.world:
      return _doubleIcon(Icons.travel_explore, Icons.pin_drop);

    // --- Modèle SingleIcon : 2 cercles + 1 icône ---
    case ContentType.frenchDepartment:
      return _singleIcon(Icons.location_city);
    case ContentType.pacificIsland:
      return _singleIcon(Icons.waves);
    case ContentType.historyHub:
      return _singleIcon(Icons.history_edu);
    case ContentType.celebrityHub:
      return _bubbles(Icons.stars);
    case ContentType.scienceHub:
      return _doubleIcon(Icons.science, Icons.eco);
    case ContentType.spaceMission:
      return _singleIcon(Icons.rocket, iconSize: 16);
    case ContentType.battle:
      return _doubleIcon(Icons.shield, Icons.local_fire_department);
    case ContentType.dinosaur:
      return _singleIcon(Icons.rowing_rounded, iconSize: 16);
    case ContentType.cinemaHub:
      return _doubleIcon(Icons.movie, Icons.star);
    case ContentType.classicCinema:
      return _rects(Icons.theaters);
    case ContentType.cinema80s90s:
      return _singleIcon(Icons.videocam, iconSize: 16);
    case ContentType.modernCinema:
      return _singleIcon(Icons.local_movies);
    case ContentType.kingOfFrance:
      return _singleIcon(Icons.castle);
    case ContentType.americanPresident:
      return _singleIcon(Icons.account_balance);
    case ContentType.star:
      return _singleIcon(Icons.star, iconSize: 16);
    case ContentType.solarSystemMoon:
      return _singleIcon(Icons.brightness_2);
    case ContentType.artHub:
      return _doubleIcon(Icons.palette, Icons.brush);
    case ContentType.painting:
      return _singleIcon(Icons.brush, iconSize: 16);
    case ContentType.frenchCommune:
      return _doubleIcon(Icons.location_city, Icons.flag);
    case ContentType.americanState:
      return _doubleIcon(Icons.flag, Icons.location_on);
    case ContentType.sculpture:
      return _singleIcon(Icons.view_in_ar_rounded, iconSize: 16);
    case ContentType.architecture:
      return _singleIcon(Icons.domain_rounded, iconSize: 16);
    case ContentType.famousArtist:
      return _doubleIcon(Icons.color_lens_rounded, Icons.brush);
    case ContentType.photographer:
      return _singleIcon(Icons.photo_camera_rounded, iconSize: 16);
    case ContentType.classicalComposer:
      return _singleIcon(Icons.music_note_rounded, iconSize: 16);
    case ContentType.nobelPrize:
      return _doubleIcon(Icons.emoji_events_rounded, Icons.star);
    case ContentType.scienceLivingHub:
      return _doubleIcon(Icons.eco, Icons.pets);
    case ContentType.scienceNonLivingHub:
      return _doubleIcon(Icons.biotech, Icons.science);
    case ContentType.artWorksHub:
      return _doubleIcon(Icons.brush, Icons.architecture);
    case ContentType.artArtistsHub:
      return _doubleIcon(Icons.groups, Icons.color_lens);
    case ContentType.chemicalElement:
      return _doubleIcon(Icons.science, Icons.blur_circular);
    case ContentType.volcano:
      return _doubleIcon(Icons.terrain, Icons.local_fire_department);
    case ContentType.insect:
      return _doubleIcon(Icons.bug_report_rounded, Icons.eco);
    case ContentType.bird:
      return _doubleIcon(Icons.flight_takeoff_rounded, Icons.air_rounded);
    case ContentType.mineral:
      return _doubleIcon(Icons.diamond_rounded, Icons.blur_circular_rounded);
    case ContentType.cloud:
      return _doubleIcon(Icons.cloud_rounded, Icons.air_rounded);
    case ContentType.humanBone:
      return _doubleIcon(Icons.medical_services_rounded, Icons.straighten_rounded);
    case ContentType.territoriesHub:
      return _doubleIcon(Icons.map_rounded, Icons.pin_drop);
    case ContentType.naturalWondersHub:
      return _doubleIcon(Icons.landscape_rounded, Icons.local_fire_department);
    case ContentType.humorHub:
      return _bubbles(Icons.sentiment_very_satisfied_rounded);
    case ContentType.personalityHub:
      return _doubleIcon(Icons.people_alt_rounded, Icons.psychology_rounded);
    case ContentType.lgbtqiaPersonality:
      return _bubbles(Icons.diversity_3_rounded);
    case ContentType.pioneerWoman:
      return _doubleIcon(Icons.woman_rounded, Icons.school_rounded);
    case ContentType.legendaryAthlete:
      return _doubleIcon(Icons.emoji_events_rounded, Icons.sports_rounded);
    case ContentType.desert:
      return _doubleIcon(Icons.wb_sunny_rounded, Icons.terrain_rounded);
    case ContentType.river:
      return _doubleIcon(Icons.water_rounded, Icons.landscape_rounded);
    case ContentType.sea:
      return _doubleIcon(Icons.sailing_rounded, Icons.waves_rounded);
    case ContentType.gamingHub:
      return _doubleIcon(Icons.sports_esports_rounded, Icons.videogame_asset_rounded);
    case ContentType.gamesHub:
      return _doubleIcon(Icons.videogame_asset_rounded, Icons.history_rounded);
    case ContentType.gamersHub:
      return _doubleIcon(Icons.groups_rounded, Icons.military_tech_rounded);
    case ContentType.gamingAnecdote:
      return _singleIcon(Icons.tips_and_updates_rounded, iconSize: 16);
    case ContentType.gamingNomination:
      return _doubleIcon(Icons.emoji_events_rounded, Icons.star_rounded);
    case ContentType.classicGame:
      return _singleIcon(Icons.history_rounded, iconSize: 16);
    case ContentType.worstGame:
      return _singleIcon(Icons.thumb_down_rounded, iconSize: 16);
    case ContentType.bannedGame:
      return _singleIcon(Icons.block_rounded, iconSize: 16);
    case ContentType.gamingLegend:
      return _doubleIcon(Icons.military_tech_rounded, Icons.sports_esports_rounded);
  }
}
