part of 'content_type.dart';

extension ContentTypeAccentColors on ContentType {
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
      case ContentType.gamingHub:
      case ContentType.gamesHub:
      case ContentType.gamingAnecdote:
      case ContentType.classicGame:
        return const Color(0xFF4ADE80);
      case ContentType.gamersHub:
      case ContentType.gamingLegend:
        return const Color(0xFF66C0F4);
      case ContentType.gamingNomination:
        return const Color(0xFFD4A017);
      case ContentType.worstGame:
      case ContentType.bannedGame:
        return const Color(0xFFEF4444);
      default:
        return gradient[0];
    }
  }
}
