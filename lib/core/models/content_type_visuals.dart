part of 'content_type.dart';

extension ContentTypeVisuals on ContentType {
  IconData get icon {
    switch (this) {
      case ContentType.anecdote:           return Icons.lightbulb_rounded;
      case ContentType.chuckNorris:        return Icons.sports_martial_arts_rounded;
      case ContentType.celebrityQuote:     return Icons.psychology_rounded;
      case ContentType.history:            return Icons.auto_stories_rounded;
      case ContentType.kingOfFrance:       return Icons.castle_rounded;
      case ContentType.americanPresident:  return Icons.account_balance_rounded;
      case ContentType.historyHub:         return Icons.history_edu_rounded;
      case ContentType.animals:            return Icons.pets_rounded;
      case ContentType.country:            return Icons.public_rounded;
      case ContentType.frenchDepartment:   return Icons.location_city_rounded;
      case ContentType.pacificIsland:      return Icons.waves_rounded;
      case ContentType.world:              return Icons.travel_explore_rounded;
      case ContentType.exoplanet:          return Icons.rocket_launch_rounded;
      case ContentType.star:               return Icons.star_rounded;
      case ContentType.solarSystemMoon:    return Icons.brightness_2_rounded;
      case ContentType.space:              return Icons.nightlight_round;
      case ContentType.cinemaHub:          return Icons.movie_rounded;
      case ContentType.classicCinema:      return Icons.theaters_rounded;
      case ContentType.cinema80s90s:       return Icons.videocam_rounded;
      case ContentType.modernCinema:       return Icons.local_movies_rounded;
      case ContentType.celebrityHub:       return Icons.stars_rounded;
      case ContentType.scienceHub:         return Icons.science_rounded;
      case ContentType.dinosaur:           return Icons.rowing_rounded;
      case ContentType.spaceMission:       return Icons.rocket_rounded;
      case ContentType.battle:             return Icons.shield_rounded;
      case ContentType.artHub:             return Icons.palette_rounded;
      case ContentType.painting:           return Icons.brush_rounded;
      case ContentType.sculpture:          return Icons.view_in_ar_rounded;
      case ContentType.architecture:       return Icons.domain_rounded;
      case ContentType.famousArtist:       return Icons.color_lens_rounded;
      case ContentType.photographer:       return Icons.photo_camera_rounded;
      case ContentType.classicalComposer:  return Icons.music_note_rounded;
      case ContentType.nobelPrize:         return Icons.emoji_events_rounded;
      case ContentType.frenchCommune:      return Icons.location_city_rounded;
      case ContentType.americanState:      return Icons.flag_rounded;
      case ContentType.scienceLivingHub:   return Icons.eco_rounded;
      case ContentType.scienceNonLivingHub: return Icons.biotech_rounded;
      case ContentType.artWorksHub:        return Icons.brush_rounded;
      case ContentType.artArtistsHub:      return Icons.groups_rounded;
      case ContentType.chemicalElement:    return Icons.science_rounded;
      case ContentType.volcano:            return Icons.terrain_rounded;
      case ContentType.insect:             return Icons.bug_report_rounded;
      case ContentType.bird:               return Icons.flight_takeoff_rounded;
      case ContentType.mineral:            return Icons.diamond_rounded;
    }
  }

  Color get color {
    switch (this) {
      case ContentType.anecdote:           return Colors.indigo;
      case ContentType.chuckNorris:        return Colors.red;
      case ContentType.celebrityQuote:     return Colors.teal;
      case ContentType.history:            return Colors.amber.shade700;
      case ContentType.kingOfFrance:       return Colors.purple;
      case ContentType.americanPresident:  return Colors.blue.shade900;
      case ContentType.historyHub:         return Colors.amber.shade700;
      case ContentType.animals:            return Colors.green;
      case ContentType.country:            return Colors.blue;
      case ContentType.frenchDepartment:   return Colors.blueGrey;
      case ContentType.pacificIsland:      return Colors.cyan;
      case ContentType.world:              return const Color(0xFF1A237E);
      case ContentType.exoplanet:          return Colors.deepPurple;
      case ContentType.star:               return Colors.amber;
      case ContentType.solarSystemMoon:    return Colors.blueGrey;
      case ContentType.space:              return Colors.deepPurple;
      case ContentType.cinemaHub:          return Colors.red.shade900;
      case ContentType.classicCinema:      return Colors.brown;
      case ContentType.cinema80s90s:       return Colors.deepOrange;
      case ContentType.modernCinema:       return Colors.red.shade700;
      case ContentType.celebrityHub:       return Colors.teal;
      case ContentType.scienceHub:         return Colors.green.shade800;
      case ContentType.dinosaur:           return Colors.brown.shade700;
      case ContentType.spaceMission:       return Colors.indigo.shade700;
      case ContentType.battle:             return Colors.red.shade900;
      case ContentType.artHub:             return Colors.purple.shade700;
      case ContentType.painting:           return Colors.purple.shade800;
      case ContentType.sculpture:          return const Color(0xFF546E7A);
      case ContentType.architecture:       return const Color(0xFF1565C0);
      case ContentType.famousArtist:       return const Color(0xFFAD1457);
      case ContentType.photographer:       return const Color(0xFF263238);
      case ContentType.classicalComposer:  return const Color(0xFF4A148C);
      case ContentType.nobelPrize:         return const Color(0xFFB8860B);
      case ContentType.frenchCommune:      return Colors.blue.shade700;
      case ContentType.americanState:      return Colors.red.shade700;
      case ContentType.scienceLivingHub:   return Colors.green.shade900;
      case ContentType.scienceNonLivingHub: return Colors.indigo.shade900;
      case ContentType.artWorksHub:        return Colors.purple.shade900;
      case ContentType.artArtistsHub:      return Colors.pink.shade900;
      case ContentType.chemicalElement:    return const Color(0xFF1A237E);
      case ContentType.volcano:            return const Color(0xFF7B0000);
      case ContentType.insect:             return const Color(0xFF2E7D32);
      case ContentType.bird:               return const Color(0xFF0277BD);
      case ContentType.mineral:            return const Color(0xFF4527A0);
    }
  }

  List<Color> get gradient {
    switch (this) {
      case ContentType.anecdote:
        return [const Color(0xFF667eea), const Color(0xFF764ba2)];
      case ContentType.chuckNorris:
        return [const Color(0xFFf85032), const Color(0xFFe73827)];
      case ContentType.celebrityQuote:
        return [const Color(0xFF11998e), const Color(0xFF38ef7d)];
      case ContentType.history:
        return [const Color(0xFFf2994a), const Color(0xFFf2c94c)];
      case ContentType.kingOfFrance:
        return [const Color(0xFF4B0082), const Color(0xFFDAA520)];
      case ContentType.americanPresident:
        return [const Color(0xFF002868), const Color(0xFFBF0A30)];
      case ContentType.historyHub:
        return [const Color(0xFFd4a017), const Color(0xFFf2994a)];
      case ContentType.animals:
        return [const Color(0xFF56ab2f), const Color(0xFFa8e063)];
      case ContentType.country:
        return [const Color(0xFF1a78c2), const Color(0xFF00b4db)];
      case ContentType.frenchDepartment:
        return [const Color(0xFF002395), const Color(0xFFED2939)];
      case ContentType.pacificIsland:
        return [const Color(0xFF006994), const Color(0xFF00C9FF)];
      case ContentType.world:
        return [const Color(0xFF1A237E), const Color(0xFF283593)];
      case ContentType.exoplanet:
        return [const Color(0xFF0F0C29), const Color(0xFF302B63)];
      case ContentType.star:
        return [const Color(0xFFf7971e), const Color(0xFFffd200)];
      case ContentType.solarSystemMoon:
        return [const Color(0xFF4b6cb7), const Color(0xFF182848)];
      case ContentType.space:
        return [const Color(0xFF0F0C29), const Color(0xFF24243e)];
      case ContentType.cinemaHub:
        return [const Color(0xFF1a1a2e), const Color(0xFF8B0000)];
      case ContentType.classicCinema:
        return [const Color(0xFF3E1F00), const Color(0xFFB8860B)];
      case ContentType.cinema80s90s:
        return [const Color(0xFF7B2FBE), const Color(0xFFFF6B35)];
      case ContentType.modernCinema:
        return [const Color(0xFF1a1a2e), const Color(0xFFE94560)];
      case ContentType.celebrityHub:
        return [const Color(0xFF11998e), const Color(0xFF71B280)];
      case ContentType.scienceHub:
        return [const Color(0xFF134E5E), const Color(0xFF71B280)];
      case ContentType.dinosaur:
        return [const Color(0xFF4B3621), const Color(0xFF8B6914)];
      case ContentType.spaceMission:
        return [const Color(0xFF0F0C29), const Color(0xFF302B63)];
      case ContentType.battle:
        return [const Color(0xFF7B0000), const Color(0xFFB71C1C)];
      case ContentType.artHub:
        return [const Color(0xFF4A148C), const Color(0xFF7B1FA2)];
      case ContentType.painting:
        return [const Color(0xFF4A148C), const Color(0xFFAB47BC)];
      case ContentType.sculpture:
        return [const Color(0xFF546E7A), const Color(0xFF78909C)];
      case ContentType.architecture:
        return [const Color(0xFF1565C0), const Color(0xFF0288D1)];
      case ContentType.famousArtist:
        return [const Color(0xFFAD1457), const Color(0xFFE91E63)];
      case ContentType.photographer:
        return [const Color(0xFF263238), const Color(0xFF455A64)];
      case ContentType.classicalComposer:
        return [const Color(0xFF4A148C), const Color(0xFF1A237E)];
      case ContentType.nobelPrize:
        return [const Color(0xFFB8860B), const Color(0xFFDAA520)];
      case ContentType.frenchCommune:
        return [const Color(0xFF002395), const Color(0xFF1565C0)];
      case ContentType.americanState:
        return [const Color(0xFF002868), const Color(0xFFBF0A30)];
      case ContentType.scienceLivingHub:
        return [const Color(0xFF1B5E20), const Color(0xFF388E3C)];
      case ContentType.scienceNonLivingHub:
        return [const Color(0xFF0D47A1), const Color(0xFF1565C0)];
      case ContentType.artWorksHub:
        return [const Color(0xFF512DA8), const Color(0xFF7E57C2)];
      case ContentType.artArtistsHub:
        return [const Color(0xFFAD1457), const Color(0xFFE91E63)];
      case ContentType.chemicalElement:
        return [const Color(0xFF1A237E), const Color(0xFF283593)];
      case ContentType.volcano:
        return [const Color(0xFF7B0000), const Color(0xFFB71C1C)];
      case ContentType.insect:
        return [const Color(0xFF1B5E20), const Color(0xFF66BB6A)];
      case ContentType.bird:
        return [const Color(0xFF0277BD), const Color(0xFF29B6F6)];
      case ContentType.mineral:
        return [const Color(0xFF37474F), const Color(0xFF7B1FA2)];
    }
  }

  Color get accentColor {
    switch (this) {
      case ContentType.exoplanet:
      case ContentType.space:
        return const Color(0xFF9B6DFF);
      case ContentType.star:
        return const Color(0xFFffd200);
      case ContentType.solarSystemMoon:
        return const Color(0xFF90CAF9);
      case ContentType.cinemaHub:
      case ContentType.classicCinema:
      case ContentType.cinema80s90s:
      case ContentType.modernCinema:
        return const Color(0xFFFFD700);
      case ContentType.spaceMission:
        return const Color(0xFF9B6DFF);
      case ContentType.battle:
        return const Color(0xFFFF6B6B);
      case ContentType.kingOfFrance:
        return const Color(0xFFDAA520);
      case ContentType.americanPresident:
        return const Color(0xFFBF0A30);
      case ContentType.frenchDepartment:
        return const Color(0xFFED2939);
      case ContentType.sculpture:
        return const Color(0xFFB0BEC5);
      case ContentType.architecture:
        return const Color(0xFF4FC3F7);
      case ContentType.famousArtist:
        return const Color(0xFFF48FB1);
      case ContentType.photographer:
        return const Color(0xFF90A4AE);
      case ContentType.classicalComposer:
        return const Color(0xFFB39DDB);
      case ContentType.nobelPrize:
        return const Color(0xFFFFD700);
      default:
        return gradient[0];
    }
  }
}
