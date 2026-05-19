import 'package:flutter/material.dart';
import '../generated/app_localizations.dart';

enum ContentType {
  anecdote,
  chuckNorris,
  celebrityQuote,
  history,
  kingOfFrance,
  americanPresident,
  historyHub,
  animals,
  country,
  frenchDepartment,
  pacificIsland,
  world,
  exoplanet,
  star,
  solarSystemMoon,
  space,
  cinemaHub,
  classicCinema,
  cinema80s90s,
  modernCinema,
}

extension ContentTypeExtension on ContentType {
  String get title {
    switch (this) {
      case ContentType.anecdote:           return 'Anecdote';
      case ContentType.chuckNorris:        return 'Chuck Norris';
      case ContentType.celebrityQuote:     return 'Celebrity Quote';
      case ContentType.history:            return 'Day of History';
      case ContentType.kingOfFrance:       return 'Kings of France';
      case ContentType.americanPresident:  return 'American Presidents';
      case ContentType.historyHub:         return 'History';
      case ContentType.animals:            return 'Animals';
      case ContentType.frenchDepartment:   return 'French Department';
      case ContentType.pacificIsland:      return 'Pacific Island';
      case ContentType.country:            return 'Countries';
      case ContentType.world:              return 'World';
      case ContentType.exoplanet:          return 'Exoplanet';
      case ContentType.star:               return 'Star';
      case ContentType.solarSystemMoon:    return 'Moon';
      case ContentType.space:              return 'Space';
      case ContentType.cinemaHub:          return 'Cinema';
      case ContentType.classicCinema:      return 'Classic Hollywood';
      case ContentType.cinema80s90s:       return '80s & 90s Movies';
      case ContentType.modernCinema:       return 'Modern Cinema';
    }
  }

  String localizedTitle(AppLocalizations loc) {
    switch (this) {
      case ContentType.anecdote:           return loc.categoryAnecdote;
      case ContentType.chuckNorris:        return loc.categoryChuckNorris;
      case ContentType.celebrityQuote:     return loc.categoryAdvice;
      case ContentType.history:            return loc.categoryDayOfHistory;
      case ContentType.kingOfFrance:       return loc.categoryKingOfFrance;
      case ContentType.americanPresident:  return loc.categoryAmericanPresident;
      case ContentType.historyHub:         return loc.categoryHistoryHub;
      case ContentType.animals:            return loc.categoryAnimals;
      case ContentType.country:            return loc.categoryCountry;
      case ContentType.frenchDepartment:   return loc.categoryFrenchDepartment;
      case ContentType.pacificIsland:      return loc.categoryPacificIsland;
      case ContentType.world:              return loc.categoryWorld;
      case ContentType.exoplanet:          return loc.categoryExoplanet;
      case ContentType.star:               return loc.categoryStar;
      case ContentType.solarSystemMoon:    return loc.categorySolarSystemMoon;
      case ContentType.space:              return loc.categorySpace;
      case ContentType.cinemaHub:          return loc.categoryCinemaHub;
      case ContentType.classicCinema:      return loc.categoryClassicCinema;
      case ContentType.cinema80s90s:       return loc.categoryCinema80s90s;
      case ContentType.modernCinema:       return loc.categoryModernCinema;
    }
  }

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
    }
  }

  Color get accentColor {
    switch (this) {
      case ContentType.exoplanet:
        return const Color(0xFF9B6DFF);
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
      default:
        return gradient[0];
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
    }
  }

  String get apiEndpoint {
    switch (this) {
      case ContentType.anecdote:
        return 'https://api.api-ninjas.com/v1/facts';
      case ContentType.chuckNorris:
        return 'https://api.api-ninjas.com/v1/chucknorris';
      case ContentType.celebrityQuote:
        return 'https://api.api-ninjas.com/v1/quotes?category=inspirational';
      case ContentType.history:
        return 'https://api.api-ninjas.com/v1/historicalevents';
      case ContentType.animals:
        return 'https://api.api-ninjas.com/v1/animals?name=lion';
      case ContentType.country:
      case ContentType.frenchDepartment:
      case ContentType.pacificIsland:
      case ContentType.world:
      case ContentType.exoplanet:
      case ContentType.star:
      case ContentType.solarSystemMoon:
      case ContentType.space:
      case ContentType.kingOfFrance:
      case ContentType.americanPresident:
      case ContentType.historyHub:
      case ContentType.cinemaHub:
      case ContentType.classicCinema:
      case ContentType.cinema80s90s:
      case ContentType.modernCinema:
        return '';
    }
  }
}
