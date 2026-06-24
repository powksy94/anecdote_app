part of 'content_type.dart';

extension ContentTypeIcons on ContentType {
  IconData get icon {
    switch (this) {
      case ContentType.anecdote:            return Icons.lightbulb_rounded;
      case ContentType.chuckNorris:         return Icons.sports_martial_arts_rounded;
      case ContentType.celebrityQuote:      return Icons.psychology_rounded;
      case ContentType.history:             return Icons.auto_stories_rounded;
      case ContentType.kingOfFrance:        return Icons.castle_rounded;
      case ContentType.americanPresident:   return Icons.account_balance_rounded;
      case ContentType.historyHub:          return Icons.history_edu_rounded;
      case ContentType.animals:             return Icons.pets_rounded;
      case ContentType.country:             return Icons.public_rounded;
      case ContentType.frenchDepartment:    return Icons.location_city_rounded;
      case ContentType.pacificIsland:       return Icons.waves_rounded;
      case ContentType.world:               return Icons.travel_explore_rounded;
      case ContentType.exoplanet:           return Icons.rocket_launch_rounded;
      case ContentType.star:                return Icons.star_rounded;
      case ContentType.solarSystemMoon:     return Icons.brightness_2_rounded;
      case ContentType.space:               return Icons.nightlight_round;
      case ContentType.cinemaHub:           return Icons.movie_rounded;
      case ContentType.classicCinema:       return Icons.theaters_rounded;
      case ContentType.cinema80s90s:        return Icons.videocam_rounded;
      case ContentType.modernCinema:        return Icons.local_movies_rounded;
      case ContentType.celebrityHub:        return Icons.stars_rounded;
      case ContentType.scienceHub:          return Icons.science_rounded;
      case ContentType.dinosaur:            return Icons.rowing_rounded;
      case ContentType.spaceMission:        return Icons.rocket_rounded;
      case ContentType.battle:              return Icons.shield_rounded;
      case ContentType.artHub:              return Icons.palette_rounded;
      case ContentType.painting:            return Icons.brush_rounded;
      case ContentType.sculpture:           return Icons.view_in_ar_rounded;
      case ContentType.architecture:        return Icons.domain_rounded;
      case ContentType.famousArtist:        return Icons.color_lens_rounded;
      case ContentType.photographer:        return Icons.photo_camera_rounded;
      case ContentType.classicalComposer:   return Icons.music_note_rounded;
      case ContentType.nobelPrize:          return Icons.emoji_events_rounded;
      case ContentType.frenchCommune:       return Icons.location_city_rounded;
      case ContentType.americanState:       return Icons.flag_rounded;
      case ContentType.scienceLivingHub:    return Icons.eco_rounded;
      case ContentType.scienceNonLivingHub: return Icons.biotech_rounded;
      case ContentType.artWorksHub:         return Icons.brush_rounded;
      case ContentType.artArtistsHub:       return Icons.groups_rounded;
      case ContentType.chemicalElement:     return Icons.science_rounded;
      case ContentType.volcano:             return Icons.terrain_rounded;
      case ContentType.insect:              return Icons.bug_report_rounded;
      case ContentType.bird:                return Icons.flight_takeoff_rounded;
      case ContentType.mineral:             return Icons.diamond_rounded;
      case ContentType.cloud:               return Icons.cloud_rounded;
      case ContentType.humanBone:           return Icons.medical_services_rounded;
      case ContentType.territoriesHub:      return Icons.map_rounded;
      case ContentType.naturalWondersHub:   return Icons.landscape_rounded;
      case ContentType.humorHub:            return Icons.sentiment_very_satisfied_rounded;
      case ContentType.personalityHub:      return Icons.people_alt_rounded;
      case ContentType.lgbtqiaPersonality:  return Icons.diversity_3_rounded;
      case ContentType.pioneerWoman:        return Icons.woman_rounded;
      case ContentType.legendaryAthlete:    return Icons.emoji_events_rounded;
      case ContentType.desert:              return Icons.wb_sunny_rounded;
      case ContentType.river:               return Icons.water_rounded;
      case ContentType.sea:                 return Icons.sailing_rounded;
    }
  }
}
